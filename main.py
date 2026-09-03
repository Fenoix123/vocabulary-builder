from dictionary_client import DictionaryClient
from storage import VocabularyStorage
from flashcard import Flashcard
from quiz import Quiz


class VocabularyBuilder:
    def __init__(self) -> None:
        self.dictionary = DictionaryClient()
        self.storage = VocabularyStorage()

    def search_and_save(self):  # Searches for a word and saves it
        word = input("Enter a word: ").strip()

        result = self.dictionary.search_word(word)

        if result is None:
            print("Word not found or dictionary service unavailable. ")
            return

        print(f"\nWord: {result.word}")
        print(f"Definition: {result.definition}")

        save = input("Save this word y/n?").strip().lower()

        if save in ["y", "yes"]:
            if self.storage.save_word(result):
                print("Word saved successfully.")
            else:
                print("Word already saved.")
    
    def review_flashcards(self):
        flashcard = Flashcard()
        flashcard.start()

    def take_quiz(self):
        quiz = Quiz()
        quiz.start()

    def run(self): # Displays the main program menu
        while True:
            print("\n=== Vocabulary Builder ===")
            print("1. Search and save a word")
            print("2. Review flashcards")
            print("3. Take a quiz")
            print("4. Exit")

            choice = input("Choose Option: ").strip()

            if choice == "1":
                self.search_and_save()

            elif choice == "2":
                self.review_flashcards()

            elif choice == "3":
                self.take_quiz()

            elif choice == "4":
                print("Goobye!")
                break

            else:
                print("Invalid option. Choose 1-4.")

if __name__ == "__main__":
    app = VocabularyBuilder()
    app.run()