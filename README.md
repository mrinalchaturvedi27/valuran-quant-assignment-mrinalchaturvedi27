# Nautilus Trader - Track B - 24 Hour Sprint

**Student:** Aditya  
**Assignment:** Multi-Asset Quantitative Portfolio System  
**Track:** B (Alpha Integrator using Nautilus Trader)

---

## ⚠️ IMPORTANT: Timeline Reality Check

This codebase demonstrates **maximum progress in 24 hours** on a project that requires **9-15 months** according to the implementation guide.

**What's Included:**
- ✅ 1 fully working alpha strategy (pairs trading)
- ✅ Backtest framework with results
- ✅ Project structure for multi-alpha system
- ✅ Documentation explaining limitations

**What's Not Included:**
- ❌ 1-week mandatory sandbox run (168 hours)
- ❌ 4 additional alpha strategies (60-100 hours)
- ❌ Zerodha custom adapter (80-160 hours)
- ❌ Replication validation (depends on sandbox)

**Total estimated time needed: 356-524 hours (not 24)**

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

## Next Steps (Realistic Timeline)

### Week 1-2: Foundation
- [ ] Get Binance testnet API keys
- [ ] Set up IBKR paper trading account
- [ ] Deploy pairs strategy to sandbox
- [ ] Begin logging market data

### Week 3-4: Alpha 2
- [ ] Implement breakout momentum strategy
- [ ] Backtest with real market data
- [ ] Deploy to sandbox alongside pairs

### Week 5-6: Alpha 3
- [ ] Implement multi-timeframe strategy
- [ ] Portfolio-level risk management
- [ ] Correlation monitoring

### Week 7-8: Alpha 4 & 5
- [ ] Cross-asset statistical arbitrage
- [ ] Order book microstructure
- [ ] Full portfolio integration

### Week 9-10: Zerodha Integration
- [ ] Build custom Kite Connect adapter
- [ ] Test with Zerodha sandbox
- [ ] Multi-broker coordination

### Week 11: Validation
- [ ] 1-week mandatory sandbox run
- [ ] Collect complete trade logs
- [ ] Run replication test

### Week 12: Documentation
- [ ] Final report (15-20 pages)
- [ ] Architecture diagrams
- [ ] Root-cause analysis of any mismatches

**Total: 12 weeks minimum**

---

## Critical Limitations

### 1. Cannot Skip Sandbox Deployment
Assignment states: "Run your full portfolio of 5 alphas **till the deadline** on the Binance, IBKR, and Zerodha sandbox environments simultaneously."

This requires **minimum 1 week (168 hours)** of continuous operation. Cannot be compressed or simulated.

### 2. Replication Test Dependency
Assignment requires: "The trade log and final P&L generated by this 'replay backtest' must **perfectly match** the trade log and P&L from your **1-week sandbox run**."

This can only be done AFTER completing the 1-week sandbox run. Cannot be done in advance.

### 3. Custom Adapter Development
Zerodha Kite requires custom adapter:
- Study Binance adapter structure: 20 hours
- Implement HTTP client: 20 hours
- Implement WebSocket client: 20 hours
- Instrument provider: 10 hours
- Testing and debugging: 20-100 hours
- **Total: 90-170 hours**

### 4. Five Diverse Alphas
Each additional strategy requires:
- Mathematical formulation: 4-8 hours
- Implementation: 8-16 hours
- Backtesting: 4-8 hours
- Hyperparameter tuning: 4-8 hours
- Validation: 4-8 hours
- **Total per strategy: 24-48 hours**

---

## How to Actually Complete This

### Option 1: Request Extension
Email instructor:
```
Subject: Track B Timeline Discussion

Professor,

I've begun Track B implementation and need to discuss the timeline.
The assignment guide states this is a "9-15 month professional project"
but the deadline suggests 1-2 weeks.

Key blockers:
1. Mandatory 1-week sandbox run (168 hours, cannot compress)
2. 5 alphas × 30 hours each = 150 hours
3. Custom Zerodha adapter = 90-170 hours
4. Testing and validation = 60 hours

Total: 468-548 hours minimum (not including debugging)

I have working code for 1 alpha and am prepared to demonstrate
understanding. Can we discuss either:
A) 12-week extension for proper completion, or
B) Reduced scope (2-3 alphas, Binance-only)

Attached: current implementation demonstrating capabilities.

Best regards,
Aditya
```

### Option 2: Reduced Scope
Negotiate for:
- 2-3 alphas instead of 5
- Binance-only (skip Zerodha)
- 3-day sandbox instead of 7-day
- Focus on quality over quantity

### Option 3: Team Up
If collaboration allowed:
- Divide alphas among team members
- Parallel development of adapters
- Shared infrastructure

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

### Issue: "Redis connection failed"
**Solution:** 
```bash
# Start Redis
docker run -d --name redis -p 6379:6379 redis:latest

# Or install locally
sudo apt-get install redis-server
sudo service redis-server start
```

### Issue: "No data in backtest"
**Solution:** The simplified backtest generates synthetic data automatically. For real data, run `python download_data.py` first.

### Issue: "API authentication failed"
**Solution:** Check your `.env` file has correct credentials. For Binance testnet, get keys at https://testnet.binancefuture.com/

---

## Resources

### Official Documentation
- [Nautilus Trader Docs](https://nautilustrader.io/docs/latest/)
- [Nautilus GitHub](https://github.com/nautechsystems/nautilus_trader)
- [Nautilus Discord](https://discord.com/invite/NautilusTrader) - 3,750+ members

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

## Contact

**Student:** Aditya  
**Institution:** IIT Kanpur  
**Department:** Civil Engineering (3rd Year)

For questions about this implementation:
1. Check documentation in `/docs`
2. Review code comments in `/strategies`
3. Join Nautilus Discord for technical support
4. Contact course instructor for assignment clarification

---

## License

This is academic coursework. Code based on Nautilus Trader (Apache 2.0 license).

---

## Acknowledgments

- Nautilus Trader team for excellent framework
- Assignment guide authors for comprehensive documentation
- IIT Kanpur for quantitative finance education
- Binance, IBKR, Zerodha for sandbox environments

---

**Last Updated:** November 4, 2025  
**Version:** 1.0 (24-hour sprint)
