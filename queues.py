# BUILDING QUEUE DATA TYPE

from collections import deque
from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from typing import Any

class IterableMixin:
    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

class Queue(IterableMixin):
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



# TESTING FIFO QUEUE

# fifo = Queue("1st", "2nd", "3rd")

# print(len(fifo))

# for element in fifo:
#     print(element)

# print(len(fifo))



# INSTANTIATING STACK CLASS THROUGH INHERITANCE

class Stack(Queue):
    def dequeue(self):
        return self._elements.pop()




# TESTING LIFO STACK

# lifo = Stack("1st", "2nd", "3rd")
# for element in lifo:
#     print(element)



# USING LISTS AS RUDIMENTARY STACKS

# lifo = []
# lifo.append("1st")
# lifo.append("2nd")
# lifo.append("3rd")

# print(lifo.pop())
# print(lifo.pop())
# print(lifo.pop())



# PRIORITY QUEUES USING HEAPS

# from heapq import heappush

# fruits = []
# heappush(fruits, "orange")
# heappush(fruits, "apple")
# heappush(fruits, "banana")

# print(fruits)



# POPPING HEAP ELEMENT

# from heapq import heappop

# print(heappop(fruits))
# print(fruits)



# PYTHON TUPLE COMPARISON

# person1 = ("John", "Brown", 42)
# person2 = ("John", "Doe", 42)
# person3 = ("John", "Doe", 24)

# print(person1 < person2)
# print(person2 < person3)



# BUILDING A PRIORITY QUEUE DATA TYPE

from collections import deque
from heapq import heappop, heappush
from itertools import count

class PriorityQueue(IterableMixin):
    def __init__(self):
        self._elements = []
        self._counter = count()

    def enqueue_with_priority(self, priority, value):
        element = (-priority, next(self._counter), value)
        heappush(self._elements, element)

    def dequeue(self):
        return heappop(self._elements)[-1]



# TESTING PRIORITY QUEUE CLASS

# from queues import PriorityQueue

# CRITICAL = 3
# IMPORTANT = 2
# NEUTRAL = 1

# messages = PriorityQueue()
# messages.enqueue_with_priority(IMPORTANT, "Windshield wipers turned on")
# messages.enqueue_with_priority(NEUTRAL, "Radio station tuned in")
# messages.enqueue_with_priority(CRITICAL, "Brake pedal depressed")
# messages.enqueue_with_priority(IMPORTANT, "Hazard lights turned on")

# print(messages.dequeue())
# print(messages.dequeue())
# print(messages.dequeue())
# print(messages.dequeue())




# HANDLING CORNER CASES IN PRIORITY QUEUE

# from dataclasses import dataclass

# @dataclass
# class Message:
#     event: str

# wipers = Message("Windshield wipers turned on")
# hazard_lights = Message("Hazard lights turned on")

# print(wipers < hazard_lights)


@dataclass(order=True)
class Element:
    priority: float
    count: int
    value: Any

class MutableMinHeap(IterableMixin):
    def __init__(self):
        super().__init__()
        self._elements_by_value = {}
        self._elements = []
        self._counter = count()
    
    def __setitem__(self, unique_value, priority):
        if unique_value in self._elements_by_value:
            self._elements_by_value[unique_value].priority = priority
            heapify(self._elements)
        else:
            element = Element(priority, next(self._counter), unique_value)
            self._elements_by_value[unique_value] = element
            heappush(self._elements, element)

    def __getitem__(self, unique_value):
        return self._elements_by_value[unique_value].priority
    
    def dequeue(self):
        return heappop(self._elements).value