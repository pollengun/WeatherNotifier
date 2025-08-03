import requests
from weatherAPIkey import api_key
from plyer import notification


def get_weather_data(city: str, api_key: str) -> dict:
    """Fetch weather data from OpenWeatherMap API."""
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
    return response.json()


def extract_weather_info(data: dict) -> tuple:
    """Extract temperature in Celsius and cloud description from API response."""
    kelvin_temp = data['main']['temp']
    celsius = round(kelvin_temp - 273.15, 2)
    description = data['weather'][0]['description']
    return celsius, description


def notify_user(message: str):
    """Send desktop notification with weather message."""
    notification.notify(
        title="Weather Update",
        message=message,
        timeout=10  # seconds
    )


def main():
    city = input("Enter your city: ")
    try:
        data = get_weather_data(city, api_key)
        if data.get("cod") != 200:
            print(f"Error: {data.get('message', 'Unable to fetch weather data')}")
            return

        temp, clouds = extract_weather_info(data)
        weather_message = f"Temperature: {temp}°C\nSky: {clouds}"

        print(weather_message)
        notify_user(weather_message)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
