import asyncio

from exchanges import ExchangeScanner
from arbitrage import ArbitrageFinder
from telegram_bot import send_message
from config import SCAN_INTERVAL


scanner = ExchangeScanner()
finder = ArbitrageFinder()


async def main():

    while True:

        try:

            prices = await scanner.get_all_prices()

            opportunities = finder.find(prices)

            if opportunities:

                message = "Arbitrage opportunities:\n\n"

                for o in opportunities[:5]:

                    message += (
                        f"{o['symbol']}\n"
                        f"Buy: {o['buy_exchange']} {o['buy_price']}\n"
                        f"Sell: {o['sell_exchange']} {o['sell_price']}\n"
                        f"Spread: {o['spread']:.2f}%\n\n"
                    )

                await send_message(message)

            else:

                print("No arbitrage opportunities")

        except Exception as e:

            print("Error:", e)

        await asyncio.sleep(SCAN_INTERVAL)


if __name__ == "__main__":

    asyncio.run(main())
