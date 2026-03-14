from config import MIN_VOLUME, MAX_VOLUME

class ArbitrageFinder:

    def normalize_symbol(self, symbol):
        return symbol.replace("-", "").replace("_", "")

    def find_opportunities(self, markets):

        coins = {}

        for exchange, data in markets.items():

            for symbol, info in data.items():

                volume = info["volume"]

                if volume < MIN_VOLUME or volume > MAX_VOLUME:
                    continue

                norm = self.normalize_symbol(symbol)

                if norm not in coins:
                    coins[norm] = {}

                coins[norm][exchange] = info["price"]

        opportunities = []

        for coin, prices in coins.items():

            if len(prices) < 2:
                continue

            min_ex = min(prices, key=prices.get)
            max_ex = max(prices, key=prices.get)

            min_price = prices[min_ex]
            max_price = prices[max_ex]

            spread = (max_price - min_price) / min_price * 100

            opportunities.append({
                "coin": coin,
                "buy_exchange": min_ex,
                "sell_exchange": max_ex,
                "buy_price": min_price,
                "sell_price": max_price,
                "spread": spread
            })

        opportunities.sort(key=lambda x: x["spread"], reverse=True)

        return opportunities[:5]