"""Bounded, Boolean-only teaching simulator. No hardware or arbitrary code execution."""
import itertools
import json
import re

class PLCError(ValueError): pass

def ladder(source,inputs):
    try:program=json.loads(source)
    except (ValueError,TypeError):raise PLCError('Build a rung with the visual controls. Its saved diagram must be valid JSON.')
    if not isinstance(program,dict) or program.get('coil') not in ('LAMP',None):raise PLCError('Choose LAMP as the output coil.')
    branches=program.get('branches')
    if not isinstance(branches,list) or len(branches)>4:raise PLCError('Use up to four parallel paths.')
    paths=[]
    for branch in branches:
        if not isinstance(branch,list) or len(branch)>4:raise PLCError('Use up to four series contacts on a path.')
        states=[]
        for contact in branch:
            if not isinstance(contact,dict) or contact.get('input') not in ('SW1','SW2') or contact.get('contact') not in ('NO','NC'):
                raise PLCError('A contact needs SW1 or SW2 and a NO or NC type.')
            value=inputs[contact['input']]
            states.append(value if contact['contact']=='NO' else not value)
        paths.append(all(states))
    return program.get('coil')=='LAMP' and any(paths)

def tokens(source):
    source=re.sub(r'\(\*.*?\*\)',' ',source,flags=re.S)
    source=re.sub(r'//[^\n]*',' ',source)
    pattern=re.compile(r'\s+|:=|[();]|[A-Za-z_][A-Za-z_0-9]*')
    result=[];position=0
    for match in pattern.finditer(source):
        if match.start()!=position:raise PLCError('This beginner lab supports BOOL signals, :=, AND, OR, NOT, parentheses and IF/THEN/ELSE/END_IF.')
        position=match.end()
        if not match.group().isspace():result.append(match.group().upper())
    if position!=len(source):raise PLCError('Check your Structured Text symbols. End assignments with a semicolon.')
    if len(result)>1200:raise PLCError('Keep this practice program short (up to 1200 tokens).')
    return result

class STParser:
    def __init__(self,source):self.parts=tokens(source);self.index=0
    def peek(self):return self.parts[self.index] if self.index<len(self.parts) else None
    def take(self,wanted=None):
        value=self.peek()
        if value is None or wanted and value!=wanted:raise PLCError('Expected '+str(wanted or 'an instruction')+', found '+str(value or 'the end of the program')+'.')
        self.index+=1;return value
    def atom(self,depth=0):
        if depth>16:raise PLCError('Use fewer nested expressions.')
        token=self.take()
        if token=='NOT':return ('not',self.atom(depth+1))
        if token=='(':
            expression=self.expression(depth+1);self.take(')');return expression
        if token in ('TRUE','FALSE'):return ('constant',token=='TRUE')
        if token in ('SW1','SW2','LAMP'):return ('value',token)
        raise PLCError('Use the predefined BOOL names SW1, SW2 and LAMP, or TRUE/FALSE.')
    def expression(self,depth=0):
        def conjunction():
            value=self.atom(depth)
            while self.peek()=='AND':self.take();value=('and',value,self.atom(depth))
            return value
        value=conjunction()
        while self.peek()=='OR':self.take();value=('or',value,conjunction())
        return value
    def statements(self,stops=(),depth=0):
        if depth>12:raise PLCError('Use fewer nested IF blocks.')
        result=[]
        while self.peek() is not None and self.peek() not in stops:
            if self.peek()=='IF':
                self.take('IF');test=self.expression();self.take('THEN')
                yes=self.statements(('ELSE','END_IF'),depth+1);no=[]
                if self.peek()=='ELSE':self.take();no=self.statements(('END_IF',),depth+1)
                self.take('END_IF');self.take(';');result.append(('if',test,yes,no))
            else:
                name=self.take()
                if name!='LAMP':raise PLCError('In this lab, SW1 and SW2 are read-only inputs. Assign only to LAMP; all three names are already BOOLs.')
                self.take(':=');value=self.expression();self.take(';');result.append(('assign',name,value))
        return result

def parse_st(source):
    parser=STParser(source);program=parser.statements()
    if parser.peek() is not None:raise PLCError('Check matching IF and END_IF blocks.')
    return program

def st_scan(program,inputs):
    values={**inputs,'LAMP':False}
    def expression(node):
        kind=node[0]
        if kind=='constant':return node[1]
        if kind=='value':return values[node[1]]
        if kind=='not':return not expression(node[1])
        if kind=='and':return expression(node[1]) and expression(node[2])
        if kind=='or':return expression(node[1]) or expression(node[2])
        raise PLCError('Unknown expression.')
    def execute(statements):
        for node in statements:
            if node[0]=='assign':values[node[1]]=expression(node[2])
            elif node[0]=='if':execute(node[2] if expression(node[1]) else node[3])
    execute(program)
    return values['LAMP']

def read_inputs(raw):
    try:data=json.loads(raw) if raw.strip() else {}
    except (ValueError,AttributeError):raise PLCError('Use the on-screen switches to choose input states.')
    if not isinstance(data,dict) or any(key not in ('SW1','SW2') or type(value)!=bool for key,value in data.items()):raise PLCError('Virtual switch states must be true or false.')
    return {'SW1':data.get('SW1',False),'SW2':data.get('SW2',False)}

def expected(kind,inputs):
    if kind=='single':return inputs['SW1']
    if kind=='and':return inputs['SW1'] and inputs['SW2']
    if kind=='or':return inputs['SW1'] or inputs['SW2']
    if kind=='not':return not inputs['SW1']
    raise PLCError('Unknown lesson logic.')

def grade_plc(job):
    result={'status':'done','output':'','passed':False,'feedback':''}
    try:
        engine=job['engine'];source=job['source']
        program=parse_st(source) if engine=='plc-st' else None
        def scan(inputs):return st_scan(program,inputs) if engine=='plc-st' else ladder(source,inputs)
        if job.get('mode')=='run':
            inputs=read_inputs(job.get('inputs',''));lamp=scan(inputs)
            result.update(passed=True,output='SW1 = '+('ON' if inputs['SW1'] else 'OFF')+'\nSW2 = '+('ON' if inputs['SW2'] else 'OFF')+'\nLAMP = '+('ON' if lamp else 'OFF'),signals={**inputs,'LAMP':lamp},feedback='One simulated scan finished. Turn in to check every switch combination.')
            return result
        if engine=='plc-ladder':scan({'SW1':False,'SW2':False})
        if engine=='plc-ladder' and json.loads(source).get('coil')!='LAMP':
            result['feedback']='Drag the LAMP coil into the output box to connect your rung.'
            return result
        lines=[];incorrect=[]
        for sw1,sw2 in itertools.product((False,True),repeat=2):
            inputs={'SW1':sw1,'SW2':sw2};actual=scan(inputs);wanted=expected(job['plc_logic'],inputs)
            line=f"SW1 {'ON' if sw1 else 'OFF'} | SW2 {'ON' if sw2 else 'OFF'} → LAMP {'ON' if actual else 'OFF'}"
            lines.append(line+(' ✓' if actual==wanted else ' · expected '+('ON' if wanted else 'OFF')))
            if actual!=wanted:incorrect.append(line)
        if incorrect:result.update(output='\n'.join(lines),feedback='Try again: your lamp does not follow the assignment for every switch combination. Check the rows marked expected.');return result
        if engine=='plc-st':
            def contains(node,kind):
                return isinstance(node,(list,tuple)) and (bool(node) and node[0]==kind or any(contains(child,kind) for child in node))
            for requirement in job.get('plc_requires',[]):
                if not contains(program,requirement):result.update(output='\n'.join(lines),feedback='Use '+requirement.upper()+' as described in this lesson.');return result
        result.update(passed=True,output='\n'.join(lines),feedback='Correct! Your logic works for all four switch combinations. The assignment is complete.')
    except (ValueError,TypeError,KeyError,RecursionError) as exc:
        result['feedback']=str(exc) or 'Check your PLC program.'
    return result

def diagram(branches):return json.dumps({'branches':branches,'coil':'LAMP'},indent=2)+'\n'
NO=lambda name:{'input':name,'contact':'NO'}
NC=lambda name:{'input':name,'contact':'NC'}
PLC_LESSONS=[]
def add(id,engine,title,logic,explain,mission,hint,solution,requires=()):
    chapter=1 if engine=='plc-ladder' else 2
    PLC_LESSONS.append(dict(id=id,track='plc',chapter=chapter,title=title,topic='Ladder Logic' if chapter==1 else 'Structured Text',engine=engine,plc_logic=logic,plc_requires=list(requires),explain=explain,mission=mission,hint=hint,starter=json.dumps({'branches':[],'coil':None},indent=2)+'\n' if chapter==1 else '// SW1 and SW2 are BOOL inputs. LAMP is a BOOL output.\nLAMP := FALSE;\n',solution=solution,expected={'single':'SW1 OFF → LAMP OFF\nSW1 ON → LAMP ON','and':'Only both switches ON → LAMP ON','or':'Either switch ON → LAMP ON','not':'SW1 OFF → LAMP ON\nSW1 ON → LAMP OFF'}[logic],checks=['Test all four combinations of SW1 and SW2.','Use the contact or Structured Text idea described in the assignment.']))

add(46,'plc-ladder','A switch and a lamp','single','A PLC reads inputs, follows a program, and updates outputs over and over. In this toy lab, SW1 is an input and LAMP is an output. A normally open contact —| |— passes a true path when its switch is ON. A coil —( )— uses the result.','Build one path with a normally open SW1 contact driving the LAMP coil. Toggle SW1 and watch the lamp.','Drag a normally open SW1 contact to a new path, then drag the LAMP coil to the output box.',diagram([[NO('SW1')]]))
add(47,'plc-ladder','Two keys for the toy box','and','Two contacts in series are like two keys in a row. The path is true only when both contacts pass. This is AND logic.','Put normally open SW1 and SW2 contacts on the same path so the lamp turns on only when both switches are ON.','Choose SW2 in the toolbox. Drag its contact to the gap after SW1. Connect the LAMP coil.',diagram([[NO('SW1'),NO('SW2')]]))
add(48,'plc-ladder','Either doorbell works','or','Parallel paths are like two doors into the same room: either path can let the signal through. This is OR logic.','Build two parallel paths: SW1 on one, SW2 on the other. Either switch should turn on the lamp.','Drag the contacts to separate new parallel paths. Connect the LAMP coil.',diagram([[NO('SW1')],[NO('SW2')]]))
add(49,'plc-ladder','The opposite-day contact','not','A normally closed contact —|/|— checks for FALSE. It passes when its switch is OFF. This is a program instruction checking a bit; it is not a claim about a physical switch’s wiring.','Use a normally closed SW1 contact so the lamp is ON when SW1 is OFF, and OFF when SW1 is ON.','Select SW1, then change the contact type from normally open to normally closed.',diagram([[NC('SW1')]]))
add(50,'plc-st','Write a lamp rule','single','Structured Text is another way to tell a PLC what to do. Use := to assign a value and ; to finish an instruction. Our lab already provides SW1, SW2 and LAMP as BOOL values.','Write a Structured Text assignment that makes LAMP follow SW1.','Try LAMP := SW1;', 'LAMP := SW1;\n')
add(51,'plc-st','Both switches, in words','and','AND in Structured Text is the same idea as two ladder contacts in series. A BOOL value is TRUE or FALSE.','Assign SW1 AND SW2 to LAMP so both switches must be ON.','Write the Boolean expression after := and finish with a semicolon.','LAMP := SW1 AND SW2;\n',('and',))
add(52,'plc-st','Either switch, in words','or','OR is the same idea as parallel ladder paths. You can use it to let either of two toy buttons light the same lamp.','Use OR to make LAMP turn ON when SW1 or SW2 is ON.','Use LAMP := followed by the two switches joined with OR.','LAMP := SW1 OR SW2;\n',('or',))
add(53,'plc-st','An opposite-day decision','not','IF checks a condition, THEN chooses the first instructions, and ELSE chooses the other instructions. END_IF; closes the choice. NOT flips a BOOL value. This looks different from Python: there is no colon, and assignments use :=.','Use IF NOT SW1 THEN / ELSE / END_IF; to turn the lamp ON when SW1 is OFF and OFF when it is ON.','In the THEN branch assign TRUE to LAMP. In ELSE assign FALSE.','IF NOT SW1 THEN\n    LAMP := TRUE;\nELSE\n    LAMP := FALSE;\nEND_IF;\n',('if','not'))
