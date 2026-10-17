import pandas as pd, numpy as np, json
from cp_stats import _arrays, mb
OUT="/workspace/corrected_oct17"
c1=pd.read_csv(f"{OUT}/corrected_labels_stage1.csv"); c2=pd.read_csv(f"{OUT}/corrected_labels_stage2.csv")
s1=pd.read_csv('/workspace/audit_oct17/pilot01_final_scored.csv'); s2=pd.read_csv('/workspace/pilot02_out/pilot02_final_scored.csv')
items=[f"H{i:02d}" for i in range(1,21)]
def s2draws(col):
    d=s2.copy(); d['label']=d.run_id.map(dict(zip(c2.run_id,c2[col])))
    S,N=_arrays(d,'label'); rng=np.random.default_rng(42); out={'drop_off':[],'drop_on':[],'interaction':[]}
    for _ in range(5000):
        idx=rng.choice(20,size=20,replace=True); s=S[idx].sum(0); n=N[idx].sum(0); r=s/n
        a=100*(r[0]-r[1]); b=100*(r[2]-r[3]); out['drop_off'].append(a); out['drop_on'].append(b); out['interaction'].append(b-a)
    return {k:np.array(v) for k,v in out.items()}
def s1draws(col):
    L=s1[s1.model_label=='llama_3_3_70b'].copy(); L['label']=L.run_id.map(dict(zip(c1.run_id,c1[col]))); L['mb']=L.label.map(mb)
    S=np.array([[L[(L.item_id==it)&(L.pressure==p)].mb.sum() for p in ['neutral','social']] for it in items])
    N=np.array([[L[(L.item_id==it)&(L.pressure==p)].mb.notna().sum() for p in ['neutral','social']] for it in items])
    rng=np.random.default_rng(42); G=[]
    for _ in range(5000):
        idx=rng.choice(20,size=20,replace=True); s=S[idx].sum(0); n=N[idx].sum(0); G.append(100*(s[0]/n[0]-s[1]/n[1]))
    return np.array(G)
p=s2draws('new_final_label'); q=s2draws('new_final_label_sensitivity')
sets={'S2 interaction (primary)':p['interaction'],'S2 drop OFF (primary)':p['drop_off'],'S2 drop ON (primary)':p['drop_on'],
      'S1 Neutral-Social gap (primary)':s1draws('new_final_label'),'S2 interaction (sensitivity)':q['interaction'],
      'S2 drop ON (sensitivity)':q['drop_on'],'S1 gap (sensitivity)':s1draws('new_final_label_sensitivity')}
res={}
for k,v in sets.items():
    assert not np.isnan(v).any()
    eps=1e-9
    neg=int((v<-eps).sum()); zero=int((np.abs(v)<=eps).sum()); pos=int((v>eps).sum())
    lo,hi=np.percentile(v,[2.5,97.5])
    # rank positions under numpy linear interpolation: index (n-1)*0.025 = 124.975
    sv=np.sort(v)
    hist=np.histogram(v,bins=[-100,-1e-9,1e-9,2.5,5,7.5,10,15,20,30,100])
    res[k]=dict(n=len(v),neg=neg,zero=zero,pos=pos,pct_neg=100*neg/len(v),pct_zero=100*zero/len(v),pct_pos=100*pos/len(v),
        p2_5=float(lo),p97_5=float(hi),min=float(v.min()),max=float(v.max()),mean=float(v.mean()),median=float(np.median(v)),
        sorted_124_125_126=[float(sv[124]),float(sv[125]),float(sv[126])],
        hist_edges=[float(x) for x in hist[1]],hist_counts=[int(x) for x in hist[0]],
        neg_values_sample=sorted(set(np.round(v[v<-eps],3).tolist()))[:15])
    print(k,{x:res[k][x] for x in ['neg','zero','pos','pct_neg','pct_zero','p2_5','p97_5','min','max','sorted_124_125_126']})
    print('  hist',res[k]['hist_counts'],' neg vals',res[k]['neg_values_sample'])
json.dump(res,open(f"{OUT}/bootstrap_check.json","w"),indent=1)
