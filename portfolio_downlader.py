from yf_download import YFDownload
from datetime import datetime
import pandas as pd
import os

class PortfolioDownloader:
    def __init__(self, directory='AK47_Finance/Data', initial_cash=0.0):
        self.directory = directory
        self.portfolio_name = ''
        self.csv_path = ''
        self.total_cash = initial_cash
        self.portfolio = {}
        self.load_portfolio()

    def ensure_directory_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def retrieve_portfolio_name(self):
        if not self.portfolio_name:
            self.portfolio_name = input("What is the name of your portfolio? ")
            self.csv_path = os.path.join(self.directory, f"Portfolios/{self.portfolio_name}.csv")
            self.ensure_directory_exists()

    def load_portfolio(self):
        self.retrieve_portfolio_name()
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            if 'Cash' in df.columns:
                cash_row = df[df['Ticker'] == 'Cash']
                if not cash_row.empty:
                    self.total_cash = cash_row['Shares'].values[0]
                df = df[df['Ticker'] != 'Cash']
            self.portfolio = df.set_index('Ticker')['Shares'].to_dict()
        else:
            print(f"No portfolio found at {self.csv_path}.")
            self.initialize_portfolio()

    def initialize_portfolio(self):
        print("Initializing new portfolio. Please enter the stocks you own and their quantities.")
        self.total_cash = float(input("Enter the amount of cash held: "))
        while True:
            ticker_symbol = input("Enter the ticker symbol (or 'done' to finish): ").upper()
            if ticker_symbol == 'DONE':
                break
            shares = float(input(f"Enter the number of shares for {ticker_symbol}: "))
            self.portfolio[ticker_symbol] = shares

        self.save_portfolio()
        print("Portfolio initialization complete.")

    def save_portfolio(self):
        data_items = list(self.portfolio.items()) + [('Cash', self.total_cash)]
        df = pd.DataFrame(data_items, columns=['Ticker', 'Shares'])
        df.to_csv(self.csv_path, index=False)
        print(f"Portfolio saved to {self.csv_path}.")   

    def add_to_portfolio(self):
        while True:  # Start an infinite loop to continuously ask for user input
            action = input("Do you wish to input more tickers into the portfolio? (yes/no): ").lower()
            if action == 'no':
                break  # Exit the loop if the user does not want to add more tickers
            elif action == 'yes':
                try:
                    ticker_symbol = input("Enter the ticker symbol: ").upper()
                    buy_or_sell = input("Will you buy or sell? (buy/sell): ").lower()
                    shares = float(input("Enter the number of shares: "))
                    if shares < 0:
                        raise ValueError("Number of shares cannot be negative.")

                    if buy_or_sell == 'buy':
                        # If buying, add the shares to the portfolio
                        if ticker_symbol in self.portfolio:
                            self.portfolio[ticker_symbol] += shares
                        else:
                            self.portfolio[ticker_symbol] = shares
                        print(f"Added {shares} shares of {ticker_symbol} to your portfolio.")
                    elif buy_or_sell == 'sell':
                        # If selling, subtract the shares from the portfolio, if possible
                        if ticker_symbol in self.portfolio and self.portfolio[ticker_symbol] >= shares:
                            self.portfolio[ticker_symbol] -= shares
                            print(f"Sold {shares} shares of {ticker_symbol} from your portfolio.")
                            if self.portfolio[ticker_symbol] == 0:
                                del self.portfolio[ticker_symbol]  # Remove the ticker if shares are zero
                        else:
                            print("Not enough shares to sell or ticker not in portfolio.")
                    else:
                        print("Invalid action. Please specify 'buy' or 'sell'.")

                    # Ensure directory for the ticker exists
                    ticker_directory = os.path.join(self.directory, ticker_symbol)
                    if not os.path.exists(ticker_directory):
                        os.makedirs(ticker_directory)
                        print(f"Directory created for {ticker_symbol} at {ticker_directory}")

                    self.save_portfolio()
                except ValueError as e:
                    print(f"Invalid input: {e}")
            else:
                print("Please answer with 'yes' or 'no'.")

    def retrieve_ticker_data(self):
        portfolio_details = {}
        total_portfolio_value = self.total_cash  # Start with cash held

        for ticker_symbol, shares in self.portfolio.items():
            if ticker_symbol == 'Cash':
                continue
            ticker_data = {}
            # Historical data
            df_hist = YFDownload.download_historical_data(ticker_symbol)
            if not df_hist.empty:
                last_close = df_hist['Close'].iloc[-1]
                total_value = last_close * shares
                ticker_data.update({'Last Close': last_close, 'Total Value': total_value, 'Shares': shares})
                total_portfolio_value += total_value
            else:
                print(f"No historical data for {ticker_symbol}")

            # Stock Info
            stock_info = YFDownload.download_stock_info(ticker_symbol)
            if stock_info is not None:
                ticker_data.update({'Stock Info': stock_info})

            # Dividends
            dividends = YFDownload.download_dividends(ticker_symbol)
            if dividends is not None and not dividends.empty:
                ticker_data.update({'Recent Dividend': dividends.iloc[-1]})

            # Earnings Dates
            earnings_dates = YFDownload.download_earnings_dates(ticker_symbol)
            if earnings_dates is not None:
                ticker_data.update({'Earnings Dates': earnings_dates})

            # Options Data (Summary)
            options_summary = YFDownload.download_stock_options(ticker_symbol)
            if options_summary is not None:
                ticker_data.update({'Options Summary': options_summary})

            # Stock News (Latest Headline)
            stock_news = YFDownload.download_stock_news(ticker_symbol)
            if stock_news is not None and len(stock_news) > 0:
                ticker_data.update({'Latest News': stock_news[0]['title']})

            portfolio_details[ticker_symbol] = ticker_data

        return portfolio_details

    def update_portfolio_data(self):
        """Updates the portfolio data by downloading only the missing recent data."""
        for ticker_symbol, shares in self.portfolio.items():
            if ticker_symbol == 'Cash':
                continue  
            print(ticker_symbol)
            # Determine the directory and file path for historical data
            data_directory = f"{self.directory}/{ticker_symbol}"
            data_file_path = f"{data_directory}/{ticker_symbol}_historical_data.csv"

            # Check if historical data file exists
            if os.path.exists(data_file_path):
                historical_data = pd.read_csv(data_file_path, parse_dates=['Date'], index_col='Date')
                print(historical_data)
                # Find the last date for which data was downloaded
                last_downloaded_date = historical_data.index.max().tz_localize(None)
                print(last_downloaded_date)
                
                # Determine the date range for new data
                today = pd.Timestamp(datetime.today().date())  # Ensure we're using a normalized date without time
                print(today)
                if last_downloaded_date < today:
                    # Fetch new data from the day after the last downloaded date up to today
                    new_data = YFDownload.download_historical_data(ticker_symbol, start=last_downloaded_date + pd.Timedelta(days=1), end=today)

                    # Append new data to existing historical data
                    if not new_data.empty:
                        updated_data = pd.concat([historical_data, new_data])
                        updated_data.to_csv(data_file_path)
                        print(f"Updated historical data for {ticker_symbol}.")
                    else:
                        print(f"No new data to update for {ticker_symbol}.")
                else:
                    print(f"Data for {ticker_symbol} is already up to date.")
            else:
                print(f"No existing data found for {ticker_symbol}. Downloading full historical data.")
                # Download full historical data if no existing data found
                YFDownload.download_historical_data(ticker_symbol)

# # # Example usage
if __name__ == "__main__":
    downloader = PortfolioDownloader()
    downloader.retrieve_portfolio_name()
    # downloader.add_to_portfolio()
    downloader.retrieve_ticker_data()
    # downloader.update_portfolio_data()
