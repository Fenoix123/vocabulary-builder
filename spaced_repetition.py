from datetime import datetime, timedelta

from storage import VocabularyStorage


class SpacedRepetitionManager:
    """Handles simple spaced-repetition scheduling for saved words."""

    def __init__(self, storage=None):
        # Reuse the app's existing vocabulary storage when one is provided.
        self.storage = storage or VocabularyStorage()

    def get_due_words(self):
        """Returns saved words that are due for review today."""
        words = self.storage.load_words()
        due_words = {}
        today = datetime.now().date()

        for word, details in words.items():
            next_review = details.get("next_review")

            # Old saved words will not have a review date yet,
            # so they should be available for their first review.
            if not next_review:
                due_words[word] = details
                continue

            try:
                review_date = datetime.strptime(
                    next_review,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                # If the stored date is invalid, allow the word to be reviewed
                # instead of crashing the application.
                due_words[word] = details
                continue

            if review_date <= today:
                due_words[word] = details

        return due_words

    def review_word(self, word, correct):
        """Updates a word's next review date after a flashcard review."""
        words = self.storage.load_words()

        if word not in words:
            return None

        details = words[word]

        # A new word begins with a one-day interval.
        interval = details.get("interval", 1)

        if correct:
            # Remembered words are reviewed less often.
            interval *= 2
        else:
            # Forgotten words return to a one-day interval.
            interval = 1

        today = datetime.now()
        next_review = today + timedelta(days=interval)

        details["interval"] = interval
        details["last_reviewed"] = today.strftime("%Y-%m-%d")
        details["next_review"] = next_review.strftime("%Y-%m-%d")

        words[word] = details
        self.storage.save_words(words)

        return {
            "interval": interval,
            "last_reviewed": details["last_reviewed"],
            "next_review": details["next_review"]
        }
