import random
from storage import VocabularyStorage


class Quiz:
    def __init__(self):  # Handles vocabulary quiz questions and scoring
        self.storage = VocabularyStorage()
        self.correct = 0
        self.wrong = 0

    def load_words(self):  # Loads saved vocabulary
        words = self.storage.load_words()

        if not words:
            return None

        return words

    def generate_question(self, words):  # Chooses a random word for the quiz
        word = random.choice(list(words.keys()))

        details = words.pop(word)  # Removes the word so it cannot be selected again

        definition = details["definition"]

        return word, definition

    def check_answer(self, answer, correct_word):  # Checks the user's answer
        if answer.strip().lower() == correct_word.lower():
            self.correct += 1
            return True

        self.wrong += 1
        return False

    def ask_question(self, words):  # Displays one quiz question
        word, definition = self.generate_question(words)

        print(f"\nDefinition: {definition}")
        answer = input("What is the word? ")

        if self.check_answer(answer, word):
            print("Correct!")
        else:
            print(f"Wrong. The correct answer is: {word}")

    def start(self):  # Starts the quiz session
        words = self.load_words()

        if not words:
            print("No saved words available for quiz.")
            return

        self.correct = 0
        self.wrong = 0

        quiz_words = words.copy()

        question_count = min(5, len(quiz_words))

        for _ in range(question_count):
            self.ask_question(quiz_words)

        print("\nQuiz finished.")
        print(f"Correct: {self.correct}")
        print(f"Wrong: {self.wrong}")


if __name__ == "__main__":
    quiz = Quiz()
    quiz.start()