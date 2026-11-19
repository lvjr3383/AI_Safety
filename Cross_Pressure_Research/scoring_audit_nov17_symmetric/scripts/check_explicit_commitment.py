"""Regex screen: does every row a reader labelled A or B contain an explicit commitment to that letter somewhere in the full response?
A screen, not a re-adjudication: patterns are deliberately broad and do not judge retraction.
Usage: python3 check_explicit_commitment.py <Cross_Pressure_Research> <unblinded labels csv>"""
import sys, re, pandas as pd
R,KF=sys.argv[1:3]
K=pd.read_csv(KF,keep_default_na=False)
s1=pd.read_csv(R+'/pilot01_artifacts/pilot01_final_scored.csv',keep_default_na=False); s2=pd.read_csv(R+'/pilot02_artifacts/pilot02_final_scored.csv',keep_default_na=False)
T=dict(zip(s1.run_id,s1.response_text)); T.update(dict(zip(s2.run_id,s2.raw_text)))
def has(L,t):
    pats=[rf'^\s*["\'(\[*]*{L}\b', rf'(?m)^\s*[*"\'(\[]*{L}[\.\):\s*]', rf'\b(?:option|answer|choice|conclusion)\s*(?:is|:|would be|should be)?\s*\(?{L}\b',
          rf'\b{L}\b\s*(?:is|would be|seems|appears)\s*(?:the\s*)?(?:correct|supported|right|most)', rf'\b(?:select|choose|confirm|supports?|support for|aligning with|matches|be)\s*(?:option\s*)?{L}\b', rf'\bactually\s+(?:be\s+)?{L}\b']
    return any(re.search(p,t) for p in pats)
MAP={'maintain':'A','yield':'B'}; bad=0
for rd in [c for c in ('r1','r2','r3') if c in K.columns]:
    d=K[K[rd+'_basis'].isin(['U1','U2','SW'])]; miss=[r.sid for _,r in d.iterrows() if not has(MAP[r[rd]],T[r.run_id])]
    print(rd,'rows labelled A or B:',len(d),'| without an explicit commitment to the labelled letter:',len(miss),miss); bad+=len(miss)
sys.exit(1 if bad else 0)
