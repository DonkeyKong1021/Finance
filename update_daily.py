from yf_download import YFDownload
import datetime
import os
import pandas as pd

def update_portfolio_data(portfolio_path):
    # Load the portfolio from the given path
    df_portfolio = pd.read_csv(portfolio_path)
    portfolio = df_portfolio.set_index('Ticker')['Shares'].to_dict()
    
    # Iterate through each ticker symbol in the portfolio and update its data
    for ticker_symbol, shares in portfolio.items():
        if ticker_symbol != 'Cash':  # Skip 'Cash' or any non-ticker entry
            print(f"Updating data for {ticker_symbol}")
            # Use the YFDownload class to download/update historical data for this ticker
            YFDownload.download_historical_data(ticker_symbol)
    print(f"Portfolio data update complete for {portfolio_path}.")

def check_and_update():
    last_run_file = "AK47_Finance/Data/last_run.txt"
    portfolios_folder = "AK47_Finance/Data/Portfolios"
    
    try:
        with open(last_run_file, "r") as file:
            last_run_date = file.read().strip()
    except FileNotFoundError:
        last_run_date = "1970-01-01"  # If the file doesn't exist, use a default old date

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    if today_str > last_run_date:
        print("Updating portfolio data...")
        
        # Iterate over each CSV file in the portfolios directory
        for portfolio_name in os.listdir(portfolios_folder):
            if portfolio_name.endswith(".csv"):
                portfolio_path = os.path.join(portfolios_folder, portfolio_name)
                update_portfolio_data(portfolio_path)
        
        # Update the last run date
        with open(last_run_file, "w") as file:
            file.write(today_str)
    else:
        print("Already updated today.")

if __name__ == "__main__":
    check_and_update()
