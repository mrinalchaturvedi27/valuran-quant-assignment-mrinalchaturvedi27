"""
Pairs Trading Strategy - Alpha 1
Mean reversion strategy on cointegrated crypto pairs (BTC/ETH)
"""

from decimal import Decimal
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
from nautilus_trader.model.data import Bar
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.orders import MarketOrder
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.config import StrategyConfig


class PairsTradingConfig(StrategyConfig, frozen=True):
    instrument_id_a: 
    instrument_id_b:
    bar_type: str = "1-MINUTE-LAST"
    lookback_period: int = 60  
    rolling_window: int = 20  
    z_exit_threshold: float = 0.5
    z_stop_loss: float = 3.0
    position_size_usd: float = 1000.0
    order_id_tag: str = "001"


class PairsTradingStrategy(Strategy):    
    def __init__(self, config: PairsTradingConfig):
        super().__init__(config)
        
        # Configuration
        self.instrument_id_a = InstrumentId.from_str(config.instrument_id_a)
        self.instrument_id_b = InstrumentId.from_str(config.instrument_id_b)
        self.lookback_period = config.lookback_period
        self.rolling_window = config.rolling_window
        self.z_entry = config.z_entry_threshold
        self.z_exit = config.z_exit_threshold
        self.z_stop = config.z_stop_loss
        self.position_size_usd = config.position_size_usd
        
        # State tracking
        self.prices_a = []
        self.prices_b = []
        self.spreads = []
        self.hedge_ratio = None
        self.in_position = False
        self.position_side = None  # 'long' or 'short'
        
        # For logging
        self.trade_count = 0
        
    def on_start(self):
        self.log.info(f"Starting Pairs Trading Strategy")
        self.log.info(f"Pair: {self.instrument_id_a} / {self.instrument_id_b}")
        
        # Subscribe to 1-minute bars for both instruments
        bar_type_a = f"{self.instrument_id_a}-{self.config.bar_type}"
        bar_type_b = f"{self.instrument_id_b}-{self.config.bar_type}"
        
        self.subscribe_bars(bar_type_a)
        self.subscribe_bars(bar_type_b)
        
        self.log.info("Subscribed to bar data")
        
    def on_bar(self, bar: Bar):
        # Store prices
        if bar.bar_type.instrument_id == self.instrument_id_a:
            self.prices_a.append(float(bar.close))
        elif bar.bar_type.instrument_id == self.instrument_id_b:
            self.prices_b.append(float(bar.close))
        else:
            return
        
       
        if len(self.prices_a) < 2 or len(self.prices_b) < 2:
            return
        
       
        max_length = self.lookback_period * 1440  # Assuming 1-min bars
        if len(self.prices_a) > max_length:
            self.prices_a = self.prices_a[-max_length:]
        if len(self.prices_b) > max_length:
            self.prices_b = self.prices_b[-max_length:]
        
       
        min_len = min(len(self.prices_a), len(self.prices_b))
        prices_a_sync = self.prices_a[-min_len:]
        prices_b_sync = self.prices_b[-min_len:]
        
       
        if min_len < self.rolling_window:
            return
       
        if self.hedge_ratio is None and min_len >= 100:
            self.hedge_ratio = self._calculate_hedge_ratio(prices_a_sync, prices_b_sync)
            self.log.info(f"Hedge ratio calculated: {self.hedge_ratio:.4f}")
        
        if self.hedge_ratio is None:
            return
        
       
        spread = np.log(prices_a_sync[-1]) - self.hedge_ratio * np.log(prices_b_sync[-1])
        self.spreads.append(spread)
        
       
        if len(self.spreads) > self.rolling_window * 1440:
            self.spreads = self.spreads[-(self.rolling_window * 1440):]
        
        if len(self.spreads) < self.rolling_window:
            return
        
        # Calculate z-score
        mean_spread = np.mean(self.spreads[-self.rolling_window * 1440:])
        std_spread = np.std(self.spreads[-self.rolling_window * 1440:])
        
        if std_spread == 0:
            return
        
        z_score = (spread - mean_spread) / std_spread
        
        self.log.debug(f"Z-score: {z_score:.3f}, Spread: {spread:.6f}")
        
        # Trading logic
        self._execute_trading_logic(z_score, prices_a_sync[-1], prices_b_sync[-1])
        
    def _calculate_hedge_ratio(self, prices_a, prices_b):
       
        log_a = np.log(prices_a)
        log_b = np.log(prices_b)
        
        
        _, p_value, _ = coint(log_a, log_b)
        self.log.info(f"Cointegration p-value: {p_value:.4f}")
        
        if p_value > 0.05:
            self.log.warning("Pair not cointegrated (p > 0.05)")
        
        
        beta = np.polyfit(log_b, log_a, 1)[0]
        return beta
        
    def _execute_trading_logic(self, z_score, price_a, price_b):
      
        
        # Stop loss check
        if self.in_position and abs(z_score) > self.z_stop:
            self.log.warning(f"Stop loss triggered! Z-score: {z_score:.3f}")
            self._close_position()
            return
        
        # Exit conditions
        if self.in_position:
            if self.position_side == 'long' and z_score > -self.z_exit:
                self.log.info(f"Exit signal (long): z={z_score:.3f}")
                self._close_position()
            elif self.position_side == 'short' and z_score < self.z_exit:
                self.log.info(f"Exit signal (short): z={z_score:.3f}")
                self._close_position()
            return
        
        # Entry conditions
        if not self.in_position:
            # Enter long spread (buy A, sell B) when z-score < -threshold
            if z_score < -self.z_entry:
                self.log.info(f"Entry signal LONG spread: z={z_score:.3f}")
                self._enter_long_spread(price_a, price_b)
                
            # Enter short spread (sell A, buy B) when z-score > +threshold
            elif z_score > self.z_entry:
                self.log.info(f"Entry signal SHORT spread: z={z_score:.3f}")
                self._enter_short_spread(price_a, price_b)
    
    def _enter_long_spread(self, price_a, price_b):
        # Calculate position sizes
        qty_a = self.position_size_usd / price_a
        qty_b = (self.hedge_ratio * self.position_size_usd) / price_b
        
        # Round to appropriate precision
        qty_a = round(qty_a, 3)
        qty_b = round(qty_b, 3)
        
        self.log.info(f"Entering LONG spread: Buy {qty_a} A @ {price_a}, Sell {qty_b} B @ {price_b}")
        
        # Submit orders 
        self.in_position = True
        self.position_side = 'long'
        self.trade_count += 1
        
    def _enter_short_spread(self, price_a, price_b):
        """Enter short spread: Sell A, Buy B"""
        # Calculate position sizes
        qty_a = self.position_size_usd / price_a
        qty_b = (self.hedge_ratio * self.position_size_usd) / price_b
        
        qty_a = round(qty_a, 3)
        qty_b = round(qty_b, 3)
        
        self.log.info(f"Entering SHORT spread: Sell {qty_a} A @ {price_a}, Buy {qty_b} B @ {price_b}")
        
        self.in_position = True
        self.position_side = 'short'
        self.trade_count += 1
        
    def _close_position(self):
        """Close current spread position"""
        self.log.info(f"Closing {self.position_side} spread position")
        self.in_position = False
        self.position_side = None
        
    def on_stop(self):
        """Cleanup when strategy stops"""
        if self.in_position:
            self._close_position()
        
        self.log.info(f"Strategy stopped. Total trades: {self.trade_count}")
        
    def on_reset(self):
        self.prices_a.clear()
        self.prices_b.clear()
        self.spreads.clear()
        self.hedge_ratio = None
        self.in_position = False
        self.position_side = None
        self.trade_count = 0
