import tkinter as tk
from tkinter import ttk
import webbrowser

class NewsWidget:
    def __init__(self, parent, news_click_callback):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.news_click_callback = news_click_callback
        self.news_items = []

        self.setup_news_display()
        
    def setup_news_display(self):
        """Setup the news display area"""
        # Title
        title_label = ttk.Label(self.frame, text="Latest News", 
                               font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10), anchor='w')
        
        # Create scrollable text widget for news
        news_frame = ttk.Frame(self.frame)
        news_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(news_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for news
        self.news_text = tk.Text(news_frame, 
                                wrap=tk.WORD, 
                                yscrollcommand=scrollbar.set,
                                font=('Arial', 9),
                                bg='white',
                                relief='flat',
                                padx=10,
                                pady=10)
        self.news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.news_text.yview)
        
        self.news_text.tag_configure('title', font=('Arial', 10, 'bold'), foreground='#0000EE', underline=True)
        self.news_text.tag_configure('time', font=('Arial', 8), foreground='gray')
        
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder text"""
        self.news_text.config(state=tk.NORMAL)
        self.news_text.delete(1.0, tk.END)
        self.news_text.insert(tk.END, "Search for a stock to view related news...")
        self.news_text.config(state=tk.DISABLED)
        
    def update_news(self, news_data, symbol):
        """Update news display with new data and make it clickable"""
        self.news_text.config(state=tk.NORMAL)
        self.news_text.delete(1.0, tk.END)
        self.news_items = news_data # Store news data
        
        if not self.news_items:
            self.show_placeholder()
            return
            
        self.news_text.insert(tk.END, f"News for {symbol}\n\n")
        
        for i, news in enumerate(self.news_items):
            tag_name = f"news_{i}"
            
            # Insert title with a unique tag
            self.news_text.insert(tk.END, f"• {news['title']}\n", ('title', tag_name))
            
            # Bind click event to the tag
            self.news_text.tag_bind(tag_name, "<Button-1>", lambda e, index=i: self.on_news_click(index))
            self.news_text.tag_bind(tag_name, "<Enter>", lambda e: self.news_text.config(cursor="hand2"))
            self.news_text.tag_bind(tag_name, "<Leave>", lambda e: self.news_text.config(cursor=""))
            
            self.news_text.insert(tk.END, f"  {news['time']} - {news['source']}\n\n", 'time')
            
        self.news_text.config(state=tk.DISABLED)

    def on_news_click(self, index):
        """Handle news item click"""
        if self.news_click_callback:
            clicked_news_item = self.news_items[index]
            self.news_click_callback(clicked_news_item)
        
    def get_frame(self):
        """Return the frame widget"""
        return self.frame