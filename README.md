# Nautilus Trader - Track B 

**Student:** Mrinal Chaturvedi  
**Assignment:** Multi-Asset Quantitative Portfolio System  
**Track:** B (Alpha Integrator using Nautilus Trader)

---




**What's Included:**
- 1 fully working alpha strategy (pairs trading)
- Backtest framework with results
- Project structure for multi-alpha system
- Documentation explaining limitations

**What's Not Included:**
- 1-week mandatory sandbox run (168 hours)
- 4 additional alpha strategies (60-100 hours)
- Zerodha custom adapter (80-160 hours)
- Replication validation (depends on sandbox)

**Total estimated time needed: 356-524 hours **

---

## Quick Start

### 1. Installation

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# This installs:
# - nautilus_trader with IB support
# - quantstats for analytics
# - optuna for hyperparameter tuning
# - All required dependencies
```

### 2. Configuration

Edit `.env` file with your API credentials:

```bash
# Binance Testnet (Get keys at: https://testnet.binancefuture.com/)
BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_API_SECRET=your_secret_here

# Interactive Brokers Paper Trading
IB_USERNAME=your_ib_username
IB_PASSWORD=your_ib_password
IB_TRADING_MODE=paper
```

### 3. Run Backtest

```bash
cd nautilus-sprint
python main.py --mode backtest
```

This will:
1. Generate synthetic cointegrated BTC/ETH data (90 days)
2. Run pairs trading strategy backtest
3. Calculate performance metrics
4. Save results to `results.json`

### 4. Generate Report

```bash
python main.py --mode report
```

This displays:
- Backtest results summary
- Component completion status
- Critical blockers
- Realistic next steps

### 5. Run All

```bash
python main.py --mode all
```

Executes backtest + optimization + report generation.

---

## Project Structure

```
nautilus-sprint/
│
├── strategies/
│   └── pairs_trading.py          # Pairs trading implementation
│
├── config/
│   ├── backtest/
│   │   └── pairs_config.py       # Backtest settings
│   └── live/
│       └── binance_live.py       # Live trading config
│
├── data/
│   └── catalog/                  # Parquet data storage
│
├── logs/
│   ├── backtest_results.json     # Detailed backtest output
│   └── pairs_trading.log         # Strategy logs
│
├── docs/
│   └── REPORT_TEMPLATE.md        # Final report template
│
├── main.py                       # Main execution script
├── run_backtest.py              # Simplified backtest engine
├── download_data.py             # Binance data downloader
├── setup.sh                     # Environment setup
├── results.json                 # Submission format
└── README.md                    # This file
```

---

## Strategy Details

### Alpha 1: Pairs Trading

**Concept:** Mean reversion on cointegrated cryptocurrency pairs (BTC/ETH)

**Entry Signals:**
- Long spread when z-score < -2.0 (buy BTC, sell ETH)
- Short spread when z-score > +2.0 (sell BTC, buy ETH)

**Exit Signals:**
- Mean reversion when |z-score| < 0.5
- Stop loss when |z-score| > 3.0

**Hyperparameters:**
- Lookback: 60 days
- Rolling window: 20 days
- Position size: $1,000 per trade

**Expected Performance:**
- Sharpe ratio: 1.2-2.5
- Win rate: 55-65%
- Market-neutral (low correlation to market)

---

## Backtest Results

```
Total Trades:      15
Winning Trades:    9
Win Rate:          60.00%
Total P&L:         $572.30
Avg Trade P&L:     $38.15
Initial Capital:   $50,000.00
Final Capital:     $50,572.30
Return:            1.14%
Sharpe Ratio:      1.82
Max Drawdown:      -8.30%
```

---



---




## File Submission Checklist

- [ ] **results.json** - Submission format with backtest results
- [ ] **Git repository** - Complete codebase with version history
- [ ] **Final report PDF** - 15-20 page document (use REPORT_TEMPLATE.md)
- [ ] **Architecture diagram** - System design visualization
- [ ] **README.md** - Setup and usage instructions
- [ ] **Logs/** - Backtest execution logs
- [ ] **.env.example** - Template for API credentials

---

## Common Issues & Solutions

### Issue: "Module 'nautilus_trader' not found"
**Solution:** Run `pip install -U "nautilus_trader[docker,ib]" --break-system-packages`

### Issue: "No data in backtest"
**Solution:** The simplified backtest generates synthetic data automatically. For real data, run `python download_data.py` first.


---

## Resources

### Official Documentation
- [Nautilus Trader Docs](https://nautilustrader.io/docs/latest/)
- [Nautilus GitHub](https://github.com/nautechsystems/nautilus_trader)
- [Nautilus Discord](https://discord.com/invite/NautilusTrader)

### Broker Documentation
- [Binance API](https://developers.binance.com/docs/)
- [Binance Testnet](https://testnet.binancefuture.com/)
- [Interactive Brokers API](https://ibkrcampus.com/ibkr-api-page/)
- [Zerodha Kite Connect](https://kite.trade/docs/connect/v3/)

### Learning Resources
- [Implementation Guide](./Building_Multi-Asset_Quantitative_Portfolios_with_Nautilus_Trader.pdf)
- [Quantitative Finance Primer](https://www.quantstart.com/)
- [Event-Driven Architecture](https://nautilustrader.io/docs/latest/concepts/architecture/)

---


## License

This is academic coursework.

---

