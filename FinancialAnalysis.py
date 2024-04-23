import os
import pandas as pd
from yf_download import YFDownload

class PortfolioAnalysis:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.directory = f"Data/{ticker_symbol}"
        self.ensure_data_availability()

    def ensure_data_availability(self):
        # Check if data for the given ticker is already downloaded
        required_files = [
            f"{self.ticker_symbol}_historical_data.csv",
            f"{self.ticker_symbol}_Info.csv",
            f"{self.ticker_symbol}_Balance_Sheet.csv",
            f"{self.ticker_symbol}_Income_Stmt.csv",
            f"{self.ticker_symbol}_Cash_Flows.csv"
        ]

        missing_files = [file for file in required_files if not os.path.exists(os.path.join(self.directory, file))]
        
        if missing_files:
            print(f"Missing data for {self.ticker_symbol}: {missing_files}")
            print("Downloading required data...")
            self.download_data()
        else:
            print(f"All required data for {self.ticker_symbol} is already available.")

    def download_data(self):
        # Utilize YFDownload to fetch and store data
        YFDownload.ensure_directory_exists(self.directory)
        YFDownload.download_historical_data(self.ticker_symbol)
        YFDownload.download_stock_info(self.ticker_symbol)
        YFDownload.download_balance_sheet(self.ticker_symbol)
        YFDownload.download_income_statement(self.ticker_symbol)
        YFDownload.download_cash_flows(self.ticker_symbol)

    def load_data(self):
        # Load the data from CSV files
        self.historical_data = pd.read_csv(f"{self.directory}/{self.ticker_symbol}_historical_data.csv", index_col='Date', parse_dates=True)
        self.balance_sheet = pd.read_csv(f"{self.directory}/{self.ticker_symbol}_Balance_Sheet.csv")
        self.income_statement = pd.read_csv(f"{self.directory}/{self.ticker_symbol}_Income_Stmt.csv")
        self.cash_flows = pd.read_csv(f"{self.directory}/{self.ticker_symbol}_Cash_Flows.csv")

    def historical_price_analysis(self):
        # Simple historical closing price analysis
        print(f"Latest closing price for {self.ticker_symbol}: {self.historical_data['Close'].iloc[0]}")
        self.historical_data['Close'].plot(title=f"{self.ticker_symbol} Historical Closing Prices")

# Example Usage
ticker_symbol = input("Enter ticker symbol: ")
portfolio_analysis = PortfolioAnalysis(ticker_symbol)
portfolio_analysis.load_data()
portfolio_analysis.historical_price_analysis()