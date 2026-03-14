import asyncio
from exchanges import ExchangeAPI
from arbitrage import ArbitrageFinder
from telegram_bot import send_message
from config import CHECK_INTERVAL


exchange_api = ExchangeAPI()
arb = ArbitrageFinder()


def format_message(opps):

    if not opps:
        return "No arbitrage opportunities"

    text = "🔥 TOP 5 Arbitrage Opportunities\n\n"

    for o in opps:

        text += (
            f"Coin: {o['coin']}\n"
            f"Buy: {o['buy_exchange']} @ {o['buy_price']}\n"
            f"Sell: {o['sell_exchange']} @ {o['sell_price']}\n"
            f"Spread: {o['spread']:.2f}%\n\n"
        )

    return text


async def run():

    while True:

        try:

            markets = await exchange_api.fetch_all()

            opps = arb.find_opportunities(markets)

            message = format_message(opps)

            await send_message(message)

            print(message)

        except Exception as e:

            print("Error:", e)

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(run())