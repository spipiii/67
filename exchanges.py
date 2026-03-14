import aiohttp

from config import MIN_VOLUME, MAX_VOLUME


class ExchangeScanner:

    def normalize_symbol(self, symbol):
        return symbol.replace("-", "").replace("_", "").upper()

    async def fetch_okx(self, session):

        url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

        async with session.get(url) as r:

            data = await r.json()

        result = {}

        for item in data["data"]:

            symbol = self.normalize_symbol(item["instId"])

            if not symbol.endswith("USDT"):
                continue

            price = float(item["last"])

            volume = float(item["volCcy24h"])

            if volume < MIN_VOLUME or volume > MAX_VOLUME:
                continue

            result[symbol] = price

        return result

    async def fetch_bybit(self, session):

        url = "https://api.bybit.com/v5/market/tickers?category=spot"

        async with session.get(url) as r:

            data = await r.json()

        result = {}

        for item in data["result"]["list"]:

            symbol = self.normalize_symbol(item["symbol"])

            if not symbol.endswith("USDT"):
                continue

            price = float(item["lastPrice"])

            volume = float(item["turnover24h"])

            if volume < MIN_VOLUME or volume > MAX_VOLUME:
                continue

            result[symbol] = price

        return result

    async def fetch_mexc(self, session):

        url = "https://api.mexc.com/api/v3/ticker/24hr"

        async with session.get(url) as r:

            data = await r.json()

        result = {}

        for item in data:

            symbol = self.normalize_symbol(item["symbol"])

            if not symbol.endswith("USDT"):
                continue

            price = float(item["lastPrice"])

            volume = float(item["quoteVolume"])

            if volume < MIN_VOLUME or volume > MAX_VOLUME:
                continue

            result[symbol] = price

        return result

    async def fetch_htx(self, session):

        url = "https://api.huobi.pro/market/tickers"

        async with session.get(url) as r:

            data = await r.json()

        result = {}

        for item in data["data"]:

            symbol = self.normalize_symbol(item["symbol"])

            if not symbol.endswith("USDT"):
                continue

            price = float(item["close"])

            volume = float(item["vol"]) * price

            if volume < MIN_VOLUME or volume > MAX_VOLUME:
                continue

            result[symbol] = price

        return result

    async def get_all_prices(self):

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:

            okx = await self.fetch_okx(session)

            bybit = await self.fetch_bybit(session)

            mexc = await self.fetch_mexc(session)

            htx = await self.fetch_htx(session)

        return {
            "okx": okx,
            "bybit": bybit,
            "mexc": mexc,
            "htx": htx
        }
