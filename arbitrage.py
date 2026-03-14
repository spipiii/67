from config import MIN_SPREAD


class ArbitrageFinder:

    def find(self, prices):

        opportunities = []

        symbols = set()

        for exchange in prices:
            symbols.update(prices[exchange].keys())

        for symbol in symbols:

            exchange_prices = {}

            for exchange in prices:

                if symbol in prices[exchange]:

                    exchange_prices[exchange] = prices[exchange][symbol]

            if len(exchange_prices) < 2:
                continue

            min_exchange = min(exchange_prices, key=exchange_prices.get)
            max_exchange = max(exchange_prices, key=exchange_prices.get)

            min_price = exchange_prices[min_exchange]
            max_price = exchange_prices[max_exchange]

            if min_price == 0:
                continue

            spread = (max_price - min_price) / min_price * 100

            if spread < MIN_SPREAD:
                continue

            opportunities.append(
                {
                    "symbol": symbol,
                    "buy_exchange": min_exchange,
                    "sell_exchange": max_exchange,
                    "buy_price": min_price,
                    "sell_price": max_price,
                    "spread": spread,
                }
            )

        return sorted(opportunities, key=lambda x: x["spread"], reverse=True)
