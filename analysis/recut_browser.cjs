// Replays the candidate's own browser panel; no estimator or tolerance changes.
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const manifest=JSON.parse(fs.readFileSync('validation-plus/MANIFEST-plus.json','utf8'));
let browser;
(async()=>{
 browser=await chromium.launch({channel:process.env.PW_CHANNEL||'msedge',headless:true});
 const page=await browser.newPage();page.setDefaultTimeout(120000);
 const errors=[],missing=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)missing.push({url:r.url(),status:r.status()});});
 await page.route('**/*',route=>new URL(route.request().url()).origin==='http://127.0.0.1:8000'?route.continue():route.abort());
 await page.goto('http://127.0.0.1:8000/meta-regression/index.html');
 await page.waitForFunction(()=>window.AlmMetaPlusValidation&&window.AlmMetaPlusUI);
 const snapshot=()=>page.evaluate(()=>({original:window._almLastFitted(),extras:window.AlmMetaPlusUI.snapshot()}));
 const before=await snapshot();
 const timeout=setTimeout(()=>{console.error('Extras browser replay exceeded 240 seconds');browser.close().finally(()=>process.exit(1));},240000);
 let result;
 try{result=await page.evaluate(()=>window.AlmMetaPlusValidation.runCorpus());}
 finally{clearTimeout(timeout);}
 assert.deepEqual(result.failed,[]);
 assert.equal(result.checks,manifest.checks);assert.equal(result.passed,manifest.checks);
 assert.deepEqual(await snapshot(),before);assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
 result.source_manifest_sha256=crypto.createHash('sha256').update(fs.readFileSync('SOURCE_SHA256.json')).digest('hex');
 fs.writeFileSync('outputs/recut/plus-browser.json',JSON.stringify(result,null,2)+'\n');
 console.log(result.passed+'/'+result.checks+' extras browser panel checks pass; input/result state restored; no page errors or missing resources');
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
