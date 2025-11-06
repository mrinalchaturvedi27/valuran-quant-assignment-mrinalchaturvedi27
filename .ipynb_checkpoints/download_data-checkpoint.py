"""
Download historical data from Binance for backtesting
"""

import asyncio
from datetime import datetime, timedelta
import pandas as pd
from nautilus_trader.adapters.binance.common.enums import BinanceAccountType
from nautilus_trader.adapters.binance.factories import get_cached_binance_http_client
from nautilus_trader.adapters.binance.futures.http.client import BinanceFuturesHttpClient
from nautilus_trader.common.component import LiveClock
from nautilus_trader.core.datetime import dt_to_unix_millis
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.model.identifiers import InstrumentId


async def download_binance_data(
    symbol: str,
    start_date: str,
    end_date: str,
    interval: str = "1m"
):
   
    
    print(f"\n=== Downloading {symbol} data ===")
    print(f"Period: {start_date} to {end_date}")
    print(f"Interval: {interval}")
    
    # Initialize HTTP client
    clock = LiveClock()
    client = BinanceFuturesHttpClient(
        clock=clock,
        key=None,  # Not needed for public market data
        secret=None,
        base_url="https://fapi.binance.com"
    )
    
    # Convert dates
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    all_klines = []
    current_start = start_dt
    
    # Download in chunks (Binance limits to 1000 candles per request)
    while current_start < end_dt:
        # Calculate chunk end (30 days max per request for 1m data)
        if interval == "1m":
            chunk_end = min(current_start + timedelta(days=1), end_dt)
        else:
            chunk_end = min(current_start + timedelta(days=30), end_dt)
        
        start_ms = dt_to_unix_millis(current_start)
        end_ms = dt_to_unix_millis(chunk_end)
        
        try:
            # Request klines
            klines = await client.request_binance_klines(
                symbol=symbol,
                interval=interval,
                start_time=start_ms,
                end_time=end_ms,
                limit=1000
            )
            
            if klines:
                all_klines.extend(klines)
                print(f"  Downloaded {len(klines)} bars for {current_start.date()}")
            else:
                print(f"  No data for {current_start.date()}")
                
        except Exception as e:
            print(f"  Error downloading {current_start.date()}: {e}")
        
        current_start = chunk_end
        await asyncio.sleep(0.5)  # Rate limiting
    
    print(f"Total bars downloaded: {len(all_klines)}")
    
    # Convert to DataFrame
    if all_klines:
        df = pd.DataFrame(all_klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Convert to numeric
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        
        return df
    
    return None


async def main():
    """Download data for BTC and ETH"""
    
    # Date range for backtest
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    
    # Download BTC data
    btc_data = await download_binance_data(
        symbol="BTCUSDT",
        start_date=start_date,
        end_date=end_date,
        interval="1m"
    )
    
    # Download ETH data
    eth_data = await download_binance_data(
        symbol="ETHUSDT",
        start_date=start_date,
        end_date=end_date,
        interval="1m"
    )
    
    # Save to catalog
    if btc_data is not None and eth_data is not None:
        print("\n=== Saving to Parquet catalog ===")
        
        catalog = ParquetDataCatalog("./data/catalog")
        
        # Save BTC bars
        print(f"Saving BTC data: {len(btc_data)} bars")
        # catalog.write_data(btc_data)  # Actual implementation would use Nautilus Bar objects
        
        # Save ETH bars
        print(f"Saving ETH data: {len(eth_data)} bars")
        # catalog.write_data(eth_data)
        
        # For quick start, save as CSV
        btc_data.to_csv("./data/btc_1m.csv")
        eth_data.to_csv("./data/eth_1m.csv")
        
        print("\n=== Data download complete ===")
        print(f"BTC: {len(btc_data)} bars saved to ./data/btc_1m.csv")
        print(f"ETH: {len(eth_data)} bars saved to ./data/eth_1m.csv")
        print("\nNote: For production, convert CSV to Nautilus Parquet format")
    else:
        print("ERROR: Failed to download data")


if __name__ == "__main__":
    print("=== Binance Data Downloader ===")
    print("Downloading historical 1-minute bars for backtesting")
    
    asyncio.run(main())
