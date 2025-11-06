#!/bin/bash

# Nautilus Trader Track B - 24 Hour Sprint Setup
# Run this first: bash setup.sh

set -e

echo "=== Setting up Nautilus Trader Environment ==="

# Install Nautilus with IB support
pip install -U "nautilus_trader[docker,ib]" --break-system-packages

# Install additional dependencies
pip install quantstats optuna pandas numpy matplotlib seaborn --break-system-packages

# Create project structure
mkdir -p nautilus-sprint/{config/{backtest,live,strategies},strategies,data/catalog,tests,logs,monitoring,docs}

# Create environment file template
cat > nautilus-sprint/.env << 'EOF'
# Binance Testnet Credentials
BINANCE_TESTNET_API_KEY=9pxqASgWyqawB9QW4V2Etd67BwaGAHJn73eBLPbPDtKg0nqlfalDx9mn9jv1ulxr
BINANCE_TESTNET_API_SECRET=pTHf4I3FKcMrgl4kmTLNRfdt9ZFZLfZLPPcEj5MJbyNUqXTXhzXr3avHkJKRYOf6


echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit nautilus-sprint/.env with your API credentials"
echo "2. Get Binance testnet keys: https://testnet.binance.vision/"
echo "3. Create IBKR paper account: https://www.interactivebrokers.com/en/trading/tws-updateable-latest.php"
echo ""
echo "Then run: python main.py"