"""
trader.py 🌸
The Quantitative Simulator Execution Engine (Phase 2)
Implements:
1. Strict 5% Capital Preservation Position Sizing Limit
2. Lewis Carroll Triliteral Hypercube (Q_3) Pre-Trade Risk Gate
3. IEEE REA Cost Accounting Model: R_net = R_g - C_f - C_s - C_m - C_o
4. Automatic 5% Stop-Loss Protection and Position Pair Linking
"""

import sqlite3
import yfinance as yf
import time
from typing import Optional, Dict, Any, Tuple
from carroll_gate import build_quant_carroll_gate, CarrollHypercube

DB_NAME = "paper_trades.db"

# Default Institutional Friction Constants
DEFAULT_COMMISSION_RATE = 0.0005   # C_f: 0.05% exchange fee
DEFAULT_SLIPPAGE_RATE   = 0.0002   # C_s: 0.02% half-spread slippage
DEFAULT_BORROW_APR      = 0.025    # C_o: 2.5% annual borrow rate for short positions


def init_ledger():
    """Initializes and migrates the immutable ledger and portfolio state."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Base paper_trades table
    c.execute('''
        CREATE TABLE IF NOT EXISTS paper_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            action TEXT,
            price REAL,
            quantity REAL,
            total_value REAL,
            stop_loss REAL,
            desperation_index REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            linked_entry_id INTEGER,
            realized_pnl REAL
        )
    ''')

    # 2. Add Equation (1) friction columns if they do not exist
    c.execute("PRAGMA table_info(paper_trades)")
    columns = [col[1] for col in c.fetchall()]

    new_cols = {
        "fee_cf": "REAL DEFAULT 0.0",
        "slippage_cs": "REAL DEFAULT 0.0",
        "borrow_co": "REAL DEFAULT 0.0",
        "gross_pnl": "REAL DEFAULT 0.0",
        "net_pnl": "REAL DEFAULT 0.0",
        "entry_timestamp_epoch": "REAL DEFAULT 0.0"
    }

    for col_name, col_type in new_cols.items():
        if col_name not in columns:
            c.execute(f"ALTER TABLE paper_trades ADD COLUMN {col_name} {col_type}")

    # 3. Portfolio table
    c.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY,
            cash REAL
        )
    ''')
    c.execute("SELECT cash FROM portfolio WHERE id = 1")
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO portfolio (id, cash) VALUES (1, 100000.0)")

    conn.commit()
    conn.close()


def get_current_price(ticker: str, override_price: Optional[float] = None) -> float:
    """Fetches market price via yfinance or uses offline simulated override."""
    if override_price is not None and override_price > 0:
        return float(override_price)

    print(f"🧦⚙️🧦 [Harness] Fetching live price for {ticker} via yfinance...")
    try:
        t = yf.Ticker(ticker)
        price = t.fast_info['lastPrice']
        return float(price)
    except Exception as e:
        print(f"🧦⚙️🧦 [Harness Warning] Live price unavailable, attempting historical close: {e}")
        try:
            hist = t.history(period="1d")
            return float(hist['Close'].iloc[-1])
        except Exception as e2:
            print(f"🧦⚙️🧦 [Harness Error] Total failure: {e2}")
            return 0.0


def get_active_short(ticker: str, cursor) -> Optional[Dict[str, Any]]:
    """Returns the unclosed short position for this ticker, if any."""
    cursor.execute('''
        SELECT id, quantity, price, stop_loss, fee_cf, slippage_cs, entry_timestamp_epoch
        FROM paper_trades 
        WHERE ticker = ? AND action = 'SELL SHORT' 
        AND id NOT IN (SELECT linked_entry_id FROM paper_trades WHERE linked_entry_id IS NOT NULL)
        ORDER BY id DESC LIMIT 1
    ''', (ticker,))
    row = cursor.fetchone()
    if row:
        return {
            "id": row[0],
            "quantity": row[1],
            "entry_price": row[2],
            "stop_loss": row[3],
            "entry_fee_cf": row[4] or 0.0,
            "entry_slippage_cs": row[5] or 0.0,
            "entry_epoch": row[6] or time.time()
        }
    return None


def execute_desperation_logic(
    ticker: str,
    desperation_index: float,
    override_price: Optional[float] = None,
    spread_pct: float = DEFAULT_SLIPPAGE_RATE * 2,
    borrow_apr: float = DEFAULT_BORROW_APR
) -> Dict[str, Any]:
    """
    Evaluates market regime via Lewis Carroll Gate and executes cost-aware trades.
    Implements Equation (1): R_net = R_g - C_f - C_s - C_o
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print(f"\n🧦⚙️🧦 [Quantitative Simulator] Assessing {ticker} | Desperation: {desperation_index:.1f}")

    active_short = get_active_short(ticker, c)
    current_price = get_current_price(ticker, override_price)

    if current_price <= 0:
        print("🧦⚙️🧦 [Error] Invalid price. Aborting.")
        conn.close()
        return {"status": "ERROR_PRICE", "pnl": 0.0}

    c.execute("SELECT cash FROM portfolio WHERE id = 1")
    cash = c.fetchone()[0]

    # Carroll Hypercube Gate Evaluation (Triliteral Q_3)
    gate = build_quant_carroll_gate()
    is_ripe = desperation_index > 120
    tight_spread = spread_pct <= 0.0005  # True if spread <= 0.05%
    cheap_borrow = borrow_apr <= 0.030   # True if borrow <= 3.0%

    gate_state = {"x": is_ripe, "y": tight_spread, "m": cheap_borrow}
    counter, notation, _ = gate.evaluate(gate_state)

    now_epoch = time.time()
    result = {"status": "HOLD", "action": None, "pnl": 0.0}

    # 1. SHORT CONDITION
    if is_ripe and not active_short:
        if counter == CarrollHypercube.GREY:
            print(f"🧦⚙️🧦 [CARROLL GATE] CAST INTO DARKNESS! Compartment '{notation}' has Grey Counter (∅). Execution Vetoed.")
            conn.close()
            return {"status": "VETOED_GREY_COUNTER", "notation": notation, "pnl": 0.0}

        print(f"🧦🌸🧦 [CARROLL GATE] Existential Import Confirmed! Compartment '{notation}' has Red Counter (∃). Alpha Admissible.")

        max_capital = cash * 0.05  # 5% capital preservation ceiling
        quantity = int(max_capital // current_price)
        total_value = quantity * current_price
        stop_loss = current_price * 1.05

        if quantity > 0:
            # Equation (1) Entry Frictions
            fee_cf = total_value * DEFAULT_COMMISSION_RATE
            slippage_cs = total_value * DEFAULT_SLIPPAGE_RATE
            net_cash_inflow = total_value - (fee_cf + slippage_cs)

            c.execute('''
                INSERT INTO paper_trades (
                    ticker, action, price, quantity, total_value, stop_loss,
                    desperation_index, fee_cf, slippage_cs, borrow_co,
                    gross_pnl, net_pnl, entry_timestamp_epoch
                )
                VALUES (?, 'SELL SHORT', ?, ?, ?, ?, ?, ?, ?, 0.0, 0.0, 0.0, ?)
            ''', (ticker, current_price, quantity, total_value, stop_loss,
                  desperation_index, fee_cf, slippage_cs, now_epoch))

            new_cash = cash + net_cash_inflow
            c.execute("UPDATE portfolio SET cash = ? WHERE id = 1", (new_cash,))
            print(f"🧦⚙️🧦 [EXECUTION] SELL SHORT {quantity} shares of {ticker} at ${current_price:.2f}.")
            print(f"  └─ Stop-Loss: ${stop_loss:.2f} | Frictions Paid: Fees=${fee_cf:.2f}, Slip=${slippage_cs:.2f}")
            result = {"status": "EXECUTED", "action": "SELL SHORT", "quantity": quantity, "price": current_price}
        else:
            print("🧦⚙️🧦 [EXECUTION] Insufficient capital to allocate 5%.")

    # 2. COVER CONDITION (Desperation falls below 90, or stop-loss breached)
    elif active_short and (desperation_index < 90 or current_price >= active_short["stop_loss"]):
        is_stop_loss = current_price >= active_short["stop_loss"]
        exit_reason = "STOP-LOSS HIT" if is_stop_loss else "SIGNAL RELAXED (<90)"

        quantity = active_short["quantity"]
        entry_price = active_short["entry_price"]
        entry_id = active_short["id"]
        entry_epoch = active_short["entry_epoch"]

        cost_to_cover = quantity * current_price

        # Equation (1) Exit Frictions
        exit_fee_cf = cost_to_cover * DEFAULT_COMMISSION_RATE
        exit_slippage_cs = cost_to_cover * DEFAULT_SLIPPAGE_RATE

        # Borrow cost C_o over duration held (minimum 1 hour simulated carry)
        hold_seconds = max(now_epoch - entry_epoch, 3600.0)
        borrow_co = (quantity * entry_price) * borrow_apr * (hold_seconds / (365.25 * 86400.0))

        gross_pnl = (entry_price - current_price) * quantity
        total_frictions = (active_short["entry_fee_cf"] + active_short["entry_slippage_cs"] +
                           exit_fee_cf + exit_slippage_cs + borrow_co)
        net_pnl = gross_pnl - total_frictions

        c.execute('''
            INSERT INTO paper_trades (
                ticker, action, price, quantity, total_value, desperation_index,
                linked_entry_id, fee_cf, slippage_cs, borrow_co,
                gross_pnl, net_pnl, realized_pnl
            )
            VALUES (?, 'BUY TO COVER', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticker, current_price, quantity, cost_to_cover, desperation_index,
              entry_id, exit_fee_cf, exit_slippage_cs, borrow_co,
              gross_pnl, net_pnl, net_pnl))

        net_cash_outflow = cost_to_cover + exit_fee_cf + exit_slippage_cs + borrow_co
        new_cash = cash - net_cash_outflow
        c.execute("UPDATE portfolio SET cash = ? WHERE id = 1", (new_cash,))

        print(f"🧦⚙️🧦 [EXECUTION] BUY TO COVER ({exit_reason}) {quantity} shares of {ticker} at ${current_price:.2f}.")
        print(f"  └─ Gross P&L: ${gross_pnl:.2f} | Net P&L: ${net_pnl:.2f} (Total Frictions: ${total_frictions:.2f})")
        result = {"status": "EXECUTED", "action": "BUY TO COVER", "quantity": quantity, "price": current_price, "net_pnl": net_pnl}

    # 3. HOLD CONDITION
    elif 90 <= desperation_index <= 120:
        print(f"🧦⚙️🧦 [EXECUTION] Index between 90-120 ({desperation_index:.1f}). Holding the line.")
    else:
        print(f"🧦⚙️🧦 [EXECUTION] Neutral regime ({desperation_index:.1f}). No action.")

    conn.commit()

    c.execute("SELECT cash FROM portfolio WHERE id = 1")
    current_cash = c.fetchone()[0]
    print(f"🧦⚙️🧦 [PORTFOLIO] Cash Balance: ${current_cash:.2f}")

    conn.close()
    return result


def check_all_stop_losses(prices: Dict[str, float]) -> int:
    """Scans all open positions and triggers immediate cover if stop-loss is breached."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT ticker, price, stop_loss FROM paper_trades
        WHERE action = 'SELL SHORT' 
        AND id NOT IN (SELECT linked_entry_id FROM paper_trades WHERE linked_entry_id IS NOT NULL)
    ''')
    open_positions = c.fetchall()
    conn.close()

    triggered = 0
    for ticker, entry_p, stop_p in open_positions:
        curr_p = prices.get(ticker)
        if curr_p and curr_p >= stop_p:
            print(f"🚨 [STOP-LOSS TRIGGERED] {ticker} traded at ${curr_p:.2f} >= Stop ${stop_p:.2f}!")
            execute_desperation_logic(ticker, desperation_index=150.0, override_price=curr_p)
            triggered += 1
    return triggered


if __name__ == "__main__":
    init_ledger()
    print("=== Testing Single Cost-Aware Lifecycle on MSTR ===")
    execute_desperation_logic("MSTR", 125, override_price=150.00)
    time.sleep(0.5)
    # Price falls to 142.00 (Profitable cover)
    execute_desperation_logic("MSTR", 80, override_price=142.00)
