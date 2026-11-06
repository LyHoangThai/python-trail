const $=id=>document.getElementById(id);
const playground=location.pathname==='/playground',quest=playground?0:Number(location.pathname.split('/').pop());
let lesson=null,ready=false,busy=false,revision=0,saveTimer=null,saveChain=Promise.resolve();
async function api(path,data){const r=await fetch('/api/'+path,data===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json','X-Trail-Client':'browser'},body:JSON.stringify(data)});const result=await r.json();if(!r.ok)throw Error(result.error||'Unable to connect to the local app.');return result}
function error(e){$('error').hidden=false;$('error').textContent=e.message}
function saveSnapshot(source,version){
 $('savestatus').textContent='Saving…';
 saveChain=saveChain.catch(()=>{}).then(()=>api('drafts',{quest,source})).then(()=>{if(revision===version)$('savestatus').textContent='Saved on this computer'}).catch(e=>{$('savestatus').textContent='Draft not saved — retry';error(e);throw e});
 return saveChain;
}
async function save(){clearTimeout(saveTimer);if(ready)await saveSnapshot($('editor').value,revision)}
$('editor').oninput=()=>{revision++;$('savestatus').textContent='Unsaved changes';clearTimeout(saveTimer);saveTimer=setTimeout(()=>save().catch(()=>{}),650)};
$('editor').onkeydown=e=>{if(e.key==='Tab'){e.preventDefault();e.target.setRangeText('    ',e.target.selectionStart,e.target.selectionEnd,'end');e.target.dispatchEvent(new Event('input'))}if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();$('run').click()}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();save().catch(()=>{})}};
$('save').onclick=()=>save().catch(()=>{});
$('reset').onclick=()=>{if(confirm('Replace this draft with the starter code? Submitted versions will stay in history.')){$('editor').value=playground?'# Try an idea!\nprint("Hello, imagination!")\n':lesson.starter;$('editor').dispatchEvent(new Event('input'))}};
async function execute(submit){
 if(!ready||busy)return;busy=true;$('run').disabled=true;$('submit').disabled=true;$('feedback').textContent='';$('receipt').textContent='';$('actionstatus').textContent=submit?'Turning in…':'Running…';$('output').textContent='Waiting for the Python worker…';
 const source=$('editor').value,version=revision;
 try{
  clearTimeout(saveTimer);await saveSnapshot(source,version);
  const job=await api(submit?'submit':'run',{quest,source,inputs:$('inputs').value});
  if(submit)$('receipt').textContent=`Turned in. Submission ${job.id}. A copy of this code is saved for parent review.`;
  const endpoint=(submit?'jobs/':'runs/')+job.id;
  for(let n=0;n<120;n++){
   const result=await api(endpoint);
   if(result.status==='done'){
    $('output').textContent=result.output||'(No output. Use print() to show something.)';
    $('feedback').textContent=result.feedback;
    $('actionstatus').textContent=submit?(result.passed?'✓ Assignment completed':'Needs revision — attempt saved'):(result.passed?'Run complete':'Python found a problem');
    if(submit&&!result.passed)$('feedback').textContent+=' Edit your code and turn it in again when ready.';
    if(!submit&&playground&&result.passed)$('feedback').textContent='Code ran successfully. Keep experimenting!';
    return;
   }
   await new Promise(resolve=>setTimeout(resolve,500));
  }
  $('actionstatus').textContent='Still queued';$('feedback').textContent=submit?'Your turn-in is saved. Its result will appear in parent history.':'The run is still waiting. Check that the worker container is running.';
 }catch(e){error(e);$('actionstatus').textContent='Could not finish';$('feedback').textContent='If you received a submission ID above, that turn-in is saved. Check parent history before resubmitting.'}
 finally{busy=false;$('run').disabled=false;$('submit').disabled=false}
}
$('run').onclick=()=>execute(false);$('submit').onclick=()=>execute(true);
window.addEventListener('beforeunload',e=>{if(ready&&$('savestatus').textContent!=='Saved on this computer'){e.preventDefault();e.returnValue=''}});
(async()=>{try{
 const data=await api('lessons');lesson=data.lessons.find(q=>q.id===quest);
 if(!playground&&!lesson)throw Error('Lesson not found. Return to your learning trail.');
 const draft=await api('drafts/'+quest);
 $('editor').value=draft.source;$('editor').disabled=false;$('run').disabled=false;$('submit').disabled=false;ready=true;$('savestatus').textContent='Saved on this computer';
 if(playground){document.querySelector('.workspacefoot a').hidden=true;$('topic').textContent='YOUR IDEAS LIVE HERE';$('title').textContent='What will you make?';$('explain').innerHTML='<p>Try a silly story, a number game, or your own experiment. This space is yours.</p><p>For input(), enter one answer per line under Program input. Run will read those answers in order.</p>';$('missionsection').hidden=true;$('submit').hidden=true;$('nextlesson').hidden=true;$('editorfile').textContent='playground.py';$('turninnote').textContent='Free play saves your draft. Runs do not create assignment submissions.';$('lessonlabel').textContent='FREE PLAYGROUND';}
 else{$('topic').textContent=lesson.topic;$('title').textContent=lesson.title;$('explain').innerHTML='<p>'+lesson.explain+'</p>';$('mission').textContent=lesson.mission;$('hint').textContent=lesson.hint;$('expected').textContent=lesson.expected;$('folder').textContent='Optional file workspace: '+lesson.assignment_path;$('lessonlabel').textContent=`LESSON ${String(quest).padStart(2,'0')} / CHAPTER ${lesson.chapter}`;$('inputsection').hidden=true;$('nextlesson').href=quest<data.lessons.length?'/lessons/'+(quest+1):'/learn';$('nextlesson').textContent=quest<data.lessons.length?'Next lesson →':'Back to your trail →';const solutions=await api('solutions');$('solution').textContent=solutions[quest];await api('start',{quest});}
}catch(e){error(e)}})();
