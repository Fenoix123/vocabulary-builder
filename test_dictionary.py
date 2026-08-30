from dictionary_client import DictionaryClient
from storage import VocabularyStorage


client = DictionaryClient()  # Handles dictionary API searches
storage = VocabularyStorage()  # Handles vocabulary storage


word = input("Enter a word: ")

result = client.search_word(word)

if result is None:
    print("Word not found or dictionary service unavailable.")

else:
    saved = storage.save_word(result)

    if saved:
        print(f"{result.word} saved successfully.")
    else:
        print(f"{result.word} is already saved.")