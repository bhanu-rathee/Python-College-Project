import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

class ChartWidget:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Style the chart
        self.figure.patch.set_facecolor('#f0f0f0')
        self.ax.set_facecolor('#ffffff')
        
        # Initialize empty chart
        self.plot_empty_chart()
        
    def plot_empty_chart(self):
        """Display empty chart with placeholder"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Search for a stock to view chart', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=12, color='gray')
        self.ax.set_title('Stock Price Chart')
        self.canvas.draw()
    
    def update_chart(self, data, symbol):
        """Update chart with new stock data"""
        if data.empty:
            self.plot_empty_chart()
            return
            
        self.ax.clear()
        
        # Plot the price line
        self.ax.plot(data['date'], data['price'], 
                    linewidth=2, color='#2E86AB', marker='o', markersize=3)
        
        # Customize the chart
        self.ax.set_title(f'{symbol} - Stock Price Trend', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date', fontsize=10)
        self.ax.set_ylabel('Price ($)', fontsize=10)
        self.ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        self.figure.autofmt_xdate()
        
        # Add some styling
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        # Tight layout to prevent clipping
        self.figure.tight_layout()
        
        # Refresh canvas
        self.canvas.draw()
    
    def get_frame(self):
        """Return the frame widget"""
        return self.frame