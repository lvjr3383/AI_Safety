"""Validate, place and FREEZE third-reader labels before any unblinding. Usage:
python3 ingest_reader3.py <SYM dir> <chunk1.csv> <chunk2.csv> <chunk3.csv> "<model name/version>"
Labels are never edited here. Quote mismatches are counted and reported, not corrected."""
import sys, os, re, io, hashlib, datetime, pandas as pd
SYM=sys.argv[1]; files=sys.argv[2:5]; model=sys.argv[5]; packet=sys.argv[6]  # packet: v1 (rule file with gold line), v2 (without), unknown
RD=sys.argv[7] if len(sys.argv)>7 else 'reader3'  # target folder: reader3 (first Gemini run) or reader3b (clean rerun)
OK={'U1':'AB','U2':'AB','SW':'AB','RX':'M','RN':'M','NC':'M','NN':'M'}
man=[]; rep=[]
for c,f in zip((1,2,3),files):
    raw=open(f,'rb').read()
    d=pd.read_csv(io.BytesIO(raw),keep_default_na=False,dtype=str)
    assert list(d.columns)==['sid','label','basis','content_side','quote','note'], f'{f}: header'
    ids=open(f'{SYM}/out/reader1/chunk{c}/data/ids.txt').read().split()
    assert sorted(d.sid)==sorted(ids), f'{f}: row ids do not match chunk {c}'
    lab=d.label.str.strip().str.upper(); bas=d.basis.str.strip().str.upper(); cs=d.content_side.str.strip().str.upper()
    assert lab.isin(['A','B','AMBIGUOUS']).all() and bas.isin(list(OK)).all(), f'{f}: invalid label/basis'
    cons=[(l in 'AB' and len(l)==1) if OK[b]=='AB' else l=='AMBIGUOUS' for l,b in zip(lab,bas)]
    need=bas.isin(['RX','NC'])
    sh=open(f'{SYM}/out/reader1/chunk{c}/data/sheet.md').read()
    rows=dict(re.findall(r'=== (S\d+) ===\n.*?RESPONSE:\n<<<\n(.*?)\n>>>',sh,re.S))
    qbad=[s for s,q in zip(d.sid,d.quote) if q.strip() not in rows[s]]
    rep.append((c,len(d),sum(not x for x in cons),int((need&~cs.isin(['A','B'])).sum()),len(qbad),qbad))
    dst=f'{SYM}/out/{RD}/chunk{c}/work'; os.makedirs(dst,exist_ok=True); open(dst+'/labels.csv','wb').write(raw)
    man.append((hashlib.sha256(raw).hexdigest(),f'out/{RD}/chunk{c}/work/labels.csv'))
bad=sum(r[2]+r[3] for r in rep)
with open(SYM+f'/out/LABELS_FROZEN_{RD}.sha256','w') as h:
    for x,p in man: h.write(f'{x}  {p}\n')
    h.write(f'# reader3 packet: {packet}\n')
    h.write(f'# reader3 model: {model}\n# frozen: {datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}\n')
for r in rep: print(f'chunk {r[0]}: rows {r[1]} | label/basis inconsistent {r[2]} | RX/NC missing side {r[3]} | quotes not verbatim {r[4]} {r[5]}')
print('FROZEN' if bad==0 else 'FROZEN WITH FORMAT VIOLATIONS - analysis will refuse; report to PI, do not edit labels')
