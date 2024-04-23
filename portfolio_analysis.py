import pandas as pd
import matplotlib.pyplot as plt
import os

class PortfolioAnalytics:
    def __init__(self, portfolios_directory='AK47_Finance/Data/Portfolios', historical_data_directory='AK47_Finance/Data'):
        self.portfolios_directory = portfolios_directory
        self.historical_data_directory = historical_data_directory
        self.historical_data = {}
    
    def load_and_analyze_all_portfolios(self):
        """Load and analyze all portfolios in the directory."""
        portfolio_files = [f for f in os.listdir(self.portfolios_directory) if f.endswith('.csv')]
        for portfolio_file in portfolio_files:
            portfolio_path = os.path.join(self.portfolios_directory, portfolio_file)
            self.load_portfolio_data(portfolio_path)
            self.load_historical_data()
            print(f"Analyzing portfolio: {portfolio_file}")
            self.visualize_asset_allocation()
            self.visualize_performance()
    
    def load_portfolio_data(self, portfolio_path):
        """Load portfolio data from CSV."""
        self.portfolio = pd.read_csv(portfolio_path).set_index('Ticker')['Shares'].to_dict()
        
    def load_historical_data(self):
        """Load historical data for each ticker in the portfolio from local files."""
        self.historical_data = {}
        for ticker, shares in self.portfolio.items():
            if ticker != 'Cash':
                data_file_path = os.path.join(self.historical_data_directory, ticker, f"{ticker}_historical_data.csv")
                if os.path.exists(data_file_path):
                    hist_data = pd.read_csv(data_file_path, index_col='Date', parse_dates=True)
                    self.historical_data[ticker] = hist_data['Close'] * shares

    def calculate_portfolio_value_over_time(self):
        """Calculate the total value of the portfolio over time."""
        portfolio_value = pd.DataFrame(self.historical_data).sum(axis=1)
        return portfolio_value
    
    def visualize_asset_allocation(self):
        """Visualize the asset allocation of the portfolio."""
        latest_close_prices = {ticker: data.iloc[-1] for ticker, data in self.historical_data.items()}
        total_value = sum(latest_close_prices.values())
        print(total_value)
        allocations = {ticker: (value / total_value) * 100 for ticker, value in latest_close_prices.items()}
        # print(allocations)
        plt.figure(figsize=(10, 7))
        plt.pie(allocations.values(), labels=allocations.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Asset Allocation')
        plt.show()

    def visualize_performance(self):
        """Visualize the performance of the portfolio over time."""
        portfolio_value = self.calculate_portfolio_value_over_time()
        portfolio_value.plot(figsize=(10, 6), title="Portfolio Value Over Time")
        plt.ylabel('Total Portfolio Value')
        plt.show()

if __name__ == "__main__":
    analytics = PortfolioAnalytics()
    analytics.load_and_analyze_all_portfolios()
