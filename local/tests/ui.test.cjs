const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const staticDir=path.join(__dirname,'../app/static');
function elements(){const map=new Map();return {map,get(id){if(!map.has(id))map.set(id,{hidden:false,textContent:'',innerHTML:'',children:[],className:'',attributes:{},setAttribute(key,value){this.attributes[key]=value},classList:{toggle(){}},focus(){}});return map.get(id)}}}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
(async()=>{
 const dom=elements(),events={},documentEvents={};let state={completed:[]},fetches=0;
 const lessons=JSON.parse(fs.readFileSync(path.join(__dirname,'../app/lessons.json'),'utf8'));
 const context={document:{getElementById:id=>dom.get(id),hidden:false,addEventListener:(name,handler)=>documentEvents[name]=handler},window:{addEventListener:(name,handler)=>events[name]=handler,history:{replaceState(){}}},location:{search:''},URLSearchParams,Set,fetch:async(route,options)=>{assert.equal(options.cache,'no-store');fetches++;return{ok:true,json:async()=>route.endsWith('lessons')?{lessons}:state}}};
 vm.runInNewContext(fs.readFileSync(path.join(staticDir,'learn.js'),'utf8'),context);await tick();await tick();
 for(const name of ['Beginner','Intermediate','Advanced','Algorithms','Data Structures','PLC'])assert.ok(dom.get('tracktabs').innerHTML.includes(name));
 assert.ok(dom.get('chapters').innerHTML.includes('Hello, explorer! · Ready to start'));
 const before=fetches;state={completed:[{quest:1}]};events.pageshow({persisted:true});await tick();await tick();
 assert.ok(fetches>before,'Returning from browser cache must fetch current progress');
 assert.ok(dom.get('chapters').innerHTML.includes('Hello, explorer! · Completed'));
 assert.ok(dom.get('total').textContent.includes('1 / 25'));
 console.log('PASS: six home tabs and completion refresh after back navigation');

 const student=fs.readFileSync(path.join(staticDir,'student.js'),'utf8');
 const banner=student.slice(student.indexOf('function showSubmissionBanner('),student.indexOf("$('bannerclose').onclick"));
 const notifications={...context,$:id=>dom.get(id),lastSubmissionId:null};
 vm.createContext(notifications);vm.runInContext(banner,notifications);
 vm.runInContext('showSubmissionBanner("correct","Great job","Saved")',notifications);
 assert.equal(dom.get('submissionbanner').className,'submissionbanner correct');assert.equal(dom.get('submissionbanner').attributes.role,'status');assert.equal(dom.get('bannerhistory').hidden,true);
 notifications.lastSubmissionId='saved-id';vm.runInContext('showSubmissionBanner("incorrect","Try again","Use an f-string")',notifications);
 assert.equal(dom.get('submissionbanner').attributes.role,'alert');assert.equal(dom.get('bannermessage').textContent,'Use an f-string');assert.equal(dom.get('bannerhistory').hidden,false);
 console.log('PASS: correct/incorrect banners, accessible result roles, saved-attempt link');

 const tabFunction=student.slice(student.indexOf('function setLessonTab('),student.indexOf("$('descriptiontab').onclick"));
 const tabs={$:id=>dom.get(id),loadLessonHistory:()=>Promise.resolve(),error:()=>{}};
 dom.get('editor').value='my unsaved idea';vm.createContext(tabs);vm.runInContext(tabFunction,tabs);vm.runInContext('setLessonTab("history")',tabs);
 assert.equal(dom.get('descriptionpanel').hidden,true);assert.equal(dom.get('historypanel').hidden,false);assert.equal(dom.get('editor').value,'my unsaved idea');
 console.log('PASS: Description/History tabs preserve the editor');
})().catch(error=>{console.error(error);process.exitCode=1});
