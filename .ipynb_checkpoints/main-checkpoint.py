
import sys
import os
import argparse
from pathlib import Path


def run_backtest():
    
    
    print("RUNNING BACKTEST")
  
    
    from run_backtest import main as backtest_main
    backtest_main()


def run_live_trading():

    print("STARTING LIVE TRADING")
    api_key = os.getenv('BINANCE_TESTNET_API_KEY')
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')
    
    if not api_key or not api_secret:
        print("\nERROR: Binance testnet credentials not found!")
        print("\nPlease set environment variables:")
        print("  export BINANCE_TESTNET_API_KEY='your_key'")
        print("  export BINANCE_TESTNET_API_SECRET='your_secret'")
        return
    
    print("Starting live trading node...")
    
   
    try:
        from nautilus_trader.live.node import TradingNode
        from config.live.binance_live import create_live_config
        
        config = create_live_config()
        node = TradingNode(config=config)
        node.start()
        node.run()
        
    except KeyboardInterrupt:
        node.stop()
        print("Shutdown complete")
        
    except Exception as e:
        print(f"\nERROR: {e}")

def run_hyperparameter_tuning():
   
  
    print("HYPERPARAMETER TUNING")


def generate_report():
    print("GENERATING FINAL REPORT")
    
    
    if not os.path.exists('./results.json'):
        print("\nERROR: No results found")
        return
    
    import json
    with open('./results.json', 'r') as f:
        results = json.load(f)
    
    print("\n=== TRACK B SUBMISSION PACKAGE ===\n")
    
    print("✓ Component Status:")
    print("  [DONE] Strategy Implementation (Pairs Trading)")
    print("  [DONE] Backtest Framework")
    print("  [DONE] Results Generation")
    print("  [TODO] 1-Week Sandbox Deployment (Cannot compress)")
    print("  [TODO] Replication Validation (Requires sandbox data)")
    
    print("\n✓ Backtest Results:")
    if 'metrics' in results:
        print(f"  - Return: {results['metrics']['return_pct']:.2f}%")
        print(f"  - Sharpe: {results['metrics']['sharpe_ratio']:.3f}")
        print(f"  - Max DD: {results['metrics']['max_drawdown']:.2%}")
        print(f"  - Win Rate: {results['metrics']['win_rate']:.2%}")
    
    print("\n Files Generated:")
    print("  - results.json (submission format)")
    print("  - logs/backtest_results.json (detailed)")
   
   


def main():
   
    parser = argparse.ArgumentParser(description='Nautilus Trader - 24 Hour Sprint')
    parser.add_argument('--mode', choices=['backtest', 'live', 'optimize', 'report', 'all'],
                       default='all', help='Execution mode')
    
    args = parser.parse_args()
    
    
   
    # Create necessary directories
    os.makedirs('./logs', exist_ok=True)
    os.makedirs('./data', exist_ok=True)
    os.makedirs('./monitoring', exist_ok=True)
    
    if args.mode == 'backtest' or args.mode == 'all':
        run_backtest()
    
    if args.mode == 'optimize' or args.mode == 'all':
        run_hyperparameter_tuning()
    
    if args.mode == 'report' or args.mode == 'all':
        generate_report()
    
    if args.mode == 'live':
        run_live_trading()
    
    

if __name__ == "__main__":
    main()
