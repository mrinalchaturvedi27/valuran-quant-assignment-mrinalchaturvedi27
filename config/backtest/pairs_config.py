
import pandas as pd
from nautilus_trader.backtest.node import BacktestNode, BacktestRunConfig
from nautilus_trader.config import BacktestVenueConfig, BacktestDataConfig, ImportableStrategyConfig
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from datetime import datetime


def create_backtest_config():
  
    
    config = BacktestRunConfig(
        engine_id="pairs_backtest_001",
        venues=[
            BacktestVenueConfig(
                name="BINANCE",
                oms_type="NETTING",
                account_type="MARGIN",  
                starting_balances=["50000 USDT"],
                base_currency="USDT",
                bar_adaptive_high_low_ordering=True,  
            )
        ],
        data=[
            # BTC data
            BacktestDataConfig(
                catalog_path="./data/catalog",
                data_cls="Bar",
                instrument_id="BTCUSDT-PERP.BINANCE",
                bar_type="1-MINUTE-LAST",
                start_time="2024-01-01T00:00:00Z",
                end_time="2024-03-31T23:59:59Z"
            ),
            # ETH data
            BacktestDataConfig(
                catalog_path="./data/catalog",
                data_cls="Bar",
                instrument_id="ETHUSDT-PERP.BINANCE",
                bar_type="1-MINUTE-LAST",
                start_time="2024-01-01T00:00:00Z",
                end_time="2024-03-31T23:59:59Z"
            ),
        ],
        strategies=[
            ImportableStrategyConfig(
                strategy_path="strategies.pairs_trading:PairsTradingStrategy",
                config_path="strategies.pairs_trading:PairsTradingConfig",
                config={
                    "instrument_id_a": "BTCUSDT-PERP.BINANCE",
                    "instrument_id_b": "ETHUSDT-PERP.BINANCE",
                    "bar_type": "1-MINUTE-LAST",
                    "lookback_period": 60,
                    "rolling_window": 20,
                    "z_entry_threshold": 2.0,
                    "z_exit_threshold": 0.5,
                    "z_stop_loss": 3.0,
                    "position_size_usd": 1000.0,
                    "order_id_tag": "001"
                }
            )
        ],
        
        fill_model={
            "prob_fill_on_limit": 0.5,  
            "prob_slippage": 0.3,  
            "random_seed": 42
        }
    )
    
    return config


if __name__ == "__main__":
    print("=== Pairs Trading Backtest Configuration ===")
    print("This configuration tests BTC/ETH pairs trading")
    print("Date range: 2024-01-01 to 2024-03-31")
    print("Strategy: Mean reversion on cointegrated pair")
