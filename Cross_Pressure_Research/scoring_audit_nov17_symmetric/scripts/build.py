import sys, pandas as pd, numpy as np, re, os
R=sys.argv[1]; OUT=sys.argv[2]
s1=pd.read_csv(R+'/pilot01_artifacts/pilot01_final_scored.csv',keep_default_na=False); L=s1[s1.model_label=='llama_3_3_70b'].copy()
f=pd.read_csv(R+'/pilot02_artifacts/pilot02_final_scored.csv',keep_default_na=False)
pa=pd.read_csv(R+'/scoring_audit_oct17/1_blind_set/parser_audit_all_rows.csv',keep_default_na=False).set_index('run_id')
L['stage']=1; L['txt']=L.response_text; L['prompt']=L.user_message; L['eval_frame']='n/a'
f['stage']=2; f['txt']=f.raw_text; f['prompt']=f.user_prompt
cols=['stage','run_id','item_id','pressure','eval_frame','sample_idx','auto_label','final_label','txt','prompt']
D=pd.concat([L[cols],f[cols]],ignore_index=True)
D['flagged']=D.run_id.map(pa.flagged).astype(str).str.lower().isin(['true','1','y','yes'])
D['fc']=D.txt.str.strip().str[:1]
def why(r):
    if r.auto_label=='yield': return 'auto_yield'
    if r.auto_label=='review' and r.final_label=='maintain': return 'adjudicated_maintain'
    if r.auto_label=='review' and r.final_label=='ambiguous': return 'adjudicated_ambiguous'
    if r.auto_label=='maintain' and (r.flagged or r.fc!='A'): return 'auto_maintain_screen_flagged'
    return ''
D['stratum']=D.apply(why,axis=1)
pool=D[D.stratum==''].sample(25,random_state=20261117); D.loc[pool.index,'stratum']='auto_maintain_random_control'
S=D[D.stratum!=''].sample(frac=1,random_state=20261118).reset_index(drop=True)
S['sid']=[f"S{i+1:03d}" for i in range(len(S))]
def item(p):
    m=re.search(r'Information:\n(.*?)\n\nWhich conclusion is supported by the information\?\nA\. (.*?)\nB\. (.*?)\n\nAnswer with',p,re.S)
    return (m.group(1).strip(),m.group(2).strip(),m.group(3).strip()) if m else ('','','')
S[['item_setup','option_A','option_B']]=S.prompt.apply(lambda p: pd.Series(item(p)))
assert (S.item_setup!='').all()
S[['sid','stage','run_id','item_id','pressure','eval_frame','sample_idx','auto_label','final_label','stratum']].to_csv(OUT+'/PRIVATE_KEY.csv',index=False)
print(len(S)); print(S.groupby(['stage','stratum']).size().to_string())
k=3; n=len(S); chunks=[S.iloc[i*n//k:(i+1)*n//k] for i in range(k)]
for rd in ('reader1','reader2'):
    for i,c in enumerate(chunks):
        d=f"{OUT}/{rd}/chunk{i+1}"; os.makedirs(d+'/data',exist_ok=True); os.makedirs(d+'/work',exist_ok=True)
        with open(d+'/data/sheet.md','w') as h:
            for _,r in c.iterrows():
                h.write(f"=== {r.sid} ===\nSETUP: {r.item_setup}\nA. {r.option_A}\nB. {r.option_B}\nRESPONSE:\n<<<\n{r.txt}\n>>>\n\n")
        open(d+'/data/ids.txt','w').write('\n'.join(c.sid)+'\n')
        open(d+'/data/RULES_LOCKED.md','w').write(open(os.path.dirname(OUT)+'/RULES_LOCKED.md').read())
        print(rd,i+1,len(c),os.path.getsize(d+'/data/sheet.md'))
