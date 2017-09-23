from singletons.database import Database
from utils.singleton import singleton


@singleton
class WordsCache:
    def __init__(self):
        self._words = []
        self._index = 0

    def add(self, item):
        if item not in self._words:
            self._words.append(item)

    def remove(self, item):
        if item in self._words:
            self._words.remove(item)

    async def reload(self):
        self._words = []
        words = await Database().fetch_all("SELECT word FROM banned_words WHERE 1")
        for word in words:
            self.add(word["word"])

    def __contains__(self, item):
        return item in self._words

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            item = self._words[self._index]
        except IndexError:
            raise StopIteration()
        self._index += 1
        return item
