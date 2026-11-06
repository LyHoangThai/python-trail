const $=id=>document.getElementById(id);
const beginnerNames=['First little steps','Pack your toolkit','Choose your adventure','Make a little magic','Meet dictionaries'];
const otherNames={intermediate:'Build your toolkit',advanced:'Bigger building blocks',algorithms:'Recipes for little puzzles','data-structures':'Ways to organize a world'};
const icons=['🌱','🎒','🧭','🏕️','📚'];
const params=new URLSearchParams(location.search);let remembered='python';try{remembered=localStorage.getItem('trail-subject')||'python'}catch{}
let subjectId=params.get('subject')||(params.get('track')==='plc'?'plc':remembered),selected=params.get('track'),refreshRequest=0,course=[],subjects=[],progress={completed:[]};
if(selected==='plc')selected='ladder';
function html(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function subjectOf(lesson){return lesson.subject||(lesson.engine?.startsWith('plc-')?'plc':'python')}
function updateURL(){window.history.replaceState(null,'','/learn?subject='+encodeURIComponent(subjectId)+'&track='+encodeURIComponent(selected))}
function selectSubject(id){if(!subjects.some(subject=>subject.id===id))return;subjectId=id;selected=subjects.find(subject=>subject.id===id).tracks[0].id;try{localStorage.setItem('trail-subject',id)}catch{}updateURL();render()}
function selectPath(id,focus=false){selected=id;updateURL();render();if(focus)$('track-'+id).focus()}
$('subjectselect').onchange=()=>selectSubject($('subjectselect').value);
function render(){
 const subject=subjects.find(item=>item.id===subjectId)||subjects[0];if(!subject)return;subjectId=subject.id;
 const paths=subject.tracks;if(!paths.some(path=>path.id===selected))selected=paths[0].id;
 const path=paths.find(item=>item.id===selected),done=new Set(progress.completed.map(q=>q.quest)),subjectLessons=course.filter(q=>subjectOf(q)===subjectId),matches=(q,p)=>q[p.field]===p.value,lessons=subjectLessons.filter(q=>matches(q,path));
 $('subjectselect').innerHTML=subjects.map(item=>`<option value="${html(item.id)}">${html(item.label)}</option>`).join('');$('subjectselect').value=subjectId;$('subjectselect').disabled=false;
 $('subjectheading').textContent='YOUR '+subject.label.toUpperCase()+' ADVENTURE';$('subjecticon').textContent=subject.icon;$('subjectexample').textContent=subject.example;$('subjectnote').textContent=`${subjectLessons.length} ${subject.label} lessons · All unlocked · Your own pace`;$('subjectplayground').hidden=subjectId!=='python';
 $('tracktabs').innerHTML=paths.map(item=>{const qs=subjectLessons.filter(q=>matches(q,item)),count=qs.filter(q=>done.has(q.id)).length;return `<button id="track-${item.id}" role="tab" aria-selected="${item.id===selected}" aria-controls="chapters" tabindex="${item.id===selected?0:-1}" data-track="${item.id}">${html(item.label)}<span>${count}/${qs.length}</span></button>`}).join('');
 for(const button of $('tracktabs').children){button.onclick=()=>selectPath(button.dataset.track);button.onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const index=paths.findIndex(item=>item.id===selected),step=e.key==='ArrowRight'?1:-1;selectPath(paths[(index+step+paths.length)%paths.length].id,true)}}}
 $('chapters').setAttribute('aria-labelledby','track-'+selected);$('trackintro').textContent=path.description;$('trailtitle').textContent=path.label+' trail';
 const next=lessons.find(q=>!done.has(q.id)),nextPath=paths.find(item=>subjectLessons.some(q=>matches(q,item)&&!done.has(q.id)));
 $('continue').href=next?'/lessons/'+next.id:nextPath?'/learn?subject='+subjectId+'&track='+nextPath.id:subjectId==='python'?'/playground':'/lessons/'+lessons[0]?.id;
 $('continue').textContent=next?(lessons.some(q=>done.has(q.id))?'Continue learning ↗':'Start '+path.label+' ↗'):nextPath?'Explore '+nextPath.label+' ↗':subjectId==='python'?'Make something of your own ↗':'Review this path ↗';
 $('total').textContent=`${lessons.filter(q=>done.has(q.id)).length} / ${lessons.length} completed here · ${subjectLessons.filter(q=>done.has(q.id)).length} / ${subjectLessons.length} in ${subject.label}`;
 $('chapters').innerHTML=[...new Set(lessons.map(q=>q.chapter))].map((chapter,index)=>{const qs=lessons.filter(q=>q.chapter===chapter),name=selected==='beginner'?beginnerNames[chapter-1]:otherNames[selected]||path.label;return `<section class="chapter"><div class="chapterhead"><span class="chaptericon">${icons[index%icons.length]}</span><div><small>${html(subject.label.toUpperCase())} · ${html(path.label.toUpperCase())}</small><h3>${html(name)}</h3></div><span class="count">${qs.filter(q=>done.has(q.id)).length}/${qs.length} completed</span></div><div class="quests">${qs.map(q=>`<a class="quest ${done.has(q.id)?'done':''}" href="/lessons/${q.id}" aria-label="${html(q.title)} · ${done.has(q.id)?'Completed':'Ready to start'}"><span class="number">${done.has(q.id)?'✓':String(q.id).padStart(2,'0')}</span><b>${html(q.title)}</b><small>${html(q.topic)}</small><span class="queststate">${done.has(q.id)?'✓ Completed':'Ready to start'}</span></a>`).join('')}</div></section>`;}).join('');
}
async function refreshLessons(){const request=++refreshRequest;try{
 const responses=await Promise.all([fetch('/api/lessons',{cache:'no-store'}),fetch('/api/progress',{cache:'no-store'}),fetch('/api/subjects',{cache:'no-store'})]);if(responses.some(r=>!r.ok))throw Error('The local app is not ready. Check Docker Desktop and reload.');
 const [data,state,registry]=await Promise.all(responses.map(r=>r.json()));if(request!==refreshRequest)return;course=data.lessons;progress=state;subjects=registry.subjects;$('error').hidden=true;render();
}catch(e){$('error').hidden=false;$('error').textContent=e.message}}
refreshLessons();
window.addEventListener('pageshow',event=>{if(event.persisted)refreshLessons()});
window.addEventListener('focus',refreshLessons);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshLessons()});
