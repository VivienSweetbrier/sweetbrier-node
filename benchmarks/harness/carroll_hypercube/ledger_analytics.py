"""
ledger_analytics.py 🌸
The Quantitative Evidence Ledger Auditor & Institutional Analytics Engine
Implements Table 1 from the IEEE REA Framework:
- Audits paper_trades.db for verified execution metrics
- Computes Net vs Gross P&L, Win Rate, Profit Factor, Max Drawdown
- Reports total friction drag (Fees C_f, Slippage C_s, Borrow C_o)
"""

import sqlite3
from typing import Dict, Any, List, Tuple

DB_NAME = "paper_trades.db"


def generate_audit_report() -> Dict[str, Any]:
    """Reads paper_trades.db and compiles comprehensive performance metrics."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Portfolio Cash & Starting Capital
    c.execute("SELECT cash FROM portfolio WHERE id = 1")
    row = c.fetchone()
    cash = row[0] if row else 100000.0
    starting_capital = 100000.0

    # 2. Total Trades Count
    c.execute("SELECT COUNT(*) FROM paper_trades")
    total_actions = c.fetchone()[0]

    # 3. Closed Trades (BUY TO COVER with linked_entry_id)
    c.execute('''
        SELECT id, ticker, price, quantity, linked_entry_id, 
               gross_pnl, net_pnl, fee_cf, slippage_cs, borrow_co, timestamp
        FROM paper_trades
        WHERE action = 'BUY TO COVER' AND linked_entry_id IS NOT NULL
        ORDER BY id ASC
    ''')
    closed_trades = c.fetchall()

    # 4. Open Positions (SELL SHORT without matching linked_entry_id)
    c.execute('''
        SELECT id, ticker, price, quantity, total_value, stop_loss, timestamp
        FROM paper_trades
        WHERE action = 'SELL SHORT' 
        AND id NOT IN (SELECT linked_entry_id FROM paper_trades WHERE linked_entry_id IS NOT NULL)
        ORDER BY id ASC
    ''')
    open_positions = c.fetchall()

    conn.close()

    # Metrics compilation
    wins = []
    losses = []
    total_gross_pnl = 0.0
    total_net_pnl = 0.0
    total_fee_cf = 0.0
    total_slippage_cs = 0.0
    total_borrow_co = 0.0

    # Equity curve tracking for Max Drawdown
    equity_curve = [starting_capital]
    current_equity = starting_capital

    for trade in closed_trades:
        g_pnl = trade[5] or 0.0
        n_pnl = trade[6] or 0.0
        cf = trade[7] or 0.0
        cs = trade[8] or 0.0
        co = trade[9] or 0.0

        total_gross_pnl += g_pnl
        total_net_pnl += n_pnl
        total_fee_cf += cf
        total_slippage_cs += cs
        total_borrow_co += co

        if n_pnl > 0:
            wins.append(n_pnl)
        elif n_pnl < 0:
            losses.append(n_pnl)

        current_equity += n_pnl
        equity_curve.append(current_equity)

    num_closed = len(closed_trades)
    win_rate = (len(wins) / num_closed * 100.0) if num_closed > 0 else 0.0
    sum_wins = sum(wins)
    sum_losses = abs(sum(losses))
    profit_factor = (sum_wins / sum_losses) if sum_losses > 0 else (999.0 if sum_wins > 0 else 1.0)
    avg_win = (sum_wins / len(wins)) if wins else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0

    # Max Drawdown Calculation
    peak = equity_curve[0]
    max_dd_dollars = 0.0
    max_dd_pct = 0.0
    for eq in equity_curve:
        if eq > peak:
            peak = eq
        dd_dollars = peak - eq
        dd_pct = (dd_dollars / peak * 100.0) if peak > 0 else 0.0
        if dd_dollars > max_dd_dollars:
            max_dd_dollars = dd_dollars
        if dd_pct > max_dd_pct:
            max_dd_pct = dd_pct

    total_friction = total_fee_cf + total_slippage_cs + total_borrow_co

    report = {
        "starting_capital": starting_capital,
        "current_cash": cash,
        "realized_equity": current_equity,
        "total_actions": total_actions,
        "num_closed_trades": num_closed,
        "num_open_positions": len(open_positions),
        "open_positions": open_positions,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": win_rate,
        "total_gross_pnl": total_gross_pnl,
        "total_net_pnl": total_net_pnl,
        "total_friction": total_friction,
        "fee_cf": total_fee_cf,
        "slippage_cs": total_slippage_cs,
        "borrow_co": total_borrow_co,
        "profit_factor": profit_factor,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "max_drawdown_dollars": max_dd_dollars,
        "max_drawdown_pct": max_dd_pct
    }
    return report


def print_audit_card():
    """Renders a formatted ASCII audit card for the researcher."""
    r = generate_audit_report()

    print("\n" + "=" * 70)
    print("  🌸 JAMIE 'SOCK' WISDOM — QUANTITATIVE EVIDENCE LEDGER AUDIT 🌸")
    print("  Framework: IEEE REA Cost Accounting & Lewis Carroll Q_3 Gate")
    print("=" * 70)
    print(f"  Initial Allocation:     ${r['starting_capital']:>12,.2f} USD")
    print(f"  Current Cash Balance:   ${r['current_cash']:>12,.2f} USD")
    print(f"  Realized Net Equity:    ${r['realized_equity']:>12,.2f} USD")
    print("-" * 70)
    print(f"  Total Closed Cycles:    {r['num_closed_trades']:>12}")
    print(f"  Open Short Exposure:    {r['num_open_positions']:>12} active positions")
    print(f"  Win / Loss Record:      {r['wins']:>8} W / {r['losses']} L")
    print(f"  Strategy Win Rate:      {r['win_rate_pct']:>11.1f}%")
    print(f"  Profit Factor:          {r['profit_factor']:>11.2f}x")
    print(f"  Average Winner:        +${r['avg_win']:>11.2f}")
    print(f"  Average Loser:         -${abs(r['avg_loss']):>11.2f}")
    print(f"  Max Peak-to-Trough DD: -${r['max_drawdown_dollars']:>11.2f} ({r['max_drawdown_pct']:.2f}%)")
    print("-" * 70)
    print("  [EQUATION 1 FRICTION AUDIT]")
    print(f"  Gross Realized Alpha:  +${r['total_gross_pnl']:>11.2f}")
    print(f"  - Exchange Fees (C_f): -${r['fee_cf']:>11.2f}")
    print(f"  - Slippage Cost (C_s): -${r['slippage_cs']:>11.2f}")
    print(f"  - Borrow Rates  (C_o): -${r['borrow_co']:>11.2f}")
    print(f"  = NET Realized Alpha:  +${r['total_net_pnl']:>11.2f}")
    print("=" * 70)

    if r["num_open_positions"] > 0:
        print("\n  [ACTIVE SHORT POSITIONS]")
        for pos in r["open_positions"]:
            print(f"  • {pos[1]}: {pos[3]} shares @ ${pos[2]:.2f} | Stop-Loss: ${pos[5]:.2f}")
        print("=" * 70)


if __name__ == "__main__":
    print_audit_card()
