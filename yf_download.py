import yfinance as yf
import pandas as pd
import os
import datetime as dt

class YFDownload:
    def __init__(self, indexes=None, data_directory="Data", market_directory="Data/Market"):
        self.data_directory = data_directory  
        self.market_directory = market_directory
        if indexes is None:
            self.indexes = ['^DJI', '^IXIC', '^GSPC']
        else:
            self.indexes = indexes

    def ensure_directory_exists(self, directory):
        full_path = os.path.join(self.data_directory, directory)  # Use base data directory
        try:
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        except Exception as e:
            print(f"Error creating directory {full_path}: {e}")

    def download_historical_data(self, ticker_symbol):
        directory = f"{ticker_symbol}" 
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            hist = stock.history(period="max").sort_index(ascending=False)
            file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_historical_data.csv")
            hist.to_csv(file_path)
            return hist
        except Exception as e:
            print(f"Error downloading historical data for {ticker_symbol}: {e}")
            return None

    def download_stock_info(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_info = stock.info
            if stock_info:
                df_stock_info = pd.DataFrame(list(stock_info.items()), columns=['Attribute', 'Value'])
                file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Info.csv")
                df_stock_info.to_csv(file_path, index=False)
            return stock_info
        except Exception as e:
            print(f"Error downloading stock info for {ticker_symbol}: {e}")
            return None

    def download_earnings_dates(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try: 
            stock = yf.Ticker(ticker_symbol)
            df_earning_dates = stock.earnings_dates
            if df_earning_dates:
                file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Earnings_Dates.csv")
                df_earning_dates.to_csv(file_path, index=False)
            return df_earning_dates
        except Exception as e: 
            print(f"Error downloading earnings dats for {ticker_symbol}: {e}")
            return None
    
    def download_stock_options(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_options = stock.options
            all_options_data = []
            if stock_options:
                for expiration_date in stock_options:
                    options_df = stock.option_chain(expiration_date)
                    options_df.calls['Expiration'] = expiration_date
                    options_df.calls['Type'] = 'Call'
                    options_df.puts['Expiration'] = expiration_date
                    options_df.puts['Type'] = 'Put'
                    all_options_data.append(options_df.calls)
                    all_options_data.append(options_df.puts)

                combined_options_df = pd.concat(all_options_data)
                file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Options_Combined.csv")
                combined_options_df.to_csv(file_path, index=False)

            return all_options_data
        except Exception as e:
            print(f"Error downloading stock options for {ticker_symbol}: {e}")
            return None 

    def download_dividends(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            dividends = stock.dividends
            file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Dividends.csv")
            dividends.to_csv(file_path, index=False)
            return dividends
        except Exception as e: 
            print(f"Error downloading stock dividends for {ticker_symbol}: {e}")
            return None

    def download_stock_news(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:  
            stock = yf.Ticker(ticker_symbol)
            stock_news = stock.news
            if stock_news:
                df_stock_news = pd.DataFrame(stock_news)
                file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_News.csv")
                df_stock_news.to_csv(file_path, index=False)
            return stock_news
        except Exception as e:
            print(f"Error downloading stock news for {ticker_symbol}: {e}")
            return None 

    def download_balance_sheet(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_balance_sheet = stock.balance_sheet
            stock_qtly_balance_sheet = stock.quarterly_balance_sheet
            if not stock_balance_sheet.empty and not stock_qtly_balance_sheet.empty:
                df_stock_balance_sheet = pd.DataFrame(stock_balance_sheet)
                df_qtly_balance_sheet = pd.DataFrame(stock_qtly_balance_sheet)
                bs_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Balance_Sheet.csv")
                qbs_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Qtly_Balance_Sheet.csv")
                df_stock_balance_sheet.to_csv(bs_file_path)
                df_qtly_balance_sheet.to_csv(qbs_file_path)
            else:
                print(f"No balance sheet data available for {ticker_symbol}")
            return stock_balance_sheet, stock_qtly_balance_sheet
        except Exception as e:
            print(f"Error downloading stock balance sheets for {ticker_symbol}: {e}")
            return None

    def download_income_statement(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_income_stmt = stock.income_stmt
            stock_qtly_income_stmt = stock.quarterly_income_stmt
            if not stock_income_stmt.empty and not stock_qtly_income_stmt.empty: 
                df_stock_income_stmt = pd.DataFrame(stock_income_stmt)
                df_stock_qtly_income_stmt = pd.DataFrame(stock_qtly_income_stmt)
                is_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Income_Stmt.csv")
                qis_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Qtly_Income_Stmt.csv")
                df_stock_income_stmt.to_csv(is_file_path)
                df_stock_qtly_income_stmt.to_csv(qis_file_path)
            else:
                print(f"No income statement data available for {ticker_symbol}")
            return stock_income_stmt, stock_qtly_income_stmt
        except Exception as e: 
            print(f"Error downloading stock income statement for {ticker_symbol}: {e}")
            return None

    def download_cash_flows(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_cash_flows = stock.cashflow  # Correct attribute for yfinance is cashflows, not cash_flow
            stock_qtly_cash_flows = stock.quarterly_cashflow  
            if not stock_cash_flows.empty and not stock_qtly_cash_flows.empty:
                df_stock_cash_flows = pd.DataFrame(stock_cash_flows)
                df_stock_qtly_cash_flows = pd.DataFrame(stock_qtly_cash_flows)
                cf_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Cash_Flows.csv")
                qcf_file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_Qtly_Cash_Flows.csv")
                df_stock_cash_flows.to_csv(cf_file_path)
                df_stock_qtly_cash_flows.to_csv(qcf_file_path)
            else:
                print(f"No cash flows data available for {ticker_symbol}")
            return stock_cash_flows, stock_qtly_cash_flows
        except Exception as e:
            print(f"Error downloading stock cash flows for {ticker_symbol}: {e}")
            return None

    def download_market_historical_data(self):
        directory = self.market_directory
        self.ensure_directory_exists(directory)
        for symbol in self.indexes:
            try:
                ticker = yf.Ticker(symbol)
                historical_data = ticker.history(period="max")
                historical_data_sorted = historical_data.sort_index(ascending=False)
                file_path = os.path.join(self.data_directory, directory, f"{symbol}_historical_data.csv")
                historical_data_sorted.to_csv(file_path)
            except Exception as e:
                print(f"Error downloading historical data for {symbol}: {e}")

    def update_historical_data(self, ticker_symbol):
        directory = f"{ticker_symbol}"
        file_name = f"{ticker_symbol}_historical_data.csv"
        file_path = os.path.join(self.data_directory, directory, file_name)
        self.ensure_directory_exists(directory)
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                print(f"Existing data for {ticker_symbol} is empty. Consider downloading the full dataset.")
                return
            if 'Date' not in df.columns:
                print(f"No 'Date' column found in the dataset for {ticker_symbol}.")
                return
            
            last_date = pd.to_datetime(df['Date'].iloc[0])
            current_date = pd.Timestamp.today().normalize()
            stock = yf.Ticker(ticker_symbol)
            
            if last_date < current_date:
                new_data = stock.history(start=last_date + pd.Timedelta(days=1))
                if not new_data.empty:
                    new_data_sorted = new_data.sort_index(ascending=False)
                    new_data_sorted.to_csv(file_path, mode='a', header=False, index=False)
                else:
                    print(f"No new data available to update for {ticker_symbol}.")
            else:
                print(f"Data for {ticker_symbol} is already up to date.")
        except Exception as e:
            print(f"Error updating historical data for {ticker_symbol}: {e}")

    def update_market_data(self):
        for index in self.indexes:
            YFDownload.update_historical_data(index)
            print(f"Update attempt for {index} completed.")

    def download_intraday_data(self, ticker_symbol, interval):
        # Define the period based on the interval to ensure adequate data coverage
        period = "7d" if interval == "1m" else "60d" if interval == "2m" else "1mo"
        directory = f"{ticker_symbol}/Intraday"
        
        self.ensure_directory_exists(directory)
        try:
            stock = yf.Ticker(ticker_symbol)
            stock_intraday = stock.history(period=period, interval=interval)
            if stock_intraday.empty:
                print(f"No intraday data available for {ticker_symbol} at {interval} interval.")
                return None
            
            # Construct the file path using os.path.join for better path management
            file_path = os.path.join(self.data_directory, directory, f"{ticker_symbol}_{interval}_data.csv")
            stock_intraday.to_csv(file_path)
            return stock_intraday
        except Exception as e:
            print(f"Error downloading {interval} interval data for {ticker_symbol}: {e}")
            return None

    def download_all_data_for_ticker(self, ticker_symbol, intraday_intervals=['1m', '2m']):
        self.download_historical_data(ticker_symbol)
        self.download_stock_info(ticker_symbol)
        self.download_earnings_dates(ticker_symbol)
        self.download_stock_options(ticker_symbol)
        self.download_dividends(ticker_symbol)
        self.download_stock_news(ticker_symbol)
        self.download_balance_sheet(ticker_symbol)
        self.download_income_statement(ticker_symbol)
        self.download_cash_flows(ticker_symbol)
        self.download_market_historical_data()
        
        for interval in intraday_intervals:
            self.download_intraday_data(ticker_symbol, interval)
        
        print(f"All available data for {ticker_symbol} has been downloaded.")

