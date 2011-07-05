
from collections import defaultdict

class PPM(object):
    def __init__(self, length):
        if length <= 0:
            raise ValueError('length must be positive')

        self._length = length
        self._pred = defaultdict(int)
        self.clear_context()

    @property
    def length(self):
        return self._length

    @property
    def context(self):
        return self._context

    def write(self, sym, train=True):
        if train:
            for i in range(len(self._context)):
                seq = self._context[-i:] if i != 0 else ''
                self._pred[seq+sym] += 1

        self._context += sym
        self._context = self._context[-self._length:]

    def predict_order(self, syms):
        s = list(syms)
        for i in range(len(self._context) + 1):
            seq = self._context[-i:] if i != 0 else ''
            s.sort(key=lambda c: self._pred[seq+c], reverse=True)
        return s

    def clear_context(self):
        self._context = ''
