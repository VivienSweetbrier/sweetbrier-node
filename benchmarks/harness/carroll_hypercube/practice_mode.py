"""
practice_mode.py 🌸
Multi-Asset Timeline Simulator for the Quantitative Research Desk
Simulates:
1. Dynamic Market Regimes across a 5-Asset Basket (MSTR, GME, TSLA, NVDA, RDDT)
2. Lewis Carroll Triliteral Hypercube Gate Filtering (Q_3)
3. Cost-Aware Execution (Equation 1: Gross vs Net P&L)
4. 5% Capital Ceiling & Automatic Stop-Loss Protection
5. End-of-Run Audit Card generation via ledger_analytics.py
"""

import time
import random
from typing import Dict, Any, List
from trader import init_ledger, execute_desperation_logic, check_all_stop_losses
from ledger_analytics import print_audit_card

# Universe of high-volatility retail/meme assets
UNIVERSE = {
    "MSTR": {"base_price": 150.00, "borrow_apr": 0.025, "spread_pct": 0.0003},
    "GME":  {"base_price": 22.50,  "borrow_apr": 0.080, "spread_pct": 0.0012},  # Hard to borrow, wide spread!
    "TSLA": {"base_price": 220.00, "borrow_apr": 0.015, "spread_pct": 0.0002},  # Liquid, cheap borrow
    "NVDA": {"base_price": 125.00, "borrow_apr": 0.010, "spread_pct": 0.0001},  # Ultra-liquid
    "RDDT": {"base_price": 65.00,  "borrow_apr": 0.035, "spread_pct": 0.0006}   # Moderate borrow fee
}


def run_timeline_simulation(steps: int = 5):
    print("=" * 70)
    print("  🌸 INITIATING MULTI-ASSET CARROLL TIMELINE SIMULATION 🌸")
    print("  Testing 5-Asset Basket against Lewis Carroll Risk Gates & REA Costs")
    print("=" * 70)

    init_ledger()

    # Track current simulated prices for each ticker
    current_prices = {ticker: data["base_price"] for ticker, data in UNIVERSE.items()}

    for t in range(1, steps + 1):
        print(f"\n--- [TIMELINE STEP {t}/{steps}] ---")

        # 1. Simulate price movements (Random Walk / Regime Shift)
        for ticker in UNIVERSE:
            pct_change = random.uniform(-0.03, 0.03)  # +/- 3% move per step
            current_prices[ticker] = round(current_prices[ticker] * (1.0 + pct_change), 2)

        # 2. Check for automatic Stop-Loss breaches across all open positions
        check_all_stop_losses(current_prices)

        # 3. Simulate Desperation Index signals for each asset
        for ticker, meta in UNIVERSE.items():
            curr_p = current_prices[ticker]

            # Generate synthetic regime signal
            if t == 1:
                # Step 1: Seed some high desperation to trigger entries
                desp_index = 130.0 if ticker in ["MSTR", "GME", "TSLA"] else 100.0
            elif t == 2:
                # Step 2: Euphoria continues
                desp_index = 125.0 if ticker == "NVDA" else 105.0
            elif t == 3:
                # Step 3: Mean reversion begins (Index drops for MSTR, stays high for GME)
                desp_index = 80.0 if ticker == "MSTR" else 115.0
            elif t == 4:
                # Step 4: Full panic relaxation on TSLA
                desp_index = 75.0 if ticker == "TSLA" else 95.0
            else:
                # Step 5: Market stabilizes
                desp_index = random.uniform(85.0, 115.0)

            # Execute via cost-aware trader engine
            execute_desperation_logic(
                ticker=ticker,
                desperation_index=desp_index,
                override_price=curr_p,
                spread_pct=meta["spread_pct"],
                borrow_apr=meta["borrow_apr"]
            )

        time.sleep(0.3)

    print("\n" + "=" * 70)
    print("  🌸 TIMELINE COMPLETE — COMPILING FINAL EVIDENCE AUDIT 🌸")
    print("=" * 70)
    print_audit_card()


if __name__ == "__main__":
    run_timeline_simulation(steps=5)
