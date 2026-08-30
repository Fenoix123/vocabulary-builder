import json

class VocabularyStorage: # Handles saving and loading vocabulary words
    def __init__(self, filename="vocabulary.json") -> None:
        self.filename= filename

    def load_words(self): # Loads saved vocabulary words from the JSON file
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError): # Returns an empty dictionary if the file is missing or invalid
            return {}

        return data

    def save_word(self,word): # Saving one word
        data = self.load_words()

        if word.word in data:  # Prevents duplicate words from being saved
            return False

        data[word.word] = word.to_dict()  # Converts the Word object into a dictionary before saving

        self.save_words(data)

        return True

    def save_words(self, data): # Writes the Saved words in the JSON file
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

