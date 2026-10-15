const fs=require('fs');
const original=require('./original/shared/permutest.js');
const patched=require('./patched/shared/permutest.js');
const c=JSON.parse(fs.readFileSync('corpus.json','utf8')).find(c=>c.id==='dat.hart1999/e1/year');
const y=c.rows.map(r=>r.yi),v=c.rows.map(r=>Math.sqrt(r.vi)**2),x=c.rows.map(r=>r.x);
const ot=original._slopeT(y,v,x),pt=patched._slopeT(y,v,x),changes=[];
function enumerate(a,i=0){
 if(i===a.length){
  const o=original._slopeT(y,v,a),p=patched._slopeT(y,v,a);
  const og=Math.abs(o)>=Math.abs(ot)-1e-10,pg=Math.abs(p)>=Math.abs(pt)-1e-10;
  if(og!==pg)changes.push({moderators:a.slice(),original_t:o,patched_t:p,original_distance_from_observed:Math.abs(o)-Math.abs(ot),patched_distance_from_observed:Math.abs(p)-Math.abs(pt),original_counted:og,patched_counted:pg});
  return;
 }
 for(let j=i;j<a.length;j++){[a[i],a[j]]=[a[j],a[i]];enumerate(a,i+1);[a[i],a[j]]=[a[j],a[i]];}
}
enumerate(x.slice());
const result={id:c.id,original:original.permTestSlope(y,v,x,{exactMax:7}),patched:patched.permTestSlope(y,v,x,{exactMax:7}),changed_classifications:changes};
fs.writeFileSync('permutation-diagnostic.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
