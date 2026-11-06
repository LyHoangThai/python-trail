const $=id=>document.getElementById(id);
const paths=[
 ['beginner','Beginner','Start here. Learn to talk to Python, store little facts, make choices, and repeat useful steps.'],
 ['intermediate','Intermediate','Build a bigger toolkit: little number machines, countdowns, tidy text, backpacks and treasure grids. Try Beginner first.'],
 ['advanced','Advanced','Ready for a stretch? Build tiny factories, safety nets and pet blueprints. These lessons take smaller ideas and combine them.'],
 ['algorithms','Algorithms','An algorithm is a recipe for solving a puzzle. Find a toy, sort marbles, count color votes, and plan a short route. Try Intermediate and Data Structures first.'],
 ['data-structures','Data Structures','Learn ways to organize things: stacks of plates, waiting lines, unique stickers, branching trees and friendship maps. Try Beginner first.'],
 ['plc','PLC','Build a pretend control panel. Explore Ladder Logic and Structured Text with virtual switches and a lamp. No equipment needed.']];
const beginnerNames=['First little steps','Pack your toolkit','Choose your adventure','Make a little magic','Meet dictionaries'];
const otherNames={plc:'PLC learning lab',intermediate:'Build your toolkit',advanced:'Bigger building blocks',algorithms:'Recipes for little puzzles','data-structures':'Ways to organize a world'};
const icons=['🌱','🎒','🧭','🏕️','📚'];
let refreshRequest=0,course=[],progress={completed:[]},selected=new URLSearchParams(location.search).get('track')||'beginner';
if(!paths.some(path=>path[0]===selected))selected='beginner';
function html(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function selectPath(id,focus=false){selected=id;window.history.replaceState(null,'','/learn?track='+id);render();if(focus)$('track-'+id).focus()}
function render(){
 const done=new Set(progress.completed.map(q=>q.quest)),lessons=course.filter(q=>(q.track||'beginner')===selected),path=paths.find(p=>p[0]===selected);
 $('tracktabs').innerHTML=paths.map(([id,label])=>{const qs=course.filter(q=>(q.track||'beginner')===id),count=qs.filter(q=>done.has(q.id)).length;return `<button id="track-${id}" role="tab" aria-selected="${id===selected}" aria-controls="chapters" tabindex="${id===selected?0:-1}" data-track="${id}">${label}<span>${count}/${qs.length}</span></button>`}).join('');
 for(const button of $('tracktabs').children){button.onclick=()=>selectPath(button.dataset.track);button.onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const i=paths.findIndex(p=>p[0]===selected),step=e.key==='ArrowRight'?1:-1;selectPath(paths[(i+step+paths.length)%paths.length][0],true)}}}
 $('chapters').setAttribute('aria-labelledby','track-'+selected);$('trackintro').textContent=path[2];$('trailtitle').textContent=path[1]+' trail';
 const next=lessons.find(q=>!done.has(q.id));$('continue').href=next?'/lessons/'+next.id:'/playground';$('continue').textContent=next?(lessons.some(q=>done.has(q.id))?'Continue learning ↗':'Start '+path[1].toLowerCase()+' ↗'):'Make something of your own ↗';
 $('total').textContent=`${lessons.filter(q=>done.has(q.id)).length} / ${lessons.length} completed here · ${done.size} / ${course.length} overall`;
 $('chapters').innerHTML=[...new Set(lessons.map(q=>q.chapter))].map((chapter,i)=>{const qs=lessons.filter(q=>q.chapter===chapter),name=selected==='plc'?(chapter===1?'Ladder Logic · draw your rules':'Structured Text · write your rules'):selected==='beginner'?beginnerNames[chapter-1]:otherNames[selected];return `<section class="chapter"><div class="chapterhead"><span class="chaptericon">${icons[i%icons.length]}</span><div><small>${html(path[1].toUpperCase())} · CHAPTER ${String(i+1).padStart(2,'0')}</small><h3>${name}</h3></div><span class="count">${qs.filter(q=>done.has(q.id)).length}/${qs.length} completed</span></div><div class="quests">${qs.map(q=>`<a class="quest ${done.has(q.id)?'done':''}" href="/lessons/${q.id}" aria-label="${html(q.title)} · ${done.has(q.id)?'Completed':'Ready to start'}"><span class="number">${done.has(q.id)?'✓':String(q.id).padStart(2,'0')}</span><b>${html(q.title)}</b><small>${html(q.topic)}</small><span class="queststate">${done.has(q.id)?'✓ Completed':'Ready to start'}</span></a>`).join('')}</div></section>`;}).join('');
}
async function refreshLessons(){const request=++refreshRequest;try{
 const responses=await Promise.all([fetch('/api/lessons',{cache:'no-store'}),fetch('/api/progress',{cache:'no-store'})]);if(responses.some(r=>!r.ok))throw Error('The local app is not ready. Check Docker Desktop and reload.');
 const [data,state]=await Promise.all(responses.map(r=>r.json()));if(request!==refreshRequest)return;course=data.lessons;progress=state;$('error').hidden=true;render();
}catch(e){$('error').hidden=false;$('error').textContent=e.message}}
refreshLessons();
window.addEventListener('pageshow',event=>{if(event.persisted)refreshLessons()});
window.addEventListener('focus',refreshLessons);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshLessons()});
