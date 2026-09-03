# Vocabulary Builder

A Python-based vocabulary learning application that uses a dictionary API to retrieve word information and stores saved vocabulary locally in a JSON file.

## Current Features

- Search for English words using the Dictionary API
- Retrieve word definitions
- Retrieve phonetic pronunciation where available
- Retrieve examples, synonyms, and antonyms
- Save vocabulary words to a JSON file
- Prevent duplicate words from being saved
- Handle invalid words and API connection errors
- Load previously saved vocabulary words

## Project Structure

```text
vocabulary-builder/
│
├── dictionary_client.py
├── quiz.py
├── models.py
├── flashcard.py
├── storage.py
├── main.py
├── test_dictionary.py
├── vocabulary.json
├── requirements.txt
├── README.md
└── .gitignore