const $=id=>document.getElementById(id),id=location.pathname.split('/').pop();
function html(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function api(path){const r=await fetch('/api/'+path);const data=await r.json();if(!r.ok)throw Error(data.error||'Unable to load submission.');return data}
async function load(){try{
 const [data,job]=await Promise.all([api('lessons'),api('submissions/'+id)]),q=data.lessons.find(q=>q.id===job.quest);
 $('reviewlabel').textContent=`LESSON ${String(job.quest).padStart(2,'0')} / ATTEMPT ${job.attempt}`;$('reviewtitle').textContent=q?.title||'Submission';$('reviewmeta').textContent=`Turned in ${new Date(job.created_at).toLocaleString()} · Submission ${job.id}`;
 $('reviewstatus').textContent=job.result?(job.result.passed?'✓ Completed':'Needs revision — this attempt is saved'):'Submitted — waiting for grading';$('baselinelabel').textContent=job.baseline_label.toLowerCase();$('previouslabel').textContent=job.baseline_label;
 $('diffnote').textContent=job.previous?'Compared with the previous turn-in for this lesson. Green + lines were added; red − lines were removed.':'First turn-in: compared with the lesson starter. Green + lines were added; red − lines were removed.';
 $('reviewdiff').innerHTML=job.diff?job.diff.split('\n').map((line,i)=>`<span class="${i<2?'header':line.startsWith('+')?'added':line.startsWith('-')?'removed':line.startsWith('@@')?'hunk':'context'}">${html(line)||' '}</span>`).join(''):html('No code-line changes from this version.');
 $('previouscode').textContent=job.baseline_source||'(empty file)';$('submittedcode').textContent=job.source||'(empty file)';$('reviewfeedback').textContent=job.result?.feedback||'Grading is pending. Use Refresh result in a moment.';$('reviewoutput').textContent=job.result?.output||'(no output)';$('error').hidden=true;
}catch(e){$('error').hidden=false;$('error').textContent=e.message}}
$('reviewrefresh').onclick=load;load();
