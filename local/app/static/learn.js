const $=id=>document.getElementById(id);
const names=['First little steps','Pack your toolkit','Choose your adventure','Make a little magic','Meet dictionaries'];
const icons=['🌱','🎒','🧭','🏕️','📚'];
function html(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
(async()=>{try{
 const responses=await Promise.all([fetch('/api/lessons'),fetch('/api/progress')]);
 if(responses.some(r=>!r.ok))throw Error('The local app is not ready. Check Docker Desktop and reload.');
 const [data,progress]=await Promise.all(responses.map(r=>r.json()));
 const lessons=data.lessons,done=new Set(progress.completed.map(q=>q.quest));
 const next=lessons.find(q=>!done.has(q.id));
 $('continue').href=next?'/lessons/'+next.id:'/playground';$('continue').textContent=next?(done.size?'Continue learning ↗':'Start learning ↗'):'Make something of your own ↗';
 $('total').textContent=`${done.size} / ${lessons.length} completed`;
 $('chapters').innerHTML=names.map((name,i)=>`<section class="chapter"><div class="chapterhead"><span class="chaptericon">${icons[i]}</span><div><small>CHAPTER 0${i+1}</small><h3>${name}</h3></div><span class="count">${lessons.filter(q=>q.chapter===i+1&&done.has(q.id)).length}/5 completed</span></div><div class="quests">${lessons.filter(q=>q.chapter===i+1).map(q=>`<a class="quest ${done.has(q.id)?'done':''}" href="/lessons/${q.id}"><span class="number">${done.has(q.id)?'✓':String(q.id).padStart(2,'0')}</span><b>${html(q.title)}</b><small>${html(q.topic)}</small></a>`).join('')}</div></section>`).join('');
}catch(e){$('error').hidden=false;$('error').textContent=e.message}})();
