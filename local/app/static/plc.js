(()=>{
 const get=id=>document.getElementById(id);let lesson=null,program=null,lastSource=null,scanned={};
 function inputs(){return {SW1:get('plcsw1').checked,SW2:get('plcsw2').checked}}
 function lamp(on){get('plclamp').classList.toggle('on',on);get('plclamp').textContent='● LAMP '+(on?'ON':'OFF')}
 function syncInputs(){const states=inputs();get('inputs').value=JSON.stringify(states);get('plcsw1state').textContent=states.SW1?'ON':'OFF';get('plcsw2state').textContent=states.SW2?'ON':'OFF';if(lesson?.engine==='plc-ladder')draw();else{get('plcscanstatus').textContent='Inputs changed. Run scan to update the lamp.';truthTable()}}
 function changed(){get('editor').value=JSON.stringify(program,null,2)+'\n';get('editor').dispatchEvent(new Event('input'));draw()}
 function closed(contact,states){return contact.contact==='NC'?!states[contact.input]:states[contact.input]}
 function draw(){
  if(!program)return;const states=inputs();get('ladderpaths').replaceChildren();
  let energized=false;
  program.branches.forEach((branch,index)=>{
   const row=document.createElement('section');row.className='ladderpath';
   const pathOn=branch.every(contact=>closed(contact,states));energized||=pathOn;
   const heading=document.createElement('div');heading.className='ladderpathhead';
   const title=document.createElement('b');title.textContent='Path '+(index+1)+(pathOn?' · passing':' · blocked');
   const remove=document.createElement('button');remove.textContent='Remove path';remove.className='darkbutton';remove.onclick=()=>{program.branches.splice(index,1);changed()};heading.append(title,remove);row.append(heading);
   const rail=document.createElement('div');rail.className='ladderrail '+(pathOn?'energized':'');
   if(!branch.length){const note=document.createElement('p');note.textContent='A bare wire always passes. Add a contact to check a switch.';note.className='plclabnote';rail.append(note)}
   branch.forEach((contact,position)=>{
    const card=document.createElement('div');card.className='laddercontact '+(closed(contact,states)?'closed':'');
    const symbol=document.createElement('strong');symbol.textContent=contact.contact==='NC'?'—|/|—':'—| |—';symbol.setAttribute('aria-label',contact.contact==='NC'?'Normally closed contact':'Normally open contact');
    const input=document.createElement('select');input.setAttribute('aria-label',`Path ${index+1} contact ${position+1} input`);
    for(const value of ['SW1','SW2']){const option=document.createElement('option');option.value=value;option.textContent=value;input.append(option)}input.value=contact.input;input.onchange=()=>{contact.input=input.value;changed()};
    const type=document.createElement('select');type.setAttribute('aria-label',`Path ${index+1} contact ${position+1} type`);
    for(const [value,label] of [['NO','Normally open'],['NC','Normally closed']]){const option=document.createElement('option');option.value=value;option.textContent=label;type.append(option)}type.value=contact.contact;type.onchange=()=>{contact.contact=type.value;changed()};
    const remove=document.createElement('button');remove.textContent='Remove contact';remove.className='darkbutton';remove.onclick=()=>{branch.splice(position,1);changed()};
    card.append(symbol,input,type,remove);rail.append(card);
   });
   const coil=document.createElement('div');coil.className='laddercoil '+(pathOn?'on':'');coil.textContent='→ JOIN';rail.append(coil);row.append(rail);
   const add=document.createElement('button');add.className='darkbutton';add.textContent='+ Add series contact';add.disabled=branch.length>=4;add.onclick=()=>{branch.push({input:branch.length?'SW2':'SW1',contact:'NO'});changed()};row.append(add);get('ladderpaths').append(row);
  });
  if(!program.branches.length){const prompt=document.createElement('p');prompt.textContent='No paths yet. Add a path, then try its contact with the switches.';prompt.className='plclabnote';get('ladderpaths').append(prompt)}
  truthTable();get('addladderpath').disabled=program.branches.length>=4;lamp(energized);get('plcscanstatus').textContent='Live preview: green contacts pass the signal. Run scan also checks the diagram in the worker.';
 }
 function truthTable(){
  if(!lesson)return;
  if(lastSource!==get('editor').value){lastSource=get('editor').value;scanned={}}
  get('plctruthrows').replaceChildren();
  for(const sw1 of [false,true])for(const sw2 of [false,true]){
   const key=Number(sw1)+''+Number(sw2),states={SW1:sw1,SW2:sw2};
   const value=lesson.engine==='plc-ladder'&&program?program.branches.some(branch=>branch.every(contact=>closed(contact,states))):scanned[key];
   const row=document.createElement('tr');for(const text of [sw1?'ON':'OFF',sw2?'ON':'OFF',value===undefined?'Not scanned':value?'ON':'OFF']){const cell=document.createElement('td');cell.textContent=text;row.append(cell)}
   const cell=document.createElement('td'),button=document.createElement('button');button.className='darkbutton';button.textContent=lesson.engine==='plc-ladder'?'Set switches':'Run case';button.setAttribute('aria-label',`Test SW1 ${sw1?'ON':'OFF'}, SW2 ${sw2?'ON':'OFF'}`);button.onclick=()=>{get('plcsw1').checked=sw1;get('plcsw2').checked=sw2;syncInputs();if(lesson.engine==='plc-st')get('run').click()};cell.append(button);row.append(cell);get('plctruthrows').append(row);
  }
 }
 function refresh(){if(lesson?.engine!=='plc-ladder')return;try{program=JSON.parse(get('editor').value);if(!program||program.coil!=='LAMP'||!Array.isArray(program.branches))throw Error();draw()}catch{get('ladderpaths').textContent='This saved diagram cannot be opened. Use Reset to starter to build it again.';program=null}}
 get('addladderpath').onclick=()=>{if(program&&program.branches.length<4){program.branches.push([{input:program.branches.length?'SW2':'SW1',contact:'NO'}]);changed()}};
 get('plcsw1').onchange=syncInputs;get('plcsw2').onchange=syncInputs;
 window.plcLab={
  configure(value){lesson=value;document.querySelector('header > span').textContent='YOUR PLC LEARNING LAB';get('folder').hidden=true;document.body.classList.add('plcpage');document.body.classList.toggle('ladderpage',lesson.engine==='plc-ladder');get('plclab').hidden=false;get('ladderbuilder').hidden=lesson.engine!=='plc-ladder';get('editor').hidden=lesson.engine==='plc-ladder';get('editor').setAttribute('aria-label',lesson.engine==='plc-st'?'Structured Text code editor':'Python code editor');get('helpersearch').placeholder='Try contact, coil, AND, IF…';refresh();syncInputs()},
  refresh,
  sourceChanged(){if(lesson?.engine==='plc-st'){truthTable();get('plclamp').classList.remove('on');get('plclamp').textContent='● LAMP awaiting scan';get('plcscanstatus').textContent='Program changed. Run a scan or choose a test case.'}},
  describe(source){try{const data=JSON.parse(source);return data.branches.map((branch,i)=>'Path '+(i+1)+': '+(branch.length?branch.map(c=>(c.contact==='NC'?'—|/|— ':'—| |— ')+c.input).join(' → '):'bare wire (always passes)')).join('\n')+'\nPaths join → ( LAMP )'}catch{return 'Diagram could not be read.'}},
  showSignals(signals){if(lastSource!==get('editor').value){lastSource=get('editor').value;scanned={}}scanned[Number(signals.SW1)+''+Number(signals.SW2)]=signals.LAMP;truthTable();const current=inputs();if(current.SW1!==signals.SW1||current.SW2!==signals.SW2){if(lesson.engine==='plc-ladder')draw();else{get('plclamp').classList.remove('on');get('plclamp').textContent='● LAMP awaiting scan'}get('plcscanstatus').textContent='Inputs changed during the scan. Run the current case again.';return}lamp(signals.LAMP);get('plcscanstatus').textContent='Scan finished: lamp is '+(signals.LAMP?'ON':'OFF')+'. Change switches or edit the program and scan again.'}
 };
})();
