"""Recompute publication artifacts from full-precision evidence, never expected totals."""
import csv,json,math,sys
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
from scipy.stats import t
from checks import *

ROOT=Path(__file__).resolve().parents[1]
def safe(x):
    if isinstance(x,float) and not math.isfinite(x):return 'Infinity' if x>0 else '-Infinity'
    if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
    if isinstance(x,list):return [safe(v) for v in x]
    return x
def dump(p,x):p.write_text(json.dumps(safe(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def csvwrite(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def csvread(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def centered_value(row,center,c,ref):
    q=row['quantity'];i=row['index'];m=center['main']
    if q in m:return seq(m[q])[i]
    assert q in ['bubble_line','bubble_ci']
    j=[0,100,200][i if q=='bubble_line' else i//2];x=ref['main']['band']['x'][j]
    pred=m['beta'][0]+m['beta'][1]*x
    if q=='bubble_line':return pred
    weights=[1/(s['vi']+m['tau2']) for s in c['rows']];sw=sum(weights);mx=sum(w*s['x'] for w,s in zip(weights,c['rows']))/sw
    sxx=sum(w*(s['x']-mx)**2 for w,s in zip(weights,c['rows']))
    se=math.sqrt(m['q']*(1/sw+(x-mx)**2/sxx));crit=t.ppf(.975,c['k']-2)
    return float(pred+(1 if i%2==0 else -1)*crit*se)
def figures(out,rows,before,n):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':10,'axes.labelsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8})
    stats=summarize(rows);old=summarize(before)
    fig,axes=plt.subplots(2,1,figsize=(170/25.4,8.4),gridspec_kw={'height_ratios':[1.6,1]})
    for ax,isls in zip(axes,[False,True]):
        qs=[q for q,s in stats.items() if q.startswith('LS_')==isls and s['tolerance']>0]
        for j,q in enumerate(qs):
            s=stats[q];b=old[q];tol=s['tolerance'];y=math.log10(max(s['max_difference'],1e-16)) if math.isfinite(s['max_difference']) else 6.5;yb=math.log10(max(b['max_difference'],1e-16)) if math.isfinite(b['max_difference']) else 6.5
            if not math.isfinite(s['max_difference']) or not math.isfinite(b['max_difference']):ax.text(6.1,j,'inf',ha='right',va='center',fontsize=8)
            ax.scatter(y,j,color='#24658a',s=22,zorder=3)
            ax.scatter(yb,j,marker='x' if b['max_difference']>tol else '+',color='#bc552c',s=30,zorder=3)
            ax.plot([math.log10(tol)]*2,[j-.4,j+.4],color='#555',ls='--',lw=1)
        ax.set_yticks(range(len(qs)),qs);ax.invert_yaxis();ax.set_xlim(-16.5,7);ax.grid(axis='x',alpha=.2)
        ax.set_xlabel('log10 maximum normalized difference (p-values: absolute)')
        ax.set_title('Experimental location-scale: reported separately' if isls else 'Main model, bubble plot and exact permutation')
    fig.suptitle('Browser versus metafor: agreement by quantity',fontsize=11)
    fig.text(.5,.015,'Blue dots: after fixes; orange crosses: before fixes (× exceeds tolerance).\nDashed: tolerances. Values below 1e-16 at -16; inf at right edge. Exact checks: Table 1.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.06,1,.96));savefig(fig,out,'figure2_agreement');plt.close(fig)
    fig=plt.figure(figsize=(170/25.4,3.8))
    boxes=[('Problem','Can a browser\nreproduce random-effects\nmeta-regression\nwith R precision?'),('Tool','One numeric moderator\nPaule–Mandel\nFloored Knapp–Hartung\nOffline allmeta'),('Validation',f'{n["datasets_used"]["value"]} metadat datasets\n{n["configurations"]["value"]:,} configurations\nR package metafor\nExact tests for k = 4–7'),('Result',f'{n["passed"]["value"]:,} of {n["checks"]["value"]:,}\nchecks pass;\n{n["documented_checks"]["value"]} documented\nconditioning differences')]
    for i,(head,body) in enumerate(boxes):
        x=.02+i*.245;fig.patches.append(FancyBboxPatch((x,.25),.22,.52,boxstyle='round,pad=0.008',transform=fig.transFigure,facecolor=['#f4ece8','#e8f0f7','#eaf4ec','#fdf6e3'][i],edgecolor='#999'))
        fig.text(x+.11,.70,head,ha='center',weight='bold',fontsize=10);fig.text(x+.11,.49,body,ha='center',va='center',fontsize=8,linespacing=1.6)
    fig.text(.5,.89,'Random-effects meta-regression in the browser',ha='center',fontsize=11,weight='bold')
    fig.text(.5,.13,'Computational stress test; moderator choice is not a scientific recommendation.',ha='center',fontsize=8)
    fig.text(.5,.07,'Experimental location-scale does not agree with metafor and is excluded above.',ha='center',fontsize=8)
    savefig(fig,out,'visual_abstract');plt.close(fig)
def savefig(fig,out,name):
    for ext in ['png','tif']:fig.savefig(out/f'{name}.{ext}',dpi=300)
def build(out=ROOT/'outputs'):
    out.mkdir(parents=True,exist_ok=True);c,b,a,r,p=inputs(ROOT)
    rows=compare(c,a,r,p);before=compare(c,b,r,p);stats=summarize(rows);old=summarize(before)
    documented(rows,read(ROOT/'expected/documented_differences.json'))
    for ss,name in [(stats,'results-patched.json'),(old,'results-original.json')]:
        ledger=read(ROOT/'results'/name)
        assert set(ss)==set(ledger['quantities'])
        for q,s in ss.items():
            orig=ledger['quantities'][q]
            assert s['checks']==orig['checks'] and s['passed']==orig['passing'],q
            assert s['max_difference']==orig['max_difference'] or (math.isinf(s['max_difference']) and orig['max_difference']=='inf'),q
    table=[dict(quantity=q,group=s['group'],checks=s['checks'],passed_before=old[q]['passed'],passed_after=s['passed'],largest_difference=s['max_difference'],largest_difference_before=old[q]['max_difference'],tolerance=s['tolerance']) for q,s in stats.items()]
    for g in ['model','bubble','exact permutation','structural','non-LS total','LS experimental']:
        rr=[x for x in rows if (x['group']!='LS experimental' if g=='non-LS total' else x['group']==g)];bb=[x for x in before if (x['group']!='LS experimental' if g=='non-LS total' else x['group']==g)]
        table.append(dict(quantity='TOTAL '+g,group=g,checks=len(rr),passed_before=sum(x['passed'] for x in bb),passed_after=sum(x['passed'] for x in rr),largest_difference=max(x['difference'] for x in rr),largest_difference_before=max(x['difference'] for x in bb),tolerance='quantity-specific'))
    csvwrite(out/'table1_by_quantity.csv',table)
    failed=[x for x in rows if not x['passed'] and x['group']!='LS experimental'];fids={x['configuration'] for x in failed}
    centered=indexed([loads(s) for s in (ROOT/'results/centered-reference.jsonl').read_text(encoding='utf-8').splitlines()],14,fids)
    table2=[]
    for row in failed:
        cr=centered_value(row,centered[row['configuration']],c[row['configuration']],r[row['configuration']])
        table2.append(dict(row,centered_reference=cr,centered_difference=difference(row['app'],cr,absolute=row['quantity'].endswith('_p')),centered_method='archived centered/scaled fit; bubble bands reconstructed from fitted tau2/q and design'))
    csvwrite(out/'table2_differences.csv',table2)
    n={}
    def add(k,v,source,transform='identity',kind='measured'):n[k]=dict(value=v,source=source,transformation=transform,kind=kind)
    audit=read(ROOT/'data/dataset-audit-final.json');recipes=read(ROOT/'data/effect-recipes.json')
    assert {v['dataset'] for v in c.values()}=={k for k,v in audit.items() if v['configurations']>0}
    assert {v['effect'] for v in c.values()}<=set(recipes)
    for k,v in [('datasets_screened',len(audit)),('datasets_used',len({v['dataset'] for v in c.values()})),('effect_definitions',len({v['effect'] for v in c.values()})),('configurations',len(c))]:add(k,v,'data/corpus.json + dataset-audit-final.json + effect-recipes.json','count unique retained entities')
    for g in ['model','bubble','exact permutation','structural','non-LS total','LS experimental']:
        s=next(x for x in table if x['quantity']=='TOTAL '+g);prefix={'non-LS total':'','LS experimental':'LS_','exact permutation':'permutation_'}.get(g,g+'_')
        for col,k in [('checks','checks'),('passed_after','passed'),('passed_before','before_passed')]:add(prefix+k,s[col],'corpus + reference + before/after app evidence','strict per-check comparison; sum '+g)
    add('LS_alpha_passed',stats['LS_alpha']['passed'],'recomputed LS_alpha checks','sum passed');add('LS_alpha_checks',stats['LS_alpha']['checks'],'recomputed LS_alpha checks','count')
    add('permutation_configurations',len(p),'results/permutation.json','unique IDs')
    for k,v in [('documented_checks',len(failed)),('documented_configurations',len(fids)),('year_configurations',sum(c[i]['moderator']=='year' for i in fids)),('difference_min',min(x['difference'] for x in failed)),('difference_max',max(x['difference'] for x in failed))]:add(k,v,'recomputed non-LS failures','count or extrema')
    ds=[]
    for id,cr in centered.items():
        for q,v in cr['main'].items():
            av=a[id]['main'][q] if q!='slope_t' else a[id]['main']['beta'][1]/a[id]['main']['se'][1]
            for avv,rv in zip(seq(av),seq(v)):ds.append(difference(avv,rv,absolute=q.endswith('_p')))
    add('centered_max',max(ds),'centered-reference.jsonl + patched-app.json','maximum across all recorded centered diagnostics')
    assert max(x['centered_difference'] for x in table2)<3e-11
    bcg=r['dat.bcg/e1/ablat']['main']
    for k,q,i,scale in [('slope','beta',1,1),('ci_lower','ci_lb',1,1),('ci_upper','ci_ub',1,1),('slope_p','p',1,1),('tau2','tau2',0,1),('R2_percent','R2',0,100),('QE','QE',0,1),('df','df',0,1),('QE_p','QE_p',0,1)]:add('usecase_'+k,seq(bcg[q])[i]*scale,'results/reference.json: dat.bcg/e1/ablat.main.'+q,'select and scale')
    for k,v in read(ROOT/'results/versions.json').items():add('version_'+k,v,'results/versions.json',kind='source metadata')
    provenance=read(ROOT/'results/provenance.json')
    for k in ['commit','pull_request']:add(k,provenance[k],'results/provenance.json',kind='static source provenance')
    expected=read(ROOT/'expected/paper_values.json');report=['# Reproduction report','','Values below are recomputed; expected values are assertions.','','| Claim | Expected | Reproduced | Verdict |','|---|---|---|---|'];ok=0
    for k,e in expected.items():
        v=n[k]['value'];actual=round(v,e['digits']) if 'digits' in e else float(format(v,f'.{e["significant"]}g')) if 'significant' in e else v
        passed=actual==e['value'];ok+=passed;report.append(f'| {k} | {e["value"]} | {actual} | {"PASS" if passed else "FAIL"} |')
    dump(out/'numbers.json',n);dump(out/'ls_replay.json',dict(checks=n['LS_checks']['value'],passed=n['LS_passed']['value']))
    figures(out,rows,before,n)
    sizes={}
    for name in ['figure2_agreement','visual_abstract']:
        for ext in ['png','tif']:
            with Image.open(out/f'{name}.{ext}') as im:sizes[f'{name}.{ext}']=dict(width_pixels=im.width,height_pixels=im.height,dpi=[float(v) for v in im.info['dpi']])
    dump(out/'sizes.json',sizes)
    final=f'PASS: {ok}/{len(expected)} paper-value assertions; {n["passed"]["value"]}/{n["checks"]["value"]} non-LS checks; 36 documented differences; LS {n["LS_passed"]["value"]}/{n["LS_checks"]["value"]} (experimental).'
    report+=['','Centered refits diagnose conditioning; they do not replace the prespecified raw reference. Figures are 300 dpi, nominal 170 mm wide, text at least 8 pt. The browser UI is replayed historical evidence in the R command; main and experimental LS references and exact permutations are freshly computed. Publication LS totals here remain the historical run. No manuscript draft is distributed.','',final]
    (out/'reproduction_report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    assert ok==len(expected),'Paper values disagree'
    print(final);return rows,before
if __name__=='__main__':build()
