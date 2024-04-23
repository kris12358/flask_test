import yfinance as yf
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime, timedelta

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA", "NVDA", "PYPL", "ADBE", "CRM", "CSCO", "INTC", "QCOM", "TXN"]
start_date = "2020-01-01"
end_date = datetime.today() - pd.offsets.BDay(1)
data = yf.download(tickers, start=start_date, end=end_date)

data1 = data.stack(level=1, dropna=False)
data1.columns = data1.columns.map(lambda x: x.lower())
data1.index = data1.index.set_names([level.lower() for level in data1.index.names])

DB_HOST = 'localhost'
DB_NAME = 'finance'
DB_USER = 'postgres'
DB_PASSWORD = '123'
DB_PORT = '5432'

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

table_name = 'stock_data'
data1.to_sql(table_name, engine, if_exists='replace')
conn.close()