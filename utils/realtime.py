import requests

coin_ids = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Solana (SOL)": "solana"
}


def get_current_price(crypto_choice):

    coin_id = coin_ids[crypto_choice]

    try:

        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin_id}&vs_currencies=usd"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data[coin_id]["usd"]

    except Exception:

        return None