import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from Bot.logging_config import setup_logging
from Bot.client import get_binance_client
from Bot.validators import validate_inputs
from Bot.orders import place_futures_order


API_KEY = "7ZXwpbQanNNqHBdzNcpZbKAcDuVrrlak6aword5wl89sMhBibZQp4Lac0xCDHIyd"
API_SECRET = "jygIvBiV1HoiDjW9RUDKcHc1ZifktieuDafcABMUpa3z4LoXobuZ6XUfIfGudQAp"


class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Futures Trading Bot")
        self.root.geometry("750x850")
        self.root.configure(bg='#1e1e1e')
        
        # Set root background for notebook
        self.root.option_add('*TNotebook.Background', '#1e1e1e')
        self.root.option_add('*TNotebook.Tab.Background', '#2d2d2d')
        self.root.option_add('*TNotebook.Tab.Foreground', '#ffffff')
        
        # Custom styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.accent_color = '#f0b90b'  # Binance yellow
        self.secondary_bg = '#2d2d2d'
        self.success_color = '#00c853'
        self.error_color = '#ff5252'
        
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Helvetica', 10))
        self.style.configure('TButton', background=self.accent_color, foreground='#000000', font=('Helvetica', 10, 'bold'), padding=10)
        self.style.map('TButton', background=[('active', '#d4a50a')])
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), foreground=self.accent_color)
        self.style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'), foreground=self.fg_color)
        self.style.configure('TLabelframe', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.accent_color, font=('Helvetica', 10, 'bold'))
        
        self.client = None
        self.logger = setup_logging()
        
        self.create_widgets()
        self.connect_to_binance()
    
    def create_widgets(self):
        # Main container with notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Trading
        trading_frame = ttk.Frame(notebook, padding="20")
        notebook.add(trading_frame, text="📊 Trading")
        
        # Tab 2: Assets
        assets_frame = ttk.Frame(notebook, padding="20")
        notebook.add(assets_frame, text="💰 Assets")
        
        # === TRADING TAB ===
        # Title
        title_label = ttk.Label(trading_frame, text="Binance Futures Trading Bot", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Connection status
        self.status_label = ttk.Label(trading_frame, text="● Connecting...", foreground="#ffa500", font=('Helvetica', 10))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Order form frame
        order_frame = ttk.LabelFrame(trading_frame, text="Order Details", padding="15")
        order_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Symbol input
        ttk.Label(order_frame, text="Trading Symbol:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.symbol_entry = tk.Entry(order_frame, width=30, bg=self.secondary_bg, fg=self.fg_color, insertbackground=self.accent_color, font=('Helvetica', 10))
        self.symbol_entry.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        self.symbol_entry.insert(0, "BTCUSDT")
        
        # Side selection
        ttk.Label(order_frame, text="Side:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.side_var = tk.StringVar(value="BUY")
        side_frame = ttk.Frame(order_frame)
        side_frame.grid(row=1, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        buy_btn = tk.Radiobutton(side_frame, text="BUY", variable=self.side_var, value="BUY", 
                                 bg=self.bg_color, fg=self.success_color, selectcolor=self.secondary_bg,
                                 font=('Helvetica', 10, 'bold'), activebackground=self.bg_color)
        buy_btn.pack(side=tk.LEFT, padx=5)
        
        sell_btn = tk.Radiobutton(side_frame, text="SELL", variable=self.side_var, value="SELL", 
                                  bg=self.bg_color, fg=self.error_color, selectcolor=self.secondary_bg,
                                  font=('Helvetica', 10, 'bold'), activebackground=self.bg_color)
        sell_btn.pack(side=tk.LEFT, padx=5)
        
        # Order Type selection
        ttk.Label(order_frame, text="Order Type:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.type_var = tk.StringVar(value="MARKET")
        type_frame = ttk.Frame(order_frame)
        type_frame.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        market_btn = tk.Radiobutton(type_frame, text="MARKET", variable=self.type_var, value="MARKET", 
                                    command=self.toggle_price_field, bg=self.bg_color, fg=self.fg_color,
                                    selectcolor=self.secondary_bg, font=('Helvetica', 10), activebackground=self.bg_color)
        market_btn.pack(side=tk.LEFT, padx=5)
        
        limit_btn = tk.Radiobutton(type_frame, text="LIMIT", variable=self.type_var, value="LIMIT", 
                                   command=self.toggle_price_field, bg=self.bg_color, fg=self.fg_color,
                                   selectcolor=self.secondary_bg, font=('Helvetica', 10), activebackground=self.bg_color)
        limit_btn.pack(side=tk.LEFT, padx=5)
        
        # Quantity input
        ttk.Label(order_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.quantity_entry = tk.Entry(order_frame, width=30, bg=self.secondary_bg, fg=self.fg_color, insertbackground=self.accent_color, font=('Helvetica', 10))
        self.quantity_entry.grid(row=3, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        self.quantity_entry.insert(0, "0.001")
        
        # Price input (for LIMIT orders)
        ttk.Label(order_frame, text="Price:").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.price_entry = tk.Entry(order_frame, width=30, bg=self.secondary_bg, fg=self.fg_color, insertbackground=self.accent_color, font=('Helvetica', 10))
        self.price_entry.grid(row=4, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        self.price_entry.insert(0, "60000")
        self.price_entry.config(state='disabled')
        
        # Submit button
        submit_button = ttk.Button(trading_frame, text="PLACE ORDER", command=self.place_order)
        submit_button.grid(row=3, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        
        # Response area
        response_frame = ttk.LabelFrame(trading_frame, text="Order Response", padding="15")
        response_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.response_text = scrolledtext.ScrolledText(response_frame, width=60, height=12, 
                                                        bg=self.secondary_bg, fg=self.fg_color,
                                                        insertbackground=self.accent_color, font=('Courier', 9))
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear button
        clear_button = ttk.Button(trading_frame, text="Clear Response", command=self.clear_response)
        clear_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        # === ASSETS TAB ===
        ttk.Label(assets_frame, text="Account Assets", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Refresh button
        refresh_button = ttk.Button(assets_frame, text="🔄 Refresh Assets", command=self.refresh_assets)
        refresh_button.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Assets display frame
        assets_display_frame = ttk.LabelFrame(assets_frame, text="USDⓈ-M Assets", padding="15")
        assets_display_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.assets_text = scrolledtext.ScrolledText(assets_display_frame, width=60, height=20,
                                                     bg=self.secondary_bg, fg=self.fg_color,
                                                     insertbackground=self.accent_color, font=('Courier', 10))
        self.assets_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        trading_frame.columnconfigure(0, weight=1)
        trading_frame.columnconfigure(1, weight=1)
        trading_frame.rowconfigure(4, weight=1)
        assets_frame.columnconfigure(0, weight=1)
        assets_frame.columnconfigure(1, weight=1)
        assets_frame.rowconfigure(2, weight=1)
    
    def toggle_price_field(self):
        """Enable/disable price field based on order type"""
        if self.type_var.get() == "LIMIT":
            self.price_entry.config(state='normal')
        else:
            self.price_entry.config(state='disabled')
    
    def connect_to_binance(self):
        """Connect to Binance API"""
        try:
            self.client = get_binance_client(API_KEY, API_SECRET)
            self.status_label.config(text="● Connected to Binance Testnet", foreground=self.success_color)
            self.log_response("Successfully connected to Binance Futures Testnet.\n")
            self.refresh_assets()
        except Exception as e:
            self.status_label.config(text="● Connection Failed", foreground=self.error_color)
            self.log_response(f"Connection Error: {str(e)}\n")
    
    def place_order(self):
        """Place the order with current form values"""
        symbol = self.symbol_entry.get().strip()
        side = self.side_var.get()
        order_type = self.type_var.get()
        quantity_str = self.quantity_entry.get().strip()
        price_str = self.price_entry.get().strip() if self.type_var.get() == "LIMIT" else None
        
        # Validate inputs
        try:
            quantity = float(quantity_str)
            price = float(price_str) if price_str else None
        except ValueError:
            messagebox.showerror("Input Error", "Quantity and Price must be valid numbers.")
            return
        
        try:
            validate_inputs(symbol, side, order_type, quantity, price)
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return
        
        # Display order summary
        self.log_response("=" * 50 + "\n")
        self.log_response("ORDER REQUEST SUMMARY\n")
        self.log_response("=" * 50 + "\n")
        self.log_response(f"Symbol:   {symbol.upper()}\n")
        self.log_response(f"Side:     {side.upper()}\n")
        self.log_response(f"Type:     {order_type.upper()}\n")
        self.log_response(f"Quantity: {quantity}\n")
        if price:
            self.log_response(f"Price:    {price}\n")
        self.log_response("=" * 50 + "\n\n")
        
        # Place order
        try:
            response = place_futures_order(self.client, symbol, side, order_type, quantity, price)
            
            self.log_response("SUCCESS: Order processed cleanly by server!\n")
            self.log_response("=" * 50 + "\n")
            self.log_response("ORDER RESPONSE DETAILS\n")
            self.log_response("=" * 50 + "\n")
            self.log_response(f"OrderID:      {response.get('orderId')}\n")
            self.log_response(f"Status:       {response.get('status')}\n")
            self.log_response(f"Executed Qty: {response.get('executedQty')}\n")
            self.log_response(f"Avg Price:    {response.get('avgPrice', 'N/A')}\n")
            self.log_response("=" * 50 + "\n\n")
            
            messagebox.showinfo("Success", "Order placed successfully!")
            
        except Exception as e:
            self.log_response(f"EXECUTION FAILURE: Binance rejected the transaction.\n")
            self.log_response(f"Reason: {str(e)}\n\n")
            messagebox.showerror("Order Failed", f"Reason: {str(e)}")
    
    def log_response(self, message):
        """Add message to response text area"""
        self.response_text.config(state='normal')
        self.response_text.insert(tk.END, message)
        self.response_text.config(state='disabled')
        self.response_text.see(tk.END)
    
    def clear_response(self):
        """Clear the response text area"""
        self.response_text.config(state='normal')
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state='disabled')
    
    def refresh_assets(self):
        """Refresh and display account assets"""
        if not self.client:
            self.log_assets("Not connected to Binance. Please check connection status.\n")
            return
        
        try:
            self.log_assets("Fetching account information...\n")
            
            # Get account information
            account = self.client.futures_account()
            
            self.log_assets("=" * 60 + "\n")
            self.log_assets("ACCOUNT ASSETS\n")
            self.log_assets("=" * 60 + "\n\n")
            
            # Display total wallet balance (matching Binance format)
            total_margin_balance = float(account.get('totalMarginBalance', 0))
            total_wallet_balance = float(account.get('totalWalletBalance', 0))
            total_unrealized_profit = float(account.get('totalUnrealizedProfit', 0))
            
            self.log_assets(f"Margin Balance:         {total_margin_balance:.4f} USDT\n")
            self.log_assets(f"Wallet Balance:         {total_wallet_balance:.4f} USDT\n")
            self.log_assets(f"Unrealized PNL:         {total_unrealized_profit:.4f} USDT\n\n")
            
            # Display individual assets
            self.log_assets("-" * 60 + "\n")
            self.log_assets("ASSETS (USDⓈ-M)\n")
            self.log_assets("-" * 60 + "\n\n")
            
            assets = account.get('assets', [])
            total_assets_count = len(assets)
            assets_with_balance = sum(1 for asset in assets if float(asset.get('walletBalance', 0)) > 0)
            
            for asset in assets:
                asset_symbol = asset.get('asset', 'N/A')
                wallet_balance = float(asset.get('walletBalance', 0))
                unrealized_pnl = float(asset.get('unrealizedProfit', 0))
                margin_balance = float(asset.get('marginBalance', 0))
                max_withdraw_amount = float(asset.get('maxWithdrawAmount', 0))
                
                self.log_assets(f"Asset:                   {asset_symbol}\n")
                self.log_assets(f"Wallet Balance:          {wallet_balance:.8f}\n")
                self.log_assets(f"Unrealized PNL:          {unrealized_pnl:.8f}\n")
                self.log_assets(f"Margin Balance:          {margin_balance:.8f}\n")
                self.log_assets(f"Available for Transfer:  {max_withdraw_amount:.8f}\n")
                self.log_assets("-" * 50 + "\n")
            
            self.log_assets("\n" + "=" * 60 + "\n")
            self.log_assets(f"Total Assets in Account: {total_assets_count}\n")
            self.log_assets(f"Assets with Balance:     {assets_with_balance}\n")
            self.log_assets("=" * 60 + "\n")
            
        except Exception as e:
            self.log_assets(f"Error fetching assets: {str(e)}\n")
    
    def log_assets(self, message):
        """Add message to assets text area"""
        self.assets_text.config(state='normal')
        # If it's the first message, clear, otherwise append
        if "Fetching account information" in message:
            self.assets_text.delete(1.0, tk.END)
        self.assets_text.insert(tk.END, message)
        self.assets_text.config(state='disabled')
        self.assets_text.see(tk.END)


def main():
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
