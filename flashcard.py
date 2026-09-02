from storage import VocabularyStorage
class Flashcard:
    def __init__(self):
        self.storage = VocabularyStorage() # It creates your storage object
        self.words = self.storage.load_words() # Loads the words already saved in vocabulary.json
    

    def start(self):

        if not self.words:
            print("No saved words available.")
            return 

        for word, details in self.words.items():
            print(f"\nWord: {word}") # Displays each word one at a time
            answer = input("show definition? (y/n or q to quit): ") # Lets the user reveal the definition or quit

            if answer.lower() in ["q", "quit"]: # exits the flashcards
                break

            if answer.lower() in ["y", "yes"]: # y/yes shows the definition
                
                print(f"Definition: {details['definition']}")

if __name__=="__main__":
    flashcard = Flashcard()
    flashcard.start()