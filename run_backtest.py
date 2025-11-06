"""
Simplified Backtest Runner - For 24-hour sprint demonstration
This creates synthetic data to demonstrate the system without needing real market data
"""

import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json


class SimplifiedPairsBacktest:
    """Simplified pairs trading backtest for demonstration"""
    
    def __init__(self, config):
        self.config = config
        self.trades = []
        self.equity_curve = []
        self.initial_capital = 50000
        self.capital = self.initial_capital
        
    def generate_synthetic_data(self, days=90):
        """Generate synthetic cointegrated price data"""
        print("Generating synthetic market data...")
        
        # Generate correlated random walks
        n_bars = days * 1440  # 1-minute bars
        
        # BTC price simulation
        btc_returns = np.random.normal(0.0001, 0.02, n_bars)
        btc_prices = 40000 * np.exp(np.cumsum(btc_returns))
        
        # ETH price simulation (cointegrated with BTC)
        correlation = 0.85
        eth_returns = (
            correlation * btc_returns + 
            np.sqrt(1 - correlation**2) * np.random.normal(0.0001, 0.02, n_bars)
        )
        eth_prices = 2500 * np.exp(np.cumsum(eth_returns))
        
        # Create timestamps
        start_date = datetime(2024, 1, 1)
        timestamps = [start_date + timedelta(minutes=i) for i in range(n_bars)]
        
        # Create DataFrames
        btc_df = pd.DataFrame({
            'timestamp': timestamps,
            'close': btc_prices,
            'open': btc_prices * (1 + np.random.uniform(-0.001, 0.001, n_bars)),
            'high': btc_prices * (1 + np.random.uniform(0, 0.002, n_bars)),
            'low': btc_prices * (1 + np.random.uniform(-0.002, 0, n_bars)),
            'volume': np.random.uniform(1000, 5000, n_bars)
        })
        
        eth_df = pd.DataFrame({
            'timestamp': timestamps,
            'close': eth_prices,
            'open': eth_prices * (1 + np.random.uniform(-0.001, 0.001, n_bars)),
            'high': eth_prices * (1 + np.random.uniform(0, 0.002, n_bars)),
            'low': eth_prices * (1 + np.random.uniform(-0.002, 0, n_bars)),
            'volume': np.random.uniform(5000, 20000, n_bars)
        })
        
        print(f"Generated {n_bars} bars for BTC and ETH")
        return btc_df, eth_df
    
    def calculate_hedge_ratio(self, btc_prices, eth_prices):
        """Calculate hedge ratio using linear regression"""
        log_btc = np.log(btc_prices)
        log_eth = np.log(eth_prices)
        
        beta = np.polyfit(log_eth, log_btc, 1)[0]
        return beta
    
    def calculate_spread(self, btc_price, eth_price, hedge_ratio):
        """Calculate spread between pairs"""
        return np.log(btc_price) - hedge_ratio * np.log(eth_price)
    
    def calculate_zscore(self, spreads, window=20*1440):
        """Calculate z-score of spread"""
        if len(spreads) < window:
            return 0
        
        recent_spreads = spreads[-window:]
        mean = np.mean(recent_spreads)
        std = np.std(recent_spreads)
        
        if std == 0:
            return 0
        
        return (spreads[-1] - mean) / std
    
    def run_backtest(self, btc_df, eth_df):
        """Run the pairs trading backtest"""
        print("\nRunning backtest...")
        
        # Calculate hedge ratio
        lookback = 60 * 1440  # 60 days
        hedge_ratio = self.calculate_hedge_ratio(
            btc_df['close'].iloc[:lookback].values,
            eth_df['close'].iloc[:lookback].values
        )
        print(f"Hedge ratio: {hedge_ratio:.4f}")
        
        # Calculate spreads
        spreads = []
        in_position = False
        position_side = None
        entry_btc = None
        entry_eth = None
        
        z_entry = self.config['z_entry_threshold']
        z_exit = self.config['z_exit_threshold']
        z_stop = self.config['z_stop_loss']
        position_size = self.config['position_size_usd']
        
        trade_count = 0
        winning_trades = 0
        total_pnl = 0
        
        # Simulate trading
        for i in range(lookback, len(btc_df)):
            btc_price = btc_df['close'].iloc[i]
            eth_price = eth_df['close'].iloc[i]
            timestamp = btc_df['timestamp'].iloc[i]
            
            # Calculate spread
            spread = self.calculate_spread(btc_price, eth_price, hedge_ratio)
            spreads.append(spread)
            
            # Calculate z-score
            z_score = self.calculate_zscore(spreads)
            
            # Track equity
            if i % 1440 == 0:  # Daily snapshot
                self.equity_curve.append({
                    'timestamp': timestamp,
                    'capital': self.capital
                })
            
            # Trading logic
            if in_position:
                # Check stop loss
                if abs(z_score) > z_stop:
                    # Close position - stop loss
                    pnl = self._close_position(
                        position_side, entry_btc, entry_eth, 
                        btc_price, eth_price, hedge_ratio, position_size
                    )
                    self.capital += pnl
                    total_pnl += pnl
                    
                    self.trades.append({
                        'entry_time': entry_time,
                        'exit_time': timestamp,
                        'side': position_side,
                        'pnl': pnl,
                        'exit_reason': 'stop_loss',
                        'z_score': z_score
                    })
                    
                    if pnl > 0:
                        winning_trades += 1
                    trade_count += 1
                    
                    in_position = False
                    position_side = None
                    
                # Check exit signal
                elif (position_side == 'long' and z_score > -z_exit) or \
                     (position_side == 'short' and z_score < z_exit):
                    # Close position - normal exit
                    pnl = self._close_position(
                        position_side, entry_btc, entry_eth,
                        btc_price, eth_price, hedge_ratio, position_size
                    )
                    self.capital += pnl
                    total_pnl += pnl
                    
                    self.trades.append({
                        'entry_time': entry_time,
                        'exit_time': timestamp,
                        'side': position_side,
                        'pnl': pnl,
                        'exit_reason': 'signal',
                        'z_score': z_score
                    })
                    
                    if pnl > 0:
                        winning_trades += 1
                    trade_count += 1
                    
                    in_position = False
                    position_side = None
            
            else:
                # Check entry signals
                if z_score < -z_entry:
                    # Enter long spread
                    in_position = True
                    position_side = 'long'
                    entry_btc = btc_price
                    entry_eth = eth_price
                    entry_time = timestamp
                    
                elif z_score > z_entry:
                    # Enter short spread
                    in_position = True
                    position_side = 'short'
                    entry_btc = btc_price
                    entry_eth = eth_price
                    entry_time = timestamp
        
        # Calculate metrics
        win_rate = winning_trades / trade_count if trade_count > 0 else 0
        avg_trade = total_pnl / trade_count if trade_count > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        if len(self.equity_curve) > 1:
            returns = pd.DataFrame(self.equity_curve)['capital'].pct_change().dropna()
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        else:
            sharpe = 0
        
        # Calculate max drawdown
        equity_series = pd.DataFrame(self.equity_curve)['capital']
        cummax = equity_series.cummax()
        drawdown = (equity_series - cummax) / cummax
        max_dd = drawdown.min()
        
        results = {
            'total_trades': trade_count,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_trade': avg_trade,
            'final_capital': self.capital,
            'return_pct': ((self.capital - self.initial_capital) / self.initial_capital) * 100,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'hedge_ratio': hedge_ratio
        }
        
        return results
    
    def _close_position(self, side, entry_btc, entry_eth, exit_btc, exit_eth, hedge_ratio, position_size):
        """Calculate P&L for closing position"""
        # Simplified P&L calculation
        if side == 'long':
            # Long BTC, Short ETH
            btc_pnl = (exit_btc - entry_btc) / entry_btc * position_size
            eth_pnl = (entry_eth - exit_eth) / entry_eth * position_size * hedge_ratio
        else:
            # Short BTC, Long ETH
            btc_pnl = (entry_btc - exit_btc) / entry_btc * position_size
            eth_pnl = (exit_eth - entry_eth) / entry_eth * position_size * hedge_ratio
        
        # Account for slippage (0.1%)
        slippage = position_size * 0.001
        
        return btc_pnl + eth_pnl - slippage


def main():
    """Run simplified backtest"""
    print("=" * 60)
    print("SIMPLIFIED PAIRS TRADING BACKTEST")
    print("=" * 60)
    
    # Configuration
    config = {
        'lookback_period': 60,
        'rolling_window': 20,
        'z_entry_threshold': 2.0,
        'z_exit_threshold': 0.5,
        'z_stop_loss': 3.0,
        'position_size_usd': 1000.0
    }
    
    # Initialize backtest
    backtest = SimplifiedPairsBacktest(config)
    
    # Generate synthetic data
    btc_df, eth_df = backtest.generate_synthetic_data(days=90)
    
    # Run backtest
    results = backtest.run_backtest(btc_df, eth_df)
    
    # Print results
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print(f"Total Trades:      {results['total_trades']}")
    print(f"Winning Trades:    {results['winning_trades']}")
    print(f"Win Rate:          {results['win_rate']:.2%}")
    print(f"Total P&L:         ${results['total_pnl']:.2f}")
    print(f"Avg Trade P&L:     ${results['avg_trade']:.2f}")
    print(f"Initial Capital:   ${backtest.initial_capital:.2f}")
    print(f"Final Capital:     ${results['final_capital']:.2f}")
    print(f"Return:            {results['return_pct']:.2f}%")
    print(f"Sharpe Ratio:      {results['sharpe_ratio']:.3f}")
    print(f"Max Drawdown:      {results['max_drawdown']:.2%}")
    print(f"Hedge Ratio:       {results['hedge_ratio']:.4f}")
    print("=" * 60)
    
    # Save results
    with open('./logs/backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to ./logs/backtest_results.json")
    
    # Generate results.json for submission
    submission_results = {
        "portfolio_pnl": {
            "sandbox_pnl": 0.0,  # To be filled from sandbox run
            "backtest_pnl": results['total_pnl'],
            "pnl_match": "PENDING"
        },
        "alphas": {
            "alpha_1_pairs": {
                "trades": results['total_trades'],
                "pnl": results['total_pnl'],
                "match": "PENDING",
                "analysis": "Backtest completed. Awaiting sandbox deployment for replication test."
            }
        },
        "metrics": {
            "win_rate": results['win_rate'],
            "sharpe_ratio": results['sharpe_ratio'],
            "max_drawdown": results['max_drawdown'],
            "return_pct": results['return_pct']
        }
    }
    
    with open('./results.json', 'w') as f:
        json.dump(submission_results, f, indent=2)
    
    print("Submission results template saved to ./results.json")


if __name__ == "__main__":
    import os
    os.makedirs('./logs', exist_ok=True)
    main()
