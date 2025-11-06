
import os
from dotenv import load_dotenv
from nautilus_trader.config import (
    TradingNodeConfig,
    LoggingConfig,
    CacheDatabaseConfig,
    DataEngineConfig,
    RiskEngineConfig,
    ExecEngineConfig,
    StreamingConfig
)
from nautilus_trader.adapters.binance.config import BinanceDataClientConfig, BinanceExecClientConfig
from nautilus_trader.adapters.binance.common.enums import BinanceAccountType

load_dotenv()
def create_live_config():
   
    
    # Load credentials from environment
    api_key = os.getenv('BINANCE_TESTNET_API_KEY', 'YOUR_API_KEY_HERE')
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET', 'YOUR_API_SECRET_HERE')
    
    
    config = TradingNodeConfig(
        trader_id="PAIRS-TRADER-001",
        
        # Logging configuration
        logging=LoggingConfig(
            log_level="INFO",
            log_file_format="json",
            log_directory="./logs",
            log_file_name="pairs_trading.log"
        ),
        
        # Cache configuration
        cache_database=CacheDatabaseConfig(
            type="redis",
            host="localhost",
            port=6379
        ),
        
        # Data engine configuration
        data_engine=DataEngineConfig(
            time_bars_build_with_no_updates=False,
            validate_data_sequence=True,
            debug=False
        ),
        
        # Risk engine configuration
        risk_engine=RiskEngineConfig(
            bypass=False,  # Enable risk checks
            max_order_submit_rate="100/00:00:01",  
            max_notional_per_order={
                "BTC/USDT": 10000,  # Max $10k per order
                "ETH/USDT": 10000
            }
        ),
        
        # Execution engine configuration
        exec_engine=ExecEngineConfig(
            load_cache=True,
            snapshot_orders=True,
            snapshot_positions=True
        ),
        
        # Streaming configuration (for monitoring)
        streaming=StreamingConfig(
            catalog_path="./data/catalog"
        ),
        
        # Binance data client
        data_clients={
            "BINANCE": BinanceDataClientConfig(
                api_key=api_key,
                api_secret=api_secret,
                account_type=BinanceAccountType.USDT_FUTURE,
                testnet=True,
                base_url_http="https://testnet.binancefuture.com",
                base_url_ws="wss://stream.binancefuture.com"
            )
        },
        
        # Binance execution client
        exec_clients={
            "BINANCE": BinanceExecClientConfig(
                api_key=api_key,
                api_secret=api_secret,
                account_type=BinanceAccountType.USDT_FUTURE,
                testnet=True,
                base_url_http="https://testnet.binancefuture.com",
                base_url_ws="wss://stream.binancefuture.com"
            )
        },
        
        # Strategy configuration
        strategies=[
            {
                "strategy_path": "strategies.pairs_trading:PairsTradingStrategy",
                "config_path": "strategies.pairs_trading:PairsTradingConfig",
                "config": {
                    "instrument_id_a": "BTCUSDT-PERP.BINANCE",
                    "instrument_id_b": "ETHUSDT-PERP.BINANCE",
                    "bar_type": "1-MINUTE-LAST",
                    "lookback_period": 60,
                    "rolling_window": 20,
                    "z_entry_threshold": 2.0,
                    "z_exit_threshold": 0.5,
                    "z_stop_loss": 3.0,
                    "position_size_usd": 100.0,  
                    "order_id_tag": "001"
                }
            }
        ],
        
        
        timeout_connection=10.0,
        timeout_reconciliation=10.0,
        timeout_portfolio=10.0,
        timeout_disconnection=10.0
    )
    
    return config


if __name__ == "__main__":
    config = create_live_config()
    print("Live trading configuration created")
    print(f"Trader ID: {config.trader_id}")
    print("Ready to connect to Binance testnet")
