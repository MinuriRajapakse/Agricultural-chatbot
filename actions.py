from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests


class ActionWeatherAPI(Action):
    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.latest_message['text']

        # Retrieve weather information
        weather_data = Weather(city)

        # Extract temperature from weather data
        temperature = int(weather_data['main']['temp'] - 273)

        dispatcher.utter_message(text=f"The temperature in {city} is {temperature}°C.")

        # Set the crop_disease slot
        crop_disease = tracker.get_slot("crop_disease")

        if (crop_disease == "potato late blight" or crop_disease == "potato early blight" or crop_disease == "late blight" or crop_disease == "early blight") and (
                24 >= temperature >= 10):
            dispatcher.utter_message(
                "According to this temperature this is the best time for tuber initiation of potato")
        elif (crop_disease == "potato late blight" or crop_disease == "potato early blight" or crop_disease == "late blight" or crop_disease == "early blight") and (
                temperature < 10 or
                temperature > 24):
            dispatcher.utter_message(
                "According to this temperature this is not the time for tuber initiation of potato.")
        elif (crop_disease == "rice brown spot" or crop_disease == "brown spot") and (16 >= temperature >= 36):
            dispatcher.utter_message(
                "You have to take immediate preventive measures to avoid spreading of this disease.")
        elif (crop_disease == "rice bacterial leaf blight" or crop_disease == "bacterial leaf blight") and (
                25 >= temperature >= 34):
            dispatcher.utter_message(
                "You have to take immediate preventive measures to avoid spreading of this disease.")
        elif (crop_disease == "rice blast" or crop_disease == "blast") and (17 >= temperature >= 20):
            dispatcher.utter_message(
                "You have to take immediate preventive measures to avoid spreading of this disease.")
        elif (crop_disease == "tea leaf spot" or crop_disease == "leaf spot") and (14 >= temperature >= 25):
            dispatcher.utter_message(
                "You have to take immediate preventive measures to avoid spreading of this disease.")
        elif (crop_disease == "tea white spot" or crop_disease == "white spot") and (18 >= temperature >= 30):
            dispatcher.utter_message(
                "You have to take immediate preventive measures to avoid spreading of this disease.")
        else:
            dispatcher.utter_message(
                "According to the temperature the possibility of spreading the disease is very low but take necessary "
                "preventive measures.")

        return [SlotSet("crop_disease", crop_disease)]


class ActionCustomFallback(Action):
    def name(self) -> str:
        return "action_custom_fallback"

    def run(self, dispatcher, tracker, domain):
        # Send the message to the user
        dispatcher.utter_message(
            text="I'm sorry, I didn't understand that. Could you please rephrase or provide more details?"
                 "\nමට සමාවෙන්න, මට ඒක තේරුණේ නැහැ. කරුණාකර ඔබට නැවත ලිවීමට හෝ වැඩි විස්තර සැපයිය හැකිද?")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


def Weather(city):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    url = api_address + city
    json_data = requests.get(url).json()
    return json_data
