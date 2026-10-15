const fs = require('fs'),path=require('path');
const {chromium}=require('<PLAYWRIGHT_MODULE>');
const root=process.argv[2]||'original', output=process.argv[3]||'app.jsonl';
(async()=>{
 const corpus=JSON.parse(fs.readFileSync('corpus.json','utf8'));
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const context=await browser.newContext();const page=await context.newPage();
 await page.route('https://**/*',r=>r.abort());await page.route('http://**/*',r=>r.abort());
 let errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(require('url').pathToFileURL(path.resolve(root,'meta-regression/index.html')).href);
 await page.waitForFunction(()=>typeof window.__almLoad==='function');
 const done=new Set(fs.existsSync(output)?fs.readFileSync(output,'utf8').trim().split('\n').filter(Boolean).map(l=>JSON.parse(l).id):[]);
 if(!fs.existsSync(output))fs.writeFileSync(output,'');
 for(let i=0;i<corpus.length;i++){
  const c=corpus[i];if(done.has(c.id))continue;errors=[];
  try{
   const r=await page.evaluate(c=>{
    document.getElementById('f-scale').checked=c.k>=4;
    window.__almLoad(c.rows);
    const f=window._almLastFitted(),hk=window._almLastHK();
    const stats=Array.from(document.querySelectorAll('.stat')).map(e=>({label:e.querySelector('.k').textContent,value:e.querySelector('.v').textContent}));
    const svg=document.querySelector('#svg-host svg')||Array.from(document.querySelectorAll('svg')).find(s=>s.querySelectorAll('circle').length===c.k);
    const ls=window.__almLocScale();
    const pi=window._almLastPI();const out=window.__almResults();
    return {id:c.id,main:f?{beta:[out.intercept,out.slope],se:[out.intercept_se,out.slope_se],ci_lb:[out.intercept_ci_lb,out.slope_ci_lb],ci_ub:[out.intercept_ci_ub,out.slope_ci_ub],tau2:out.tau2_pm,R2:out.R2_tau2,QE:out.QE,QE_p:out.QE_p,q:out.hksj_q,df:out.hksj_q_df,pred:pi?.pred,pred_se:pi?.se,pi_lb:pi?.lo,pi_ub:pi?.hi}: {error:'page did not fit'},fitted:f,hk,ls,permutation:window._almLastPerm(),stats,svg:svg?{circles:Array.from(svg.querySelectorAll('circle')).map(e=>['cx','cy','r'].map(a=>+e.getAttribute(a))),line:svg.querySelector('polyline')?.getAttribute('points'),band:svg.querySelector('polygon')?.getAttribute('points')}:null,parsed:window._almLastStudies().length};
   },c);
   r.pageErrors=errors;fs.appendFileSync(output,JSON.stringify(r)+'\n');
  }catch(e){fs.appendFileSync(output,JSON.stringify({id:c.id,error:e.message,pageErrors:errors})+'\n');}
  if((i+1)%25===0)console.log(`${i+1}/${corpus.length} app configurations`);
 }
 await page.screenshot({path:output+'.png',fullPage:true});await browser.close();
 console.log(`${corpus.length} app configurations recorded (${root})`);
})().catch(e=>{console.error(e);process.exit(1)});
