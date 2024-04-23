from yf_download import YFDownload
import pandas as pd 
import os 
import numpy as np
import matplotlib.pyplot as plt 

class MarketAnalysisTool:
    def __init__(self, data_directory="Data", ticker_symbol=None):
        self.data_directory = data_directory
        self.market_directory = f"{data_directory}/Market"
        if ticker_symbol is None:
            ticker_symbol = input("Enter a ticker symbol for market analysis: ")
        self.ticker_symbol = ticker_symbol
        self.yf = YFDownload()
        self.ensure_directories()
        # self.perform_market_analysis(ticker_symbol)

    def ensure_directories(self):
        self.yf.ensure_directory_exists(self.data_directory)
        self.yf.ensure_directory_exists(self.market_directory)
        ticker_data_directory = f"{self.data_directory}/{self.ticker_symbol}"
        self.yf.ensure_directory_exists(ticker_data_directory)

        if not os.listdir(ticker_data_directory):  # Directory is empty; download data
            self.yf.download_all_data(self.ticker_symbol)
        
        market_data_exists = all(os.path.exists(f"{self.market_directory}/{index}_historical_data.csv") 
                                 for index in ['^DJI', '^IXIC', '^GSPC'])
        if not market_data_exists:
            self.yf.download_market_historical_data()
        else:
            self.yf.update_historical_data(self.ticker_symbol)
            self.yf.update_market_data()
            print("Data updated")

if __name__ == "__main__":
    MarketAnalysisTool()
