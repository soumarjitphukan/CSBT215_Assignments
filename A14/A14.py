import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

    def __del__(self):
        print(f"{self.name} is being garbage collected")

gc.disable()

A = Node("A")
B = Node("B")

A.link = B
B.link = A

print("Reference count of A:", sys.getrefcount(A))
print("Reference count of B:", sys.getrefcount(B))

print("\nObjects tracked before deletion:")
for obj in gc.get_objects():
    if isinstance(obj, Node):
        print(obj.name)

del A
del B

print("\nObjects still in memory after del:")
for obj in gc.get_objects():
    if isinstance(obj, Node):
        print(obj.name)

print("\nRunning garbage collector...")
collected = gc.collect()

print("Unreachable objects collected:", collected)

print("\nObjects remaining after gc.collect():")
for obj in gc.get_objects():
    if isinstance(obj, Node):
        print(obj.name)