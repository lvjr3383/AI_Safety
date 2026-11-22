"""Figure 1: the Stage 2 interaction under each scoring of the same frozen generations, grouped by procedure.
Usage: python3 make_fig1.py <final_results_FINAL.json> <out.pdf>"""
import sys, json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
res=json.load(open(sys.argv[1]))
groups=[('Original analysis',[('Parser with review of flagged rows','L1','p')]),
        ('October audit',[('Primary coding','L2','p'),('Second reader on 20 borderline rows','L3','p')]),
        ('Symmetric rule, primary coding',[('Reader 1 (Opus)','SYM_r1','p'),('Reader 2 (Sonnet)','SYM_r2','p'),('Reader 3 (Gemini)','SYM_r3','p')]),
        ('Symmetric rule, strict-U2 coding',[('Reader 1 (Opus)','SYM_r1_strict','s'),('Reader 2 (Sonnet)','SYM_r2_strict','s'),('Reader 3 (Gemini)','SYM_r3_strict','s')])]
ink='#1f2933'; fig,ax=plt.subplots(figsize=(6.6,3.75)); y=0.0; ticks=[]; labs=[]; XL=-10; XR=41
for gi,(title,rows) in enumerate(groups):
    if gi: 
        y-=0.45; ax.axhline(y,color='#d9dee4',lw=0.7,zorder=0); y-=0.2
    y-=0.75; ax.text(XL,y,title,fontsize=8.5,fontweight='bold',color=ink,va='center',ha='left')
    for lab,k,kind in rows:
        y-=1.0; x=float(res[k]['interaction']); lo,hi=[float(v) for v in res[k]['inter_ci']]
        ax.plot([lo,hi],[y,y],color=ink,lw=1.4,solid_capstyle='round')
        ax.plot([x],[y],'o',ms=6.5,mfc=(ink if kind=='p' else 'white'),mec=ink,mew=1.4,zorder=3)
        ax.text(XR-0.5,y,f"{x:+.1f}".replace('-','−'),va='center',ha='right',fontsize=8.5,color=ink)
        ticks.append(y); labs.append(lab)
ax.axvline(0,color='#9aa5b1',lw=0.9,zorder=0)
ax.set_yticks(ticks); ax.set_yticklabels(labs,fontsize=8.5)
ax.set_xlim(XL,XR); ax.set_xticks(range(-10,36,5)); ax.set_ylim(y-0.7,-0.2)
ax.set_xlabel('Evaluation-framing interaction (percentage points), with item-clustered 95% CI',fontsize=8.5)
ax.tick_params(axis='x',labelsize=8.5); ax.tick_params(axis='y',length=0)
for s in ('top','right','left'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(sys.argv[2]); print('wrote',sys.argv[2])
