/* The lesson data and saved diagram stay shared with the regular lesson workspace. */
(()=>{
 const get=id=>document.getElementById(id);let mounted=false;
 function node(tag,cls,text){const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el}
 function button(text,action,cls='studio-button'){const el=node('button',cls,text);el.type='button';el.onclick=action;return el}
 function symbol(kind){const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 120 48');svg.setAttribute('aria-hidden','true');svg.classList.add('ladder-symbol');const paths={NO:'M0 24H46M46 9V39M74 9V39M74 24H120',NC:'M0 24H46M46 9V39M74 9V39M74 24H120M40 41L80 7',coil:'M0 24H40M50 7C33 14 33 34 50 41M70 7C87 14 87 34 70 41M80 24H120'};const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d',paths[kind]);path.setAttribute('fill','none');path.setAttribute('stroke','currentColor');path.setAttribute('stroke-width','2.5');svg.append(path);return svg}
 function mount(actions){
  if(mounted)return;mounted=true;
  const workspace=document.querySelector('.workspace'),coding=document.querySelector('.coding'),article=workspace.querySelector('article');
  const dialog=node('dialog','studio-lesson');dialog.id='plclessondialog';const close=button('Close lesson ×',()=>dialog.close());dialog.append(close,article);document.querySelector('main').append(dialog);dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
  const toolbar=node('section','studio-toolbar');toolbar.setAttribute('aria-label','Ladder workspace controls');
  const title=node('div','studio-title');title.append(node('b','','Ladder studio'),node('span','','BUILD · TEST · DISCOVER'));toolbar.append(title);
  const views=node('div','studio-views');views.setAttribute('role','group');views.setAttribute('aria-label','Simulator view');
  for(const [value,label] of [['ladder','Ladder'],['split','Split'],['panel','I/O Panel']]){const control=button(label,()=>{workspace.dataset.view=value;for(const item of views.children)item.setAttribute('aria-pressed',String(item===control))});control.setAttribute('aria-pressed',String(value==='ladder'));views.append(control)}
  toolbar.append(views,button('Assignment & history',()=>dialog.showModal()),get('ladderundo'),get('ladderredo'));
  const live=node('span','studio-live','● LIVE PREVIEW');toolbar.append(live,get('run'),get('submit'));workspace.before(toolbar);
  const tags=node('section','studio-tags');workspace.prepend(tags);tags.setAttribute('aria-label','PLC tags');tags.append(node('h2','','Tags & inputs'),node('p','studio-muted','Flip an input. Follow the signal.'));
  const taghead=node('div','tag-heading');for(const label of ['TAG','TYPE','VALUE'])taghead.append(node('span','',label));tags.append(taghead);
  const switches=document.querySelector('.plcswitches');tags.append(switches);
  const outputrow=node('div','tag-output');outputrow.append(node('b','','LAMP'),node('span','','BOOL · output'));tags.append(outputrow,get('plclamp'));
  const guide=node('div','studio-guide');guide.append(node('b','','Your challenge'),node('p','',get('title').textContent),button('Read assignment →',()=>dialog.showModal()));tags.append(guide);
  const cases=node('details','studio-cases');cases.append(node('summary','','Test all 4 input combinations'),document.querySelector('.plctruthwrap'));tags.append(cases);
  const palette=node('section','studio-palette');workspace.append(palette);palette.setAttribute('aria-label','Ladder objects');palette.append(node('h2','','Ladder objects'),node('p','studio-muted','Drag an object onto a dashed target.'));
  const toolbox=document.querySelector('.laddertoolbox');palette.append(toolbox,get('laddertrash'));
  const filters=node('div','studio-filters');filters.setAttribute('role','group');filters.setAttribute('aria-label','Object category');
  for(const [value,label] of [['all','All'],['contacts','Contacts'],['coils','Coils']]){const control=button(label,()=>{get('toolno').hidden=value==='coils';get('toolnc').hidden=value==='coils';get('toolcoil').hidden=value==='contacts';for(const item of filters.children)item.setAttribute('aria-pressed',String(item===control))});control.setAttribute('aria-pressed',String(value==='all'));filters.append(control)}toolbox.before(filters);
  for(const [id,kind,name,description] of [['toolno','NO','NO','Normally open contact'],['toolnc','NC','NC','Normally closed contact'],['toolcoil','coil','Coil','LAMP output']]){const tool=get(id);tool.replaceChildren(symbol(kind));const caption=node('span','object-caption');caption.append(node('b','',name),node('small','',description));tool.append(caption)}
  const lab=get('plclab');lab.querySelector('.plclabnote').hidden=true;
  const canvashead=node('div','studio-canvashead');canvashead.append(node('b','','Rung 000 · LAMP'),node('span','studio-muted','One assignment · one output'));
  const zoomlabel=node('label','','Zoom '),zoom=node('select');zoom.id='canvaszoom';zoom.setAttribute('aria-label','Ladder canvas zoom');for(const value of [80,100,120,140]){const option=node('option','',value+'%');option.value=value;zoom.append(option)}zoom.value='100';zoom.onchange=()=>get('rungnetwork').style.zoom=Number(zoom.value)/100;zoomlabel.append(zoom);canvashead.append(zoomlabel);lab.prepend(canvashead);
  const network=node('div','rungnetwork');network.id='rungnetwork';network.append(get('ladderpaths'),get('laddercoilzone'));get('ladderbuilder').prepend(network);
  const empty=node('p','studio-empty','Drag a contact here to start. Put contacts in a row for AND, or add a parallel path for OR.');empty.id='ladderempty';get('ladderpaths').append(empty);
  const hmi=node('section','studio-hmi');hmi.id='studiohmi';hmi.setAttribute('aria-label','Interactive operator panel');hmi.append(node('h3','','Operator panel'),node('p','studio-muted','These buttons control the same SW1 and SW2 tags.'));
  for(const input of ['SW1','SW2']){const control=button(input+' · OFF',()=>actions.toggle(input),'hmi-switch');control.id='hmi'+input;control.setAttribute('aria-label','Operator panel '+input);control.setAttribute('aria-pressed','false');hmi.append(control)}const hmibulb=node('div','hmi-lamp','LAMP');hmibulb.id='hmilamp';hmibulb.setAttribute('role','status');hmi.append(hmibulb);lab.append(hmi);
  const console=node('details','studio-console');console.id='studioconsole';console.append(node('summary','','Output & Helper'),document.querySelector('.consoletop'),get('outputpanel'),get('helperpanel'));coding.append(console);
  const footer=node('div','studio-footer');footer.append(get('save'),get('reset'),get('savestatus'));coding.append(footer);
  for(const id of ['run','submit'])get(id).addEventListener('click',()=>console.open=true);
  workspace.replaceChildren(tags,coding,palette);workspace.dataset.view='ladder';
  const heading=document.querySelector('.lessonheading');const parent=node('a','','Parent dashboard ↗');parent.href='/parent';heading.append(parent);
 }
 function update(on,states){if(!mounted)return;get('hmilamp').classList.toggle('on',on);get('hmilamp').textContent='LAMP · '+(on?'ON':'OFF');for(const input of ['SW1','SW2']){const control=get('hmi'+input);control.textContent=input+' · '+(states[input]?'ON':'OFF');control.setAttribute('aria-pressed',String(states[input]))}}
 window.PLCStudio={mount,symbol,update,openLesson(){get('plclessondialog')?.showModal()}};
})();
