const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const root=process.argv[2]||'app';const browser=await chromium.launch({channel:'chrome'});const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://**/*',r=>r.abort());await page.route('http://**/*',r=>r.abort());await page.goto(require('url').pathToFileURL(path.resolve(root,'meta-regression/index.html')).href);
 const corpus=JSON.parse(fs.readFileSync('data/corpus.json','utf8'));let checks=[];
 for(const k of [3,4]){
  const c=corpus.find(c=>c.k===k);await page.evaluate(c=>{document.getElementById('f-scale').checked=true;window.__almLoad(c.rows)},c);
  const result=await page.evaluate(()=>({k:window.__almResults().k,fit:!!window._almLastFitted(),ls:!!window.__almLocScale(),perm:window._almLastPerm(),bubbles:document.querySelectorAll('#svg-host circle').length}));
  checks.push({name:`k=${k} computation and plot`,pass:result.k===k&&result.fit&&result.bubbles===k&&result.ls===(k>=4)&&!!result.perm===(k>=4),actual:result});
 }
 const example=corpus.find(c=>c.id==='dat.bcg/e1/ablat');await page.evaluate(c=>{document.getElementById('f-scale').checked=false;document.getElementById('f-title').value='BCG studies: absolute latitude';document.getElementById('f-modlabel').value='Absolute latitude (degrees)';document.getElementById('f-effectlabel').value='Log risk ratio';window.__almLoad(c.rows)},example);
 await page.screenshot({path:'outputs/ui-smoke.png',fullPage:true});
 await page.evaluate(c=>window.__almLoad(c.rows.slice(0,2)),example);
 const state=await page.evaluate(()=>({fit:window._almLastFitted(),pi:window._almLastPI(),perm:window._almLastPerm()}));
 checks.push({name:'k=2 refusal clears results',pass:state.fit===null&&state.pi===null&&state.perm===null,actual:state});
 checks.push({name:'no page errors',pass:errors.length===0,actual:errors});
 fs.writeFileSync('results/ui-smoke.json',JSON.stringify(checks,null,2));await browser.close();assert(checks.every(c=>c.pass),JSON.stringify(checks));console.log(`${checks.filter(c=>c.pass).length}/${checks.length} UI contracts pass (${root})`);
})().catch(e=>{console.error(e);process.exit(1)});
