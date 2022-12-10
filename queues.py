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

# fifo = Queue("1st", "2nd", "3rd")

# print(len(fifo))

# for element in fifo:
#     print(element)

# print(len(fifo))

class Stack(Queue):
    def dequeue(self):
        return self._elements.pop()

# Testing LIFO Stack

# lifo = Stack("1st", "2nd", "3rd")
# for element in lifo:
#     print(element)

# Using Lists as rudimentary stack

lifo = []
lifo.append("1st")
lifo.append("2nd")
lifo.append("3rd")

print(lifo.pop())
print(lifo.pop())
print(lifo.pop())