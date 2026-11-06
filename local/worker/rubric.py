"""Learning requirements and changed-input cases, independent of expected output."""
import ast
import copy
import io
import tokenize
from new_lessons import RULES

CHECKS={
1:['Display the required message with print().'],2:['Display both lines in the required order.'],
3:['Calculate the answer with multiplication, rather than printing 56 directly.'],
4:['Include a real Python comment and print the message.'],5:['Print the launch sequence in order.'],
6:['Store Pip in name and print the variable.','The printed value must follow changes to name.'],
7:['Start coins at 10, add 5, and print the updated variable.'],
8:['Print an f-string that inserts the name variable with {name}.','The greeting must work when name changes.'],
9:['Calculate shares with // and leftovers with %.','Use the snacks and friends variables.'],
10:['Use name and level in the printed character card.','Both values must update when the variables change.'],
11:['Use an if condition based on coins.','Open the gate only for 10 or more coins.'],
12:['Use if / else based on raining.','Handle both rainy and dry weather.'],
13:['Use if / elif with the door variable.','Keep the door 1 and door 2 messages working.'],
14:['Use and to require both has_map and has_key.'],
15:['Use if / elif / else for Gold, Silver and Bronze.','Check boundaries at 50 and 80 as well as other scores.'],
16:['Print the greeting inside a for loop.'],17:['Print each number from a for loop.'],
18:['Loop through the backpack list and print its actual items.'],
19:['Define cheer() with its print instruction, then call it twice.'],
20:['Define welcome(name) and use its parameter in the greeting.','Call welcome from a loop over explorers.'],
21:['Create the hero dictionary and read its name and level keys.'],
22:['Start hero with level 1, update its level entry, and print that entry.'],
23:['Use hero.get("pet", "No pet yet") in the output.','Return a pet value if one is present.'],
24:['Loop through bag.items() and print each key and value.'],
25:['Define introduce(hero), read its dictionary values, and call it from a loop over heroes.']}

def functions(tree):
    return {n.name:n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}

def calls_in(statements,defs):
    """Follow function calls; an unused definition does not satisfy a requirement."""
    roots=[];seen=set()
    class Calls(ast.NodeVisitor):
        def visit_FunctionDef(self,node): pass
        def visit_AsyncFunctionDef(self,node): pass
        def visit_Call(self,node):
            roots.append(node)
            if isinstance(node.func,ast.Name) and node.func.id in defs and node.func.id not in seen:
                seen.add(node.func.id)
                for statement in defs[node.func.id].body:self.visit(statement)
            self.generic_visit(node)
    visitor=Calls()
    for statement in statements:visitor.visit(statement)
    return roots

def output_flow(tree):
    defs=functions(tree);bindings={}
    def bind(target,value):
        for node in ast.walk(target):
            if isinstance(node,ast.Name):bindings.setdefault(node.id,[]).append(value)
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign):
            for target in node.targets:bind(target,node.value)
        elif isinstance(node,ast.AnnAssign) and node.value:bind(node.target,node.value)
        elif isinstance(node,ast.AugAssign):bind(node.target,node.value)
        elif isinstance(node,ast.For):bind(node.target,node.iter)
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in defs:
            for parameter,value in zip(defs[node.func.id].args.args,node.args):bindings.setdefault(parameter.arg,[]).append(value)
    result=set();names=set();seen_functions=set()
    def add(node):
        if node in result:return
        result.add(node)
        if isinstance(node,ast.Name) and node.id not in names:
            names.add(node.id)
            for value in bindings.get(node.id,[]):add(value)
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in defs and node.func.id not in seen_functions:
            seen_functions.add(node.func.id)
            for item in ast.walk(defs[node.func.id]):
                if isinstance(item,ast.Return) and item.value:add(item.value)
        for child in ast.iter_child_nodes(node):add(child)
    printed=[n for n in calls_in(tree.body,defs) if isinstance(n.func,ast.Name) and n.func.id=='print']
    for call in printed:
        for argument in call.args:add(argument)
    return result,printed

def names_in(node):return {n.id for n in ast.walk(node) if isinstance(n,ast.Name)}
def has_output(body,defs):return any(isinstance(n.func,ast.Name) and n.func.id=='print' for n in calls_in(body,defs))
def assigned(tree,name):
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):return node
        if isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name) and node.target.id==name:return node
    return None

def extended_requirement(tree,quest):
    rule=RULES[quest];nodes=list(ast.walk(tree));flow,_=output_flow(tree);defs=functions(tree)
    for name in rule.get('variables',[]):
        if assigned(tree,name) is None:return f'Keep and use the lesson variable {name}.'
    for name in rule.get('defs',[]):
        if name not in defs or not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name for n in nodes):return f'Define and call {name}() as described in the assignment.'
    for kind in rule.get('nodes',[]):
        scope=flow if kind=='ListComp' else nodes
        if not any(isinstance(n,getattr(ast,kind)) for n in scope):return 'Use the '+kind+' technique described in the assignment.'
    for method in rule.get('methods',[]):
        scope=flow if quest==28 else calls_in(tree.body,defs)
        if not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr==method for n in scope):return f'Use .{method}() in your solution.'
    for name in rule.get('calls',[]):
        if not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name for n in nodes):return f'Use {name}() in your solution.'
    for name in rule.get('forbid',[]):
        if any(isinstance(n,ast.Call) and (isinstance(n.func,ast.Name) and n.func.id==name or isinstance(n.func,ast.Attribute) and n.func.attr==name) for n in nodes):return 'Practice the algorithm itself rather than calling sort() or sorted().'
    if rule.get('nested_for') and not any(any(isinstance(inner,ast.For) for statement in n.body for inner in ast.walk(statement)) for n in nodes if isinstance(n,ast.For)):
        return 'Use one for loop inside another for repeated neighbor comparisons.'
    if quest==38 and not any(isinstance(n,ast.Compare) and any(isinstance(v,ast.Subscript) and isinstance(v.slice,ast.BinOp) and isinstance(v.slice.op,ast.Add) and isinstance(v.slice.right,ast.Constant) and v.slice.right.value==1 for v in ast.walk(n)) for n in nodes):
        return 'Compare neighboring positions, such as marbles[j] and marbles[j + 1].'
    if rule.get('recursive'):
        name=rule['recursive']
        if not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name for statement in defs[name].body for n in ast.walk(statement)):
            return f'Call {name}() from inside itself, with a smaller problem and a stopping condition.'
    if quest in (36,37):
        name=rule['defs'][0];body=list(ast.walk(defs[name]))
        loop_type=ast.For if quest==36 else ast.While
        if not any(isinstance(n,loop_type) and any(isinstance(v,ast.Return) for statement in n.body for v in ast.walk(statement)) for n in body):return f'Perform the search inside the loop in {name}(), returning when the target is found.'
    return ''

def requirement(source,quest):
    tree=ast.parse(source);nodes=list(ast.walk(tree));flow,prints=output_flow(tree);defs=functions(tree)
    if quest in RULES:return extended_requirement(tree,quest)
    if not prints:return 'Use print() to display the result of your code.'
    def used(kind):return any(isinstance(n,kind) for n in flow)
    def value_used(name):return any(isinstance(n,ast.Name) and n.id==name for n in flow)
    def variable(name):return assigned(tree,name) is not None and value_used(name)
    def method(name):return any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr==name for n in flow)
    def key_read(key):
        return any(isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and n.slice.value==key or isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='get' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value==key for n in flow)
    if quest==3 and not used(ast.Mult):return 'Calculate the printed answer using multiplication (*), rather than printing 56 directly.'
    if quest==4 and not any(t.type==tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(source).readline)):
        return 'Include a real comment beginning with #. A # inside a string is not a comment.'
    if quest in (6,7,8,9,10,11,12,13,14,15,18,20,21,22,23,24,25):
        required={6:['name'],7:['coins'],8:['name'],9:['snacks','friends'],10:['name','level'],11:['coins'],12:['raining'],13:['door'],14:['has_map','has_key'],15:['score'],18:['backpack'],20:['explorers'],21:['hero'],22:['hero'],23:['hero'],24:['bag'],25:['heroes']}[quest]
        # Control variables need assignment but do not have to appear in print arguments.
        if not all(assigned(tree,name) for name in required):return 'Keep the lesson variables: '+', '.join(required)+'.'
        if quest not in (11,12,13,14,15) and not all(value_used(name) for name in required):
            return 'Use the lesson variables to build the printed result, rather than hardcoding the answer.'
    if quest==7 and not any(isinstance(n,(ast.BinOp,ast.AugAssign)) and isinstance(n.op,ast.Add) for n in nodes):return 'Add 5 to coins before printing the updated value.'
    if quest==8:
        if not any(isinstance(n,ast.JoinedStr) and any(isinstance(v,ast.FormattedValue) and 'name' in names_in(v.value) for v in n.values) for n in flow):
            return 'Print an f-string containing {name}, for example print(f"Hello, {name}!"). A plain string or unused f-string does not meet this lesson.'
    if quest==9 and not all(used(k) for k in (ast.FloorDiv,ast.Mod)):return 'Use // and % to calculate the values you print; unused calculations do not count.'
    if quest in (11,12,13,14,15):
        conditions=[n for n in nodes if isinstance(n,ast.If) and set(required)<=names_in(n.test) and has_output(n.body+n.orelse,defs)]
        if not conditions:return 'Use an if condition based on '+', '.join(required)+' to choose what gets printed.'
        if quest==12 and not any(n.orelse and has_output(n.orelse,defs) for n in conditions):return 'Use an else branch for dry weather.'
        if quest in (13,15) and not any(n.orelse and isinstance(n.orelse[0],ast.If) for n in conditions):return 'Use elif to check the next condition.'
        if quest==15 and not any(n.orelse and not isinstance(n.orelse[0],ast.If) and has_output(n.orelse,defs) for n in nodes if isinstance(n,ast.If)):return 'Include an else branch for Bronze.'
        if quest==14 and not any(any(isinstance(v,ast.BoolOp) and isinstance(v.op,ast.And) for v in ast.walk(n.test)) for n in conditions):return 'Use and so both the map and the key are required.'
    if quest in (16,17,18,20,24,25):
        loops=[n for n in nodes if isinstance(n,ast.For) and has_output(n.body,defs)]
        if not loops:return 'Put the printing instruction (or your printing function call) inside a for loop.'
        iterable={18:'backpack',20:'explorers',24:'bag',25:'heroes'}.get(quest)
        if iterable and not any(iterable in names_in(n.iter) for n in loops):return f'Loop through {iterable} to produce the output.'
        if quest==24 and not any(isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Attribute) and n.iter.func.attr=='items' for n in loops):return 'Loop through bag.items() to get each key and value together.'
    if quest in (19,20,25):
        name={19:'cheer',20:'welcome',25:'introduce'}[quest];definition=defs.get(name)
        if not definition or not has_output(definition.body,defs):return f'Define {name}() with the printing instruction inside it.'
        callers=[n for n in calls_in(tree.body,defs) if isinstance(n.func,ast.Name) and n.func.id==name]
        if not callers:return f'Call your {name}() function; defining an unused function is not enough.'
        if quest!=19:
            if not definition.args.args:return f'Give {name}() its lesson parameter and use it in the message.'
            if not value_used(definition.args.args[0].arg):return 'Build the message from the function parameter.'
            if not any(any(isinstance(c.func,ast.Name) and c.func.id==name for c in calls_in(n.body,defs)) for n in nodes if isinstance(n,ast.For)):
                return f'Call {name}() inside the for loop.'
    if quest in (21,22,23,24,25):
        if not any(isinstance(n,ast.Dict) or isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='dict' for n in flow):return 'Use the lesson dictionary to produce the printed output.'
        if quest in (21,22,25) and not (used(ast.Subscript) or method('get')):return 'Read the values from the dictionary rather than printing hardcoded values.'
        if quest==22:
            initial=assigned(tree,'hero').value
            try:
                value=ast.literal_eval(initial)
            except (ValueError,TypeError):
                try:value={kw.arg:ast.literal_eval(kw.value) for kw in initial.keywords} if isinstance(initial,ast.Call) and isinstance(initial.func,ast.Name) and initial.func.id=='dict' and not initial.args else None
                except (ValueError,TypeError):value=None
            if isinstance(value,dict) and value.get('level')!=1:return 'Start hero with level 1, then update its level entry.'
            if not key_read('level'):return 'Print the updated level entry from the hero dictionary.'
            changes=[n for n in nodes if isinstance(n,(ast.Assign,ast.AugAssign)) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='hero' and isinstance(t.slice,ast.Constant) and t.slice.value=='level' for t in (n.targets if isinstance(n,ast.Assign) else [n.target]))]
            updates=[n for n in nodes if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='hero' and n.func.attr=='update' and (any(kw.arg=='level' for kw in n.keywords) or any(isinstance(arg,ast.Dict) and any(isinstance(key,ast.Constant) and key.value=='level' for key in arg.keys) for arg in n.args))]
            if not changes and not updates:return 'Update hero["level"] (or use hero.update) before printing its level.'
        if quest in (21,25) and not all(key_read(key) for key in ('name','level')):return 'Read both the name and level keys from the lesson dictionary.'
        if quest==23 and not method('get'):return 'Use hero.get("pet", "No pet yet") to produce the printed value.'
    return ''

def variant(tree,values):
    changed=copy.deepcopy(tree)
    for name,value in values.items():
        node=assigned(changed,name)
        if node is None:return None
        node.value=ast.parse(repr(value),mode='eval').body
    return ast.unparse(ast.fix_missing_locations(changed))

def cases(source,quest):
    tree=ast.parse(source)
    if quest in RULES:
        rule=RULES[quest]
        result=[(variant(tree,values),expected,'Try other values for '+', '.join(values)+'. The result must follow the inputs.') for values,expected in rule.get('cases',[])]
        if rule.get('extra_call'):
            result.append((source+'\n'+rule['extra_call']+'\n',rule['extra_output'],'Make the object or generator reusable; use its method or yielded values rather than hardcoding the output.'))
        return result
    specs={
      6:[({'name':'Nova'},'Nova')],7:[({'coins':20},'25')],8:[({'name':'Nova'},'Hello, Nova!'),({'name':'Kai'},'Hello, Kai!')],
      9:[({'snacks':23,'friends':5},'4\n3'),({'snacks':8,'friends':3},'2\n2')],
      10:[({'name':'Nova','level':3},'Explorer: Nova\nLevel: 3')],
      11:[({'coins':9},''),({'coins':10},'Gate open!')],12:[({'raining':True},'Bring a coat')],
      13:[({'door':1},'A sleepy dragon')],14:[({'has_map':False},''),({'has_key':False},'')],
      15:[({'score':s},'Gold' if s>=80 else 'Silver' if s>=50 else 'Bronze') for s in [80,79,65,50,49,20]],
      18:[({'backpack':['compass','water']},'compass\nwater')],
      20:[({'explorers':['Moss','Luna']},'Welcome, Moss!\nWelcome, Luna!')],
      21:[({'hero':{'name':'Nova','level':3}},'Nova\n3')],
      23:[({'hero':{'name':'Pip','pet':'A frog'}},'A frog')],
      24:[({'bag':{'rope':2,'water':4}},'rope: 2\nwater: 4')],
      25:[({'heroes':[{'name':'Moss','level':4},{'name':'Luna','level':7}]},'Moss is level 4\nLuna is level 7')]}
    result=[]
    for values,expected in specs.get(quest,[]):
        code=variant(tree,values)
        result.append((code,expected,'Try changing '+', '.join(values)+'. The output should follow those values.'))
    if quest==3:
        flow,_=output_flow(tree)
        chosen=next((n for n in ast.walk(tree) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mult) and n in flow),None)
        if chosen:
            changed=copy.deepcopy(tree)
            class Multiply(ast.NodeTransformer):
                def visit_BinOp(self,node):
                    if (node.lineno,node.col_offset)==(chosen.lineno,chosen.col_offset):return ast.copy_location(ast.parse('3 * 4',mode='eval').body,node)
                    return self.generic_visit(node)
            changed=Multiply().visit(changed)
            result.append((ast.unparse(ast.fix_missing_locations(changed)),'12','The output must use the multiplication result.'))
    if quest in (16,17):
        changed=copy.deepcopy(tree);defs=functions(changed)
        loop=next((n for n in ast.walk(changed) if isinstance(n,ast.For) and has_output(n.body,defs)),None)
        if loop:
            loop.iter=ast.parse('[0, 1]' if quest==16 else '[2, 3, 4]',mode='eval').body
            result.append((ast.unparse(ast.fix_missing_locations(changed)),'Hello!\nHello!' if quest==16 else '2\n3\n4','Print from the loop, using the current item when the mission asks for it.'))
    if quest in (19,20,25):
        changed=copy.deepcopy(tree);name={19:'cheer',20:'welcome',25:'introduce'}[quest];definition=functions(changed).get(name)
        if definition:
            if quest==19:
                definition.body=ast.parse('print("Keep exploring!")').body
                expected='Keep exploring!\nKeep exploring!'
            else:
                parameter=definition.args.args[0].arg
                expression=f'print("Checked", {parameter})' if quest==20 else f'print("Checked", {parameter}["name"], {parameter}["level"])'
                definition.body=ast.parse(expression).body
                expected='Checked Pip\nChecked Nova\nChecked Ash' if quest==20 else 'Checked Pip 1\nChecked Nova 2'
            result.append((ast.unparse(ast.fix_missing_locations(changed)),expected,f'Generate the output by calling {name}(), rather than duplicating its message outside the function.'))
    return result
