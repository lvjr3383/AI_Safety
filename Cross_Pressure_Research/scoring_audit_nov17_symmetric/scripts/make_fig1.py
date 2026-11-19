"""Figure 1: the Stage 2 interaction under each scoring of the same frozen generations.
Usage: python3 make_fig1.py <final_results_FINAL.json> <out.pdf>"""
import sys, json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
res=json.load(open(sys.argv[1]))
rows=[('Original analysis (Aug--Sep)','L1','p'),('October audit, primary','L2','p'),('October audit, second reader','L3','p'),
      ('Symmetric, Reader 1 (Opus)','SYM_r1','p'),('Symmetric, Reader 2 (Sonnet)','SYM_r2','p'),('Symmetric, Reader 3 (Gemini)','SYM_r3','p'),
      ('Symmetric strict-U2, Reader 1','SYM_r1_strict','s'),('Symmetric strict-U2, Reader 2','SYM_r2_strict','s'),('Symmetric strict-U2, Reader 3','SYM_r3_strict','s')]
ink='#1f2933'; fig,ax=plt.subplots(figsize=(6.6,3.3)); n=len(rows)
for i,(lab,k,kind) in enumerate(rows):
    y=n-1-i; x=float(res[k]['interaction']); lo,hi=[float(v) for v in res[k]['inter_ci']]
    ax.plot([lo,hi],[y,y],color=ink,lw=1.4,solid_capstyle='round')
    ax.plot([x],[y],'o',ms=6.5,mfc=(ink if kind=='p' else 'white'),mec=ink,mew=1.4,zorder=3)
    ax.text(40.5,y,f"{x:+.1f}".replace('-','−'),va='center',ha='right',fontsize=8.5,color=ink)
ax.axvline(0,color='#9aa5b1',lw=0.9,zorder=0)
for yb in (5.5,2.5): ax.axhline(yb,color='#d9dee4',lw=0.7,zorder=0)
ax.set_yticks(range(n)); ax.set_yticklabels([r[0].replace('--','–') for r in rows][::-1],fontsize=8.5)
ax.set_xlim(-10,41); ax.set_xticks(range(-10,36,5)); ax.set_ylim(-0.6,n-0.4); ax.set_xlabel('Evaluation-framing interaction (percentage points), with item-clustered 95% CI',fontsize=8.5)
ax.tick_params(axis='x',labelsize=8.5); ax.tick_params(axis='y',length=0)
for s in ('top','right','left'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(sys.argv[2]); print('wrote',sys.argv[2])
