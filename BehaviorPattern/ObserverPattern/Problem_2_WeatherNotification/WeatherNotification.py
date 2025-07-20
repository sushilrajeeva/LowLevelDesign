""" Observer Pattern – Weather Notification System

    Problem:

    Build a weather alert service for a small broadcast app. The system should:

    1. Allow channels (Phone, TV, Radio) to **subscribe** or **unsubscribe** at any time.
    2. Track the current weather (Sunny, Rainy, Windy, Cloudy).
    3. Whenever the weather **changes**, notify **all** subscribed channels exactly once.
    4. Suppress notifications if the same weather is posted twice in a row.

    Real‐World Analogy:

    Like a local meteorological service pushing updates to your mobile app, TV ticker, and car radio—only the devices you’ve opted into should receive each new weather alert.
"""


# WeatherNotification.py
from abc import ABC, abstractmethod
from typing import Optional, Set, List

from enum import Enum

class Weather(Enum):
    SUNNY = "Sunny"
    RAINY = "Rainy"
    WINDY = "Windy"
    CLOUDY = "Cloudy"


# -------- Observer Interface --------
class Observer(ABC):
    @abstractmethod
    def update(self, weather: Weather) -> None:
        pass

# -------- Observeable / Subect Interface --------
class Subject(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_all(self, weather: Weather) -> None:
        pass

# -------- Concrete Observable / Subject Implementation --------
class WeatherStation(Subject):

    def __init__(self):
        self._weather: Optional[Weather] = None
        self._observers: Set[Observer] = set()

    def subscribe(self, observer: Observer) -> None:
        self._observers.add(observer)

    def unsubscribe(self, observer: Observer) ->None:
        self._observers.discard(observer)
        # self._observers.discard(observer) can use this if we wan't to raise exception if the observer we are removing is not found

    def notify_all(self, weather: Weather) -> None:
        for observer in self._observers:
            observer.update(weather)

    def set_weather(self, weather: Weather) -> None:
        if self._weather == weather:
            print("No change in weather.")
            return
        self._weather = weather
        print("Weather has changed... notifying all")
        self.notify_all(self._weather)


class Receiver(Observer):
    def __init__(self):
        self._weather: Optional[Weather] = None

    def update(self, weather: Weather) -> None:
        self._weather = weather
        self._display()

    @abstractmethod
    def _display(self) -> None:
        pass

    @abstractmethod
    def about(self) -> str:
        pass


class PhoneObserver(Receiver):

    def _display(self,) -> None:
        print(f"📱 Phone Notification: Weather is now {self._weather.value}")

    def about(self) -> str:
        return "📱 Phone observer"


class TVObserver(Receiver):

    def _display(self) -> None:
        print(f"📺 TV Notification: Weather is now {self._weather.value}")

    def about(self) -> str:
        return "📺 TV observer"
        
        
class RadioObserver(Receiver):

    def _display(self) -> None:
        print(f"📻 Radio Notification: Weather is now {self._weather.value}")

    def about(self) -> str:
        return "📻 Radio observer"


def print_divider(title: str) -> None:
    print("\n" + "=" * 40)
    print(f"  {title}")
    print("=" * 40 + "\n")


# -------- Demo --------
if __name__ == "__main__":
    print_divider("CREATING Weather Station")
    weather_station: WeatherStation = WeatherStation()



    print_divider("Creating Observer List")
    observers: List[Receiver] = [PhoneObserver(), TVObserver(), RadioObserver()]

    print_divider("Adding all observers to the weather station")
    for observer in observers:
        print(observer.about(), "added")
        weather_station.subscribe(observer)


    # print_divider("Updating Weather to sunny")
    # weatherStation.setWeather(Weather.SUNNY)

    # print_divider("Updating Weather to rainy")
    # weatherStation.setWeather(Weather.RAINY)

    # print_divider("Updating Weather to windy")
    # weatherStation.setWeather(Weather.WINDY)

    # print_divider("Updating Weather to cloudy")
    # weatherStation.setWeather(Weather.CLOUDY)

    # print_divider("Updating Weather to cloudy")
    # weatherStation.setWeather(Weather.CLOUDY)

    print_divider("Setting Weathers")
    for w in (Weather.SUNNY, Weather.RAINY, Weather.WINDY, Weather.CLOUDY, Weather.CLOUDY):
        print_divider(f"SETTING WEATHER TO {w.name}")
        weather_station.set_weather(w)


    print_divider("Removing radio observer")
    weather_station.unsubscribe(observers[-1])

    print_divider("Updating weather to rainy")
    weather_station.set_weather(Weather.RAINY)





