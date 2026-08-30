import json
from models import Word

class VocabularyStorage: # For Storing the saved words
    def __init__(self, filename="vocabulary.json") -> None:
        self.filename= filename

    def load_words(self): # For loading the file with saved words
        try:
            with open("vocabulary.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

        return data

    def save_word(self,word): # Saving one word
        data = self.load_words()

        if word.word in data:
            return False

        data[word.word] = word.to_dict()

        self.save_words(data)

        return True

    def save_words(self, data): # Writes the Saved words in the JSON file
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

