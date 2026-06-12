import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

A = Node("A")
B = Node("B")

A.link = B
B.link = A

print("Reference count of A:", sys.getrefcount(A))
print("Reference count of B:", sys.getrefcount(B))

del A
del B

print("Objects deleted from namespace.")

collected = gc.collect()
print("Objects collected by GC:", collected)