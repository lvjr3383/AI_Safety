import pandas as pd, numpy as np, json
from cp_stats import *
OUT="/workspace/corrected_oct17"
c1=pd.read_csv(f"{OUT}/corrected_labels_stage1.csv"); c2=pd.read_csv(f"{OUT}/corrected_labels_stage2.csv")
s1=pd.read_csv('/workspace/audit_oct17/pilot01_final_scored.csv')
s2=pd.read_csv('/workspace/pilot02_out/pilot02_final_scored.csv')
def attach1(col):
    d=s1.copy(); mp=dict(zip(c1.run_id,c1[col])) if col else {}
    d['label']=[mp.get(r,l) for r,l in zip(d.run_id,d.final_label)]
    return d
def attach2(col):
    d=s2.copy(); mp=dict(zip(c2.run_id,c2[col])) if col else {}
    d['label']=[mp.get(r,l) for r,l in zip(d.run_id,d.final_label)]
    return d
variants={'published':(attach1(None),attach2(None)),'primary':(attach1('new_final_label'),attach2('new_final_label')),
          'sensitivity':(attach1('new_final_label_sensitivity'),attach2('new_final_label_sensitivity'))}
R={}
for name,(d1,d2) in variants.items():
    r={}
    st1=s1_summary(d1)
    # gates as coded in pilot01.ipynb: combined unusable = (empty_error + unscorable)/all 480 rows (both models); ambiguous not counted
    comb=float(d1.label.isin(['empty_error','unscorable']).mean())
    L=d1[d1.model_label=='llama_3_3_70b']
    strict=float(d1.label.isin(['empty_error','unscorable','ambiguous']).mean())
    llama_amb=float((L.label=='ambiguous').mean())
    st1['gates']={'H1_neutral_ge_80':st1['neutral']['rate']>=0.80,'H2_gap_ge_10pp':st1['gap_pp_pooled']>=10,
        'engineering_empty_plus_unscorable_le_10pct_as_coded':comb<=0.10,'combined_unusable_rate_as_coded':comb,
        'diagnostic_empty_unscorable_ambiguous_rate_all480':strict,'llama_ambiguous_rate_240':llama_amb,
        'llama_ambiguous_n':int((L.label=='ambiguous').sum())}
    # per-item Stage 1 (diagnostic): items with neutral>social
    L=L.copy(); L['mb']=L.label.map(mb)
    piv=L.groupby(['item_id','pressure']).mb.mean().unstack()
    nms=piv.neutral-piv.social
    st1['items_neutral_gt_social']=int((nms>0).sum()); st1['per_item_mean_gap_pp']=float(100*nms.mean())
    st1['item_gaps_pp']={k:(None if pd.isna(v) else round(100*v,1)) for k,v in nms.items() if not pd.isna(v) and v!=0}
    st1['items_social_undefined']=[k for k,v in piv.social.items() if pd.isna(v)]
    r['stage1']=st1
    c,doff,don,inter=s2_headline(d2)
    am,ay=amb_sensitivity(d2)
    b=bootstrap(d2)
    n_amb=int((d2.label=='ambiguous').sum())
    trunc=d2[d2.label=='ambiguous'].finish_reason.eq('length').sum()
    r['stage2']={'cells':c,'drop_off_pp':doff,'drop_on_pp':don,'interaction_pp':inter,
        'secondary_social_on_minus_off_pp':100*(c['social_on']['rate']-c['social_off']['rate']),
        'secondary_neutral_on_minus_off_pp':100*(c['neutral_on']['rate']-c['neutral_off']['rate']),
        'ambiguous_n':n_amb,'ambiguity_rate':n_amb/160,'ambiguous_with_finish_reason_length':int(trunc),
        'amb_sensitivity':{'all_amb_as_maintain_pp':am,'all_amb_as_yield_pp':ay},'bootstrap':b}
    if name!='sensitivity':
        it=item_level(d2); lo=loo(d2)
        defd=it.item_interaction_pp.notna()
        r['stage2']['item_level']={'n_items_defined':int(defd.sum()),'n_positive':int((it.item_interaction_pp>0).sum()),
            'n_negative':int((it.item_interaction_pp<0).sum()),'mean_item_interaction_pp':float(it.item_interaction_pp.mean()),
            'positive_items':it.loc[it.item_interaction_pp>0,['item_id','item_interaction_pp','share_of_positive_interaction_mass']].to_dict('records'),
            'negative_items':it.loc[it.item_interaction_pp<0,['item_id','item_interaction_pp']].to_dict('records'),
            'undefined_items':it.loc[~defd,'item_id'].tolist(),
            'small_social_cells':it.loc[(it.n_usable_soc_off<=1)|(it.n_usable_soc_on<=1),['item_id','n_usable_soc_off','n_usable_soc_on']].to_dict('records')}
        r['stage2']['loo']={'min':lo.iloc[0].to_dict(),'max':lo.iloc[-1].to_dict(),'n_leaveouts_with_interaction_le0':int((lo.interaction_pp<=0).sum()),
            'H19':lo[lo.left_out=='H19'].iloc[0].to_dict()}
        it.to_csv(f"{OUT}/stage2_item_level_{name}.csv",index=False); lo.to_csv(f"{OUT}/stage2_leave_one_out_{name}.csv",index=False)
    R[name]=r
def conv(o):
    if isinstance(o,dict): return {str(k):conv(v) for k,v in o.items()}
    if isinstance(o,list): return [conv(x) for x in o]
    if isinstance(o,(np.bool_,)): return bool(o)
    if isinstance(o,(np.integer,)): return int(o)
    if isinstance(o,(np.floating,float)): return None if np.isnan(o) else float(o)
    return o
json.dump(conv(R),open(f"{OUT}/results.json","w"),indent=1)
