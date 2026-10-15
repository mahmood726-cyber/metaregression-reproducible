"""Strict, keyed recreation of the historical comparison; no missing-value defaults."""
import json, math
from pathlib import Path

N=1742
MAIN=['beta','se','ci_lb','ci_ub','tau2','R2','QE','QE_p','q','df','pred','pred_se','pi_lb','pi_ub']
STRUCT={'record_present','no_page_error','fit_status','parsed_rows'}
def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('Duplicate JSON key: '+k)
        out[k]=v
    return out
def loads(s):return json.loads(s,object_pairs_hook=unique,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('Nonfinite JSON '+s)))
def read(p):return loads(Path(p).read_text(encoding='utf-8'))
def indexed(records,n=None,ids=None):
    assert isinstance(records,list) and (n is None or len(records)==n),'Record cardinality'
    out={}
    for r in records:
        assert isinstance(r,dict) and isinstance(r['id'],str) and r['id'],'Record ID'
        assert r['id'] not in out,'Duplicate record ID'
        out[r['id']]=r
    assert ids is None or set(out)==set(ids),'Record coverage'
    return out
def finite(x):return type(x) in (int,float) and math.isfinite(x)
def num(x,nullable=False):
    assert finite(x) or (nullable and x is None),'Numeric type/nonfinite'
    return x
def vector(x,n,nullable=False):
    assert isinstance(x,list) and len(x)==n,'Vector cardinality'
    for v in x:num(v,nullable)
    return x
def seq(x):return x if isinstance(x,list) else [x]
def difference(a,b,absolute=False,nullable=False,boolean=False):
    if boolean:
        assert type(a) is bool and type(b) is bool,'Boolean type'
        return int(a!=b)
    num(a,nullable);num(b,nullable)
    if a is None or b is None:return 0 if a is b and nullable else math.inf
    return abs(a-b)/(1 if absolute else max(1,abs(b)))
def group(q):
    return 'LS experimental' if q.startswith('LS_') else 'structural' if q in STRUCT else 'bubble' if q.startswith('bubble_') else 'exact permutation' if q.startswith('exact_') else 'model'
def cards(a):
    assert isinstance(a['stats'],list),'Stats array'
    out={}
    for v in a['stats']:
        assert isinstance(v['label'],str) and isinstance(v['value'],str) and v['label'] not in out,'Card shape/duplicate'
        out[v['label']]=v['value']
    return out
def display(cs,ls=False):
    vals=[v for k,v in cs.items() if (k.startswith('LS α') and 'slope' in k) if ls] if ls else [v for k,v in cs.items() if 'test' in k and 'β' in k]
    assert len(vals)==1,'Missing/duplicate p-value card'
    s=vals[0].split('p = ')
    assert len(s)==2,'Malformed p card'
    if ls and s[1]=='--':return None  # page's explicit undefined scale-SE display
    return num(float(s[1]))
def shape(c,a,r):
    k=c['k'];assert type(k) is int and k>=3 and len(c['rows'])==k
    for row in c['rows']:
        for q in ['yi','vi','x']:num(row[q])
        assert row['vi']>0
    assert len({x['x'] for x in c['rows']})>1
    assert isinstance(a['pageErrors'],list) and type(a['parsed']) is int
    assert r['k']==k
    for m in [a['main'],r['main']]:
        for q in MAIN:
            vector(m[q],2) if q in MAIN[:4] else num(m[q])
        assert all(v>0 for v in m['se'])
    for q in ['t','p']:vector(r['main'][q],2)
    for q in ['pred','lo','hi','x']:vector(r['main']['band'][q],201)
    svg=a['svg'];assert isinstance(svg,dict)
    assert isinstance(svg['circles'],list) and len(svg['circles'])==k
    for p in svg['circles']:vector(p,3)
    for q,n in [('line',201),('band',402)]:
        assert isinstance(svg[q],str) and len(svg[q].split())==n,'SVG sample coverage'
        for p in svg[q].split():vector([float(z) for z in p.split(',')],2)
    return k
def compare(corpus,app,reference,perms,include_ls=True):
    assert len(corpus)==N and set(corpus)==set(app)==set(reference),'Exact configuration coverage'
    assert set(perms)=={i for i,c in corpus.items() if 4<=c['k']<=7} and len(perms)==365,'Permutation coverage'
    rows=[];counts={}
    def check(id,q,a,b,tol=1e-9,absolute=False,nullable=False,boolean=False):
        ix=counts.get((id,q),0);counts[id,q]=ix+1
        d=difference(a,b,absolute,nullable,boolean)
        rows.append(dict(configuration=id,quantity=q,index=ix,group=group(q),app=a,reference=b,difference=d,tolerance=tol,passed=d<=tol))
    for id,c in corpus.items():
        a=app[id];r=reference[id];k=shape(c,a,r);cs=cards(a);ar=a['main'];rr=r['main']
        check(id,'record_present',True,True,0,boolean=True)
        check(id,'no_page_error',not a['pageErrors'] and 'error' not in a,True,0,boolean=True)
        check(id,'fit_status','error' not in ar and 'error' not in a,'error' not in rr,0,boolean=True)
        for q in MAIN:
            for av,rv in zip(seq(ar[q]),seq(rr[q])):check(id,q,av,rv,absolute=q.endswith('_p'))
        check(id,'parsed_rows',a['parsed'],k,0)
        check(id,'slope_t',ar['beta'][1]/ar['se'][1],rr['t'][1])
        check(id,'slope_p_display',display(cs),round(rr['p'][1],3),0,True)
        svg=a['svg'];check(id,'bubble_count',len(svg['circles']),k,0)
        lo=min(x['yi']-1.959963984540054*math.sqrt(x['vi']) for x in c['rows']);hi=max(x['yi']+1.959963984540054*math.sqrt(x['vi']) for x in c['rows']);pad=(hi-lo)*.1;lo-=pad;hi+=pad
        inv=lambda p:hi-(float(p.split(',')[1])-60)/380*(hi-lo)
        line=svg['line'].split();band=svg['band'].split()
        for j in [0,100,200]:
            check(id,'bubble_line',inv(line[j]),rr['band']['pred'][j])
            check(id,'bubble_ci',inv(band[j]),rr['band']['hi'][j])
            check(id,'bubble_ci',inv(band[-1-j]),rr['band']['lo'][j])
        maxw=max(1/x['vi'] for x in c['rows'])
        for s,p in zip(c['rows'],svg['circles']):check(id,'bubble_radius',p[2],4+10/s['vi']/maxw)
        if include_ls and k>=4:
            al=a['ls'];rl=r['ls'];assert al is None or isinstance(al,dict)
            assert isinstance(rl,dict)
            check(id,'LS_fit_status',bool(al) and 'error' not in a,'error' not in rl,0,boolean=True)
            if al and 'error' not in rl and 'error' not in a:
                for q in ['beta','betaSE','alpha','alphaSE','logLik','tau2']:
                    size=k if q=='tau2' else 1 if q=='logLik' else 2
                    for m in [al,rl]:vector(seq(m[q]),size,nullable=q in ['betaSE','alphaSE'])
                    for av,rv in zip(seq(al[q]),seq(rl[q])):check(id,'LS_'+q,av,rv,1e-6,nullable=q in ['betaSE','alphaSE'])
                for j in range(2):
                    for q,sgn in [('beta_lb',-1),('beta_ub',1)]:
                        vector(rl[q],2,True)
                        v=al['beta'][j]+sgn*1.959963984540054*al['betaSE'][j] if al['betaSE'][j] is not None else None
                        check(id,'LS_'+q,v,rl[q][j],1e-6,nullable=True)
                vector(rl['alpha_p'],2,True);v=rl['alpha_p'][1]
                check(id,'LS_alpha_p_display',display(cs,True),round(v,3) if v is not None else None,0,True,True)
                for q,fn in [('tau2_min',min),('tau2_max',max)]:check(id,'LS_'+q,fn(seq(al['tau2'])),fn(seq(rl['tau2'])),1e-6)
        if 4<=k<=7:
            pr=perms[id]['result'];pa=a['permutation'];assert isinstance(pa,dict) and isinstance(pr,dict)
            assert pa['exact'] is True and type(pr['exact']) is int and pr['exact']>0
            check(id,'exact_permutation_record',True,True,0,boolean=True)
            check(id,'exact_permutation_status',bool(pa),'error' not in pr,0,boolean=True)
            check(id,'exact_permutation_p',pa['p'],pr['p'],absolute=True)
    assert len({key(x) for x in rows})==len(rows),'Duplicate comparison key'
    assert sum(x['group']!='LS experimental' for x in rows)==129903,'Check coverage'
    return rows
def key(r):return (r['configuration'],r['quantity'],r['index'])
def documented(rows,expected):
    failures={key(r) for r in rows if not r['passed'] and r['group']!='LS experimental'}
    pins=[key(r) for r in expected]
    assert len(pins)==len(set(pins))==36,'Documented keys cardinality'
    assert failures==set(pins),'Unexpected, disappeared or changed documented differences'
def summarize(rows):
    out={}
    for r in rows:
        s=out.setdefault(r['quantity'],dict(checks=0,passed=0,max_difference=0,tolerance=r['tolerance'],group=r['group']))
        s['checks']+=1;s['passed']+=r['passed'];s['max_difference']=max(s['max_difference'],r['difference'])
    return out
def inputs(root):
    c=indexed(read(root/'data/corpus.json'),N)
    return c,indexed(read(root/'results/app.json'),N,c),indexed(read(root/'results/patched-app.json'),N,c),indexed(read(root/'results/reference.json'),N,c),indexed(read(root/'results/permutation.json'),365)
