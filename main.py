import requests
import json
import os
import re
import random
from datetime import datetime, timedelta


# ============================================================
# VOCABULARY BUILDER & SMART FLASHCARD APP
# Beginner-Friendly Version
# ============================================================


DATA_FOLDER = "vocabulary_data"
SAVED_WORDS_FILE = os.path.join(DATA_FOLDER, "saved_words.json")
FLASHCARDS_FILE = os.path.join(DATA_FOLDER, "flashcards.json")
QUIZ_SCORES_FILE = os.path.join(DATA_FOLDER, "quiz_scores.json")


# ============================================================
# WORD CLASS
# ============================================================

class Word:
    def __init__(
        self,
        word,
        definition="",
        phonetic="",
        example="",
        synonyms=None,
        antonyms=None
    ):
        self.word = word
        self.definition = definition
        self.phonetic = phonetic
        self.example = example
        self.synonyms = synonyms or []
        self.antonyms = antonyms or []

    def to_dict(self):
        return {
            "word": self.word,
            "definition": self.definition,
            "phonetic": self.phonetic,
            "example": self.example,
            "synonyms": self.synonyms,
            "antonyms": self.antonyms
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("word", ""),
            data.get("definition", ""),
            data.get("phonetic", ""),
            data.get("example", ""),
            data.get("synonyms", []),
            data.get("antonyms", [])
        )

    def display(self):
        print("\n" + "=" * 50)
        print("WORD:", self.word)
        print("PHONETIC:", self.phonetic or "Not available")
        print("DEFINITION:", self.definition or "Not available")
        print("EXAMPLE:", self.example or "Not available")

        print("SYNONYMS:",
              ", ".join(self.synonyms) if self.synonyms else "Not available")

        print("ANTONYMS:",
              ", ".join(self.antonyms) if self.antonyms else "Not available")

        print("=" * 50)


# ============================================================
# DICTIONARY CLIENT
# ============================================================

class DictionaryClient:
    def __init__(self):
        self.base_url = (
            "https://api.dictionaryapi.dev/api/v2/entries/en"
        )

    def validate_word(self, word):
        word = word.strip().lower()

        if not word:
            raise ValueError("Please enter a word.")

        if not re.fullmatch(r"[A-Za-z]+", word):
            raise ValueError(
                "Please enter letters only. "
                "Numbers and punctuation are not allowed."
            )

        return word

    def search_word(self, word):

        word = self.validate_word(word)

        url = f"{self.base_url}/{word}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                print("\nSorry, that word was not found.")
                return None

            response.raise_for_status()

            data = response.json()

            if not data:
                print("\nNo information was returned.")
                return None

            entry = data[0]

            word_text = entry.get("word", word)

            phonetic = entry.get("phonetic", "")

            if not phonetic:
                phonetics = entry.get("phonetics", [])

                for item in phonetics:
                    if item.get("text"):
                        phonetic = item.get("text")
                        break

            definition = ""
            example = ""
            synonyms = []
            antonyms = []

            meanings = entry.get("meanings", [])

            for meaning in meanings:

                if not definition:
                    definitions = meaning.get("definitions", [])

                    if definitions:
                        definition = definitions[0].get(
                            "definition", ""
                        )

                        example = definitions[0].get(
                            "example", ""
                        )

                synonyms.extend(
                    meaning.get("synonyms", [])
                )

                antonyms.extend(
                    meaning.get("antonyms", [])
                )

            synonyms = list(dict.fromkeys(synonyms))
            antonyms = list(dict.fromkeys(antonyms))

            return Word(
                word_text,
                definition,
                phonetic,
                example,
                synonyms,
                antonyms
            )

        except requests.exceptions.Timeout:
            print("\nThe dictionary request timed out.")
            return None

        except requests.exceptions.ConnectionError:
            print("\nCould not connect to the internet.")
            return None

        except requests.exceptions.RequestException as error:
            print("\nDictionary API error:", error)
            return None

        except (ValueError, KeyError, IndexError) as error:
            print("\nCould not process the dictionary response:", error)
            return None


# ============================================================
# FILE MANAGER
# ============================================================

class FileManager:

    @staticmethod
    def create_data_folder():

        try:
            if not os.path.exists(DATA_FOLDER):
                os.makedirs(DATA_FOLDER)

        except OSError as error:
            print("Could not create data folder:", error)

    @staticmethod
    def save_json(filename, data):

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True

        except (OSError, TypeError) as error:
            print("Could not save data:", error)
            return False

    @staticmethod
    def load_json(filename, default):

        try:

            if not os.path.exists(filename):
                return default

            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except (OSError, json.JSONDecodeError) as error:
            print("Could not read data:", error)
            return default


# ============================================================
# FLASHCARD CLASS
# ============================================================

class Flashcard:
    def __init__(
        self,
        word,
        definition,
        next_review=None,
        interval=1
    ):
        self.word = word
        self.definition = definition
        self.next_review = next_review
        self.interval = interval

    def to_dict(self):
        return {
            "word": self.word,
            "definition": self.definition,
            "next_review": self.next_review,
            "interval": self.interval
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("word", ""),
            data.get("definition", ""),
            data.get("next_review"),
            data.get("interval", 1)
        )


# ============================================================
# SPACED REPETITION MANAGER
# ============================================================

class SpacedRepetitionManager:

    def review_card(self, flashcard, correct):

        if correct:

            flashcard.interval *= 2

            next_date = datetime.now() + timedelta(
                days=flashcard.interval
            )

            flashcard.next_review = next_date.strftime(
                "%Y-%m-%d"
            )

            print(
                f"\nCorrect! Review this word again in "
                f"{flashcard.interval} day(s)."
            )

        else:

            flashcard.interval = 1

            next_date = datetime.now() + timedelta(days=1)

            flashcard.next_review = next_date.strftime(
                "%Y-%m-%d"
            )

            print(
                "\nKeep practicing! "
                "You should review this word tomorrow."
            )


# ============================================================
# QUIZ GENERATOR
# ============================================================

class QuizGenerator:

    def create_question(self, word):

        question = (
            f"\nWhat is the meaning of the word "
            f"'{word.word}'?"
        )

        correct_answer = word.definition

        wrong_answers = [
            "A type of food",
            "A place to visit",
            "A person's name"
        ]

        options = [correct_answer] + wrong_answers

        random.shuffle(options)

        return question, options, correct_answer

    def run_quiz(self, words):

        if not words:
            print("\nYou have no saved words for the quiz.")
            return 0

        score = 0

        number_of_questions = min(5, len(words))

        selected_words = random.sample(
            words,
            number_of_questions
        )

        for number, word in enumerate(
            selected_words,
            start=1
        ):

            question, options, correct = (
                self.create_question(word)
            )

            print("\nQuestion", number)
            print(question)

            for index, option in enumerate(options, start=1):
                print(f"{index}. {option}")

            while True:

                answer = input(
                    "Choose an answer (1-4): "
                ).strip()

                if answer in ["1", "2", "3", "4"]:
                    break

                print("Please choose a number from 1 to 4.")

            selected_answer = options[int(answer) - 1]

            if selected_answer == correct:
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
                print("Correct answer:", correct)

        print(
            f"\nYour score: {score}/{number_of_questions}"
        )

        return score


# ============================================================
# SIMPLE AI HELPER
# ============================================================

class AIHelper:

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")

    def generate_learning_help(self, word):

        if not self.api_key:
            return self.local_learning_help(word)

        prompt = f"""
You are a beginner-friendly vocabulary teacher.

Word: {word.word}
Definition: {word.definition}

Give:
1. A simple explanation
2. One easy example sentence
3. One memory trick

Keep everything short and easy to understand.
"""

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-2.5-flash:generateContent"
        )

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            text = (
                data["candidates"][0]["content"]
                ["parts"][0]["text"]
            )

            return text

        except Exception:
            return self.local_learning_help(word)

    def local_learning_help(self, word):

        simple = (
            f"Simple meaning: {word.definition}"
        )

        example = word.example

        if not example:
            example = (
                f"The word '{word.word}' can be "
                f"used when talking about something "
                f"related to its meaning."
            )

        memory = (
            f"Memory trick: Say the word '{word.word}' "
            f"several times and connect it with the "
            f"meaning: {word.definition}"
        )

        return (
            "\n" + simple +
            "\nExample: " + example +
            "\n" + memory
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

class VocabularyApp:

    def __init__(self):

        FileManager.create_data_folder()

        self.dictionary = DictionaryClient()
        self.quiz_generator = QuizGenerator()
        self.spaced_repetition = SpacedRepetitionManager()
        self.ai_helper = AIHelper()

        self.saved_words = []
        self.flashcards = []
        self.quiz_scores = []

        self.load_data()

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    def load_data(self):

        words_data = FileManager.load_json(
            SAVED_WORDS_FILE,
            []
        )

        flashcards_data = FileManager.load_json(
            FLASHCARDS_FILE,
            []
        )

        scores_data = FileManager.load_json(
            QUIZ_SCORES_FILE,
            []
        )

        self.saved_words = [
            Word.from_dict(item)
            for item in words_data
        ]

        self.flashcards = [
            Flashcard.from_dict(item)
            for item in flashcards_data
        ]

        self.quiz_scores = scores_data

    # --------------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------------

    def save_data(self):

        words_data = [
            word.to_dict()
            for word in self.saved_words
        ]

        flashcards_data = [
            card.to_dict()
            for card in self.flashcards
        ]

        FileManager.save_json(
            SAVED_WORDS_FILE,
            words_data
        )

        FileManager.save_json(
            FLASHCARDS_FILE,
            flashcards_data
        )

        FileManager.save_json(
            QUIZ_SCORES_FILE,
            self.quiz_scores
        )

    # --------------------------------------------------------
    # SEARCH WORD
    # --------------------------------------------------------

    def search_word(self):

        user_input = input(
            "\nEnter a word: "
        ).strip()

        try:

            word = self.dictionary.search_word(
                user_input
            )

            if word:
                word.display()

                print(
                    "\nAI Learning Help:"
                )

                print(
                    self.ai_helper.generate_learning_help(
                        word
                    )
                )

                save = input(
                    "\nSave this word? (y/n): "
                ).strip().lower()

                if save == "y":

                    already_saved = any(
                        item.word.lower() ==
                        word.word.lower()
                        for item in self.saved_words
                    )

                    if already_saved:

                        print(
                            "\nThis word is already saved."
                        )

                    else:

                        self.saved_words.append(word)

                        card = Flashcard(
                            word.word,
                            word.definition,
                            datetime.now().strftime(
                                "%Y-%m-%d"
                            ),
                            1
                        )

                        self.flashcards.append(card)

                        self.save_data()

                        print(
                            "\nWord and flashcard saved!"
                        )

        except ValueError as error:

            print("\nInput error:", error)

    # --------------------------------------------------------
    # VIEW SAVED WORDS
    # --------------------------------------------------------

    def view_saved_words(self):

        if not self.saved_words:

            print("\nNo saved words yet.")
            return

        print("\nSAVED WORDS")

        for number, word in enumerate(
            self.saved_words,
            start=1
        ):

            print(
                f"{number}. {word.word} - "
                f"{word.definition}"
            )

    # --------------------------------------------------------
    # REVIEW FLASHCARDS
    # --------------------------------------------------------

    def review_flashcards(self):

        if not self.flashcards:

            print("\nYou have no flashcards yet.")
            return

        print("\nFLASHCARD REVIEW")

        for card in self.flashcards:

            print("\n" + "-" * 40)

            print(
                "WORD:",
                card.word
            )

            input(
                "Press Enter to reveal the definition..."
            )

            print(
                "DEFINITION:",
                card.definition
            )

            answer = input(
                "Did you remember it? (y/n): "
            ).strip().lower()

            self.spaced_repetition.review_card(
                card,
                answer == "y"
            )

        self.save_data()

    # --------------------------------------------------------
    # TAKE QUIZ
    # --------------------------------------------------------

    def take_quiz(self):

        score = self.quiz_generator.run_quiz(
            self.saved_words
        )

        if self.saved_words:

            record = {
                "date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "score": score,
                "total": min(
                    5,
                    len(self.saved_words)
                )
            }

            self.quiz_scores.append(record)

            self.save_data()

    # --------------------------------------------------------
    # VIEW QUIZ SCORES
    # --------------------------------------------------------

    def view_scores(self):

        if not self.quiz_scores:

            print("\nNo quiz scores yet.")
            return

        print("\nQUIZ SCORES")

        for score in self.quiz_scores:

            print(
                f"{score['date']} - "
                f"{score['score']}/{score['total']}"
            )

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    def run(self):

        print("\n" + "=" * 55)

        print(
            "      VOCABULARY BUILDER & SMART FLASHCARD APP"
        )

        print("=" * 55)

        while True:

            print("\nMAIN MENU")

            print("1. Search for a word")
            print("2. View saved words")
            print("3. Review flashcards")
            print("4. Take quiz")
            print("5. View quiz scores")
            print("6. Exit")

            choice = input(
                "\nChoose an option: "
            ).strip()

            if choice == "1":

                self.search_word()

            elif choice == "2":

                self.view_saved_words()

            elif choice == "3":

                self.review_flashcards()

            elif choice == "4":

                self.take_quiz()

            elif choice == "5":

                self.view_scores()

            elif choice == "6":

                self.save_data()

                print(
                    "\nThank you for using "
                    "Vocabulary Builder!"
                )

                break

            else:

                print(
                    "\nInvalid option. "
                    "Please choose 1-6."
                )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    try:

        app = VocabularyApp()

        app.run()

    except KeyboardInterrupt:

        print(
            "\n\nProgram stopped safely."
        )

    except Exception as error:

        print(
            "\nAn unexpected error occurred:"
        )

        print(error)
