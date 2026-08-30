class Word: # Vocabulary word information
    def __init__(self, word, definition, phonetic="", examples=None, synonyms=None, antonyms=None) -> None:
        self.word =word
        self.definition = definition
        self.phonetic = phonetic

       # Use empty lists when no examples, synonyms or antonyms are provided
        self.examples = examples or []
        self.synonyms = synonyms or []
        self.antonyms = antonyms or []

    def to_dict(self): # Converts the Word object into a dictionary for JSON storage
        return{"word": self.word,"definition": self.definition, "phonetic": self.phonetic, "examples": self.examples, "synonyms": self.synonyms, "antonyms": self.antonyms}