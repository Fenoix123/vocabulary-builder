import tkinter as tk

from dictionary_client import DictionaryClient
from storage import VocabularyStorage
from quiz import Quiz


class VocabularyGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.dictionary = DictionaryClient()
        self.storage = VocabularyStorage()
        self.current_result = None

        self.root.title("Vocabulary Builder")
        self.root.geometry("600x500")

        # Main title
        title = tk.Label(
            self.root,
            text="Vocabulary Builder",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        # Search button
        search_button = tk.Button(
            self.root,
            text="Search Word",
            width=20,
            command=self.open_search_window
        )
        search_button.pack(pady=10)

        # Flashcard button
        flashcard_button = tk.Button(
            self.root,
            text="Flashcards",
            width=20,
            command=self.open_flashcard_window
        )
        flashcard_button.pack(pady=10)

        # Quiz button
        quiz_button = tk.Button(
            self.root,
            text="Take Quiz",
            width=20,
            command=self.open_quiz_window
        )
        quiz_button.pack(pady=10)

        # Exit button
        exit_button = tk.Button(
            self.root,
            text="Exit",
            width=20,
            command=self.root.destroy
        )
        exit_button.pack(pady=10)

    def open_search_window(self):  # Opens the word search window
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Word")
        search_window.geometry("500x450")

        title = tk.Label(
            search_window,
            text="Search for a Word",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        word_entry = tk.Entry(
            search_window,
            width=30,
            font=("Arial", 12)
        )
        word_entry.pack(pady=10)

        result_label = tk.Label(
            search_window,
            text="",
            wraplength=400,
            justify="left"
        )
        result_label.pack(pady=20)

        def search():  # Searches for the word entered
            self.current_result = None

            word = word_entry.get().strip()

            if not word:
                result_label.config(text="Please enter a word.")
                return

            result = self.dictionary.search_word(word)

            if result is None:
                result_label.config(
                    text="Word not found or dictionary service unavailable."
                )
                return

            self.current_result = result

            result_label.config(
                text=f"Word: {result.word}\n\n"
                     f"Definition: {result.definition}\n\n"
                     f"Phonetic: {result.phonetic or 'Not available'}"
            )

        def save_word():  # Saves the searched word
            if self.current_result is None:
                result_label.config(text="Search for a word first.")
                return

            if self.storage.save_word(self.current_result):
                result_label.config(
                    text=f"Word: {self.current_result.word}\n\n"
                         f"Definition: {self.current_result.definition}\n\n"
                         f"Phonetic: {self.current_result.phonetic or 'Not available'}\n\n"
                         "Word saved successfully."
                )
            else:
                result_label.config(
                    text="This word is already saved."
                )

        # Search button
        search_button = tk.Button(
            search_window,
            text="Search",
            width=15,
            command=search
        )
        search_button.pack(pady=10)

        # Save button
        save_button = tk.Button(
            search_window,
            text="Save Word",
            width=15,
            command=save_word
        )
        save_button.pack(pady=10)

        close_button = tk.Button( search_window, text="Close",width=15,command=search_window.destroy
    )
        close_button.pack(pady=10)

    def open_flashcard_window(self):  # Opens the flashcard window
        words = self.storage.load_words()

        flashcard_window = tk.Toplevel(self.root)
        flashcard_window.title("Flashcards")
        flashcard_window.geometry("500x450")

        if not words:
            message = tk.Label(
                flashcard_window,
                text="No saved words available.",
                font=("Arial", 14)
            )
            message.pack(pady=50)
            return

        word_list = list(words.items())
        self.flashcard_index = 0

        word_label = tk.Label(
            flashcard_window,
            text="",
            font=("Arial", 22, "bold")
        )
        word_label.pack(pady=40)

        definition_label = tk.Label(
            flashcard_window,
            text="",
            font=("Arial", 12),
            wraplength=400
        )
        definition_label.pack(pady=20)

        def show_word():  # Displays the current flashcard
            word, details = word_list[self.flashcard_index]

            word_label.config(text=word)
            definition_label.config(text="")

        def show_definition():  # Reveals the word definition
            word, details = word_list[self.flashcard_index]

            definition_label.config(
                text=details["definition"]
            )

        def next_word():  # Moves to the next flashcard
            self.flashcard_index += 1

            if self.flashcard_index >= len(word_list):
                self.flashcard_index = 0

            show_word()

        show_word()

        reveal_button = tk.Button(
            flashcard_window,
            text="Show Definition",
            width=20,
            command=show_definition
        )
        reveal_button.pack(pady=10)

        next_button = tk.Button(
            flashcard_window,
            text="Next Word",
            width=20,
            command=next_word
        )
        next_button.pack(pady=10)

        close_button = tk.Button(
        flashcard_window,
        text="Close",
        width=20,
        command=flashcard_window.destroy
    )
        close_button.pack(pady=10)

    def open_quiz_window(self):  # Opens the quiz window
        quiz = Quiz()
        words = quiz.load_words()

        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Vocabulary Quiz")
        quiz_window.geometry("550x500")

        if not words:
            message = tk.Label(
                quiz_window,
                text="No saved words available for quiz.",
                font=("Arial", 14)
            )
            message.pack(pady=50)
            return

        # Makes a copy so quiz questions can be removed without changing saved data
        quiz_words = words.copy()

        question_count = min(5, len(quiz_words))
        current_question = 0
        current_word = ""

        title = tk.Label(
            quiz_window,
            text="Vocabulary Quiz",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        progress_label = tk.Label(
            quiz_window,
            text=""
        )
        progress_label.pack(pady=5)

        question_label = tk.Label(
            quiz_window,
            text="",
            wraplength=450,
            font=("Arial", 12)
        )
        question_label.pack(pady=25)

        answer_entry = tk.Entry(
            quiz_window,
            width=30,
            font=("Arial", 12)
        )
        answer_entry.pack(pady=10)

        feedback_label = tk.Label(
            quiz_window,
            text="",
            font=("Arial", 12)
        )
        feedback_label.pack(pady=15)

        def show_question():
            nonlocal current_question, current_word

            current_word, definition = quiz.generate_question(quiz_words)
            current_question += 1

            progress_label.config(
                text=f"Question {current_question} of {question_count}"
            )

            question_label.config(
                text=f"Definition:\n{definition}"
            )

            answer_entry.delete(0, tk.END)
            answer_entry.config(state="normal")

            feedback_label.config(text="")

            submit_button.config(state="normal")
            next_button.config(state="disabled")

        def submit_answer():
            answer = answer_entry.get().strip()

            if not answer:
                feedback_label.config(
                    text="Please enter an answer."
                )
                return

            if quiz.check_answer(answer, current_word):
                feedback_label.config(
                    text="Correct!"
                )
            else:
                feedback_label.config(
                    text=f"Wrong. The correct answer is: {current_word}"
                )

            answer_entry.config(state="disabled")
            submit_button.config(state="disabled")
            next_button.config(state="normal")

            # Changes button text after the final question
            if current_question == question_count:
                next_button.config(text="Finish Quiz")

        def next_question():
            if current_question >= question_count:
                question_label.config(
                    text="Quiz Finished!"
                )

                progress_label.config(
                    text=f"Correct: {quiz.correct}    Wrong: {quiz.wrong}"
                )

                feedback_label.config(text="")

                answer_entry.pack_forget()
                submit_button.pack_forget()
                next_button.pack_forget()

                return

            show_question()

        submit_button = tk.Button(
            quiz_window,
            text="Submit Answer",
            width=20,
            command=submit_answer
        )
        submit_button.pack(pady=10)

        next_button = tk.Button(
            quiz_window,
            text="Next Question",
            width=20,
            command=next_question,
            state="disabled"
        )
        next_button.pack(pady=10)

        close_button = tk.Button(
        quiz_window,
        text="Close Quiz",
        width=20,
        command=quiz_window.destroy
    )
        close_button.pack(pady=10)

        quiz_window.geometry("550x500")

        # Displays the first question
        show_question()

    def run(self):  # Starts the GUI
        self.root.mainloop()


if __name__ == "__main__":
    app = VocabularyGUI()
    app.run()