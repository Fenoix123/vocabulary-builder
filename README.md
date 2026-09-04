# Vocabulary Builder

Vocabulary Builder is a Python application for searching, saving, reviewing, and testing English vocabulary.

The application uses an online dictionary API to retrieve word information and provides a graphical user interface built with Tkinter.

## Features

- Search for English words
- View word definitions
- View phonetic information when available
- Save words to a local vocabulary file
- Prevent duplicate words from being saved
- Review saved words using flashcards
- Reveal definitions during flashcard review
- Move through saved flashcards
- Take vocabulary quizzes based on saved words
- Track correct and wrong quiz answers
- Handle empty vocabulary lists without crashing
- Graphical User Interface built with Tkinter
- Remember and forget saved wors

## Project Structure

```text
vocabulary-builder/
│
├── dictionary_client.py   # Connects to the dictionary API
├── flashcard.py           # Flashcard functionality
├── gui.py                 # Tkinter graphical user interface
├── main.py                # Launches the application
├── models.py              # Word model
├── quiz.py                # Quiz functionality and scoring
├── storage.py             # Saves and loads vocabulary
├── test_dictionary.py     # Dictionary functionality testing
├── vocabulary.json        # Stores saved vocabulary
├── requirements.txt       # External Python dependencies
├── .gitignore             # Files excluded from Git
├── spaced_repetition.py   # Handles Spaced repetition
└── README.md              # Project documentation
```

## Requirements

- Python 3
- `requests`
- Tkinter

The `requests` package can be installed using the provided `requirements.txt` file.

Tkinter is included with most standard Python installations.

## Installation

Clone the repository:

```bash
git clone https://github.com/Fenoix123/vocabulary-builder.git
```

Move into the project directory:

```bash
cd vocabulary-builder
```

Install the required package:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start Vocabulary Builder with:

```bash
python main.py
```

The graphical user interface will open with the following options:

- Search Word
- Flashcards
- Take Quiz
- Exit

## Search and Save

The **Search Word** feature allows the user to enter an English word.

The application retrieves the word from the dictionary service and displays:

- Word
- Definition
- Phonetic information, when available

The searched word can then be saved to `vocabulary.json`.

Duplicate words are not saved again.

## Flashcards

The **Flashcards** feature loads words stored in `vocabulary.json`.

Users can:

- View a saved word
- Reveal its definition
- Move to the next saved word

After reaching the final word, the flashcards cycle back to the beginning.

## Quiz

The **Take Quiz** feature generates questions from saved vocabulary.

A definition is displayed and the user enters the corresponding word.

The quiz:

- Checks the user's answer
- Shows whether the answer is correct or wrong
- Displays the correct answer when necessary
- Avoids repeating words during the same quiz
- Uses a maximum of five questions per quiz
- Displays the final number of correct and wrong answers

If fewer than five words are saved, the quiz uses the available number of words.

## Data Storage

Saved vocabulary is stored locally in:

```text
vocabulary.json
```

The application handles an empty vocabulary file without crashing.

## Dictionary API

Vocabulary Builder uses the Free Dictionary API for word information:

```text
https://dictionaryapi.dev/
```

Internet access is required when searching for new words.

Previously saved words can still be loaded from the local JSON file.

## Technologies Used

- Python
- Tkinter
- Requests
- JSON
- Git
- GitHub

## Running Individual Modules

The complete application should normally be started with:

```bash
python main.py
```

Some modules can also be run independently during development and testing.

## Project Purpose

This project was developed as part of an Advanced Python group project to demonstrate concepts including:

- Object-Oriented Programming
- API integration
- File handling
- Exception handling
- Modular programming
- GUI development
- Version control with Git and GitHub