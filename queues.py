# Building a Queue Data Type

from collections import deque

class Queue:
    def __init__(self, *elements):
        self._elements = deque(elements)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()

# Testing FIFO queue

fifo = Queue("1st", "2nd", "3rd")

print(len(fifo))

for element in fifo:
    print(element)

print(len(fifo))
