import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from data_retriever import DataRetriever


class PortfolioGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Portfolio Manager")
        self.geometry("800x600")  # Set the size of the window

        # Assuming DataRetriever is correctly implemented to load portfolio names
        self.data_retriever = DataRetriever(directory='AK47_Finance/Data')

        # Initialize GUI components
        self.setup_menu_buttons()
        self.setup_portfolio_explorer()
        self.setup_main_content_frame()
        self.setup_news_section()

        # Load and display portfolio names in the explorer
        self.load_and_display_portfolio_names()
        # self.load_and_display_ticker_info()

    def setup_menu_buttons(self):
        # Menu Buttons
        self.menu_frame = tk.Frame(self, height=50, bg='gray')
        self.menu_frame.pack(side="top", fill="x")

        self.add_button = tk.Button(self.menu_frame, text="Add Stock", command=self.add_stock)
        self.add_button.pack(side="left")

        self.remove_button = tk.Button(self.menu_frame, text="Remove Stock", command=self.remove_stock)
        self.remove_button.pack(side="left")

    def setup_portfolio_explorer(self):
        self.explorer_frame = tk.Frame(self, width=200)
        self.explorer_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.portfolio_listbox = tk.Listbox(self.explorer_frame)
        self.portfolio_listbox.pack(fill='both', expand=True)

        # Bind the selection event
        self.portfolio_listbox.bind('<<ListboxSelect>>', self.on_portfolio_selected)

    def setup_main_content_frame(self):
        # Main Content Frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(expand=True, fill="both")

        # Top Main Content Frame 
        # Create a bin for the top of the main content frame that will hold the Portfolio Details Frame to hold two bins side by side on top of the News Bin 
        self.top_content_frame = tk.Frame(self.content_frame)
        self.top_content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Left side of the Top Content Frame - Portfolio Details Frame
        self.details_frame = tk.Frame(self.top_content_frame, bg='light grey', bd=2, relief="groove")
        # Do not pack the details_frame yet until we know the total width of the columns

        self.tree = ttk.Treeview(self.details_frame, columns=("Ticker", "Shares", "Value", "Total_Value", "Weight"), show="headings")
        self.tree.bind('<<TreeviewSelect>>', self.on_ticker_selected)
        
        # Measure the header text and adjust the column widths accordingly
        total_width = 0  # Variable to keep track of total width
        header_font = tkFont.Font(family="TkDefaultFont", size=10, weight="bold")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title(), anchor='center')
            col_width = header_font.measure(col.title()) + 20  # Add some padding
            total_width += col_width  # Add the column width to the total width
            self.tree.column(col, width=col_width, anchor='center', stretch=False)

        # Now that we know the total width, we can pack the details_frame with that width
        self.details_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.tree.pack(expand=False, fill="y", side="top")  # No longer fill both

        self.details_frame.config(width=total_width)  # Set the frame width to the total width of the columns

        # Right side of the Top Content Frame - Empty Section
        self.empty_frame = tk.Frame(self.top_content_frame, bg='light grey', bd=2, relief="groove")
        self.empty_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # Placeholder for future content in the empty frame
        self.placeholder_label = tk.Label(self.empty_frame, text="Empty Section", bg='light grey')
        self.placeholder_label.pack(side="top", pady=10)

    def setup_news_section(self):
        # News Section
        self.news_frame = tk.Frame(self.content_frame, height=150, bg='light grey')
        self.news_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.news_label = tk.Label(self.news_frame, text="Latest News", bg='light grey')
        self.news_label.pack()

        self.news_text = tk.Text(self.news_frame, wrap="word", state='disabled', bg='white')
        self.news_text.pack(expand=True, fill="both", padx=10, pady=10)

    def load_and_display_portfolio_names(self):
        portfolio_names = self.data_retriever.load_all_portfolios().keys()
        for name in portfolio_names:
            self.portfolio_listbox.insert(tk.END, name)

    def on_portfolio_selected(self, event):
        if not event.widget.curselection():
            return
        index = event.widget.curselection()[0]
        portfolio_name = event.widget.get(index)
        self.load_and_display_ticker_info(portfolio_name)

    def on_ticker_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:  # Check if something is selected
            item = self.tree.item(selected_item)
            ticker = item['values'][0]  # Assuming the first value in the row is the ticker symbol
            self.display_news_for_ticker(ticker)

    def load_and_display_ticker_info(self, portfolio_name):
        # Clear existing data in the table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Retrieve the portfolio details
        portfolio_details = self.data_retriever.get_portfolio_total_values(portfolio_name)

        # Populate the table with the ticker info
        for ticker, details in portfolio_details.items():
            self.tree.insert("", tk.END, values=(
                ticker,
                f"{details['Shares']:,}",  # Formats with commas for thousands
                f"${details['Value']:,.2f}",  # Formats with commas and rounds to 2 decimal places
                f"${details['Total Value']:,.2f}",  # Formats with commas and rounds to 2 decimal places
                f"{details['Weight']:.2f}%"))

        # Update the application's title or another widget to show the selected portfolio name
        self.title(f"Portfolio Manager - {portfolio_name}")

    def add_stock(self):
        # Method to handle adding stock
        pass

    def remove_stock(self):
        # Method to handle removing stock
        pass

    def update_portfolio_details(self):
        # Method to update the portfolio details in the treeview
        pass

    def display_news_for_ticker(self, ticker):
        # Clear existing news
        self.news_text.config(state='normal')
        self.news_text.delete('1.0', tk.END)

        # Retrieve news data
        news_df = self.data_retriever.retrieve_news_for_ticker(ticker)
        if news_df is not None and not news_df.empty:
            # Format and display each news item
            for index, row in news_df.iterrows():
                title = row.get('Title', 'No Title')  # Assuming your CSV has a 'Title' column
                date = row.get('Date', 'No Date')  # Assuming your CSV has a 'Date' column
                content = row.get('Content', 'No Content')  # Assuming your CSV has a 'Content' column
                news_entry = f"{title}\n{date}\n{content}\n\n"
                self.news_text.insert(tk.END, news_entry)
        else:
            self.news_text.insert(tk.END, "No news found for this ticker.")

        self.news_text.config(state='disabled')

# Create the GUI application
app = PortfolioGUI()
app.mainloop()
