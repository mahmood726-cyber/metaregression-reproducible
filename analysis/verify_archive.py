"""Offline inventory, evidence, output and metadata verification; permits git metadata."""
import hashlib,re,tempfile
from pathlib import Path
import yaml
from PIL import Image
from make_outputs import ROOT,build,csvread
from checks import *

def source_files(root=ROOT):
    excluded={'.git','__pycache__','.pytest_cache','outputs','.validate-work','node_modules'}
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in excluded or x.startswith('.verify-') for x in p.relative_to(root).parts) and p.relative_to(root).as_posix() not in {'SOURCE_SHA256.json','PROGRESS.md'})
def hashes(files,root):return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
def verify_manifest(manifest,actual):
    assert manifest and manifest==actual,'Hash/inventory mismatch'
def text_safety(p):
    raw=p.read_bytes();assert not raw.startswith(b'\xef\xbb\xbf'),'UTF-8 BOM'
    s=raw.decode('utf-8');assert not re.search(r'(?<![A-Za-z])[A-Za-z]:[\\/](?:Users|Projects|claude-temp|E156|ProjectIndex)[\\/]',s),'Machine path'
    assert p.name.lower() not in {'paper.md','manuscript.md','paper_v2_dictated_text.md'},'Manuscript draft'
def verify_rtable(path,rows):
    tab=csvread(path);assert len(tab)==129903,'Fresh R table coverage'
    indexed_tab={}
    for row in tab:
        k=(row['configuration'],row['quantity'],int(row['index']))
        assert k not in indexed_tab,'Fresh R duplicate key';indexed_tab[k]=row
        av,rv,d,tol=map(float,[row['App'],row['R'],row['Difference'],row['Tolerance']])
        assert all(math.isfinite(x) for x in [av,rv,d,tol]) and tol>=0,'Fresh R nonfinite'
        expected=abs(av-rv)/(1 if row['quantity'].endswith('_p') or row['quantity'].endswith('_display') else max(1,abs(rv)))
        assert math.isclose(d,expected,rel_tol=1e-5,abs_tol=5e-14),'Fresh R difference arithmetic'
        assert row['Result']==('PASS' if d<=tol else 'FAIL'),'Fresh R verdict'
    primary={key(r):r for r in rows if r['group']!='LS experimental'}
    assert set(indexed_tab)==set(primary),'Fresh R exact key coverage'
    assert {k for k,v in indexed_tab.items() if v['Result']=='FAIL'}=={k for k,v in primary.items() if not v['passed']},'Fresh R failures changed'
    for k,r in indexed_tab.items():
        assert float(r['Tolerance'])==primary[k]['tolerance'],'Fresh R tolerance changed'
        assert math.isclose(float(r['App']),primary[k]['app'],rel_tol=1e-13,abs_tol=5e-13),'Fresh R app evidence changed'
def verify_images(out):
    sizes=read(out/'sizes.json');assert set(sizes)=={f'{n}.{e}' for n in ['figure2_agreement','visual_abstract'] for e in ['png','tif']}
    for name,s in sizes.items():
        with Image.open(out/name) as im:
            assert (im.width,im.height)==(s['width_pixels'],s['height_pixels'])
            assert abs(im.width/300*25.4-170)<.1 and all(abs(v-300)<.001 for v in im.info['dpi']),'Image dimensions/DPI'
            assert list(im.info['dpi'])==s['dpi']
    for name in ['figure2_agreement','visual_abstract']:
        with Image.open(out/f'{name}.png') as a,Image.open(out/f'{name}.tif') as b:assert a.convert('RGB').tobytes()==b.convert('RGB').tobytes(),'Paired image pixels'
def main():
    manifest=read(ROOT/'SOURCE_SHA256.json');verify_manifest(manifest,hashes(source_files(),ROOT))
    app=ROOT/'app';ap=read(app/'app-sha256.json')
    verify_manifest(ap,hashes([p for p in app.rglob('*') if p.is_file() and p.name!='app-sha256.json'],app))
    assert sorted(ap)==read(ROOT/'results/provenance.json')['app_assets']
    for p in source_files():
        if p.suffix.lower() in {'.py','.r','.cjs','.js','.md','.txt','.csv','.json','.jsonl','.css','.html','.cff','.patch'}:text_safety(p)
    for p in [ROOT/'validate.R',*(ROOT/'bench').glob('*.R')]:assert not re.search(r'\$[A-Za-z]',p.read_text(encoding='utf-8')),'Non-exact R access'
    page=app/'meta-regression/index.html'
    for name in re.findall(r'(?:src|href)=["\']([^"\']+\.(?:js|css))["\']',page.read_text(encoding='utf-8')):
        target=(page.parent/name).resolve();assert target.is_relative_to(app.resolve()) and target.is_file(),'Missing page asset'
    for lang in ['', '.es','.ar','.zh']:assert (app/f'hub/shared/glossary{lang}.json').is_file()
    c,b,a,r,p=inputs(ROOT)
    for name,active in [('app.jsonl',b),('patched-app.jsonl',a),('reference.jsonl',r)]:
        raw=indexed([loads(s) for s in (ROOT/'results/raw'/name).read_text(encoding='utf-8').splitlines()],1808)
        for id,v in active.items():
            # reference.json adds exact permutations to the initial main/LS journal.
            if name=='reference.jsonl':assert all(v[k]==raw[id][k] for k in raw[id] if k!='permutation')
            else:assert v==raw[id]
    combined=[]
    for file in sorted((ROOT/'results/raw').glob('permutation-*.jsonl')):combined.extend(loads(s) for s in file.read_text(encoding='utf-8').splitlines())
    assert indexed(combined,365)==p,'Permutation journal merge'
    with tempfile.TemporaryDirectory(prefix='.verify-',dir=ROOT) as tmp:
        temp=Path(tmp);rows,before=build(temp)
        for file in temp.iterdir():assert file.read_bytes()==(ROOT/'outputs'/file.name).read_bytes(),'Output reproduction: '+file.name
    verify_images(ROOT/'outputs')
    table=csvread(ROOT/'outputs/table2_differences.csv');assert len(table)==36 and len({x['configuration'] for x in table})==14
    assert all(float(x['centered_difference'])<3e-11 for x in table),'Centered differences'
    if (ROOT/'outputs/validate_R_table.csv').exists():verify_rtable(ROOT/'outputs/validate_R_table.csv',rows)
    title='Random-effects meta-regression in the browser: validation against the R package metafor'
    z=read(ROOT/'.zenodo.json');cff=yaml.safe_load((ROOT/'CITATION.cff').read_text(encoding='utf-8'))
    assert z['title']==cff['title']==title and z['version']==cff['version']=='1.0.0' and z['license']==cff['license']=='MIT'
    assert z['creators']==[{'name':'Ahmad, Mahmood'}] and cff['authors']==[{'family-names':'Ahmad','given-names':'Mahmood'}]
    assert {(x['identifier'],x['relation']) for x in z['related_identifiers']}=={('https://github.com/mahmood726-cyber/allmeta','isDerivedFrom'),('10.5281/zenodo.23288388','isDerivedFrom')}
    assert any(x.get('doi')=='10.5281/zenodo.23288388' and x.get('notes')=='isDerivedFrom' for x in cff['references'])
    assert (ROOT/'.gitattributes').read_text().strip()=='* -text'
    print(f'ARCHIVE PASS: {len(ap)} app hashes; {len(manifest)} source hashes; 129867/129903 non-LS checks; 36 documented differences; tables, images, coverage and metadata verified.')
if __name__=='__main__':main()
