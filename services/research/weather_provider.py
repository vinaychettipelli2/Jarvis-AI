        import requests


class WeatherProvider:

    """
    Weather Provider

    Uses wttr.in (Free)
    No API Key Required.
    """

    BASE_URL = "https://wttr.in"

    def get_weather(self, city):

        try:

            response = requests.get(

                f"{self.BASE_URL}/{city}?format=j1",

                timeout=10

            )

            response.raise_for_status()

            data = response.json()

            current = data["current_condition"][0]

            return {

                "success": True,

                "city": city,

                "temperature": current["temp_C"],

                "feels_like": current["FeelsLikeC"],

                "humidity": current["humidity"],

                "weather": current["weatherDesc"][0]["value"],

                "wind_speed": current["windspeedKmph"]

            }

        except Exception as e:

            return {

                "success": False,

                "message": str(e)

            }