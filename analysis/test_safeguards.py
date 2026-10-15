"""Negative mutations of actual evidence: fail closed before aggregation."""
import copy,json,subprocess,tempfile
from pathlib import Path
import pytest
from checks import *
from verify_archive import verify_manifest,text_safety,source_files,verify_rtable

ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture(scope='module')
def evidence():return inputs(ROOT)
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),float('-inf'),'1',True,{},[]])
def test_non_numeric_rejected(bad):
    with pytest.raises(AssertionError):difference(bad,bad,nullable=True)
def test_explicit_null_only():
    assert difference(None,None,nullable=True)==0
    assert math.isinf(difference(None,1,nullable=True))
    with pytest.raises(AssertionError):difference(None,None)
@pytest.mark.parametrize('s',['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'])
def test_json_invalid(s):
    with pytest.raises(ValueError):loads(s)
@pytest.mark.parametrize('records,n,ids',[([{'id':'a'},{'id':'a'}],2,None),([{'id':'a'}],2,None),([{'id':'a'}],1,{'b'}),([{'id':''}],1,None)])
def test_record_guards(records,n,ids):
    with pytest.raises(AssertionError):indexed(records,n,ids)
@pytest.mark.parametrize('mutation',['missing','nonfinite','null','wrongtype','shortbeta','shortband','shortcircles','bad_svg','bad_variance','constant_x','wrong_k','bad_parsed','missing_card','duplicate_card','malformed_card'])
def test_shape_and_display_mutations(evidence,mutation):
    corpus,b,app,ref,p=evidence;id=next(iter(corpus));c=copy.deepcopy(corpus[id]);a=copy.deepcopy(app[id]);r=copy.deepcopy(ref[id])
    if mutation=='missing':del a['main']['tau2']
    elif mutation=='nonfinite':a['main']['tau2']=float('nan')
    elif mutation=='null':a['main']['tau2']=None
    elif mutation=='wrongtype':a['main']['tau2']='0'
    elif mutation=='shortbeta':a['main']['beta'].pop()
    elif mutation=='shortband':r['main']['band']['pred'].pop()
    elif mutation=='shortcircles':a['svg']['circles'].pop()
    elif mutation=='bad_svg':a['svg']['line']='NaN,NaN '*201
    elif mutation=='bad_variance':c['rows'][0]['vi']=0
    elif mutation=='constant_x':
        for row in c['rows']:row['x']=1
    elif mutation=='wrong_k':c['k']+=1
    elif mutation=='bad_parsed':a['parsed']='5'
    elif mutation=='missing_card':a['stats']=[s for s in a['stats'] if 'test' not in s['label']]
    elif mutation=='duplicate_card':a['stats'].append(a['stats'][0])
    elif mutation=='malformed_card':
        for s in a['stats']:
            if 'test' in s['label']:s['value']='not a p-value'
    with pytest.raises((AssertionError,KeyError,ValueError)):
        shape(c,a,r);display(cards(a))
def test_boolean_type():
    with pytest.raises(AssertionError):difference(1,True,boolean=True)
def test_permutation_coverage(evidence):
    c,b,a,r,p=evidence;p=dict(p);p.pop(next(iter(p)))
    with pytest.raises(AssertionError,match='Permutation coverage'):compare(c,a,r,p)
def test_configuration_coverage(evidence):
    c,b,a,r,p=evidence;a=dict(a);a.pop(next(iter(a)))
    with pytest.raises(AssertionError,match='configuration coverage'):compare(c,a,r,p)
@pytest.mark.parametrize('mode',['unexpected','disappeared','changed','duplicate_pin'])
def test_documented_failure_gate(mode):
    pins=read(ROOT/'expected/documented_differences.json');rows=[dict(p,passed=False,group='model') for p in pins]
    if mode=='unexpected':rows.append(dict(rows[0],index=99))
    elif mode=='disappeared':rows[0]['passed']=True
    elif mode=='changed':rows[0]['quantity']='changed'
    else:pins[0]=pins[1]
    with pytest.raises(AssertionError):documented(rows,pins)
def test_manifest_empty_missing_changed_extra():
    for m in [{},{'a':'1'},{'a':'2','b':'3'}]:
        with pytest.raises(AssertionError):verify_manifest(m,{'a':'2'})
@pytest.mark.parametrize('s',['\ufefftext','C:'+chr(92)+'Users'+chr(92)+'someone'])
def test_text_safety(tmp_path,s):
    p=tmp_path/'x.txt';p.write_text(s,encoding='utf-8')
    with pytest.raises(AssertionError):text_safety(p)
def test_draft_safety(tmp_path):
    p=tmp_path/'manuscript.md';p.write_text('draft')
    with pytest.raises(AssertionError):text_safety(p)
def test_git_allowed(tmp_path):
    (tmp_path/'.git').mkdir();(tmp_path/'.git/config').write_text('local');(tmp_path/'README.md').write_text('ok')
    assert [p.name for p in source_files(tmp_path)]==['README.md']
def test_r_guards():
    # Source helpers without invoking the expensive main routine.
    code='''source('validate.R')
reject<-function(expr){ok<-inherits(tryCatch({force(expr);NULL},error=function(e)e),'error');if(!ok)stop('negative test did not reject')}
reject(field(list(foobar=1),'foo'))
reject(tree(structure(list(1,2),names=c('a','a'))))
reject(index(list(list(id='a'),list(id='a')),2))
reject(index(list(list(id='a')),2))
reject(index(list(list(id='a')),1,'b'))
reject(vec(list(1),2));reject(vec(list(NULL),1));reject(vec(list('1'),1))
for(v in list(NA_real_,NaN,Inf,-Inf,'1',TRUE,NULL))reject(compare_difference(v,v))
reject(compare_difference(1,TRUE,boolean=TRUE))
pins<-lapply(0:35,function(i)list(configuration='a',quantity='q',index=i))
tab<-data.frame(configuration='a',quantity='q',index=0:35,Result='FAIL')
check_documented(tab,pins)
reject(check_documented(tab[-1,],pins))
tab[['index',exact=TRUE]][1]<-99;reject(check_documented(tab,pins))
cat('R safeguard negative tests PASS\\n')
'''
    proc=subprocess.run(['Rscript','-e',code],cwd=ROOT,capture_output=True,text=True)
    assert proc.returncode==0,proc.stdout+proc.stderr

@pytest.mark.parametrize('kind',['metafor','R'])
def test_version_guards(kind,tmp_path):
    code='source('+json.dumps((ROOT/'validate.R').as_posix())+');requireNamespace<-function(...)TRUE;'
    if kind=='metafor':
        code+="packageVersion<-function(pkg)numeric_version('5.0.1');"
        expected='Wrong package version'
    else:
        code+="packageVersion<-function(pkg)numeric_version(if(pkg=='metafor')'5.2.1' else '1.6.0');getRversion<-function()numeric_version('4.5.0');"
        expected='Require R 4.6.0'
    code+="msg<-tryCatch({main();'NO ERROR'},error=function(e)conditionMessage(e));stopifnot(grepl("+json.dumps(expected)+",msg,fixed=TRUE))"
    proc=subprocess.run(['Rscript','-e',code],cwd=tmp_path,capture_output=True,text=True)
    assert proc.returncode==0,proc.stdout+proc.stderr
