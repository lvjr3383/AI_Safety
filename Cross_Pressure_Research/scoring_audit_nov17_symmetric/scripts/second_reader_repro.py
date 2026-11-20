"""Regenerates the second-reader (Oct 20) statistics from public repo files only.
Maps B-ids to rows by exact response text (the mapping is recoverable from published text, so it is published here).
Usage: python3 second_reader_repro.py <path to Cross_Pressure_Research> <out dir>"""
import sys, json, numpy as np, pandas as pd
R,OUT=sys.argv[1],sys.argv[2]
ITEMS=[f"H{i:02d}" for i in range(1,21)]; mb=lambda l:{"maintain":1.0,"yield":0.0}.get(l,np.nan)
sh=pd.read_csv(R+'/scoring_audit_oct17/second_reader_check/second_reader_sheet.csv',keep_default_na=False)
lb=pd.read_csv(R+'/scoring_audit_oct17/second_reader_check/second_reader_labels.csv',keep_default_na=False)
c1=pd.read_csv(R+'/scoring_audit_oct17/3_corrected_results/corrected_labels_stage1.csv',keep_default_na=False)
c2=pd.read_csv(R+'/scoring_audit_oct17/3_corrected_results/corrected_labels_stage2.csv',keep_default_na=False)
s1=pd.read_csv(R+'/pilot01_artifacts/pilot01_final_scored.csv',keep_default_na=False); s2=pd.read_csv(R+'/pilot02_artifacts/pilot02_final_scored.csv',keep_default_na=False)
txt=pd.concat([s1[['run_id','response_text']].rename(columns={'response_text':'t'}),s2[['run_id','raw_text']].rename(columns={'raw_text':'t'})])
bord=set(c1[c1.borderline=='Y'].run_id)|set(c2[c2.borderline=='Y'].run_id)
txt=txt[txt.run_id.isin(bord)].assign(k=lambda d:d.t.str.strip()); sh['k']=sh.raw_response.str.strip()
m=sh.merge(txt,on='k',how='left',validate='one_to_one').merge(lb[['id','label']].rename(columns={'label':'second_reader_label'}),on='id')
assert m.run_id.notna().all() and len(m)==20
m[['id','run_id','second_reader_label']].to_csv(OUT+'/second_reader_id_map.csv',index=False)
r2=m.set_index('run_id').second_reader_label
for c in (c1,c2): c['L3']=[r2.get(x,p) for x,p in zip(c.run_id,c.new_final_label)]
c1['eval_frame']='n/a'
def boot(d,cells,fn):
    x=d.assign(mb=d.L3.map(mb)); S=np.zeros((20,len(cells))); N=np.zeros_like(S)
    for i,it in enumerate(ITEMS):
        for j,(p,f) in enumerate(cells):
            u=x[(x.item_id==it)&(x.pressure==p)&(x.eval_frame==f)].mb.dropna(); S[i,j]=u.sum(); N[i,j]=len(u)
    rng=np.random.default_rng(42); v=[]
    for _ in range(5000):
        i=rng.choice(20,20,replace=True)
        with np.errstate(all='ignore'): v.append(fn(S[i].sum(0)/N[i].sum(0)))
    v=np.array(v); v=v[~np.isnan(v)]; return fn(S.sum(0)/N.sum(0)),float(np.percentile(v,2.5)),float(np.percentile(v,97.5))
g=boot(c1,[('neutral','n/a'),('social','n/a')],lambda r:100*(r[0]-r[1]))
t=boot(c2,[('neutral','off'),('social','off'),('neutral','on'),('social','on')],lambda r:100*((r[2]-r[3])-(r[0]-r[1])))
out=dict(borderline_labels=m.second_reader_label.value_counts().to_dict(),stage1_gap_pp=round(g[0],2),stage1_gap_ci=[round(g[1],2),round(g[2],2)],stage1_ambiguous=int((c1.L3=='ambiguous').sum()),
 stage2_interaction_pp=round(t[0],2),stage2_interaction_ci=[round(t[1],2),round(t[2],2)],stage2_ambiguous=int((c2.L3=='ambiguous').sum()))
json.dump(out,open(OUT+'/second_reader_results.json','w'),indent=1); print(json.dumps(out,indent=1))
