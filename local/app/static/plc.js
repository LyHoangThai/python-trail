(()=>{
 const get=id=>document.getElementById(id);let lesson=null,program=null,lastSource=null,scanned={};
 function inputs(){return {SW1:get('plcsw1').checked,SW2:get('plcsw2').checked}}
 function lamp(on){get('plclamp').classList.toggle('on',on);get('plclamp').textContent='● LAMP '+(on?'ON':'OFF');window.PLCStudio?.update(on,inputs())}
 function syncInputs(){const states=inputs();get('inputs').value=JSON.stringify(states);get('plcsw1state').textContent=states.SW1?'ON':'OFF';get('plcsw2state').textContent=states.SW2?'ON':'OFF';if(lesson?.engine==='plc-ladder')draw();else{get('plcscanstatus').textContent='Inputs changed. Run scan to update the lamp.';truthTable()}}
 function changed(){get('editor').value=JSON.stringify(program,null,2)+'\n';get('editor').dispatchEvent(new Event('input'));draw()}
 function closed(contact,states){return contact.contact==='NC'?!states[contact.input]:states[contact.input]}
 let selected=null,undo=[],redo=[];
 function message(text){get('laddermessage').textContent=text}
 function apply(payload,target){try{if(!payload)throw Error('Choose a toolbox item first.');const next=window.LadderModel.edit(program,payload,target);if(JSON.stringify(next)!==JSON.stringify(program)){undo.push(JSON.stringify(program));if(undo.length>30)undo.shift();redo=[];program=next;changed()}selected=null;message('Diagram updated. Try the switches!')}catch(error){message(error.message)}}
 function draggable(el,payload){el.draggable=true;el.ondragstart=e=>{selected=payload();e.dataTransfer.setData('application/x-ladder',JSON.stringify(selected));e.dataTransfer.effectAllowed='copyMove'};el.onclick=e=>{e.stopPropagation();selected=payload();message('Selected. Choose a dashed drop zone.')}}
 function dropzone(el,target){el.ondragover=e=>{e.preventDefault();el.classList.add('over')};el.ondragleave=()=>el.classList.remove('over');el.ondrop=e=>{e.preventDefault();e.stopPropagation();el.classList.remove('over');let payload=selected;try{const data=e.dataTransfer.getData('application/x-ladder');if(data&&data.length<1000)payload=JSON.parse(data)}catch{}apply(payload,target)};el.onclick=()=>apply(selected,target);if(el.tagName!=='BUTTON')el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();apply(selected,target)}}}
 function draw(){
  if(!program)return;const states=inputs();get('ladderpaths').replaceChildren();
  const energized=program.coil==='LAMP'&&program.branches.some(branch=>branch.every(c=>closed(c,states)));
  const network=get('rungnetwork');if(network){network.classList.toggle('on',energized);const count=Math.max(1,...program.branches.map(branch=>branch.length));network.style.minWidth=Math.max(500,count*95+(count+1)*27+148)+'px'}
  program.branches.forEach((branch,index)=>{
   const row=document.createElement('section');row.className='ladderpath';const heading=document.createElement('b');heading.className='pathlabel';heading.textContent='Path '+(index+1);row.append(heading);
   const rail=document.createElement('div');rail.className='ladderrail '+(branch.every(c=>closed(c,states))?'energized':'');
   for(let position=0;position<=branch.length;position++){
    const gap=document.createElement('button');gap.className='ladderdrop contactgap';gap.textContent='+';gap.setAttribute('aria-label',`Path ${index+1} insert contact ${position+1}`);dropzone(gap,{type:'slot',path:index,index:position});rail.append(gap);
    if(position===branch.length)break;const c=branch[position],card=document.createElement('div');card.className='laddercontact '+(closed(c,states)?'closed':'');
    const handle=document.createElement('button');handle.className='contacthandle';const tag=document.createElement('span');tag.className='contacttag';tag.textContent=c.input;handle.append(tag,window.PLCStudio.symbol(c.contact));handle.setAttribute('aria-label',`Move ${c.input} ${c.contact} contact on path ${index+1}`);draggable(handle,()=>({type:'move',path:index,index:position}));
    const label=document.createElement('small');label.textContent=c.contact==='NC'?'Normally closed':'Normally open';const remove=document.createElement('button');remove.className='darkbutton';remove.textContent='Remove';remove.setAttribute('aria-label',`Remove path ${index+1} contact ${position+1}`);remove.onclick=()=>apply({type:'move',path:index,index:position},{type:'trash'});card.append(handle,label,remove);rail.append(card);
   }row.append(rail);get('ladderpaths').append(row);
  });
  const coil=get('laddercoilzone');coil.replaceChildren();coil.classList.toggle('on',energized);if(program.coil==='LAMP'){const handle=document.createElement('button');handle.className='contacthandle';const tag=document.createElement('span');tag.className='contacttag';tag.textContent='LAMP';handle.append(tag,window.PLCStudio.symbol('coil'));handle.setAttribute('aria-label','Move LAMP coil');draggable(handle,()=>({type:'move-coil'}));coil.append(handle)}else{const placeholder=document.createElement('span');placeholder.textContent='Drop LAMP coil';coil.append(window.PLCStudio.symbol('coil'),placeholder)}dropzone(coil,{type:'coil'});
  if(!program.branches.length){const empty=document.createElement('p');empty.className='studio-empty';empty.textContent='Drag a contact to the new path box below to start your rung.';get('ladderpaths').append(empty)}get('ladderundo').disabled=!undo.length;get('ladderredo').disabled=!redo.length;truthTable();lamp(energized);get('plcscanstatus').textContent=program.coil==='LAMP'?'Live preview: green contacts pass the signal. Run scan checks your diagram.':'Connect the LAMP coil to see your output.';
 }
 function truthTable(){
  if(!lesson)return;
  if(lastSource!==get('editor').value){lastSource=get('editor').value;scanned={}}
  get('plctruthrows').replaceChildren();
  for(const sw1 of [false,true])for(const sw2 of [false,true]){
   const key=Number(sw1)+''+Number(sw2),states={SW1:sw1,SW2:sw2};
   const value=lesson.engine==='plc-ladder'&&program?program.coil==='LAMP'&&program.branches.some(branch=>branch.every(contact=>closed(contact,states))):scanned[key];
   const row=document.createElement('tr');for(const text of [sw1?'ON':'OFF',sw2?'ON':'OFF',value===undefined?'Not scanned':value?'ON':'OFF']){const cell=document.createElement('td');cell.textContent=text;row.append(cell)}
   const cell=document.createElement('td'),button=document.createElement('button');button.className='darkbutton';button.textContent=lesson.engine==='plc-ladder'?'Set switches':'Run case';button.setAttribute('aria-label',`Test SW1 ${sw1?'ON':'OFF'}, SW2 ${sw2?'ON':'OFF'}`);button.onclick=()=>{get('plcsw1').checked=sw1;get('plcsw2').checked=sw2;syncInputs();if(lesson.engine==='plc-st')get('run').click()};cell.append(button);row.append(cell);get('plctruthrows').append(row);
  }
 }
 function refresh(){if(lesson?.engine!=='plc-ladder')return;try{program=JSON.parse(get('editor').value);if(!program||!['LAMP',null].includes(program.coil)||!Array.isArray(program.branches))throw Error();undo=[];redo=[];selected=null;draw()}catch{get('ladderpaths').textContent='This saved diagram cannot be opened. Use Reset to starter to build it again.';program=null}}
 for(const [id,type] of [['toolno','NO'],['toolnc','NC']])draggable(get(id),()=>({type:'contact',input:get('toolboxinput').value,contact:type}));
 draggable(get('toolcoil'),()=>({type:'coil'}));dropzone(get('newparallelzone'),{type:'parallel'});dropzone(get('laddertrash'),{type:'trash'});
 get('ladderundo').onclick=()=>{if(!undo.length)return;redo.push(JSON.stringify(program));program=JSON.parse(undo.pop());selected=null;changed();message('Undid your edit.')};
 get('ladderredo').onclick=()=>{if(!redo.length)return;undo.push(JSON.stringify(program));program=JSON.parse(redo.pop());selected=null;changed();message('Redid your edit.')};
 get('plcsw1').onchange=syncInputs;get('plcsw2').onchange=syncInputs;
 window.plcLab={
  configure(value){lesson=value;document.querySelector('header > span').textContent='YOUR PLC LEARNING LAB';get('folder').hidden=true;document.querySelector('aside a[href="/playground"]').hidden=true;document.querySelector('.workspacefoot a').hidden=true;document.body.classList.add('plcpage');document.body.classList.toggle('ladderpage',lesson.engine==='plc-ladder');get('plclab').hidden=false;get('ladderbuilder').hidden=lesson.engine!=='plc-ladder';get('editor').hidden=lesson.engine==='plc-ladder';get('editor').setAttribute('aria-label',lesson.engine==='plc-st'?'Structured Text code editor':'Python code editor');get('helpersearch').placeholder='Try contact, coil, AND, IF…';if(lesson.engine==='plc-ladder')window.PLCStudio.mount({toggle(input){get(input==='SW1'?'plcsw1':'plcsw2').checked=!inputs()[input];syncInputs()}});refresh();syncInputs()},
  refresh,
  sourceChanged(){if(lesson?.engine==='plc-st'){truthTable();get('plclamp').classList.remove('on');get('plclamp').textContent='● LAMP awaiting scan';get('plcscanstatus').textContent='Program changed. Run a scan or choose a test case.'}},
  describe(source){try{const data=JSON.parse(source);return data.branches.map((branch,i)=>'Path '+(i+1)+': '+(branch.length?branch.map(c=>(c.contact==='NC'?'—|/|— ':'—| |— ')+c.input).join(' → '):'bare wire (always passes)')).join('\n')+'\nPaths join → '+(data.coil==='LAMP'?'( LAMP )':'no coil connected')}catch{return 'Diagram could not be read.'}},
  showSignals(signals){if(lastSource!==get('editor').value){lastSource=get('editor').value;scanned={}}scanned[Number(signals.SW1)+''+Number(signals.SW2)]=signals.LAMP;truthTable();const current=inputs();if(current.SW1!==signals.SW1||current.SW2!==signals.SW2){if(lesson.engine==='plc-ladder')draw();else{get('plclamp').classList.remove('on');get('plclamp').textContent='● LAMP awaiting scan'}get('plcscanstatus').textContent='Inputs changed during the scan. Run the current case again.';return}lamp(signals.LAMP);get('plcscanstatus').textContent='Scan finished: lamp is '+(signals.LAMP?'ON':'OFF')+'. Change switches or edit the program and scan again.'}
 };
})();
