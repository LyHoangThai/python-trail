const $=id=>document.getElementById(id);
const playground=location.pathname==='/playground',quest=playground?0:Number(location.pathname.split('/').pop());
let lesson=null,ready=false,busy=false,revision=0,saveTimer=null,saveChain=Promise.resolve(),historyOffset=0,historyCount=0,historySelection=null,lessonHistoryRequest=0,lastSubmissionId=null;
async function api(path,data){const r=await fetch('/api/'+path,data===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json','X-Trail-Client':'browser'},body:JSON.stringify(data)});const result=await r.json();if(!r.ok)throw Error(result.error||'Unable to connect to the local app.');return result}
function error(e){$('error').hidden=false;$('error').textContent=e.message}
function showSubmissionBanner(kind,title,message){
 const banner=$('submissionbanner');banner.hidden=false;banner.className='submissionbanner '+kind;
 banner.setAttribute('role',kind==='incorrect'||kind==='warning'?'alert':'status');
 $('bannertitle').textContent=title;$('bannermessage').textContent=message;$('bannerhistory').hidden=!lastSubmissionId;
}
$('bannerclose').onclick=()=>$('submissionbanner').hidden=true;
$('bannerhistory').onclick=()=>{if(lastSubmissionId){setLessonTab('history');openAttempt(lastSubmissionId);$('historytab').focus()}};
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
 if(!ready||busy)return;if(window.showPythonOutput)window.showPythonOutput();busy=true;$('run').disabled=true;$('submit').disabled=true;$('feedback').textContent='';$('receipt').textContent='';$('actionstatus').textContent=submit?'Turning in…':'Running…';$('output').textContent='Waiting for the Python worker…';
 const source=$('editor').value,version=revision;
 if(submit){lastSubmissionId=null;showSubmissionBanner('pending','Turning in your assignment…','Saving your answer and checking your code.')} 
 try{
  clearTimeout(saveTimer);await saveSnapshot(source,version);
  const job=await api(submit?'submit':'run',{quest,source,inputs:$('inputs').value});
  if(submit){lastSubmissionId=job.id;showSubmissionBanner('pending','Assignment turned in','Your answer is saved. The Python worker is checking it.')}
  if(submit)$('receipt').textContent=`Turned in. Submission ${job.id}. A copy of this code is saved for parent review.`;
  const endpoint=(submit?'jobs/':'runs/')+job.id;
  for(let n=0;n<120;n++){
   const result=await api(endpoint);
   if(result.status==='done'){
    $('output').textContent=result.output||'(No output. Use print() to show something.)';
    $('feedback').textContent=result.feedback;
    $('actionstatus').textContent=submit?(result.passed?'✓ Assignment completed':'Needs revision — attempt saved'):(result.passed?'Run finished — not graded':'Python found a problem');
    if(submit)showSubmissionBanner(result.passed?'correct':'incorrect',result.passed?'✓ Nice work — assignment complete!':'Keep going — your answer needs another try',result.feedback+' Your answer is saved in History.');
    if(submit){const updates=await Promise.allSettled([refreshLessonState(),loadLessonHistory(true)]);for(const update of updates)if(update.status==='rejected')error(update.reason)}
    if(submit&&!result.passed)$('feedback').textContent+=' Edit your code and turn it in again when ready.';
    if(!submit&&playground&&result.passed)$('feedback').textContent='Code ran successfully. Keep experimenting!';
    return;
   }
   await new Promise(resolve=>setTimeout(resolve,500));
  }
  if(submit)showSubmissionBanner('pending','Your turn-in is saved','Grading is taking a little longer. Check this attempt in History.');
  $('actionstatus').textContent='Still queued';$('feedback').textContent=submit?'Your turn-in is saved. Its result will appear in parent history.':'The run is still waiting. Check that the worker container is running.';
 }catch(e){if(submit)showSubmissionBanner('warning',lastSubmissionId?'Your turn-in is saved':'Could not turn in yet',lastSubmissionId?'We could not load the result. Check History before submitting again.':'Check that the local app is connected, then try turning it in again.');error(e);$('actionstatus').textContent='Could not finish';$('feedback').textContent='If you received a submission ID above, that turn-in is saved. Check parent history before resubmitting.'}
 finally{busy=false;$('run').disabled=false;$('submit').disabled=false}
}
$('run').onclick=()=>execute(false);$('submit').onclick=()=>execute(true);
window.addEventListener('beforeunload',e=>{if(ready&&$('savestatus').textContent!=='Saved on this computer'){e.preventDefault();e.returnValue=''}});
(async()=>{try{
 const data=await api('lessons');lesson=data.lessons.find(q=>q.id===quest);
 if(!playground&&!lesson)throw Error('Lesson not found. Return to your learning trail.');
 const draft=await api('drafts/'+quest);
 $('editor').value=draft.source;$('editor').disabled=false;$('run').disabled=false;$('submit').disabled=false;ready=true;$('savestatus').textContent='Saved on this computer';
 if(playground){$('lessontabs').hidden=true;$('lessonstate').hidden=true;document.querySelector('.workspacefoot a').hidden=true;$('topic').textContent='YOUR IDEAS LIVE HERE';$('title').textContent='What will you make?';$('explain').innerHTML='<p>Try a silly story, a number game, or your own experiment. This space is yours.</p><p>For input(), enter one answer per line under Program input. Run will read those answers in order.</p>';$('missionsection').hidden=true;$('submit').hidden=true;$('nextlesson').hidden=true;$('editorfile').textContent='playground.py';$('turninnote').textContent='Free play saves your draft. Runs do not create assignment submissions.';$('lessonlabel').textContent='FREE PLAYGROUND';}
 else{$('topic').textContent=lesson.topic;$('title').textContent=lesson.title;$('explain').innerHTML='<p>'+lesson.explain+'</p>';$('mission').textContent=lesson.mission;$('requirements').replaceChildren(...(lesson.checks||[]).map(text=>{const item=document.createElement('li');item.textContent=text;return item}));$('hint').textContent=lesson.hint;$('expected').textContent=lesson.expected;$('folder').textContent='Optional file workspace: '+lesson.assignment_path;$('lessonlabel').textContent=`${(lesson.track||'beginner').replace('data-structures','data structures').toUpperCase()} / LESSON ${String(quest).padStart(2,'0')}`;document.querySelector('.lessonheading a').href='/learn?track='+lesson.track;$('inputsection').hidden=true;const siblings=data.lessons.filter(item=>item.track===lesson.track),next=siblings[siblings.findIndex(item=>item.id===quest)+1];$('nextlesson').href=next?'/lessons/'+next.id:'/learn?track='+lesson.track;$('nextlesson').textContent=next?'Next lesson →':'Back to this learning path →';const solutions=await api('solutions');$('solution').textContent=solutions[quest];await api('start',{quest});await refreshLessonState();await loadLessonHistory(true);}
}catch(e){error(e)}})();

async function refreshLessonState(){
 if(playground)return;
 const progress=await api('progress');
 const done=progress.completed.some(item=>item.quest===quest);
 const latest=progress.recent.find(item=>item.quest===quest);
 const retry=latest?.result&&!latest.result.passed;
 $('lessonstate').textContent=done?(retry?'Previously completed · latest turn-in needs revision':'✓ Lesson completed'):'Lesson not yet completed';
 $('lessonstate').classList.toggle('completed',done&&!retry);
 $('nextlesson').classList.toggle('completednext',done);
}
function setLessonTab(tab){
 const history=tab==='history';
 $('descriptionpanel').hidden=history;$('historypanel').hidden=!history;
 $('descriptiontab').setAttribute('aria-selected',String(!history));$('historytab').setAttribute('aria-selected',String(history));
 $('descriptiontab').tabIndex=history?-1:0;$('historytab').tabIndex=history?0:-1;
 if(history)loadLessonHistory(true).catch(error);
}
$('descriptiontab').onclick=()=>setLessonTab('description');$('historytab').onclick=()=>setLessonTab('history');
for(const id of ['descriptiontab','historytab'])$(id).onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const target=id==='descriptiontab'?'historytab':'descriptiontab';setLessonTab(target==='historytab'?'history':'description');$(target).focus()}};
async function loadLessonHistory(reset=false){
 if(playground)return;
 const request=++lessonHistoryRequest;
 if(reset)historyOffset=0;
 const data=await api(`submissions?quest=${quest}&offset=${historyOffset}`);
 if(request!==lessonHistoryRequest)return;
 if(reset)$('lessonhistorylist').replaceChildren();
 historyCount=data.total;$('historytab').textContent=`History (${data.total})`;
 $('lessonhistorycount').textContent=data.total?`${data.total} saved turn-in${data.total===1?'':'s'}`:'No answers turned in yet. Your saved submissions will appear here.';
 for(const attempt of data.submissions){
  const button=document.createElement('button');button.className='attemptbutton';button.dataset.id=attempt.id;
  const status=attempt.result?(attempt.result.passed?'Completed':'Needs revision'):'Grading';
  button.textContent=`Attempt ${attempt.attempt} · ${status}\n${new Date(attempt.created_at).toLocaleString()}`;
  button.onclick=()=>openAttempt(attempt.id);$('lessonhistorylist').append(button);
 }
 historyOffset+=data.submissions.length;$('olderattempts').hidden=historyOffset>=data.total;
}
async function openAttempt(id){
 historySelection=id;
 try{const attempt=await api('submissions/'+id);if(historySelection!==id)return;
  $('attemptdetail').hidden=false;$('attempttitle').textContent=`Attempt ${attempt.attempt}`;
  $('attemptstatus').textContent=`${new Date(attempt.created_at).toLocaleString()} · ${attempt.result?(attempt.result.passed?'Completed':'Needs revision'):'Waiting for grading'}`;
  $('attemptcode').textContent=attempt.source;$('attemptfeedback').textContent=attempt.result?.feedback||'Still grading. Select this attempt again in a moment.';$('attemptoutput').textContent=attempt.result?.output||'(no output)';
  $('attemptreview').href='/parent/submissions/'+id;
  document.querySelectorAll('.attemptbutton').forEach(button=>button.classList.toggle('selected',button.dataset.id===id));
 }catch(e){error(e)}
}
$('olderattempts').onclick=()=>loadLessonHistory().catch(error);
window.addEventListener('pageshow',event=>{if(event.persisted&&ready&&!playground){refreshLessonState().catch(error);loadLessonHistory(true).catch(error)}});
window.addEventListener('focus',()=>{if(ready&&!playground)refreshLessonState().catch(error)});
