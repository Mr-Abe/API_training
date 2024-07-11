# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import requests
import os
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from hashlib import md5
from datetime import datetime

class ActionFetchMarvelCharacter(Action):
    def name(self):
        return "action_fetch_marvel_character"
    
    def run(self, dispatcher, tracker, domain):
        character_name = tracker.get_slot('character')
        if not character_name:
            dispatcher.utter_message(text="Please specify a character name.")
            return []

        ts = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        public_key = os.getenv('PUBLIC_API_KEY')
        private_key = os.getenv('PRIVATE_API_KEY')
        hash = md5(f"{ts}{private_key}{public_key}".encode()).hexdigest()
        url = f"http://gateway.marvel.com/v1/public/characters?name={character_name}&ts={ts}&apikey={public_key}&hash={hash}"
        
        try:
            response = requests.get(url).json()
            results = response['data']['results']
            if results:
                data = results[0]
                description = data['description'] if data['description'] else "No description available."
                dispatcher.utter_message(text=f"Name: {character_name}\nDescription: {description}")
            else:
                dispatcher.utter_message(text="No results found for the specified character. Please try another name.")
        except Exception as e:
            dispatcher.utter_message(text=f"Failed to fetch character details due to: {str(e)}")
            return []

        return []
