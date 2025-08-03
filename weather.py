import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from plyer import notification
from weatherAPIkey import api_key


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


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setFixedSize(300, 200)

        # Widgets
        self.label = QLabel("Enter your city:")
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("e.g., Kathmandu")
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.fetch_weather)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def fetch_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        try:
            data = get_weather_data(city, api_key)
            if data.get("cod") != 200:
                error_msg = data.get("message", "Unable to fetch weather data")
                QMessageBox.critical(self, "API Error", f"Error: {error_msg}")
                return

            temp, clouds = extract_weather_info(data)
            message = f"Temperature: {temp}°C\nSky: {clouds}"
            self.result_label.setText(message)
            notify_user(message)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
