import os
import random

from typing import Tuple


MAX_INFER_LENGTH = os.environ.get("MAX_INFER_LENGTH", 100)


try:
    from .DankEncoder import DankEncoder
except ImportError as ex:
    print(f'dank module failed to load: {ex}')


def infer_size_bounds(regex: str) -> Tuple[int, int]:
    i, low, high = 1, 0, 0
    t = DankEncoder(regex, MAX_INFER_LENGTH)
    while i < MAX_INFER_LENGTH:
        words = t.num_words(i, i)
        if words != 0:
            low = i
            break
        i += 1
    i = MAX_INFER_LENGTH
    while i >= low:
        words = t.num_words(i, i)
        if words != 0:
            high = i
            break
        i -= 1
    return (low, high)


class DankGenerator:
    def __init__(self, regex: str, size: Tuple[int, int] = (0,0), number: int = 0, random: bool = False):
        self.size = infer_size_bounds(regex) if size == (0,0) else size
        self.encoder = DankEncoder(regex, self.size[1])
        self.words = self.encoder.num_words(self.size[0], self.size[1])
        self.number = number if number else self.words
        self.random = random
        self.count = 0
        self.encoder.set_fixed_slice(size[0])
        self.current_size = size[0]
        self.current_words = self.encoder.num_words(size[0], size[0])

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.number:
            raise StopIteration
        self.count += 1
        if self.random:
            l = random.randint(self.size[0], self.size[1])
            self.encoder.set_fixed_slice(l)
            self.words = self.encoder.num_words(l, l)
            while self.words == 0:
                l = random.randint(self.size[0], self.size[1])
                self.encoder.set_fixed_slice(l)
                self.words = self.encoder.num_words(l, l)
            r = random.randint(0, self.words)
            return self.encoder.unrank(r)
        else:
            while self.current_words == 0:
                self.current_size += 1
                self.current_words = self.encoder.num_words(self.current_size, self.current_size)
                self.encoder.set_fixed_slice(self.current_size)
            self.current_words -= 1
            return self.encoder.unrank(self.current_words)
