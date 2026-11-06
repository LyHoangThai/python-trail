"""Kid-friendly next steps and declarative grading cases for the extra tracks."""
LESSONS=[]
RULES={}
def add(id,track,title,topic,explain,mission,hint,starter,solution,expected,checks,rule):
    LESSONS.append(dict(id=id,track=track,title=title,topic=topic,chapter=1,explain=explain,mission=mission,hint=hint,starter=starter,solution=solution,expected=expected,checks=checks))
    RULES[id]=rule

add(26,'intermediate','The doubling machine','Return values',
'Imagine a little machine: a number goes in, and its double comes out. <code>return</code> sends a value back to the code that called your function. Printing shows a value; returning lets other code use it.',
'Define double(number) to return twice its number. Print double(number) with number set to 6.',
'Inside double, return number * 2. Outside, print(double(number)).',
'number = 6\n\ndef double(number):\n    pass\n\n# Print what the machine gives back\n',
'number = 6\n\ndef double(number):\n    return number * 2\n\nprint(double(number))','12',
['Define and call double(number).','Return a calculated value; it must work for other numbers too.'],
{'defs':['double'],'nodes':['Return'],'variables':['number'],'cases':[({'number':9},'18')]})

add(27,'intermediate','Rocket, keep counting!','While loops',
'A <code>while</code> loop is like saying “keep going while this is true.” Change the counter each turn, or your rocket will count forever! A for loop visits items; a while loop watches a condition.',
'Start count at 3. Use a while loop to print 3, 2, 1 on separate lines, then print Liftoff!.',
'Use while count > 0:, print count, and subtract 1 inside the loop.',
'count = 3\n# Count down while count is bigger than zero\n',
'count = 3\nwhile count > 0:\n    print(count)\n    count -= 1\nprint("Liftoff!")','3\n2\n1\nLiftoff!',
['Use a while loop with a changing count.','Start at the given count and stop at zero.'],
{'nodes':['While'],'variables':['count'],'cases':[({'count':2},'2\n1\nLiftoff!')]})

add(28,'intermediate','Tidy the name tag','String methods',
'A name tag can arrive with messy spaces and lowercase letters. <code>text.strip()</code> trims its edges, and <code>text.title()</code> gives words capital initials. Each method returns new text; it does not change the old string.',
'Use strip() and title() on label, then print the tidy name tag: Captain Nova.',
'Try label.strip().title(), then print the result.',
'label = "  captain nova  "\n# Tidy this name tag\n',
'label = "  captain nova  "\nprint(label.strip().title())','Captain Nova',
['Use both strip() and title() in the text you print.','Work with the label variable.'],
{'methods':['strip','title'],'variables':['label'],'cases':[({'label':'  little ROBOT  '},'Little Robot')]})

add(29,'intermediate','Pack one more snack','Growing lists',
'Your list is a backpack. <code>backpack.append(item)</code> puts one new item at the end. It changes the list and returns None, so print the backpack afterward rather than printing append() itself.',
'Append snack to backpack, then print every item on its own line. Start with map and add apple.',
'Call backpack.append(snack), then loop through backpack.',
'backpack = ["map"]\nsnack = "apple"\n',
'backpack = ["map"]\nsnack = "apple"\nbackpack.append(snack)\nfor item in backpack:\n    print(item)','map\napple',
['Use append() to add snack to backpack.','Loop over the updated backpack.'],
{'nodes':['For'],'methods':['append'],'variables':['backpack','snack'],'cases':[({'backpack':['torch'],'snack':'pear'},'torch\npear')]})

add(30,'intermediate','A tiny treasure grid','Nested lists',
'A list can hold other lists, like rows in a treasure map. <code>grid[row][column]</code> first chooses a row, then an item in that row. Counting starts at zero.',
'Print grid[row][column]. With row 1 and column 0, the treasure is key.',
'Use two pairs of square brackets: grid[row][column].',
'grid = [["rock", "coin"], ["key", "gem"]]\nrow = 1\ncolumn = 0\n',
'grid = [["rock", "coin"], ["key", "gem"]]\nrow = 1\ncolumn = 0\nprint(grid[row][column])','key',
['Use nested list indexing with row and column.'],
{'nodes':['Subscript'],'variables':['grid','row','column'],'cases':[({'row':0,'column':1},'coin'),({'grid':[['a','b'],['c','d']],'row':1,'column':1},'d')]})

add(31,'advanced','The square factory','Comprehensions',
'A list comprehension is a compact factory: take each item, transform it, and collect the results. <code>[x * 2 for x in numbers]</code> makes a new list without changing numbers.',
'Use a list comprehension to square every item in numbers. Print the new list.',
'A square is a number multiplied by itself: [n * n for n in numbers].',
'numbers = [1, 2, 3, 4]\n',
'numbers = [1, 2, 3, 4]\nsquares = [n * n for n in numbers]\nprint(squares)','[1, 4, 9, 16]',
['Build the printed list with a list comprehension.','Square the actual input values.'],
{'nodes':['ListComp'],'variables':['numbers'],'cases':[({'numbers':[2,5]},'[4, 25]')]})

add(32,'advanced','A friendly safety net','Exceptions',
'Sometimes a program gets an unexpected value. <code>try</code> attempts a job; <code>except ValueError</code> catches a number-conversion problem. A safety net helps the program explain what happened.',
'Try converting text to an integer and print it. If conversion raises ValueError, print Please use digits. Start with text set to seven.',
'Put int(text) in try, then catch ValueError and print the friendly message.',
'text = "seven"\n# Try the conversion and catch ValueError\n',
'text = "seven"\ntry:\n    print(int(text))\nexcept ValueError:\n    print("Please use digits")','Please use digits',
['Use try / except for the conversion.','Handle both numeric text and invalid text.'],
{'nodes':['Try'],'calls':['int'],'variables':['text'],'cases':[({'text':'12'},'12'),({'text':'oops'},'Please use digits')]})

add(33,'advanced','Meet your pet blueprint','Classes',
'A class is a blueprint. An object is one thing made from it. A method is a function on that object; <code>self</code> means “this particular pet.” Calling pet.speak() asks that pet to do its job.',
'Define class Pet with speak(self) that prints Hi, friend!. Make pet = Pet() and call pet.speak().',
'Indent speak inside class Pet. Then create the pet outside the class.',
'class Pet:\n    def speak(self):\n        pass\n\n# Make and greet your pet\n',
'class Pet:\n    def speak(self):\n        print("Hi, friend!")\n\npet = Pet()\npet.speak()','Hi, friend!',
['Define class Pet and its speak method.','Create a Pet object and call its speak method.'],
{'nodes':['ClassDef'],'calls':['Pet'],'methods':['speak'],'extra_call':'pet.speak()','extra_output':'Hi, friend!\nHi, friend!'})

add(34,'advanced','The echo staircase','Recursion',
'A recursive function calls itself to solve a smaller version of a problem. Imagine stepping down stairs: each call takes one step. The stopping rule is the ground floor—without it, you never stop.',
'Define countdown(n). If n is greater than 0, print n and call countdown(n - 1). Call countdown(start) with start set to 3.',
'Put the recursive call inside if n > 0:. When n is 0, do nothing.',
'start = 3\n\ndef countdown(n):\n    pass\n\ncountdown(start)\n',
'start = 3\n\ndef countdown(n):\n    if n > 0:\n        print(n)\n        countdown(n - 1)\n\ncountdown(start)','3\n2\n1',
['Use a countdown function that calls itself.','Stop at zero and handle other starting values.'],
{'defs':['countdown'],'nodes':['If'],'recursive':'countdown','variables':['start'],'cases':[({'start':2},'2\n1'),({'start':0},'')]})

add(35,'advanced','One snack at a time','Generators',
'A generator is a snack dispenser: it gives one item, pauses, then gives the next when asked. <code>yield</code> hands out an item without finishing the whole function. A for loop can collect its items.',
'Define snacks() to yield apple, then pear. Loop over snacks() and print each item.',
'Use two yield lines inside snacks(), then for item in snacks(): print(item).',
'def snacks():\n    pass\n\n# Collect and print each yielded snack\n',
'def snacks():\n    yield "apple"\n    yield "pear"\n\nfor item in snacks():\n    print(item)','apple\npear',
['Define and call the snacks generator.','Use yield and a for loop.'],
{'defs':['snacks'],'nodes':['Yield','For'],'extra_call':'print(list(snacks()))','extra_output':"apple\npear\n['apple', 'pear']"})

add(36,'algorithms','Find the missing toy','Linear search',
'An algorithm is a set of steps for a job. Linear search checks items one by one, like looking through a toy shelf. It works even when the items are not sorted.',
'Define find_toy(toys, target). Loop through toys; return True when an item matches target, otherwise return False after the loop. Print its result.',
'Keep return False outside the loop so you check the whole shelf.',
'toys = ["ball", "robot", "kite"]\ntarget = "robot"\n\ndef find_toy(toys, target):\n    pass\n\nprint(find_toy(toys, target))\n',
'toys = ["ball", "robot", "kite"]\ntarget = "robot"\n\ndef find_toy(toys, target):\n    for toy in toys:\n        if toy == target:\n            return True\n    return False\n\nprint(find_toy(toys, target))','True',
['Search with a loop and comparison inside find_toy.','Handle a missing toy and an empty shelf.'],
{'defs':['find_toy'],'nodes':['For','If','Return'],'variables':['toys','target'],'cases':[({'target':'car'},'False'),({'toys':[]},'False'),({'target':'kite'},'True')]})

add(37,'algorithms','Guess the secret shelf','Binary search',
'On a sorted shelf, check the middle first. If your target is smaller, keep only the left half; otherwise keep the right half. Binary search keeps cutting the job in half. It needs sorted input.',
'Define binary_find(numbers, target) with low/high bounds, a while loop and a middle index. Return True if target is found, otherwise False. Print the result.',
'Start low = 0 and high = len(numbers) - 1. While low <= high, use middle = (low + high) // 2 and move a bound past the middle.',
'numbers = [2, 4, 6, 8, 10]\ntarget = 8\n\ndef binary_find(numbers, target):\n    pass\n\nprint(binary_find(numbers, target))\n',
'numbers = [2, 4, 6, 8, 10]\ntarget = 8\n\ndef binary_find(numbers, target):\n    low = 0\n    high = len(numbers) - 1\n    while low <= high:\n        middle = (low + high) // 2\n        if numbers[middle] == target:\n            return True\n        elif numbers[middle] < target:\n            low = middle + 1\n        else:\n            high = middle - 1\n    return False\n\nprint(binary_find(numbers, target))','True',
['Use a while loop and a middle index calculated with // inside binary_find.','Handle targets at both ends and a missing target.'],
{'defs':['binary_find'],'nodes':['While','FloorDiv','Subscript'],'variables':['numbers','target'],'cases':[({'target':2},'True'),({'target':10},'True'),({'target':7},'False'),({'numbers':[]},'False')]})

add(38,'algorithms','Bubble the marbles','Bubble sort',
'Compare neighboring marbles. If the left one is bigger, swap them. Repeat, and big marbles bubble toward the end. Bubble sort is easy to see but makes many comparisons on long lists.',
'Use nested for loops to bubble-sort marbles in ascending order, swapping neighboring values when needed. Print marbles. Do not use sort() or sorted().',
'For each pass, compare marbles[j] and marbles[j + 1]. Swap them with a, b = b, a.',
'marbles = [3, 1, 2]\n# Compare neighbors over repeated passes\n',
'marbles = [3, 1, 2]\nfor turn in range(len(marbles)):\n    for j in range(len(marbles) - 1):\n        if marbles[j] > marbles[j + 1]:\n            marbles[j], marbles[j + 1] = marbles[j + 1], marbles[j]\nprint(marbles)','[1, 2, 3]',
['Use nested loops, compare neighbors and update marbles.','Practice the algorithm without sort() or sorted().'],
{'nodes':['For','If','Subscript'],'nested_for':True,'forbid':['sort','sorted'],'variables':['marbles'],'cases':[({'marbles':[4,2,4,1]},'[1, 2, 4, 4]'),({'marbles':[]},'[]')]})

add(39,'algorithms','Count the color votes','Frequency counting',
'Give each color a tally. A dictionary stores a color as the key and its count as the value. Each time that color appears, add one to its tally. This is frequency counting.',
'Build counts by looping over votes and increasing counts[color] with get(color, 0) + 1. Print the number of red votes.',
'Start counts = {}. For each color, set counts[color] = counts.get(color, 0) + 1.',
'votes = ["red", "blue", "red"]\ncounts = {}\n',
'votes = ["red", "blue", "red"]\ncounts = {}\nfor color in votes:\n    counts[color] = counts.get(color, 0) + 1\nprint(counts.get("red", 0))','2',
['Loop over votes and maintain dictionary counts.','Use get() for a missing count.'],
{'nodes':['For','Dict'],'methods':['get'],'variables':['votes','counts'],'cases':[({'votes':['red','red','red']},'3'),({'votes':['blue']},'0')]})

add(40,'algorithms','Shortest path to the park','Breadth-first search',
'Imagine a map of paths between places. Breadth-first search checks places one step away, then two steps away. A queue keeps that order. On this unweighted map, the first time you reach the park gives the fewest steps.',
'Use a deque queue of (place, steps), a visited set and a while loop to find the shortest route from start to goal. Print the step count, or -1 if there is no route.',
'Begin with queue = deque([(start, 0)]). Pop from the left, check the goal, then add unvisited neighbors with one more step.',
'from collections import deque\ngraph = {"home": ["shop"], "shop": ["park"], "park": []}\nstart = "home"\ngoal = "park"\n# Explore in queue order\n',
'from collections import deque\ngraph = {"home": ["shop"], "shop": ["park"], "park": []}\nstart = "home"\ngoal = "park"\nqueue = deque([(start, 0)])\nvisited = {start}\nanswer = -1\nwhile queue:\n    place, steps = queue.popleft()\n    if place == goal:\n        answer = steps\n        break\n    for neighbor in graph.get(place, []):\n        if neighbor not in visited:\n            visited.add(neighbor)\n            queue.append((neighbor, steps + 1))\nprint(answer)','2',
['Explore a graph using a queue, popleft() and a visited set.','Return the shortest number of steps or -1 when unreachable.'],
{'nodes':['While','For'],'calls':['deque'],'methods':['popleft','append','add'],'variables':['graph','start','goal'],'cases':[({'start':'park'},'0'),({'graph':{'home':['park','shop'],'shop':['park'],'park':[]}},'1'),({'graph':{'home':[],'park':[]}},'-1'),({'graph':{'home':['shop'],'shop':['home'],'park':[]}},'-1')]})

add(41,'data-structures','Stack the plates','Stacks',
'A stack is like a pile of plates: the last plate added is the first one removed. A Python list can be a stack. append() puts an item on top; pop() takes the top item off.',
'Append plate to stack, pop the top plate and print it, then print the remaining stack.',
'Use stack.append(plate), then print(stack.pop()), then print(stack).',
'stack = ["blue"]\nplate = "red"\n',
'stack = ["blue"]\nplate = "red"\nstack.append(plate)\nprint(stack.pop())\nprint(stack)','red\n[\'blue\']',
['Use append() and pop() for last-in, first-out behavior.'],
{'methods':['append','pop'],'variables':['stack','plate'],'cases':[({'stack':['green'],'plate':'yellow'},"yellow\n['green']")]})

add(42,'data-structures','Wait your turn','Queues',
'A queue is a waiting line: the first person in is served first. collections.deque is a handy Python queue. append() joins the back; popleft() serves the front.',
'Create queue = deque(people), append newcomer, then print each person as you serve the queue with popleft() in a while loop.',
'Import deque from collections. While queue is not empty, print(queue.popleft()).',
'from collections import deque\npeople = ["Ari", "Bo"]\nnewcomer = "Cy"\n',
'from collections import deque\npeople = ["Ari", "Bo"]\nnewcomer = "Cy"\nqueue = deque(people)\nqueue.append(newcomer)\nwhile queue:\n    print(queue.popleft())','Ari\nBo\nCy',
['Build a deque and use append() and popleft().','Serve people in first-in, first-out order.'],
{'nodes':['While'],'calls':['deque'],'methods':['append','popleft'],'variables':['people','newcomer'],'cases':[({'people':['Dee'],'newcomer':'Eli'},'Dee\nEli')]})

add(43,'data-structures','Collect unique colors','Sets',
'A set is a collection of unique items, like stickers without duplicates. set(colors) removes repeated values. Sets have no display order, so use sorted() when you want a predictable list to show.',
'Make unique = set(colors). Print its size with len(), then print sorted(unique).',
'Use len(unique) for the count and sorted(unique) for a stable display.',
'colors = ["red", "blue", "red"]\n',
'colors = ["red", "blue", "red"]\nunique = set(colors)\nprint(len(unique))\nprint(sorted(unique))',"2\n['blue', 'red']",
['Use set() to collect unique values.','Count and display the actual unique items.'],
{'calls':['set','len','sorted'],'variables':['colors'],'cases':[({'colors':['green','green','yellow']},"2\n['green', 'yellow']")]})

add(44,'data-structures','A branching family tree','Trees',
'A tree branches from a root into children. This tiny tree uses dictionaries: each node has a name and a children list. A for loop can visit the root’s immediate children.',
'Print tree["name"], then loop through tree["children"] and print each child’s name.',
'Use for child in tree["children"]: and print(child["name"]).',
'tree = {"name": "Oak", "children": [{"name": "Leaf A"}, {"name": "Leaf B"}]}\n',
'tree = {"name": "Oak", "children": [{"name": "Leaf A"}, {"name": "Leaf B"}]}\nprint(tree["name"])\nfor child in tree["children"]:\n    print(child["name"])','Oak\nLeaf A\nLeaf B',
['Read a root node and visit its immediate children.','Use dictionary keys and a loop.'],
{'nodes':['For','Subscript'],'variables':['tree'],'cases':[({'tree':{'name':'Pine','children':[{'name':'Cone'}]}},'Pine\nCone')]})

add(45,'data-structures','A map of friendships','Graphs',
'A graph stores things and their connections. In an adjacency list, each dictionary key is a person and its list contains their friends. Unlike a tree, connections can circle back.',
'Loop through graph[person] and print each friend. Start with person Ari, whose friends are Bo and Cy.',
'Use for friend in graph[person]: print(friend).',
'graph = {"Ari": ["Bo", "Cy"], "Bo": ["Ari"], "Cy": ["Ari"]}\nperson = "Ari"\n',
'graph = {"Ari": ["Bo", "Cy"], "Bo": ["Ari"], "Cy": ["Ari"]}\nperson = "Ari"\nfor friend in graph[person]:\n    print(friend)','Bo\nCy',
['Read the selected person’s neighbor list and loop through it.'],
{'nodes':['For','Subscript'],'variables':['graph','person'],'cases':[({'person':'Bo'},'Ari'),({'graph':{'Ari':['Dee']}},'Dee')]})
