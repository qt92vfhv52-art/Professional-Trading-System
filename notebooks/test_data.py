from data.yahoo_provider import YahooProvider
from data.data_loader import DataLoader

provider = YahooProvider()

loader = DataLoader(provider)

df = loader.load(
    symbol="BTC-USD",
    interval="1d",
)

print(df.head())

print(df.tail())

print(df.info())
