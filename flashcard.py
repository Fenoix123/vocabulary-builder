from storage import VocabularyStorage
class Flashcard:
    def __init__(self):
        self.storage = VocabularyStorage() # It creates your storage object
        self.words = self.storage.load_words() # Loads the words already saved in vocabulary.json
        print(self.words)

    def start(self):

        if not self.words:
            print(str("No saved words available."))
        for word, details in self.words.items():
            print(f"\nWord: {word}") # it displays each word one at a time
            answer = input("show definition? (y/n or q to quit): ") #this asks the user to choose what to dor each word

            if answer.lower() in ["q", "quit"]: # makes q , quit all work
                break

            if answer.lower() in ["y", "yes"]: # y/yes shows the definition
                # n/no does not show the definition but moves to the next word
                # exits the flashcards
                print(f"Definition: {details['definition']}")

if __name__=="__main__":
    flashcard = Flashcard()
    flashcard.start()