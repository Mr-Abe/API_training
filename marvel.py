import os
from pprint import pprint 
from dotenv import load_dotenv
import hashlib
import time
import requests

# Load environment variables from .env file
load_dotenv()

def generate_auth_params(public_key, private_key):
    """
    Generates authentication parameters required by the Marvel API.
    
    Parameters:
    - public_key (str): The public API key.
    - private_key (str): The private API key.
    
    Returns:
    - dict: A dictionary containing the 'apikey', 'ts' (timestamp), and 'hash' (md5 hash of timestamp, private key, and public key).
    """
    ts = str(time.time())
    hash = hashlib.md5(f"{ts}{private_key}{public_key}".encode()).hexdigest()
    return {'apikey': public_key, 'ts': ts, 'hash': hash}

def make_request(endpoint, params):
    """
    Makes a GET request to the specified Marvel API endpoint.
    
    Parameters:
    - endpoint (str): The API endpoint to request.
    - params (dict): The query parameters for the request.
    
    Returns:
    - dict: The JSON response from the API.
    """
    base_url = "http://gateway.marvel.com/v1/public"
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def search_comics(title, auth_params):
    """
    Searches for comics by title.
    
    Parameters:
    - title (str): The title of the comic to search for.
    - auth_params (dict): Authentication parameters.
    
    Returns:
    - dict: The JSON response from the API.
    """
    params = {'title': title, **auth_params}
    return make_request('comics', params)

def normalize_character_data(character):
    character['name'] = character.get('name', 'N/A').title()
    character['description'] = character.get('description', 'No description available').strip()
    if 'thumbnail' in character and character['thumbnail']:
        character['thumbnail'] = f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}"
    return character

def get_characters(character_id, auth_params):
    character_data = make_request(f'characters/{character_id}', auth_params)
    if character_data and 'data' in character_data and 'results' in character_data['data']:
        return [normalize_character_data(char) for char in character_data['data']['results']]
    return []

def search_characters_by_name(name, auth_params):
    """
    Searches for characters by their names using the Marvel API.

    Parameters:
    - name (str): The name of the character to search for.
    - auth_params (dict): Authentication parameters.

    Returns:
    - dict: The JSON response from the API.
    """
    params = {'nameStartsWith': name, **auth_params}
    return make_request('characters', params)

def explore_series(series_id, auth_params):
    """
    Explores a specific series by ID.
    
    Parameters:
    - series_id (str): The unique ID of the series.
    - auth_params (dict): Authentication parameters.
    
    Returns:
    - dict: The JSON response from the API.
    """
    return make_request(f'series/{series_id}', auth_params)

def main():
    """
    Main function to run the script.
    """
    # Retrieve API keys from environment variables
    public_key = os.getenv('PUBLIC_API_KEY')
    private_key = os.getenv('PRIVATE_API_KEY')
    auth_params = generate_auth_params(public_key, private_key)
    
    # User input for action choice
    choice = input("Choose an option: 1. Search Comics 2. Get Character Details 3. Explore Series 4. Search Character by Name: ")
    if choice == '1':
        title = input("Enter comic title: ")
        pprint(search_comics(title, auth_params))
    elif choice == '2':
        character_id = input("Enter character ID: ")
        characters = get_characters(character_id, auth_params)
        for character in characters:
            pprint(character)
    elif choice == '3':
        series_id = input("Enter series ID: ")
        pprint(explore_series(series_id, auth_params))
    elif choice == '4':
        character_name = input("Enter character name: ")
        pprint(search_characters_by_name(character_name, auth_params))
    else:
        pprint("Invalid choice")

if __name__ == "__main__":
    main()