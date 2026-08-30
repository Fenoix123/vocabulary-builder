class Word: # Vocabulary word information
    def __init__(self, word, definition, phonetic="", examples=None, synonyms=None, antonyms=None) -> None:
        self.word =word
        self.definition = definition
        self.phonetic = phonetic
        self.examples = examples or []
        self.synonyms = synonyms or []
        self.antonyms = antonyms or []

    def to_dict(self): # Convert Word Object for storage
        return{"word": self.word,"definition": self.definition, "phonetic": self.phonetic, "examples": self.examples, "synonyms": self.synonyms, "antonyms": self.antonyms}