import pprint
import requests

def get_random_facts(animal_type='cat', amount=2):
    url = f"https://cat-fact.herokuapp.com/facts/random"
    params = {
        'animal_type': animal_type,
        'amount': amount
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        facts = response.json()
        return facts
    else:
        return None

# Example usage
facts = get_random_facts()
pprint(facts)
