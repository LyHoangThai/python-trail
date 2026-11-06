(()=>{
 const get=id=>document.getElementById(id);
 let catalog=null,category='all',catalogURL='';
 function selectConsole(name){
  const helper=name==='helper';get('outputpanel').hidden=helper;get('helperpanel').hidden=!helper;
  for(const key of ['output','helper']){get(key+'tab').setAttribute('aria-selected',String(key===name));get(key+'tab').tabIndex=key===name?0:-1}
  if(helper)load().catch(e=>{get('helpercount').textContent=e.message});
 }
 window.showPythonOutput=()=>selectConsole('output');
 get('outputtab').onclick=()=>selectConsole('output');get('helpertab').onclick=()=>selectConsole('helper');
 for(const key of ['output','helper'])get(key+'tab').onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const target=key==='output'?'helper':'output';selectConsole(target);get(target+'tab').focus()}};
 async function load(){
  const plc=window.lessonEngine?.startsWith('plc-'),url=plc?'/plc-helper.json':'/helper.json';
  if(catalog&&catalogURL===url){render();return}
  catalogURL=url;category='all';get('helpercategories').replaceChildren();get('helpersearch').value='';
  get('helpercategories').setAttribute('aria-label',plc?'PLC concepts':'Python data types');document.querySelector('label[for=helpersearch]').textContent=plc?'Search contacts, coils and Structured Text':'Search methods, functions and operations';
  document.querySelector('.helperintro').textContent=plc?'Look up contacts, coils and Boolean rules. These examples use our small teaching simulator, not a complete industrial PLC runtime.':'Find something you can do with a Python value. Methods use a dot; built-in functions wrap a value; operators go between or before values.';
  document.querySelector('.helpersources').hidden=plc;
  const response=await fetch(url);if(!response.ok)throw Error('Could not load Helper. Check the local app and try again.');catalog=await response.json();
  for(const item of catalog.categories){const button=document.createElement('button');button.id='helpertype-'+item.id;button.type='button';button.role='tab';button.setAttribute('aria-controls','helperresults');button.textContent=item.label;button.dataset.type=item.id;button.onclick=()=>{category=item.id;render()};button.onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const i=catalog.categories.findIndex(c=>c.id===category);const step=e.key==='ArrowRight'?1:-1;category=catalog.categories[(i+step+catalog.categories.length)%catalog.categories.length].id;render();get('helpertype-'+category).focus()}};get('helpercategories').append(button)}
  render();
 }
 function render(){
  const raw=get('helpersearch').value.toLowerCase().trim();
  const query=({length:'len',integer:'int',decimal:'float',dictionary:'dict',string:'str',boolean:'bool'})[raw]||raw;
  const matches=catalog.entries.filter(entry=>(category==='all'||entry.category===category)&&[entry.name,entry.description,entry.category,entry.note,entry.kind].join(' ').toLowerCase().includes(query));
  for(const button of get('helpercategories').children){const selected=button.dataset.type===category;button.setAttribute('aria-selected',String(selected));button.tabIndex=selected?0:-1}
  get('helperresults').setAttribute('aria-labelledby','helpertype-'+category);
  get('helpercount').textContent=matches.length?`${matches.length} useful operation${matches.length===1?'':'s'} · choose one for an example`:'No matches in this category. Try All or a different search.';
  get('helperresults').replaceChildren();
  for(const entry of matches){
   const details=document.createElement('details');details.className='helpercard';
   const summary=document.createElement('summary'),name=document.createElement('code'),kind=document.createElement('span');name.textContent=entry.name;kind.textContent=entry.kind+' · '+entry.category;kind.className='helperkind';summary.append(name,kind);
   const description=document.createElement('p');description.textContent=entry.description;
   const example=document.createElement('pre');example.textContent=entry.example;
   const output=document.createElement('pre');output.className='helperexampleoutput';output.textContent='Output:\n'+entry.output;
   details.append(summary,description,example,output);
   if(entry.note){const note=document.createElement('p');note.textContent=entry.note;note.className='helpernote';details.append(note)}
   get('helperresults').append(details);
  }
 }
 get('helpersearch').oninput=()=>{if(catalog)render()};
})();
