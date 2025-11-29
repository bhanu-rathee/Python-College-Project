import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from stock_data import StockDataProvider
from chart_widget import ChartWidget
from news_widget import NewsWidget
from news_analysis_window import NewsAnalysisWindow # Import the new window

class StockMarketViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Stock Market Viewer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize data provider
        self.stock_data = StockDataProvider()
        
        # Current stock being viewed
        self.current_symbol = None
        self.auto_refresh = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start the application
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3) # Give more weight to left panel
        main_frame.columnconfigure(1, weight=2) # Give less weight to right panel
        main_frame.rowconfigure(1, weight=1)
        
        self.setup_search_section(main_frame)
        self.setup_content_area(main_frame)
        self.setup_status_bar() # Pass root instead of main_frame for correct grid placement
        
    def setup_search_section(self, parent):
        """Setup stock search section"""
        search_frame = ttk.LabelFrame(parent, text="Search Stock", padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Stock symbol entry
        ttk.Label(search_frame, text="Stock Symbol:").grid(row=0, column=0, padx=(0, 5))
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol_var, width=15)
        self.symbol_entry.grid(row=0, column=1, padx=(0, 10))
        self.symbol_entry.bind('<Return>', self.search_stock)
        
        # Search button
        self.search_btn = ttk.Button(search_frame, text="Search", command=self.search_stock)
        self.search_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.auto_refresh_var = tk.BooleanVar()
        self.auto_refresh_cb = ttk.Checkbutton(search_frame, text="Auto Refresh (30s)", 
                                              variable=self.auto_refresh_var,
                                              command=self.toggle_auto_refresh)
        self.auto_refresh_cb.grid(row=0, column=3, padx=(20, 0))
        
        popular_frame = ttk.Frame(search_frame)
        popular_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky=tk.W)
        
        ttk.Label(popular_frame, text="Popular (India):").pack(side=tk.LEFT, padx=(0, 5))
        
        # Changed to popular Indian stocks
        popular_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']
        for stock in popular_stocks:
            btn = ttk.Button(popular_frame, text=stock, width=12,
                           command=lambda s=stock: self.quick_search(s))
            btn.pack(side=tk.LEFT, padx=2)
    
    def setup_content_area(self, parent):
        """Setup main content area with chart and info"""
        left_panel = ttk.Frame(parent)
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_panel.rowconfigure(1, weight=1)
        left_panel.columnconfigure(0, weight=1)
        
        self.setup_stock_info(left_panel)
        
        chart_frame = ttk.LabelFrame(left_panel, text="Price Chart", padding="5")
        chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.columnconfigure(0, weight=1)
        
        self.chart_widget = ChartWidget(chart_frame)
        self.chart_widget.get_frame().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        right_panel = ttk.LabelFrame(parent, text="Market News", padding="5")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.rowconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)

        # Pass the callback function to the NewsWidget
        self.news_widget = NewsWidget(right_panel, self.open_news_analysis)
        self.news_widget.get_frame().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def open_news_analysis(self, news_item):
        """Callback function to open the news analysis window."""
        if self.current_symbol:
            NewsAnalysisWindow(self.root, self.current_symbol, news_item, self.stock_data)
        else:
            messagebox.showinfo("Info", "No stock selected.")
    
    def setup_stock_info(self, parent):
        """Setup stock information display"""
        info_frame = ttk.LabelFrame(parent, text="Stock Information", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Create info labels
        self.info_labels = {}
        
        ttk.Label(info_frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.info_labels['symbol'] = ttk.Label(info_frame, text="--", font=('Arial', 12, 'bold'))
        self.info_labels['symbol'].grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(info_frame, text="Price:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.info_labels['price'] = ttk.Label(info_frame, text="--", font=('Arial', 12, 'bold'))
        self.info_labels['price'].grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(info_frame, text="Change:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.info_labels['change'] = ttk.Label(info_frame, text="--")
        self.info_labels['change'].grid(row=1, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(info_frame, text="Volume:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.info_labels['volume'] = ttk.Label(info_frame, text="--")
        self.info_labels['volume'].grid(row=1, column=3, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(info_frame, text="Last Updated:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.info_labels['updated'] = ttk.Label(info_frame, text="--", font=('Arial', 8))
        self.info_labels['updated'].grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=(5, 0))
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter a stock symbol to begin (e.g., RELIANCE.NS)")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=2)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def search_stock(self, event=None):
        """Search for stock data"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol.")
            return
            
        self.current_symbol = symbol
        self.status_var.set(f"Loading data for {symbol}...")
        
        threading.Thread(target=self.load_stock_data, args=(symbol,), daemon=True).start()
    
    def quick_search(self, symbol):
        """Quick search for popular stocks"""
        self.symbol_var.set(symbol)
        self.search_stock()
    
    def load_stock_data(self, symbol):
        """Load stock data in background thread"""
        try:
            stock_info = self.stock_data.get_stock_price(symbol)
            
            if stock_info:
                self.root.after(0, self.update_stock_info, stock_info)
                
                historical_data = self.stock_data.get_historical_data(symbol)
                self.root.after(0, self.chart_widget.update_chart, historical_data, symbol)
                
                news_data = self.stock_data.get_stock_news(symbol)
                self.root.after(0, self.news_widget.update_news, news_data, symbol)
                
                self.root.after(0, lambda: self.status_var.set(f"Displaying data for {symbol} | All data from Yahoo Finance."))
            else:
                self.root.after(0, lambda: self.status_var.set(f"Failed to load data for {symbol}. Check the symbol and try again."))
                messagebox.showerror("Error", f"Could not find data for symbol '{symbol}'.\nFor Indian stocks, use the '.NS' (NSE) or '.BO' (BSE) suffix.")
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
    
    def update_stock_info(self, stock_info):
        """Update stock information display"""
        self.info_labels['symbol'].config(text=stock_info['symbol'])
        self.info_labels['price'].config(text=f"₹{stock_info['price']}") # Changed to Rupee symbol
        
        change_text = f"{stock_info['change']:+.2f} ({stock_info['change_percent']:+.2f}%)"
        change_color = 'green' if stock_info['change'] >= 0 else 'red'
        self.info_labels['change'].config(text=change_text, foreground=change_color)
        
        self.info_labels['volume'].config(text=f"{int(stock_info['volume']):,}")
        self.info_labels['updated'].config(text=stock_info['last_updated'])
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh and self.current_symbol:
            self.status_var.set(f"Auto-refresh enabled for {self.current_symbol}. Updating every 30 seconds.")
            threading.Thread(target=self.auto_refresh_loop, daemon=True).start()
        else:
            self.status_var.set(f"Auto-refresh disabled.")

    def auto_refresh_loop(self):
        """Auto-refresh loop"""
        while self.auto_refresh and self.current_symbol:
            time.sleep(30)
            if self.auto_refresh and self.current_symbol:
                # Use load_stock_data directly to avoid UI pop-ups on failure
                threading.Thread(target=self.load_stock_data, args=(self.current_symbol,), daemon=True).start()
    
    def on_closing(self):
        """Handle application closing"""
        self.auto_refresh = False
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StockMarketViewer()
    app.run()