/* Pure diagram edits shared by native drag/drop and the keyboard/touch fallback. */
(function(root){
 function contact(value){if(!value||!['SW1','SW2'].includes(value.input)||!['NO','NC'].includes(value.contact))throw Error('Choose SW1 or SW2 and a normally open or closed contact.');return {input:value.input,contact:value.contact}}
 function edit(original,payload,target){
  if(!original||!Array.isArray(original.branches)||!payload||!target)throw Error('Choose a toolbox item and a drop zone.');
  const program=JSON.parse(JSON.stringify(original));let moved=null,fromBranch=null,destination={...target};
  if(payload.type==='coil'||payload.type==='move-coil'){
   if(target.type==='coil'){program.coil='LAMP';return program}
   if(target.type==='trash'&&payload.type==='move-coil'){program.coil=null;return program}
   throw Error('Drop the lamp coil in its output box, or move an existing coil to the bin.');
  }
  if(payload.type==='move'){
   if(!Number.isInteger(payload.path)||!Number.isInteger(payload.index)||!program.branches[payload.path]?.[payload.index])throw Error('That contact has moved. Pick it up again.');
   fromBranch=program.branches[payload.path];moved=contact(fromBranch[payload.index]);fromBranch.splice(payload.index,1);
   if(destination.type==='slot'&&destination.path===payload.path&&destination.index>payload.index)destination.index--;
  }else if(payload.type==='contact')moved=contact(payload);
  else throw Error('This toolbox item is not supported.');
  if(destination.type==='trash'){
   if(payload.type!=='move')throw Error('Drag an existing contact to the bin to remove it.');
  }else if(destination.type==='parallel')program.branches.push([moved]);
  else if(destination.type==='slot'){
   const branch=program.branches[destination.path];
   if(!Number.isInteger(destination.path)||!branch||!Number.isInteger(destination.index)||destination.index<0||destination.index>branch.length)throw Error('Drop on a dashed gap between contacts.');
   branch.splice(destination.index,0,moved);
  }else throw Error('Contacts go on a path; coils go in the output box.');
  if(fromBranch&&!fromBranch.length)program.branches=program.branches.filter(branch=>branch!==fromBranch);
  if(program.branches.length>4)throw Error('This practice rung supports up to four parallel paths.');
  if(program.branches.some(branch=>branch.length>4))throw Error('This practice path supports up to four contacts.');
  return program;
 }
 const api={edit};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.LadderModel=api;
})(typeof window!=='undefined'?window:globalThis);
