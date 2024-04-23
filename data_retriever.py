import os
import pandas as pd

class DataRetriever:
    def __init__(self, directory='AK47_Finance/Data'):
        self.directory = directory
        self.portfolios_directory = os.path.join(self.directory, 'Portfolios')
        self.historical_data_directory = self.directory

    def load_all_portfolios(self):
        """Load all portfolios from the directory."""
        portfolio_names = [f[:-4] for f in os.listdir(self.portfolios_directory) if f.endswith('.csv')]
        portfolios = {}
        for name in portfolio_names:
            path = os.path.join(self.portfolios_directory, name + '.csv')
            portfolios[name] = pd.read_csv(path).set_index('Ticker')['Shares'].to_dict()
        return portfolios

    def retrieve_historical_data(self, ticker_symbol):
        data_file_path = os.path.join(self.directory, ticker_symbol, f"{ticker_symbol}_historical_data.csv")
        if os.path.exists(data_file_path):
            return pd.read_csv(data_file_path, index_col='Date', parse_dates=True)
        else:
            print(f"No data found for {ticker_symbol}.")
            return None

    def retrieve_all_historical_data_for_portfolio(self, portfolio):
        historical_data = {}
        for ticker_symbol in portfolio.keys():
            if ticker_symbol != 'Cash':  # Assuming 'Cash' is a special entry and not an actual ticker
                data = self.retrieve_historical_data(ticker_symbol)
                if data is not None:
                    historical_data[ticker_symbol] = data
        return historical_data

    def retrieve_news_for_ticker(self, ticker_symbol):
        news_file_path = os.path.join(self.directory, ticker_symbol, f"{ticker_symbol}_News.csv")
        if os.path.exists(news_file_path):
            return pd.read_csv(news_file_path)
        else:
            print(f"No news found for {ticker_symbol}.")
            return None

    def retrieve_all_news_for_portfolio(self, portfolio):
        news_data = {}
        for ticker_symbol in portfolio.keys():
            if ticker_symbol != 'Cash':  # Again, skipping 'Cash'
                news = self.retrieve_news_for_ticker(ticker_symbol)
                if news is not None:
                    news_data[ticker_symbol] = news
        return news_data
    
    def get_portfolio_total_values(self, portfolio_name):
        """Calculate and return details of each ticker in the specified portfolio."""
        portfolio_path = os.path.join(self.portfolios_directory, f"{portfolio_name}.csv")
        if not os.path.exists(portfolio_path):
            print(f"No portfolio found for {portfolio_name}.")
            return {}

        portfolio = pd.read_csv(portfolio_path)
        detailed_values = {}
        total_portfolio_value = 0

        # First pass to calculate total portfolio value
        for index, row in portfolio.iterrows():
            ticker, shares = row['Ticker'], row['Shares']
            if ticker != 'Cash':
                data_file_path = os.path.join(self.historical_data_directory, ticker, f"{ticker}_historical_data.csv")
                if os.path.exists(data_file_path):
                    hist_data = pd.read_csv(data_file_path, index_col='Date', parse_dates=True)
                    latest_close = hist_data['Close'].iloc[0]
                    total_portfolio_value += latest_close * shares

        # Second pass to calculate individual details and weights
        for index, row in portfolio.iterrows():
            ticker, shares = row['Ticker'], row['Shares']
            if ticker != 'Cash':
                data_file_path = os.path.join(self.historical_data_directory, ticker, f"{ticker}_historical_data.csv")
                if os.path.exists(data_file_path):
                    hist_data = pd.read_csv(data_file_path, index_col='Date', parse_dates=True)
                    latest_close = hist_data['Close'].iloc[0]
                    total_value = latest_close * shares
                    weight = (total_value / total_portfolio_value) * 100
                    detailed_values[ticker] = {'Shares': shares, 'Value': latest_close, 'Total Value': total_value, 'Weight': weight}
                else:
                    print(f"No historical data found for {ticker}.")
                    detailed_values[ticker] = {'Shares': shares, 'Value': 0, 'Total Value': 0, 'Weight': 0}

        return detailed_values


# # Example usage
# if __name__ == "__main__":
#     data_retriever = DataRetriever()
#     all_portfolios = data_retriever.load_all_portfolios()
#     for portfolio_name, portfolio in all_portfolios.items():
#         print(f"\nPortfolio: {portfolio_name}")
#         all_data = data_retriever.retrieve_all_historical_data_for_portfolio(portfolio)
#         all_news = data_retriever.retrieve_all_news_for_portfolio(portfolio)
#         for ticker, data in all_data.items():
#             print(f"Data for {ticker}:")
#             print(data.head())  # Print the first few rows as an example
#         for ticker, news in all_news.items():
#             print(f"News for {ticker}:")
#             print(news.head())  # Print the first few rows as an example
