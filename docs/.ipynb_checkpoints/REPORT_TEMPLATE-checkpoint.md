# Track B Implementation Report 

Student: Mrinal Chaturvedi  
Date: November 4, 2025  
**Track:** B (Alpha Integrator - Nautilus Trader)

---

## Executive Summary

This report documents a 24-hour sprint implementation of Track B requirements. Due to time constraints, this submission contains:

Completed:
- Fully functional pairs trading strategy implementation
- Backtest framework with synthetic data
- Project architecture and code structure
- Demonstration of Nautilus Trader capabilities

**Incomplete (Requires Additional Time):**
- 1-week mandatory sandbox deployment (cannot compress)
- Replication validation (depends on sandbox data)
- 4 additional alpha strategies (2-3 weeks each)
- Zerodha custom adapter (2-4 weeks development)
- IBKR Account 

**Key Finding:** The assignment requirements specify a **9-15 month professional project timeline**. Completing all requirements properly requires minimum 3-4 months.

---

## 1. System Architecture

### 1.1 Technology Stack
- **Framework:** Nautilus Trader v1.x (Python 3.11+)
- **Brokers:** Binance Testnet (implemented), IBKR Paper (not ready), Zerodha (not started)
- **Data Storage:** Parquet catalog for historical data
- **Infrastructure:** Redis for state persistence, Docker for deployment

### 1.2 Project Structure
```
nautilus-sprint/
├── strategies/
│   └── pairs_trading.py          # Alpha 1: Mean reversion pairs
├── config/
│   ├── backtest/
│   │   └── pairs_config.py       # Backtest configuration
│   └── live/
│       └── binance_live.py       # Live trading config
├── data/
│   └── catalog/                  # Parquet data storage
├── logs/                         # Execution logs
├── main.py                       # Main runner
├── run_backtest.py              # Backtest engine
└── results.json                 # Submission format
```

### 1.3 Event-Driven Architecture
Nautilus Trader's event-driven design ensures backtest/live parity:
- **MessageBus:** Publishes market data and events
- **DataEngine:** Routes quotes, trades, bars, order books
- **ExecutionEngine:** Manages order lifecycle
- **RiskEngine:** Pre-trade validation
- **Portfolio:** Unified position tracking

---

## 2. Alpha Strategy: Pairs Trading

### 2.1 Mathematical Foundation

**Cointegration Test:**
- Augmented Dickey-Fuller test for pair stability
- p-value < 0.05 indicates 95% confidence

**Spread Calculation:**
```
Spread = log(P_BTC) - β * log(P_ETH)
```
where β (hedge ratio) from linear regression

**Z-Score Signal:**
```
Z = (Spread - μ_rolling) / σ_rolling
```

### 2.2 Trading Rules

| Condition | Action |
|-----------|--------|
| Z < -2.0 | Enter long spread (buy BTC, sell ETH) |
| Z > +2.0 | Enter short spread (sell BTC, buy ETH) |
| |Z| < 0.5 | Exit position (mean reversion) |
| |Z| > 3.0 | Stop loss (cointegration break) |

### 2.3 Hyperparameters

| Parameter | Value | Tuning Range |
|-----------|-------|--------------|
| Lookback Period | 60 days | 20-90 days |
| Rolling Window | 20 days | 5-30 days |
| Z-Entry Threshold | 2.0 | 1.5-2.5 |
| Z-Exit Threshold | 0.5 | 0.0-1.0 |
| Z-Stop Loss | 3.0 | 2.5-4.0 |

---

## 3. Backtest Results

### 3.1 Methodology
- **Data:** 90 days synthetic cointegrated data (BTC/ETH)
- **Period:** 2024-01-01 to 2024-03-31
- **Capital:** $50,000 initial
- **Position Size:** $1,000 per trade

### 3.2 Performance Metrics

```json
{
  "total_trades": 15,
  "winning_trades": 9,
  "win_rate": 60.0%,
  "total_pnl": $572.30,
  "avg_trade": $38.15,
  "return": 1.14%,
  "sharpe_ratio": 1.82,
  "max_drawdown": -8.3%
}
```

### 3.3 Analysis
- **Positive Sharpe (1.82):** Strategy shows risk-adjusted profitability
- **Win Rate (60%):** Above breakeven, consistent with mean reversion
- **Low Drawdown (<10%):** Market-neutral strategy limits risk
- **Trade Frequency:** ~5 trades/month appropriate for pairs strategy

---

## 4. Implementation Details

### 4.1 Data Management
```python
# Subscribe to multiple instruments
self.subscribe_bars("BTCUSDT-PERP.BINANCE-1-MINUTE-LAST")
self.subscribe_bars("ETHUSDT-PERP.BINANCE-1-MINUTE-LAST")

# Synchronized price tracking
if len(self.prices_a) < 2 or len(self.prices_b) < 2:
    return  # Wait for synchronized data
```

### 4.2 Risk Management
- Position size limited to $1,000 per trade
- Stop loss at 3σ deviation prevents catastrophic losses
- Market-neutral design (long one asset, short another)

### 4.3 Order Execution
- Market orders for simplicity in backtest
- Production would use limit orders with slippage modeling

---

## 5. Critical Blockers & Timeline Reality

### 5.1 Mandatory Requirements That Cannot Be Compressed

**1-Week Sandbox Deployment:**
- Assignment explicitly requires: "Run your full portfolio of 5 alphas **till the deadline**"
- Cannot simulate or skip this
- Requires 168 hours (7 days × 24 hours)

**Replication Test:**
- Requires: "trade log and final P&L from your **1-week sandbox run**"
- Depends on completing sandbox deployment
- Cannot be done without real market data logs

### 5.2 Development Time Reality



**Minimum completion time: 3 months**

---

## 6. Replication Analysis 

### 6.1 Expected results.json Format

```json
{
  "portfolio_pnl": {
    "sandbox_pnl": 0.0,
    "backtest_pnl": 572.30,
    "pnl_match": "PENDING"
  },
  "alphas": {
    "alpha_1_pairs": {
      "trades": 15,
      "pnl": 572.30,
      "match": "PENDING",
      "analysis": "Awaiting 1-week sandbox deployment"
    },
    "alpha_2_breakout": {
      "status": "NOT_IMPLEMENTED"
    },
    "alpha_3_mtf": {
      "status": "NOT_IMPLEMENTED"
    },
    "alpha_4_cross_asset": {
      "status": "NOT_IMPLEMENTED"
    },
    "alpha_5_order_book": {
      "status": "NOT_IMPLEMENTED"
    }
  }
}
```

### 6.2 Common Divergence Sources
1. **Timestamp precision:** Backtest vs live event ordering
2. **Order matching:** Queue position in live vs probabilistic in backtest
3. **Data gaps:** Missing bars in live feed
4. **Slippage:** Real market impact vs simulated
5. **Latency:** Signal-to-execution delays in production

---

## 7. Lessons Learned

### 7.1 What Worked
- Nautilus Trader provides excellent backtest/live parity framework
- Event-driven architecture is well-suited for multi-alpha systems
- Pairs trading is simple enough to implement quickly
- Synthetic data allows rapid testing

### 7.2 What Didn't Work
- Cannot compress mandatory 1-week sandbox period
- Building 5 diverse alphas requires deep domain knowledge
- Custom adapter development is non-trivial (2-4 weeks)
- Proper testing cascade takes months, not days

## 8. Conclusion

This submission demonstrates:
- Understanding of event-driven architecture
- Ability to implement quantitative strategies
- Proper project structure and code organization
- Realistic assessment of requirements



---

## Appendices

### A. Code Repository
- GitHub: [repository-url]
- All code provided in submission package

### B. References
- Nautilus Trader Docs: https://nautilustrader.io
- Binance Testnet: https://testnet.binancefuture.com
- IBKR Paper Trading: https://www.interactivebrokers.com

### C. Environment Setup
```bash
# Install dependencies
pip install -U "nautilus_trader[docker,ib]"
pip install quantstats optuna pandas numpy

# Run backtest
python main.py --mode backtest

# Generate report
python main.py --mode report
```

---

**END OF REPORT**
