"""
Finex XAU/USD Scalping Trading Bot
Strategy: EMA Crossover + RSI + MACD confirmation
Platform: MT5 via MetaTrader5 Python library
Account: Demo 60677667
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinexScalpingBot:
    def __init__(self):
        self.symbol = "XAUUSD"
        self.timeframe = mt5.TIMEFRAME_M5
        self.lot_size = 0.01
        self.magic_number = 12345
        
        # Strategy parameters
        self.ema_fast = 5
        self.ema_slow = 10
        self.rsi_period = 14
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        
        # Risk management
        self.stop_loss_pips = 75
        self.take_profit_pips = 40
        self.trailing_stop_pips = 20
        self.max_daily_loss = 5  # USD
        self.min_win_probability = 0.80  # 80% confidence
        
        self.connected = False
        self.daily_pnl = 0
        
    def connect(self, login, password, server):
        """Connect to Finex MT5"""
        try:
            if mt5.initialize(login=login, password=password, server=server):
                self.connected = True
                logger.info(f"Connected to {server} - Account: {login}")
                return True
            else:
                logger.error(f"Failed to connect: {mt5.last_error()}")
                return False
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def get_rates(self, bars=100):
        """Get candle data"""
        try:
            rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, bars)
            if rates is None or len(rates) == 0:
                logger.error(f"No data for {self.symbol}")
                return None
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            logger.error(f"Error getting rates: {e}")
            return None
    
    def calculate_indicators(self, df):
        """Calculate EMA, RSI, MACD"""
        try:
            # EMA
            df['ema_fast'] = df['close'].ewm(span=self.ema_fast).mean()
            df['ema_slow'] = df['close'].ewm(span=self.ema_slow).mean()
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema12 = df['close'].ewm(span=self.macd_fast).mean()
            ema26 = df['close'].ewm(span=self.macd_slow).mean()
            df['macd'] = ema12 - ema26
            df['macd_signal'] = df['macd'].ewm(span=self.macd_signal).mean()
            df['macd_histogram'] = df['macd'] - df['macd_signal']
            
            return df
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return None
    
    def check_buy_signal(self, df):
        """Check if all conditions align for BUY (80%+ confidence)"""
        if len(df) < 2:
            return False, 0.0
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        signals = []
        
        # EMA condition: EMA5 > EMA10 (bullish)
        if latest['ema_fast'] > latest['ema_slow']:
            if prev['ema_fast'] <= prev['ema_slow']:  # Crossover
                signals.append(1.0)  # Strong signal
            else:
                signals.append(0.7)  # Trending
        
        # RSI condition: RSI < 30 (oversold) or 30-50 (good entry)
        if latest['rsi'] < 50 and latest['rsi'] > self.rsi_oversold:
            signals.append(0.8)
        elif latest['rsi'] < self.rsi_oversold:
            signals.append(0.6)  # Very oversold, risky
        
        # MACD condition: MACD > Signal & Histogram positive
        if latest['macd'] > latest['macd_signal']:
            if latest['macd_histogram'] > 0:
                signals.append(1.0)
            else:
                signals.append(0.7)
        
        if not signals:
            return False, 0.0
        
        confidence = np.mean(signals)
        return confidence >= self.min_win_probability, confidence
    
    def check_sell_signal(self, df):
        """Check if all conditions align for SELL"""
        if len(df) < 2:
            return False, 0.0
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        signals = []
        
        # EMA condition: EMA5 < EMA10 (bearish)
        if latest['ema_fast'] < latest['ema_slow']:
            if prev['ema_fast'] >= prev['ema_slow']:  # Crossover
                signals.append(1.0)
            else:
                signals.append(0.7)
        
        # RSI condition: RSI > 70 (overbought)
        if latest['rsi'] > self.rsi_overbought:
            signals.append(1.0)
        elif latest['rsi'] > 50:
            signals.append(0.7)
        
        # MACD condition: MACD < Signal
        if latest['macd'] < latest['macd_signal']:
            if latest['macd_histogram'] < 0:
                signals.append(1.0)
            else:
                signals.append(0.7)
        
        if not signals:
            return False, 0.0
        
        confidence = np.mean(signals)
        return confidence >= self.min_win_probability, confidence
    
    def get_position_info(self):
        """Get current position info"""
        try:
            positions = mt5.positions_get(symbol=self.symbol)
            if positions:
                return positions[0]
            return None
        except Exception as e:
            logger.error(f"Error getting position: {e}")
            return None
    
    def place_buy_order(self, ask_price):
        """Place BUY order with SL & TP"""
        try:
            sl = ask_price - (self.stop_loss_pips * 0.01)
            tp = ask_price + (self.take_profit_pips * 0.01)
            
            request = {
                "action": mt5.TRADE_ACTION_BUY,
                "symbol": self.symbol,
                "volume": self.lot_size,
                "type": mt5.ORDER_TYPE_BUY,
                "price": ask_price,
                "sl": sl,
                "tp": tp,
                "magic": self.magic_number,
                "comment": "Scalping BUY - EMA+RSI+MACD",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"BUY order placed: Ticket {result.order}, Price {ask_price}, SL {sl}, TP {tp}")
                return True
            else:
                logger.error(f"BUY order failed: {result.comment}")
                return False
        except Exception as e:
            logger.error(f"Error placing BUY order: {e}")
            return False
    
    def place_sell_order(self, bid_price):
        """Place SELL order with SL & TP"""
        try:
            sl = bid_price + (self.stop_loss_pips * 0.01)
            tp = bid_price - (self.take_profit_pips * 0.01)
            
            request = {
                "action": mt5.TRADE_ACTION_SELL,
                "symbol": self.symbol,
                "volume": self.lot_size,
                "type": mt5.ORDER_TYPE_SELL,
                "price": bid_price,
                "sl": sl,
                "tp": tp,
                "magic": self.magic_number,
                "comment": "Scalping SELL - EMA+RSI+MACD",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"SELL order placed: Ticket {result.order}, Price {bid_price}, SL {sl}, TP {tp}")
                return True
            else:
                logger.error(f"SELL order failed: {result.comment}")
                return False
        except Exception as e:
            logger.error(f"Error placing SELL order: {e}")
            return False
    
    def close_position(self, position):
        """Close existing position"""
        try:
            if position['type'] == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(self.symbol).bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(self.symbol).ask
            
            request = {
                "action": mt5.TRADE_ACTION_CLOSE,
                "symbol": self.symbol,
                "volume": position['volume'],
                "type": order_type,
                "price": price,
                "position": position['ticket'],
                "magic": self.magic_number,
                "comment": "Close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"Position closed: Ticket {position['ticket']}, PnL: {position['profit']}")
                self.daily_pnl += position['profit']
                return True
            else:
                logger.error(f"Close position failed: {result.comment}")
                return False
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return False
    
    def update_trailing_stop(self, position):
        """Update trailing stop for position"""
        try:
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return False
            
            if position['type'] == mt5.ORDER_TYPE_BUY:
                # Buy position: trailing stop goes up
                new_sl = tick.bid - (self.trailing_stop_pips * 0.01)
                if new_sl > position['sl']:
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": self.symbol,
                        "sl": new_sl,
                        "tp": position['tp'],
                        "position": position['ticket'],
                    }
                    result = mt5.order_send(request)
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        logger.info(f"Trailing stop updated (BUY): New SL {new_sl}")
                        return True
            else:
                # Sell position: trailing stop goes down
                new_sl = tick.ask + (self.trailing_stop_pips * 0.01)
                if new_sl < position['sl']:
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": self.symbol,
                        "sl": new_sl,
                        "tp": position['tp'],
                        "position": position['ticket'],
                    }
                    result = mt5.order_send(request)
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        logger.info(f"Trailing stop updated (SELL): New SL {new_sl}")
                        return True
            return False
        except Exception as e:
            logger.error(f"Error updating trailing stop: {e}")
            return False
    
    def run(self, login, password, server):
        """Main trading loop"""
        if not self.connect(login, password, server):
            logger.error("Failed to connect. Exiting.")
            return
        
        logger.info("=" * 50)
        logger.info("Finex XAU/USD Scalping Bot Started")
        logger.info("=" * 50)
        logger.info(f"Symbol: {self.symbol}")
        logger.info(f"Timeframe: {self.timeframe}")
        logger.info(f"Lot Size: {self.lot_size}")
        logger.info(f"Min Win Probability: {self.min_win_probability*100}%")
        logger.info("=" * 50)
        
        last_signal = None
        loop_count = 0
        
        try:
            while True:
                loop_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get current price
                tick = mt5.symbol_info_tick(self.symbol)
                if not tick:
                    logger.warning("Cannot get tick data")
                    time.sleep(5)
                    continue
                
                # Get candle data
                df = self.get_rates(100)
                if df is None or len(df) < 20:
                    logger.warning("Insufficient data")
                    time.sleep(5)
                    continue
                
                # Calculate indicators
                df = self.calculate_indicators(df)
                
                # Check current position
                position = self.get_position_info()
                
                # If position exists, check trailing stop & close conditions
                if position:
                    logger.info(f"[{timestamp}] Position open - Type: {'BUY' if position['type'] == 0 else 'SELL'}, Profit: ${position['profit']:.2f}")
                    
                    # Update trailing stop
                    self.update_trailing_stop(position)
                    
                    # Check for opposite signal (sell if long, buy if short)
                    if position['type'] == mt5.ORDER_TYPE_BUY:
                        sell_signal, sell_conf = self.check_sell_signal(df)
                        if sell_signal:
                            logger.info(f"[{timestamp}] Sell signal detected (confidence: {sell_conf:.2%}). Closing position.")
                            self.close_position(position)
                    else:
                        buy_signal, buy_conf = self.check_buy_signal(df)
                        if buy_signal:
                            logger.info(f"[{timestamp}] Buy signal detected (confidence: {buy_conf:.2%}). Closing position.")
                            self.close_position(position)
                else:
                    # No position - check for entry signals
                    buy_signal, buy_conf = self.check_buy_signal(df)
                    sell_signal, sell_conf = self.check_sell_signal(df)
                    
                    if buy_signal and (last_signal != "BUY"):
                        logger.info(f"[{timestamp}] ✓ BUY Signal - Confidence: {buy_conf:.2%} | Ask: {tick.ask}")
                        self.place_buy_order(tick.ask)
                        last_signal = "BUY"
                    
                    elif sell_signal and (last_signal != "SELL"):
                        logger.info(f"[{timestamp}] ✓ SELL Signal - Confidence: {sell_conf:.2%} | Bid: {tick.bid}")
                        self.place_sell_order(tick.bid)
                        last_signal = "SELL"
                    
                    else:
                        logger.debug(f"[{timestamp}] No signal. Buy conf: {buy_conf:.2%}, Sell conf: {sell_conf:.2%}")
                
                # Daily loss check
                if self.daily_pnl < -self.max_daily_loss:
                    logger.warning(f"Daily loss limit reached (${self.daily_pnl:.2f}). Stopping bot.")
                    break
                
                # Wait before next check (5 seconds minimum)
                time.sleep(5)
        
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            mt5.shutdown()
            logger.info("MT5 connection closed")

if __name__ == "__main__":
    bot = FinexScalpingBot()
    
    # EDIT THESE WITH YOUR CREDENTIALS
    LOGIN = 60677667  # Your Finex account number
    PASSWORD = "your_password_here"  # Your MT5 password
    SERVER = "Finex-Demo"  # Server name (check MT5 for exact name)
    
    bot.run(LOGIN, PASSWORD, SERVER)
