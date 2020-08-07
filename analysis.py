import pandas as pd

stock_df = pd.read_json('result.json')
print(stock_df.head())