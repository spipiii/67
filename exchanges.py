import aiohttp
import asyncio

class ExchangeAPI:

    async def fetch_okx(self, session):
        url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

        async with session.get(url) as r:
            data = await r.json()

        result = {}

        for item in data["data"]:
            symbol = item["instId"]
            price = float(item["last"])
            volume = float(item["volCcy24h"])

            result[symbol] = {
                "price": price,
                "volume": volume
            }

        return result

    async def fetch_bybit(self, session):
        url = "https://api.bybit.com/v5/market/tickers?category=spot"

        async with session.get(url) as r:
            data = await r.json()

        result = {}

        for item in data["result"]["list"]:
            symbol = item["symbol"]
            price = float(item["lastPrice"])
            volume = float(item["turnover24h"])

            result[symbol] = {
                "price": price,
                "volume": volume
            }

        return result

    async def fetch_mexc(self, session):
        url = "https://api.mexc.com/api/v3/ticker/24hr"

        async with session.get(url) as r:
            data = await r.json()

        result = {}

        for item in data:
            symbol = item["symbol"]
            price = float(item["lastPrice"])
            volume = float(item["quoteVolume"])

            result[symbol] = {
                "price": price,
                "volume": volume
            }

        return result

    async def fetch_htx(self, session):
        url = "https://api.huobi.pro/market/tickers"

        async with session.get(url) as r:
            data = await r.json()

        result = {}

        for item in data["data"]:
            symbol = item["symbol"].upper()
            price = float(item["close"])
            volume = float(item["vol"])

            result[symbol] = {
                "price": price,
                "volume": volume
            }

        return result

    async def fetch_all(self):

        async with aiohttp.ClientSession() as session:

            tasks = [
                self.fetch_okx(session),
                self.fetch_bybit(session),
                self.fetch_mexc(session),
                self.fetch_htx(session)
            ]

            okx, bybit, mexc, htx = await asyncio.gather(*tasks)

            return {
                "okx": okx,
                "bybit": bybit,
                "mexc": mexc,
                "htx": htx
            }