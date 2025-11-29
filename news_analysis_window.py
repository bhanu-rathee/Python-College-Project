import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewsAnalysisWindow(tk.Toplevel):
    def __init__(self, parent, symbol, news_item, stock_data_provider):
        super().__init__(parent)
        self.symbol = symbol
        self.news_item = news_item
        self.news_date = news_item['publish_timestamp'].date()
        self.stock_data_provider = stock_data_provider

        self.title(f"News Impact Analysis for {self.symbol}")
        self.geometry("800x600")

        self.historical_data = None
        
        self.setup_ui()
        self.load_data_and_plot()

    def setup_ui(self):
        """Setup UI elements like chart and sliders."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # News Title Label
        news_title_label = ttk.Label(main_frame, text=self.news_item['title'], wraplength=780, font=('Arial', 10, 'bold'))
        news_title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Matplotlib Chart
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sliders Frame
        sliders_frame = ttk.Frame(main_frame, padding="10")
        sliders_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        sliders_frame.columnconfigure(1, weight=1)
        sliders_frame.columnconfigure(3, weight=1)

        # Before Slider
        ttk.Label(sliders_frame, text="Days Before:").grid(row=0, column=0, padx=5)
        self.before_var = tk.IntVar(value=30)
        self.before_slider = ttk.Scale(sliders_frame, from_=1, to=90, orient=tk.HORIZONTAL, variable=self.before_var, command=self.update_plot)
        self.before_slider.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.before_label = ttk.Label(sliders_frame, textvariable=self.before_var)
        self.before_label.grid(row=0, column=2, padx=5)

        # After Slider
        ttk.Label(sliders_frame, text="Days After:").grid(row=1, column=0, padx=5)
        self.after_var = tk.IntVar(value=15)
        self.after_slider = ttk.Scale(sliders_frame, from_=1, to=90, orient=tk.HORIZONTAL, variable=self.after_var, command=self.update_plot)
        self.after_slider.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.after_label = ttk.Label(sliders_frame, textvariable=self.after_var)
        self.after_label.grid(row=1, column=2, padx=5)

    def load_data_and_plot(self):
        """Fetch a wide range of data initially, then plot."""
        # Fetch 1 year of data to have enough for the sliders
        self.historical_data = self.stock_data_provider.get_historical_data(self.symbol, period="1y")
        if not self.historical_data.empty:
            self.update_plot()

    def update_plot(self, _=None):
        """Clear and redraw the plot based on slider values."""
        if self.historical_data is None or self.historical_data.empty:
            return

        days_before = self.before_var.get()
        days_after = self.after_var.get()

        start_date = self.news_date - timedelta(days=days_before)
        end_date = self.news_date + timedelta(days=days_after)
        
        # Filter data based on the selected date range
        mask = (self.historical_data['date'].dt.date >= start_date) & (self.historical_data['date'].dt.date <= end_date)
        plot_data = self.historical_data.loc[mask]

        if plot_data.empty:
            return

        self.ax.clear()
        
        # Plot price trend
        self.ax.plot(plot_data['date'], plot_data['price'], color='#2E86AB', marker='.', markersize=4)
        
        # Add a vertical line for the news date
        self.ax.axvline(x=pd.to_datetime(self.news_date), color='r', linestyle='--', label='News Event')
        
        self.ax.set_title(f'Price Trend Around News Event ({self.symbol})')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        
        self.canvas.draw()