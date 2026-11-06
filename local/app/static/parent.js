const $=id=>document.getElementById(id);
let lessons=[],historyOffset=0,historyRequest=0;
function html(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function date(s){return s?new Date(s).toLocaleString():''}
async function api(path){const r=await fetch('/api/'+path);const data=await r.json();if(!r.ok)throw Error(data.error||'Unable to load parent history.');return data}
function error(e){$('error').hidden=false;$('error').textContent=e.message}
async function loadHistory(){
 const requestId=++historyRequest,query=new URLSearchParams({offset:String(historyOffset)}),filter=$('historylesson').value;if(filter)query.set('quest',filter);
 const data=await api('submissions?'+query);if(requestId!==historyRequest)return;
 $('historycount').textContent=data.total?`Showing ${data.offset+1}–${Math.min(data.offset+data.limit,data.total)} of ${data.total} turn-ins`:'No assignments turned in yet.';
 $('historyrows').innerHTML=data.submissions.map(job=>{const q=lessons.find(q=>q.id===job.quest);return `<tr><td>${html(q?.title||job.quest)}</td><td>#${job.attempt}</td><td>${job.result?(job.result.passed?'✓ Completed':'Needs revision'):'Submitted · grading'}</td><td>${html(date(job.created_at))}</td><td><a class="reviewbutton" href="/parent/submissions/${job.id}">Review code & changes</a></td></tr>`}).join('')||'<tr><td colspan="5">Turn in an assignment to start its history.</td></tr>';
 $('historyprev').disabled=data.offset===0;$('historynext').disabled=data.offset+data.limit>=data.total;
}
async function refresh(){try{
 const progress=await api('progress'),done=new Set(progress.completed.map(q=>q.quest)),active=lessons.find(q=>q.id===progress.active?.quest),attempts=new Map(progress.attempts.map(q=>[q.quest,q.count]));
 $('current').textContent=active?`Currently learning: ${active.topic}`:'No lesson started yet';$('activity').textContent=active?`${active.title} · Lesson ${active.id} · ${attempts.get(active.id)||0} turn-ins · Last activity ${date(progress.active.updated_at)}`:'Choose a lesson in the student learning space to get started.';
 $('topics').innerHTML=[...new Set(lessons.map(q=>q.topic))].map(topic=>{const qs=lessons.filter(q=>q.topic===topic),n=qs.filter(q=>done.has(q.id)).length;return `<div class="topic ${active?.topic===topic?'current':''}"><b>${html(topic)}</b><small>${n}/${qs.length} completed${active?.topic===topic?' · Current':''}</small><progress value="${n}" max="${qs.length}" aria-label="${html(topic)} completion"></progress></div>`}).join('');
 await loadHistory();$('error').hidden=true;$('connection').textContent='Local services connected';
}catch(e){error(e)}}
$('historylesson').onchange=()=>{historyOffset=0;loadHistory().catch(error)};$('historyprev').onclick=()=>{historyOffset=Math.max(0,historyOffset-20);loadHistory().catch(error)};$('historynext').onclick=()=>{historyOffset+=20;loadHistory().catch(error)};
(async()=>{try{lessons=(await api('lessons')).lessons;$('historylesson').innerHTML='<option value="">All lessons</option>'+lessons.map(q=>`<option value="${q.id}">${String(q.id).padStart(2,'0')} · ${html(q.title)} (${html(q.topic)})</option>`).join('');await refresh();setInterval(refresh,3000)}catch(e){error(e)}})();
