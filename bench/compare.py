import json, math, sys, collections
from pathlib import Path
def load(f):return {x['id']:x for x in map(json.loads,Path(f).read_text(encoding='utf-8').splitlines())}
refs=load('reference.jsonl'); apps=load(sys.argv[1] if len(sys.argv)>1 else 'app.jsonl')
perms={}
for p in [Path('permutation-reference.jsonl'),*sorted(Path('.').glob('permutation-[0-9].jsonl'))]:
 if p.exists():perms.update(load(p))
corpus={c['id']:c for c in json.loads(Path('corpus.json').read_text())}
stats={}; failures=[]
def check(q,a,b,id,tol=1e-9,absolute=False):
 s=stats.setdefault(q,dict(checks=0,passing=0,max_difference=0,tolerance=tol,worst=None))
 s['checks']+=1
 if isinstance(a,bool) or isinstance(b,bool):diff=0 if a==b else 1
 elif a is None or b is None:diff=0 if a is None and b is None else math.inf
 else:diff=abs(a-b)/(1 if absolute else max(1,abs(b))) if math.isfinite(a) and math.isfinite(b) else math.inf
 if diff<=tol:s['passing']+=1
 else:failures.append(dict(id=id,quantity=q,app=a,reference=b,difference=diff))
 if diff>s['max_difference']:s['max_difference']=diff;s['worst']=id
def seq(x):return x if isinstance(x,list) else [x]
def group(prefix,a,b,keys,id,tol):
 for key in keys:
  av,bv=seq(a.get(key)),seq(b.get(key))
  if len(av)!=len(bv):check(prefix+key+'_length',len(av),len(bv),id,0);continue
  for x,y in zip(av,bv):check(prefix+key,x,y,id,tol,absolute=key.endswith('_p'))
for id,c in corpus.items():
 a=apps.get(id,{});r=refs.get(id,{})
 check('record_present',bool(a) and bool(r),True,id,0)
 if not a or not r:continue
 check('no_page_error',not bool(a.get('pageErrors')) and 'error' not in a,True,id,0)
 ar=a.get('main',{});rr=r.get('main',{})
 check('fit_status',bool(ar) and 'error' not in ar and 'error' not in a,bool(rr) and 'error' not in rr,id,0)
 if ar and rr and 'error' not in ar and 'error' not in rr and 'error' not in a:
  group('',ar,rr,['beta','se','ci_lb','ci_ub','tau2','R2','QE','QE_p','q','df','pred','pred_se','pi_lb','pi_ub'],id,1e-9)
  check('parsed_rows',a.get('parsed'),c['k'],id,0)
  # Full precision t is simple arithmetic on the page's exposed coefficient/SE.
  check('slope_t',ar['beta'][1]/ar['se'][1],rr['t'][1],id)
  cards={v['label']:v['value'] for v in a.get('stats',[])}
  slope=next((v for k,v in cards.items() if 'test' in k and 'β' in k),None)
  if slope:
   pv=float(slope.split('p = ')[1]);check('slope_p_display',pv,round(rr['p'][1],3),id,0,True)
  svg=a.get('svg');check('bubble_count',len(svg['circles']) if svg else None,c['k'],id,0)
  if svg and svg.get('line') and svg.get('band'):
   rows=c['rows'];yl=min(x['yi']-1.959963984540054*math.sqrt(x['vi']) for x in rows);yh=max(x['yi']+1.959963984540054*math.sqrt(x['vi']) for x in rows);pad=(yh-yl)*.1;yl-=pad;yh+=pad
   # Default example title gives T=60, plotting height=380.
   inv=lambda p:yh-(float(p.split(',')[1])-60)/380*(yh-yl)
   line=svg['line'].split();band=svg['band'].split();nr=min(len(line),201)
   for j in [0,nr//2,nr-1]:
    check('bubble_line',inv(line[j]),rr['band']['pred'][j],id)
    check('bubble_ci',inv(band[j]),rr['band']['hi'][j],id)
    check('bubble_ci',inv(band[-1-j]),rr['band']['lo'][j],id)
   maxw=max(1/x['vi'] for x in rows)
   for s,point in zip(rows,svg['circles']):check('bubble_radius',point[2],4+10/s['vi']/maxw,id)
 if c['k']>=4:
  al=a.get('ls');rl=r.get('ls',{})
  check('LS_fit_status',bool(al) and 'error' not in a,'error' not in rl,id,0)
  if al and 'error' not in rl and 'error' not in a:
   group('LS_',al,rl,['beta','betaSE','alpha','alphaSE','logLik'],id,1e-6)
   group('LS_',al,rl,['tau2'],id,1e-6)
   for j in range(2):
    for bound,sgn in [('beta_lb',-1),('beta_ub',1)]:
     v=al['beta'][j]+sgn*1.959963984540054*al['betaSE'][j] if al['beta'][j] is not None and al['betaSE'][j] is not None else None
     check('LS_'+bound,v,rl[bound][j],id,1e-6)
   cards={v['label']:v['value'] for v in a.get('stats',[])}
   ap=next((v for k,v in cards.items() if k.startswith('LS α') and 'slope' in k),None)
   if ap:
    try:pv=float(ap.split('p = ')[1])
    except ValueError:pv=None
    rv=rl.get('alpha_p',[None,None])[1]
    check('LS_alpha_p_display',pv,round(rv,3) if rv is not None else None,id,0,True)
   for name,fun in [('tau2_min',min),('tau2_max',max)]:
    check('LS_'+name,fun(seq(al['tau2'])) if all(x is not None for x in seq(al['tau2'])) else None,fun(seq(rl['tau2'])) if all(x is not None for x in seq(rl['tau2'])) else None,id,1e-6)
 if 4<=c['k']<=7:
  pr=perms.get(id);check('exact_permutation_record',bool(pr),True,id,0)
  if pr:
   pa=a.get('permutation');pb=pr['result'];check('exact_permutation_status',bool(pa),'error' not in pb,id,0)
   if pa and 'error' not in pb:check('exact_permutation_p',pa.get('p'),pb['p'],id,1e-9,True)
summary=dict(configurations=len(corpus),reference_records=len(refs),app_records=len(apps),quantities=stats,checks=sum(s['checks'] for s in stats.values()),passing=sum(s['passing'] for s in stats.values()),failures=failures)
for q,s in stats.items():print(f"{q}: {s['passing']}/{s['checks']} pass; max={s['max_difference']:.12g}; tolerance={s['tolerance']}")
print(f"{summary['passing']}/{summary['checks']} checks pass")
prefix=sys.argv[2] if len(sys.argv)>2 else 'results-original'
def safe(v):
 if isinstance(v,float) and not math.isfinite(v):return str(v)
 if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
 if isinstance(v,list):return [safe(x) for x in v]
 return v
Path(prefix+'.json').write_text(json.dumps(safe(summary),indent=2,allow_nan=False),encoding='utf-8')
