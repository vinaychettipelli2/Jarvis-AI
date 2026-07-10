import requests


class CryptoProvider:
    """
    Crypto Provider

    Uses CoinGecko Free API.
    No API Key Required.
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_price(self, coin="bitcoin"):

        try:

            url = (
                f"{self.BASE_URL}/simple/price"
                f"?ids={coin}"
                f"&vs_currencies=usd,inr"
                f"&include_24hr_change=true"
            )

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if coin not in data:

                return {

                    "success": False,

                    "message": f"{coin} not found."

                }

            coin_data = data[coin]

            return {

                "success": True,

                "coin": coin.title(),

                "usd": coin_data["usd"],

                "inr": coin_data["inr"],

                "change_24h": coin_data.get(
                    "usd_24h_change",
                    0
                )

            }

        except Exception as e:

            return {

                "success": False,

                "message": str(e)

            }