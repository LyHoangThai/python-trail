# Lesson 40: Shortest path to the park
# Read README.md, then edit this file.
# Save and run: Trail: Turn in assignment

from collections import deque
graph = {"home": ["shop"], "shop": ["park"], "park": []}
start = "home"
goal = "park"
# Explore in queue order

