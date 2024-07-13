import httpx
import os
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from hashlib import md5
from datetime import datetime

class ActionFetchMarvelCharacter(Action):
    def name(self):
        return "action_fetch_marvel_character"
    
    async def run(self, dispatcher, tracker, domain):
        # Retrieve the character name from the slot
        character_name = tracker.get_slot('character')
        if not character_name:
            dispatcher.utter_message(text="Please specify a character name.")
            return []

        # Generate the necessary parameters for the Marvel API request
        ts = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        public_key = os.getenv('PUBLIC_API_KEY')
        private_key = os.getenv('PRIVATE_API_KEY')
        hash_signature = md5(f"{ts}{private_key}{public_key}".encode()).hexdigest()
        url = f"http://gateway.marvel.com/v1/public/characters?name={character_name}&ts={ts}&apikey={public_key}&hash={hash_signature}"
        
        # Use httpx.AsyncClient for asynchronous HTTP requests
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()  # This will raise an exception for HTTP errors
                results = response.json()['data']['results']

                if results:
                    data = results[0]
                    description = data['description'] if data['description'] else "No description available."
                    dispatcher.utter_message(text=f"Name: {character_name}\nDescription: {description}")
                else:
                    dispatcher.utter_message(text="No results found for the specified character. Please try another name.")
            except httpx.HTTPStatusError as e:
                dispatcher.utter_message(text=f"Failed to fetch character details, HTTP error occurred: {e.response.status_code}")
            except Exception as e:
                dispatcher.utter_message(text=f"Failed to fetch character details due to: {str(e)}")

        return []