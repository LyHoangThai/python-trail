# Assignment grading checklist

The current worker checks expected output plus the requirements below. Selected exercises are rerun with changed variables, boundaries or function calls to check that the idea works beyond the example. Basic printing lessons use direct output checks because displaying the specified message is their learning objective.

Run code executes Python without awarding completion. Turn in assignment saves a source snapshot and grades it. Historical records are preserved; re-submit an older answer to apply the latest checks. These checks guide learning; they are not proof of mastery or a comprehensive adversarial code verifier.

PLC exercises use a separate Boolean simulator and check all four SW1/SW2 combinations. ST exercises also check the language construct named in the mission. See PLC.md for the supported subset.

| Lesson | Path | What is checked |
| --- | --- | --- |
| 01 · Hello, explorer! | beginner | Display the required message with print(). |
| 02 · A tiny postcard | beginner | Display both lines in the required order. |
| 03 · Pocket calculator | beginner | Calculate the answer with multiplication, rather than printing 56 directly. |
| 04 · Secret notes | beginner | Include a real Python comment and print the message. |
| 05 · Launch countdown | beginner | Print the launch sequence in order. |
| 06 · Name your explorer | beginner | Store Pip in name and print the variable. The printed value must follow changes to name. |
| 07 · Treasure pouch | beginner | Start coins at 10, add 5, and print the updated variable. |
| 08 · Say it your way | beginner | Print an f-string that inserts the name variable with {name}. The greeting must work when name changes. |
| 09 · Sharing snacks | beginner | Calculate shares with // and leftovers with %. Use the snacks and friends variables. |
| 10 · Explorer ID | beginner | Use name and level in the printed character card. Both values must update when the variables change. |
| 11 · The forest gate | beginner | Use an if condition based on coins. Open the gate only for 10 or more coins. |
| 12 · Rain or shine | beginner | Use if / else based on raining. Handle both rainy and dry weather. |
| 13 · Three secret doors | beginner | Use if / elif with the door variable. Keep the door 1 and door 2 messages working. |
| 14 · Both keys | beginner | Use and to require both has_map and has_key. |
| 15 · Treasure judge | beginner | Use if / elif / else for Gold, Silver and Bronze. Check boundaries at 50 and 80 as well as other scores. |
| 16 · Echo meadow | beginner | Print the greeting inside a for loop. |
| 17 · Stepping stones | beginner | Print each number from a for loop. |
| 18 · Backpack inventory | beginner | Loop through the backpack list and print its actual items. |
| 19 · A reusable spell | beginner | Define cheer() with its print instruction, then call it twice. |
| 20 · The final campfire | beginner | Define welcome(name) and use its parameter in the greeting. Call welcome from a loop over explorers. |
| 21 · A character dictionary | beginner | Create the hero dictionary and read its name and level keys. |
| 22 · Level up | beginner | Start hero with level 1, update its level entry, and print that entry. |
| 23 · A missing key | beginner | Use hero.get("pet", "No pet yet") in the output. Return a pet value if one is present. |
| 24 · Inventory report | beginner | Loop through bag.items() and print each key and value. |
| 25 · Your explorer registry | beginner | Define introduce(hero), read its dictionary values, and call it from a loop over heroes. |
| 26 · The doubling machine | intermediate | Define and call double(number). Return a calculated value; it must work for other numbers too. |
| 27 · Rocket, keep counting! | intermediate | Use a while loop with a changing count. Start at the given count and stop at zero. |
| 28 · Tidy the name tag | intermediate | Use both strip() and title() in the text you print. Work with the label variable. |
| 29 · Pack one more snack | intermediate | Use append() to add snack to backpack. Loop over the updated backpack. |
| 30 · A tiny treasure grid | intermediate | Use nested list indexing with row and column. |
| 31 · The square factory | advanced | Build the printed list with a list comprehension. Square the actual input values. |
| 32 · A friendly safety net | advanced | Use try / except for the conversion. Handle both numeric text and invalid text. |
| 33 · Meet your pet blueprint | advanced | Define class Pet and its speak method. Create a Pet object and call its speak method. |
| 34 · The echo staircase | advanced | Use a countdown function that calls itself. Stop at zero and handle other starting values. |
| 35 · One snack at a time | advanced | Define and call the snacks generator. Use yield and a for loop. |
| 36 · Find the missing toy | algorithms | Search with a loop and comparison inside find_toy. Handle a missing toy and an empty shelf. |
| 37 · Guess the secret shelf | algorithms | Use a while loop and a middle index calculated with // inside binary_find. Handle targets at both ends and a missing target. |
| 38 · Bubble the marbles | algorithms | Use nested loops, compare neighbors and update marbles. Practice the algorithm without sort() or sorted(). |
| 39 · Count the color votes | algorithms | Loop over votes and maintain dictionary counts. Use get() for a missing count. |
| 40 · Shortest path to the park | algorithms | Explore a graph using a queue, popleft() and a visited set. Return the shortest number of steps or -1 when unreachable. |
| 41 · Stack the plates | data-structures | Use append() and pop() for last-in, first-out behavior. |
| 42 · Wait your turn | data-structures | Build a deque and use append() and popleft(). Serve people in first-in, first-out order. |
| 43 · Collect unique colors | data-structures | Use set() to collect unique values. Count and display the actual unique items. |
| 44 · A branching family tree | data-structures | Read a root node and visit its immediate children. Use dictionary keys and a loop. |
| 45 · A map of friendships | data-structures | Read the selected person’s neighbor list and loop through it. |
| 46 · A switch and a lamp | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 47 · Two keys for the toy box | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 48 · Either doorbell works | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 49 · The opposite-day contact | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 50 · Write a lamp rule | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 51 · Both switches, in words | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 52 · Either switch, in words | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
| 53 · An opposite-day decision | plc | Test all four combinations of SW1 and SW2. Use the contact or Structured Text idea described in the assignment. |
