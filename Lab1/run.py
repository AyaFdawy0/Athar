
import json
import os
import pathlib

import dotenv
import requests

ENV_PATH = pathlib.Path(__file__).resolve().parent / ".env"
ENV_LOADED = dotenv.load_dotenv(
    dotenv_path=ENV_PATH,
    encoding="utf-8-sig",  # tolerates a UTF-8 BOM
    override=True,         # .env wins over an empty OS-level variable
)


class OpenWeatherClient:

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, lat=31.1316, lon=33.7984):  # El-Arish, Egypt (approx.)
        self.api_key = (os.getenv("OPENWEATHER_API_KEY") or "").strip()
        self.lat = lat
        self.lon = lon
        self.session = requests.Session()
        if not self.api_key:
            raise ValueError(
                f"OPENWEATHER_API_KEY not found. Looked for {ENV_PATH} "
                f"(exists={ENV_PATH.exists()}, loaded={ENV_LOADED})"
            )

    def get_weather(self):
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": "metric",
        }
        response = self.session.get(self.BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        raise RuntimeError(
            f"Failed to retrieve weather data ({response.status_code}): {response.text}"
        )

if __name__ == "__main__":
    print(OpenWeatherClient().get_weather())

