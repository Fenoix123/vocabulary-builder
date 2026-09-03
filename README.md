# Vocabulary Builder

A Python vocabulary learning application that allows users to search for words, save vocabulary, review flashcards, and take quizzes.

## Features

- Search for English words using an online dictionary API
- Display word definitions and phonetics
- Save vocabulary to a JSON file
- Prevent duplicate saved words
- Review saved words using flashcards
- Reveal definitions during flashcard review
- Move through saved flashcards
- Take vocabulary quizzes
- Track correct and wrong quiz answers
- Graphical User Interface using Tkinter
- Command-line interface available through `main.py`

## Project Structure

```text
vocabulary-builder/
│
├── dictionary_client.py   # Connects to the dictionary API
├── flashcard.py           # Flashcard functionality
├── gui.py                 # Tkinter graphical user interface
├── main.py                # Command-line application integration
├── models.py              # Word model
├── quiz.py                # Quiz functionality
├── storage.py             # Saves and loads vocabulary
├── test_dictionary.py     # Dictionary API testing
├── vocabulary.json        # Stores saved vocabulary
├── requirements.txt       # Required external packages
└── README.md              # Project documentation