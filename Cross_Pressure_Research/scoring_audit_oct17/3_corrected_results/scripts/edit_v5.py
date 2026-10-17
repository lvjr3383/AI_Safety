import json
P="/workspace/corrected_oct17/arxiv_pack_v5/main.tex"
s=open(P,encoding='utf-8').read()
E=[
("Header","DRAFT FOR REVIEW (v4)","DRAFT FOR REVIEW (v5)"),
("Header comment","%% REVIEW COPY v4","%% REVIEW COPY v5"),
("Preamble: fvextra",r"\usepackage{fancyvrb}",r"\usepackage{fvextra} % loads fancyvrb; adds line breaking"),
("Preamble: breakable verbatim",r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\scriptsize,xleftmargin=0pt,baselinestretch=0.9}",
 r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\footnotesize,xleftmargin=0pt,baselinestretch=0.9,breaklines=true,breakanywhere=true,breaksymbolleft={},breaksymbolright={}}"),
("Abstract: item bank",r"on a 20-item honesty item bank with gold answers",r"on a 20-item forced-choice answer-maintenance bank designed to measure whether the model maintains the supported answer under pressure, with gold answers"),
("Abstract: conclusion",r"I find no reliable evidence that evaluation framing widened the gap, and I offer the case",r"The corrected analysis does not support the original claim that evaluation framing widened the gap. I offer the case"),
("Contributions",r"re-adjudication of all auto-scored positives with decoys",r"re-adjudication of all auto-scored yields with decoys"),
("Discussion recommendation",r"\textbf{Review all auto-scored positives} (here, yields), not only rows",r"\textbf{Review all auto-scored yields}, not only rows"),
("Conclusion",r"I find no reliable evidence that evaluation framing widened the gap.",r"The corrected analysis does not support the original claim that evaluation framing widened the gap."),
]
log=[]
for sec,o,n in E:
    c=s.count(o); assert c==1,(sec,c); s=s.replace(o,n); log.append(dict(section=sec,old=o,new=n))
open(P,'w',encoding='utf-8').write(s)
json.dump(log,open('/workspace/corrected_oct17/scripts/v5_edits.json','w'),indent=1,ensure_ascii=False)
