
import os
import pathlib
import webbrowser

import dotenv
import requests
from html import escape


# Load environment variables
ENV_PATH = pathlib.Path(__file__).resolve().parent / ".env"

ENV_LOADED = dotenv.load_dotenv(
    dotenv_path=ENV_PATH,
    encoding="utf-8-sig",
    override=True
)


class OpenWeatherClient:

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, lat=31.1316, lon=33.7984):

        self.api_key = (
            os.getenv("OPENWEATHER_API_KEY") or ""
        ).strip()

        self.lat = lat
        self.lon = lon

        self.session = requests.Session()

        if not self.api_key:
            raise ValueError(
                f"OPENWEATHER_API_KEY not found in {ENV_PATH}"
            )

    def get_weather(self):

        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": "metric"
        }

        response = self.session.get(
            self.BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


def generate_html(data):

    # Extract weather information
    city = escape(data["name"])
    country = escape(data["sys"]["country"])

    temperature = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    weather = escape(
        data["weather"][0]["description"].title()
    )

    icon = data["weather"][0]["icon"]

    icon_url = (
        f"https://openweathermap.org/img/wn/{icon}@4x.png"
    )

    wind_speed = data["wind"]["speed"]

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Weather Dashboard</title>

        <link rel="preconnect"
              href="https://fonts.googleapis.com">

        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
              rel="stylesheet">

        <style>

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Inter', sans-serif;
                min-height: 100vh;

                background: linear-gradient(
                    135deg,
                    #dbeafe,
                    #eff6ff,
                    #bfdbfe
                );

                display: flex;
                justify-content: center;
                align-items: center;

                padding: 30px 15px;
                color: #172554;
            }}

            .dashboard {{
                width: 100%;
                max-width: 750px;

                background: rgba(255, 255, 255, 0.85);

                backdrop-filter: blur(15px);

                border: 1px solid rgba(255,255,255,0.8);

                border-radius: 28px;

                padding: 40px;

                box-shadow: 0 20px 60px
                    rgba(30,64,175,0.12);
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .header h1 {{
                font-size: 27px;
                font-weight: 800;
                color: #1e40af;
            }}

            .header p {{
                color: #64748b;
                margin-top: 8px;
                font-size: 13px;
            }}

            .live {{
                background: #dcfce7;
                color: #15803d;
                padding: 8px 13px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
            }}

            .weather-main {{
                text-align: center;
                padding: 30px 0;
            }}

            .weather-main h2 {{
                font-size: 27px;
                color: #1e3a8a;
            }}

            .weather-icon img {{
                width: 140px;
                height: 140px;
                object-fit: contain;
            }}

            .temperature {{
                font-size: 85px;
                font-weight: 800;
                letter-spacing: -5px;
                color: #2563eb;
            }}

            .description {{
                font-size: 21px;
                color: #64748b;
                margin-top: 5px;
                font-weight: 500;
            }}

            .feels {{
                color: #64748b;
                margin-top: 12px;
                font-size: 14px;
            }}

            .section-title {{
                font-size: 16px;
                margin-bottom: 15px;
                color: #334155;
            }}

            .details {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}

            .item {{
                background: linear-gradient(
                    135deg,
                    #eff6ff,
                    #f8fafc
                );

                border: 1px solid #dbeafe;
                border-radius: 18px;
                padding: 22px;
                transition: 0.3s;
            }}

            .item:hover {{
                transform: translateY(-4px);

                box-shadow: 0 8px 20px
                    rgba(37,99,235,0.1);
            }}

            .item-label {{
                color: #64748b;
                font-size: 13px;
            }}

            .item-value {{
                font-size: 23px;
                font-weight: 700;
                color: #1d4ed8;
                margin-top: 10px;
            }}

            .item-icon {{
                font-size: 23px;
                margin-bottom: 12px;
            }}

            footer {{
                text-align: center;
                margin-top: 30px;
                color: #94a3b8;
                font-size: 12px;
            }}

            @media(max-width: 500px) {{

                .dashboard {{
                    padding: 25px 18px;
                }}

                .temperature {{
                    font-size: 65px;
                }}

                .item {{
                    padding: 16px;
                }}

                .item-value {{
                    font-size: 19px;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="dashboard">

            <header class="header">

                <div>
                    <h1>Weatherly</h1>
                    <p>Real-time weather information</p>
                </div>

                <span class="live">LIVE WEATHER</span>

            </header>


            <section class="weather-main">

                <h2>{city}, {country}</h2>

                <div class="weather-icon">

                    <img
                        src="{icon_url}"
                        alt="{weather}"
                        onerror="this.style.display='none'"
                    >

                </div>

                <div class="temperature">
                    {temperature}°C
                </div>

                <div class="description">
                    {weather}
                </div>

                <div class="feels">
                    Feels like {feels_like}°C
                </div>

            </section>


            <h3 class="section-title">
                Weather Details
            </h3>


            <section class="details">

                <div class="item">

                    <div class="item-icon">💧</div>

                    <div class="item-label">
                        Humidity
                    </div>

                    <div class="item-value">
                        {humidity}%
                    </div>

                </div>


                <div class="item">

                    <div class="item-icon">🌬️</div>

                    <div class="item-label">
                        Wind Speed
                    </div>

                    <div class="item-value">
                        {wind_speed} m/s
                    </div>

                </div>


                <div class="item">

                    <div class="item-icon">🌡️</div>

                    <div class="item-label">
                        Pressure
                    </div>

                    <div class="item-value">
                        {pressure} hPa
                    </div>

                </div>


                <div class="item">

                    <div class="item-icon">🌤️</div>

                    <div class="item-label">
                        Feels Like
                    </div>

                    <div class="item-value">
                        {feels_like}°C
                    </div>

                </div>

            </section>


            <footer>
                Weather data powered by OpenWeather API
            </footer>

        </div>

    </body>

    </html>
    """

    # Save HTML file
    output = (
        pathlib.Path(__file__).resolve().parent
        / "weather.html"
    )

    output.write_text(
        html_content,
        encoding="utf-8"
    )

    print(f"HTML report created: {output}")

    # Open report in browser
    webbrowser.open(output.as_uri())


if __name__ == "__main__":

    try:

        client = OpenWeatherClient()

        weather_data = client.get_weather()

        generate_html(weather_data)

    except requests.exceptions.HTTPError as error:

        print(f"API Error: {error}")

    except requests.exceptions.RequestException as error:

        print(f"Connection Error: {error}")

    except (ValueError, KeyError, TypeError) as error:

        print(f"Error: {error}")
