import requests
from models import Word


class DictionaryClient: # Class For Dictionary API searches 
    MAIN_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"

    def search_word(self,word): # Searches for a word using the dictionary API
        url = f"{self.MAIN_URL}/{word}"

        response = requests.get(url)

        if response.status_code != 200:
            return None


        data = response.json()  # Converts API response into Python data

    
        entry = data[0] # Uses the first dictionary entry returned

        definition = entry["meanings"][0]["definitions"][0]["definition"] # Gets the first available definition

        phonetic = entry.get("phonetic","")


        examples = []
        synonyms = []
        antonyms = []

        for meaning in entry.get("meanings", []):  # Goes through all meanings of the word
            synonyms.extend(meaning.get("synonyms", []))
            antonyms.extend(meaning.get("antonyms", []))
            
            for definition_item in meaning.get("definitions", []):
                example = definition_item.get("example")

                if example:
                    examples.append(example)

                synonyms.extend(definition_item.get("synonyms", []))

                antonyms.extend(definition_item.get("antonyms", []))

        examples = list(dict.fromkeys(examples)) # Removes Duplicates
        synonyms = list(dict.fromkeys(synonyms))
        antonyms = list(dict.fromkeys(antonyms))

        return Word(word=word, definition=definition, phonetic=phonetic, synonyms=synonyms, examples=examples, antonyms=antonyms  )



