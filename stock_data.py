import yfinance as yf
import pandas as pd
from datetime import datetime
from gnews import GNews # Import the GNews library

class StockDataProvider:
    def __init__(self):
        # Initialize the GNews client once for efficiency.
        # It will fetch news from India in English.
        self.google_news = GNews(language='en', country='IN', max_results=10)
        
    def get_stock_price(self, symbol):
        """Get current stock price and basic info using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            # Use history() to get the most recent closing price
            hist = ticker.history(period="2d")
            if hist.empty:
                return None

            latest_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2]
            
            change = latest_price - previous_close
            change_percent = (change / previous_close) * 100
            
            return {
                'symbol': symbol.upper(),
                'price': round(latest_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': hist['Volume'].iloc[-1],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol, period="1y"):
        """Get historical stock data for charting"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # Reset index to make 'Date' a column
            data.reset_index(inplace=True)
            # Rename columns to match what the chart widget expects
            data.rename(columns={'Date': 'date', 'Close': 'price'}, inplace=True)
            
            # Convert timezone-aware datetimes to timezone-naive
            data['date'] = data['date'].dt.tz_localize(None)

            return data[['date', 'price']]
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_news(self, symbol):
        """Get news related to a stock using the gnews library."""
        # Search for the company name (e.g., "Reliance" from "RELIANCE.NS")
        search_query = symbol.split('.')[0]
        
        try:
            news_list = self.google_news.get_news(f"{search_query} stock")
            formatted_news = []

            for article in news_list:
                # The 'published date' from gnews is a string, e.g., "Sat, 27 Sep 2025 00:00:00 GMT"
                # We need to parse it into a datetime object for our analysis window.
                try:
                    # The format code for parsing the gnews date string
                    publish_time = datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S GMT')
                except (ValueError, TypeError):
                    # If parsing fails or the date is missing, skip this article
                    continue

                # Transform the gnews article into the format our application needs
                formatted_news.append({
                    'title': article['title'],
                    'time': publish_time.strftime("%Y-%m-%d %H:%M"),
                    'source': article['publisher']['title'],
                    'link': article['url'],
                    'publish_timestamp': publish_time  # The crucial datetime object for the analysis chart
                })
            
            return formatted_news
        except Exception as e:
            print(f"Error fetching news from GNews for {symbol}: {e}")
            return []