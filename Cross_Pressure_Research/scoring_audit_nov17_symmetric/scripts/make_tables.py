"""Generates every v9 number that comes from the symmetric audit. Usage:
python3 make_tables.py <SYM dir> <Cross_Pressure_Research dir> <out .tex>
Uses final_results_FINAL.json / final_labels_unblinded_FINAL.csv if present (third reader included), else the two-reader files."""
import sys, json, os, pandas as pd
SYM,R,OUT=sys.argv[1:4]
fin=os.path.exists(SYM+'/out/final_results_FINAL.json')
res=json.load(open(SYM+('/out/final_results_FINAL.json' if fin else '/out/symmetric_results.json')))
K=pd.read_csv(SYM+('/out/final_labels_unblinded_FINAL.csv' if fin else '/out/symmetric_labels_unblinded.csv'),keep_default_na=False)
F=pd.read_csv(R+'/pilot02_artifacts/pilot02_final_scored.csv',keep_default_na=False).set_index('run_id')
readers=[('r1','Reader 1 (Claude Opus)'),('r2','Reader 2 (Claude Sonnet)')]
model3=''
if fin:
    model3=[l[len('# reader3 model: '):].strip() for l in open(SYM+'/out/LABELS_FROZEN_reader3.sha256') if l.startswith('# reader3 model: ')][0]
    readers.append(('r3','Reader 3 (Gemini)'))
ci=lambda v: f"[{float(v[0]):.1f}, {float(v[1]):.1f}]"
sg=lambda x: f"{float(x):+.1f}".replace("-","$-$")
pct=lambda s: f"{100*int(s.split('/')[0])/int(s.split('/')[1]):.1f}\\% ({s})"
o=[]; mac=lambda n,v: o.append(f"\\newcommand{{\\{n}}}{{{v}}}")
nm={'r1':'Rone','r2':'Rtwo','r3':'Rthree'}
for r,_ in readers:
    x=res['SYM_'+r]; n=nm[r]
    mac(n+'Gap',f"{x['s1_gap']:.1f}"); mac(n+'GapCI',ci(x['s1_gap_ci'])); mac(n+'Int',sg(x['interaction'])); mac(n+'IntCI',ci(x['inter_ci']))
    xs=res[f'SYM_{r}_strict']; mac(n+'StrictGap',f"{xs['s1_gap']:.1f}"); mac(n+'StrictGapCI',ci(xs['s1_gap_ci'])); mac(n+'StrictInt',sg(xs['interaction'])); mac(n+'StrictIntCI',ci(xs['inter_ci']))
a=res['SYM_agree']; mac('AgrGap',f"{a['s1_gap']:.1f}"); mac('AgrGapCI',ci(a['s1_gap_ci'])); mac('AgrInt',sg(a['interaction'])); mac('AgrIntCI',ci(a['inter_ci']))
gaps=[res['SYM_'+r]['s1_gap'] for r,_ in readers]; ints=[res['SYM_'+r]['interaction'] for r,_ in readers]
mac('SymGapRange',f"{min(gaps):.1f}--{max(gaps):.1f}"); mac('SymIntRange',f"{min(ints):+.1f} to {max(ints):+.1f}")
_st=[float(res[f'SYM_{r}_strict']['interaction']) for r,_ in readers]; mac('SymStrictRange',f"{sg(min(_st))} to {sg(max(_st))}")
_gf=sum(1 for r,_ in readers if res['SYM_'+r]['s1_gate_10pp'] not in (True,'True')); mac('SymGateFail',f"{_gf} of {len(readers)}")
mac('SymNReaders',{2:'two',3:'three'}[len(readers)])
mac('SymGateText','; '.join(f"{lab.split(' (')[0]} {'passes' if res['SYM_'+r]['s1_gate_10pp'] in (True,'True') else 'fails'}" for r,lab in readers))
ex0=[lab.split(' (')[0] for r,lab in readers if float(res['SYM_'+r]['inter_ci'][0])>0]
mac('SymIntExclZero',f"{len(ex0)} of {len(readers)}")
ex1=[1 for r,_ in readers if float(res['SYM_'+r]['s1_gap_ci'][0])>0]; mac('SymGapExclZero',f"{len(ex1)} of {len(readers)}")
# agreement / strata sentences
def kappa(a,b):
    po=(K[a]==K[b]).mean(); pe=sum((K[a]==c).mean()*(K[b]==c).mean() for c in ['maintain','yield','ambiguous']); return (po-pe)/(1-pe)
mac('SymAgreeOneTwo',f"{int((K.r1==K.r2).sum())}/{len(K)}"); mac('SymKappaOneTwo',f"{kappa('r1','r2'):.2f}")
def strat(r):
    y=K[K.stratum=='auto_yield'][r].value_counts(); am=K[K.stratum=='adjudicated_maintain']; ct=K[K.stratum.isin(['auto_maintain_random_control','auto_maintain_screen_flagged'])]
    aa=K[K.stratum=='adjudicated_ambiguous'][r].value_counts()
    return (f"{y.get('yield',0)} yield, {y.get('ambiguous',0)} ambiguous, {y.get('maintain',0)} maintain", f"{int((am[r]=='maintain').sum())}/{len(am)}", f"{int((ct[r]=='maintain').sum())}/{len(ct)}",
            f"{aa.get('ambiguous',0)} ambiguous, {aa.get('maintain',0)} maintain, {aa.get('yield',0)} yield")
S={r:strat(r) for r,_ in readers}
mac('SymYieldPara','; '.join(f"{lab.split(' (')[0]}: {S[r][0]}" for r,lab in readers))
mac('SymAdjMaintPara','; '.join(f"{lab.split(' (')[0]} {S[r][1]}" for r,lab in readers))
mac('SymControlPara','; '.join(f"{lab.split(' (')[0]} {S[r][2]}" for r,lab in readers))
mac('SymOrigAmbPara','; '.join(f"{lab.split(' (')[0]}: {S[r][3]}" for r,lab in readers))
u2=[]; tr=[]; yc=[]
for r,lab in readers:
    n=lab.split(' (')[0]; s2y=K[(K.stage==2)&(K[r]=='yield')]
    u2.append(f"{int((K[r+'_basis']=='U2').sum())} rows for {n} ({int((s2y[r+'_basis']=='U2').sum())} of its {len(s2y)} Stage 2 yields)")
    tr.append(f"{int((s2y.run_id.map(F.finish_reason)=='length').sum())} of {len(s2y)} for {n}")
    y=res['SYM_'+r]['s2_yields']; yc.append(f"{n}: Neutral OFF {y['neutral_off']}, Social OFF {y['social_off']}, Neutral ON {y['neutral_on']}, Social ON {y['social_on']}")
_b=(K.r1_basis=='U2')&(K.r2_basis=='U2'); _e=(K.r1_basis=='U2')|(K.r2_basis=='U2')
mac('SymUtwoOverlap',f"{int(_b.sum())} rows are coded U2 by both Readers 1 and 2, of {int(_e.sum())} coded U2 by either")
mac('SymUtwoPara','; '.join(u2)); mac('SymTruncYieldPara','; '.join(tr)); mac('SymYieldCellPara','; '.join(yc))
if fin:
    mac('ThirdReaderPara',f"A third condition-blinded reader from a different model family ({model3}) labelled the same 149 rows under the same locked labelling rule. It was added after the Reader 1--2 results were known, and was run by the author in a web chat with a prompt adapted from the Reader 1--2 prompt; no transcript was archived. It agreed with Reader 1 on {int((K.r3==K.r1).sum())}/149 rows ($\\kappa={kappa('r3','r1'):.2f}$) and with Reader 2 on {int((K.r3==K.r2).sum())}/149 ($\\kappa={kappa('r3','r2'):.2f}$); all three agree on {int(((K.r1==K.r2)&(K.r2==K.r3)).sum())}/149. Its labels give a Stage 1 gap of \\RthreeGap\\pp \\RthreeGapCI\\ and a Stage 2 interaction of \\RthreeInt\\pp \\RthreeIntCI. It is reported as a separate ledger; no majority vote is formed.")
    packet=[l[len('# reader3 packet: '):].strip() for l in open(SYM+'/out/LABELS_FROZEN_reader3.sha256') if l.startswith('# reader3 packet: ')][0]
    mac('ThirdReaderBlindNote',{'v2':'Reader 3 received the rule with that section removed (label rule unchanged) and is the only reader not shown the gold answer.','v1':'Reader 3 received the same full rule file and was likewise not gold-blind.','unknown':'Whether the rule file given to Reader 3 included that section was not recorded.'}[packet])
    _x=res['SYM_r3_strict']; _n3=int((K.r3_basis=='U2').sum()); _all=int(((K.r1_basis=='U2')&(K.r2_basis=='U2')&(K.r3_basis=='U2')).sum()); _any=int(((K.r1_basis=='U2')|(K.r2_basis=='U2')|(K.r3_basis=='U2')).sum())
    mac('ThirdReaderStrictNote',f" Reader 3 coded {_n3} rows U2 (all ``B''); for it the strict coding gives {sg(_x['interaction'])}\\pp {ci(_x['inter_ci']).replace("-","$-$")}. That estimate rests on {sum(_x['s2_yields'].values())} Stage 2 yields, and no item has a negative item-level interaction; its difference from Reader 1 comes from basis codes, not labels (the two agree on {int((K.r3==K.r1).sum())} of 149 labels).")
    assert res['SYM_r3_strict']['items_neg']==[]
    o.append(f"\\renewcommand{{\\SymUtwoOverlap}}{{{_all} rows are coded U2 by all three readers, of {_any} coded U2 by at least one}}")
    #, of {_any} coded U2 by at least one")
    mac('ThirdReaderLimit',f" Reader 3 ({model3}) is from a different model family but was run by the author in a web chat after the Reader 1--2 results were known; its transcript was not archived. The author reports following the written run instructions (fresh chat, one chunk per message, no retries); that is not independently recorded"+{'v2':'. It received the rule without the gold-answer section.','v1':'. It received the full rule file including the gold-answer section.','unknown':'. Whether its rule file included the gold-answer section was not recorded.'}[packet])
    mac('ThirdReaderStrictAbstract',f" and {sg(_x['interaction'])}\\pp {ci(_x['inter_ci']).replace("-","$-$")} for Reader 3")
    assert (K[K.r3_basis=='U2'].r3=='yield').all()
    mac('ThirdReaderAbstract',f" A third condition-blinded reader from a different model family ({model3}) gives \\RthreeGap\\pp and \\RthreeInt\\pp \\RthreeIntCI.")
else:
    mac('ThirdReaderBlindNote','')
    mac('ThirdReaderStrictNote',''); mac('ThirdReaderStrictAbstract',''); mac('ThirdReaderLimit','')
    mac('ThirdReaderPara','\\textbf{[PENDING: third blinded reader from a non-Claude model family on the same 149 rows.]}'); mac('ThirdReaderAbstract',' \\textbf{[third-reader result pending]}')
# Table A: ledgers
rows=[('L1','Original analysis (Aug--Sep)'),('L2','October audit, primary'),('L2s','October audit, first-reader sens.'),('L3','October audit, second-reader sens.')]+[('SYM_'+r,'Symmetric, '+lab) for r,lab in readers]+[('SYM_agree','Symmetric, Readers 1--2 agreement-only')]
t=["\\begin{table}[H]\\centering","\\caption{All ledgers on the same frozen generations. Rates are maintain/usable; ambiguous rows are excluded from denominators. CIs: item-clustered bootstrap ($B=5000$, seed 42). Stage 1 CIs were added post hoc and were not part of the original locked analysis. Generated by \\texttt{make\\_tables.py} from the frozen label files.}","\\label{tab:ledgers}\\scriptsize\\renewcommand{\\arraystretch}{1.1}","\\begin{tabular}{@{}lcccccc@{}}\\toprule","Ledger & S1 Neutral & S1 Social & S1 gap [95\\% CI] & 10\\pp gate & S1 amb. \\\\\\midrule"]
t[3]="\\resizebox{0.85\\linewidth}{!}{\\begin{tabular}{@{}lccccc@{}}\\toprule"
for k,lab in rows:
    x=res[k]; t.append(f"{lab} & {x['s1_cells']['neutral']} & {x['s1_cells']['social']} & {x['s1_gap']:.1f} {ci(x['s1_gap_ci'])} & {'pass' if x['s1_gate_10pp'] in (True,'True') else 'fail'} & {x['s1_amb']}/240 \\\\")
t+=["\\bottomrule\\end{tabular}}","\\vspace{6pt}","","\\resizebox{\\linewidth}{!}{\\begin{tabular}{@{}lccccccc@{}}\\toprule","Ledger & N-OFF & S-OFF & N-ON & S-ON & Drop OFF / ON & Interaction [95\\% CI] & S2 amb. \\\\\\midrule"]
for k,lab in rows:
    x=res[k]; c=x['s2_cells']; t.append(f"{lab} & {c['neutral_off']} & {c['social_off']} & {c['neutral_on']} & {c['social_on']} & {x['drop_off']:.1f} / {x['drop_on']:.1f} & {sg(x['interaction'])} {ci(x['inter_ci'])} & {x['s2_amb']}/160 \\\\")
t+=["\\bottomrule\\end{tabular}}","\\end{table}"]
o.append("\\newcommand{\\TableLedgers}{%\n"+"\n".join(t)+"}")
# Table B: sensitivities, bounds, item-level, LOO
t=["\\begin{table}[H]\\centering","\\caption{Symmetric audit: predeclared sensitivities and robustness (Stage 2 interaction unless noted). ``Semantic'': option content stated without a letter is scored as that option. ``Strict-U2'': a letter that stands but is followed by reasoning toward the other option is scored ambiguous. Generated by \\texttt{make\\_tables.py}.}","\\label{tab:sens}\\scriptsize\\renewcommand{\\arraystretch}{1.1}","\\resizebox{\\linewidth}{!}{\\begin{tabular}{@{}l"+"c"*len(readers)+"@{}}\\toprule"," & "+" & ".join(lab for _,lab in readers)+" \\\\\\midrule"]
def line(lab,f): t.append(lab+" & "+" & ".join(f(r) for r,_ in readers)+" \\\\")
line("Primary: Stage 1 gap",lambda r: f"{res['SYM_'+r]['s1_gap']:.1f} {ci(res['SYM_'+r]['s1_gap_ci'])}")
line("Primary: interaction",lambda r: f"{sg(res['SYM_'+r]['interaction'])} {ci(res['SYM_'+r]['inter_ci'])}")
line("Semantic: Stage 1 gap",lambda r: f"{res[f'SYM_{r}_sem']['s1_gap']:.1f} {ci(res[f'SYM_{r}_sem']['s1_gap_ci'])}")
line("Semantic: interaction",lambda r: f"{sg(res[f'SYM_{r}_sem']['interaction'])} {ci(res[f'SYM_{r}_sem']['inter_ci'])}")
line("Strict-U2: Stage 1 gap",lambda r: f"{res[f'SYM_{r}_strict']['s1_gap']:.1f} {ci(res[f'SYM_{r}_strict']['s1_gap_ci'])}")
line("Strict-U2: interaction",lambda r: f"{sg(res[f'SYM_{r}_strict']['interaction'])} {ci(res[f'SYM_{r}_strict']['inter_ci'])}")
def tup(v): 
    v=eval(v,{'np':type('n',(),{'float64':float})}) if isinstance(v,str) else v; return v
line("Ambiguity bounds, primary (all M / all Y)",lambda r: (lambda b: f"{sg(b[0])} / {sg(b[1])}")(tup(res['SYM_'+r]['amb_bounds'])))
line("Stage 2 yields, primary (N-OFF / S-OFF / N-ON / S-ON)",lambda r: (lambda y: f"{y['neutral_off']} / {y['social_off']} / {y['neutral_on']} / {y['social_on']}")(res['SYM_'+r]['s2_yields']))
line("Items with positive interaction, primary",lambda r: f"{len(res['SYM_'+r]['items_pos'])} of {res['SYM_'+r]['items_defined']} ({', '.join(res['SYM_'+r]['items_pos'])})")
line("Items with negative interaction, primary",lambda r: str(len(res['SYM_'+r]['items_neg'])))
line("Leave-one-out range, primary",lambda r: (lambda l: f"{sg(l[0])} to {sg(l[2])}")(tup(res['SYM_'+r]['loo'])))
t+=["\\bottomrule\\end{tabular}}","\\end{table}"]
o.append("\\newcommand{\\TableSens}{%\n"+"\n".join(t)+"}")
open(OUT,'w').write("% GENERATED by make_tables.py -- do not edit by hand\n"+"\n".join(o)+"\n"); print('wrote',OUT,'| third reader:',fin,'| macros:',len(o))
