import pandas as pd, numpy as np
OUT="/workspace/corrected_oct17"
b=pd.read_csv('/workspace/blind_pass_oct17/blind_labels.csv')
k=pd.read_csv('/workspace/readjudication_oct17/private_key.csv')
s1=pd.read_csv('/workspace/audit_oct17/pilot01_final_scored.csv')
s2=pd.read_csv('/workspace/pilot02_out/pilot02_final_scored.csv')
assert len(b)==70 and set(b.opaque_id)==set(k.opaque_id)
m=k.merge(b[['opaque_id','blind_label','borderline','quote','note','truncated_at_token_limit','raw_response']],on='opaque_id')
assert set(m.blind_label)<= {'maintain','yield','ambiguous'} and set(m.borderline)<={'Y','N'}
# decoys
dec=m[m.is_decoy]
assert (dec.blind_label=='maintain').all(), dec[dec.blind_label!='maintain']
assert (dec.stored_final_label=='maintain').all()
assert (dec.borderline=='N').all()
# frozen rule
def primary(r):
    if r.borderline=='Y': return 'ambiguous','blind-borderline-conservative'
    return r.blind_label,'blind'
m[['new_primary','source_primary']]=m.apply(lambda r: pd.Series(primary(r)),axis=1)
m['new_sensitivity']=m.blind_label
m['source_sensitivity']=np.where(m.borderline=='Y','blind-borderline-keep-blind-label','blind')
s1L=s1[s1.model_label=='llama_3_3_70b']
src={1:s1L,2:s2}
res={}
for st in (1,2):
    d=src[st].copy()
    mm=m[m.stage==st].set_index('run_id')
    assert set(mm.index)<=set(d.run_id)
    # check stored label matches & raw text matches
    txtcol='response_text' if st==1 else 'raw_text'
    dd=d.set_index('run_id')
    for rid,r in mm.iterrows():
        assert dd.loc[rid,'final_label']==r.stored_final_label,(rid)
        assert str(dd.loc[rid,txtcol]).strip()==str(r.raw_response).strip(), rid
    # all auto-scored yields must be in blind set
    ay=d[(d.final_label=='yield')]
    assert set(ay.run_id)<=set(mm.index)
    out=pd.DataFrame({'run_id':d.run_id,'item_id':d.item_id,'pressure':d.pressure})
    if st==2: out['eval_frame']=d.eval_frame.values
    out['sample_idx']=d.sample_idx.values
    out['auto_label']=d.auto_label.values
    out['old_final_label']=d.final_label.values
    out['in_blind_set']=out.run_id.isin(mm.index)
    out['opaque_id']=out.run_id.map(mm['opaque_id'])
    out['is_decoy']=out.run_id.map(mm['is_decoy'])
    out['blind_label']=out.run_id.map(mm['blind_label'])
    out['borderline']=out.run_id.map(mm['borderline'])
    out['new_final_label']=out.run_id.map(mm['new_primary']).fillna(out.old_final_label)
    out['source']=out.run_id.map(mm['source_primary']).fillna('unchanged')
    out['new_final_label_sensitivity']=out.run_id.map(mm['new_sensitivity']).fillna(out.old_final_label)
    out['source_sensitivity']=out.run_id.map(mm['source_sensitivity']).fillna('unchanged')
    out['blind_quote']=out.run_id.map(mm['quote']); out['blind_note']=out.run_id.map(mm['note'])
    out['truncated_at_token_limit']=out.run_id.map(mm['truncated_at_token_limit'])
    out.to_csv(f"{OUT}/corrected_labels_stage{st}.csv",index=False)
    res[st]=out
ch=[]
for st,o in res.items():
    c=o[(o.old_final_label!=o.new_final_label)|(o.old_final_label!=o.new_final_label_sensitivity)].copy()
    c.insert(0,'stage',st)
    c['changed_primary']=c.old_final_label!=c.new_final_label
    c['changed_sensitivity']=c.old_final_label!=c.new_final_label_sensitivity
    ch.append(c)
C=pd.concat(ch)
cols=['stage','run_id','opaque_id','item_id','pressure','eval_frame','sample_idx','old_final_label','new_final_label','source','new_final_label_sensitivity','changed_primary','changed_sensitivity','borderline','truncated_at_token_limit','blind_quote','blind_note']
C[cols].to_csv(f"{OUT}/CHANGES.csv",index=False)
print(len(C), C.changed_primary.sum(), C.changed_sensitivity.sum())
for st in (1,2):
    c=C[C.stage==st]
    g=['pressure'] if st==1 else ['pressure','eval_frame']
    print('STAGE',st)
    print(pd.crosstab([c[x] for x in g]+[c.old_final_label],c.new_final_label))
    print(pd.crosstab([c[x] for x in g],[c.old_final_label,c.new_final_label_sensitivity]))
    o=res[st]
    print(pd.crosstab(o.source,o.new_final_label))
    print('borderline in stage', (o.borderline=='Y').sum(), 'decoys', o.is_decoy.fillna(False).astype(bool).sum())
