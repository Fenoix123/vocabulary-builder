from dictionary_client import DictionaryClient
from storage import VocabularyStorage


client = DictionaryClient()
storage = VocabularyStorage()

word_input = input("Enter a word: ").strip()

result = client.search_word(word_input)

if result is None:
    print("Word not found.")

else:
    saved = storage.save_word(result)

    if saved:
        print(f"{result.word} saved successfully.")
    else:
        print(f"{result.word} is already in your vocabulary.")