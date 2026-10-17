# V5_CHANGES (Oct 17, 2026)

v5 is in `/workspace/corrected_oct17/arxiv_pack_v5/`. It was copied from v4, and v4 and earlier versions were not touched.
- It is still a review copy: the header reads DRAFT FOR REVIEW (v5) and the watermark is unchanged.
- The PDF is `main_structure_review.pdf`: 9 pages.
- Compile result: 0 errors, 0 overfull hboxes, 0 LaTeX warnings, 0 BibTeX warnings, and 5 harmless underfull hboxes (loose lines in the abstract and appendix paragraphs).
- `main.bbl` was regenerated.

## 1. Verbatim blocks
- **Package:** `fancyvrb` was replaced by `fvextra`. fvextra loads fancyvrb and is a standard TeX Live/CTAN package that arXiv has.
- **Environment:** `verbatim` is redefined as `Verbatim` with `fontsize=\footnotesize`, `breaklines=true`, `breakanywhere=true`, and empty `breaksymbolleft` and `breaksymbolright`.
- **Content:** there are 7 verbatim blocks. All 7 are byte-identical to v4, checked by a script.
- **Visual check:** I rendered every page at 80 dpi into `v5_pages/page-1.png` … `page-9.png` and looked at each one. No text crosses the right margin. Appendix A is on pages 8–9, and its lines now wrap.
- **Log check:** 0 overfull hboxes.
- **Page count:** the larger font pushed two lines onto a 10th page. I set the artifact-manifest paragraphs to `\small\raggedright`, a formatting-only change with no text edits. That brought the PDF back to 9 pages and removed the underfull boxes in the manifest.

## 2. Item bank wording
- **Abstract (first mention):** now reads "a 20-item forced-choice answer-maintenance bank designed to measure whether the model maintains the supported answer under pressure".
- **Introduction:** now reads "a cleaned 20-item answer-maintenance bank".
- **Remaining "honest" in main.tex:** the Related Work heading "Honesty under pressure" and "separating honesty from factual accuracy". Both describe MASK and other literature.
- **Not changed:** `ARXIV_METADATA.md` is a stale file carried over from the first draft. It still has the old title and the phrase "model honesty". It is not compiled into the PDF.

## 3. Conclusion sentence
- **Replaced in three places:** the abstract, §6 "What changed" (the bold sentence), and the Conclusion.
- **Remaining "reliable evidence":** none.
- **Kept:** "uncertain rather than a precise null" in §6.

## 4. "positives" changed to "yields"
- **Changed in two places:** Contributions (c) and the Discussion recommendation, which is now "Review all auto-scored yields".
- **"positive" uses left as they are:**
  - "clear positive effects" (§1, about statistics)
  - "positive item-level interaction" (§4 and §6)
  - "Leave-one-out stays positive"
  - "positive training feedback" (verbatim wrapper text)
  - "positive draws" (appendix)
  - Table 3 "Items with positive interaction"

## Every edit, old → new
### 1. Header
Old:
```latex
DRAFT FOR REVIEW (v4)
```
New:
```latex
DRAFT FOR REVIEW (v5)
```

### 2. Header comment
Old:
```latex
%% REVIEW COPY v4
```
New:
```latex
%% REVIEW COPY v5
```

### 3. Preamble: fvextra
Old:
```latex
\usepackage{fancyvrb}
```
New:
```latex
\usepackage{fvextra} % loads fancyvrb; adds line breaking
```

### 4. Preamble: breakable verbatim
Old:
```latex
\DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\scriptsize,xleftmargin=0pt,baselinestretch=0.9}
```
New:
```latex
\DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\footnotesize,xleftmargin=0pt,baselinestretch=0.9,breaklines=true,breakanywhere=true,breaksymbolleft={},breaksymbolright={}}
```

### 5. Abstract: item bank
Old:
```latex
on a 20-item honesty item bank with gold answers
```
New:
```latex
on a 20-item forced-choice answer-maintenance bank designed to measure whether the model maintains the supported answer under pressure, with gold answers
```

### 6. Abstract: conclusion
Old:
```latex
I find no reliable evidence that evaluation framing widened the gap, and I offer the case
```
New:
```latex
The corrected analysis does not support the original claim that evaluation framing widened the gap. I offer the case
```

### 7. Contributions
Old:
```latex
re-adjudication of all auto-scored positives with decoys
```
New:
```latex
re-adjudication of all auto-scored yields with decoys
```

### 8. Discussion recommendation
Old:
```latex
\textbf{Review all auto-scored positives} (here, yields), not only rows
```
New:
```latex
\textbf{Review all auto-scored yields}, not only rows
```

### 9. Conclusion
Old:
```latex
I find no reliable evidence that evaluation framing widened the gap.
```
New:
```latex
The corrected analysis does not support the original claim that evaluation framing widened the gap.
```

### 10. Sec 6 'What changed': conclusion
Old:
```latex
The same generations support a much weaker conclusion: \textbf{no reliable evidence that evaluation framing widened the Neutral$-$Social gap}, and at most a small, uncertain social-pressure cost (Stage~1: 4.7~pp; Stage~2 OFF: 6.2~pp).
```
New:
```latex
The same generations support a much weaker conclusion. \textbf{The corrected analysis does not support the original claim that evaluation framing widened the Neutral$-$Social gap}, and it leaves at most a small, uncertain social-pressure cost (Stage~1: 4.7~pp; Stage~2 OFF: 6.2~pp).
```

### 11. Introduction: item bank
Old:
```latex
on a cleaned 20-item honesty item bank (gold answers;
```
New:
```latex
on a cleaned 20-item answer-maintenance bank (gold answers;
```

### 12. Appendix artifact manifest: formatting only (\small\raggedright), no text change
Old:
```latex
\begin{sloppypar}
\paragraph{Original artifacts.}
```
New:
```latex
\begin{sloppypar}\small\raggedright
\paragraph{Original artifacts.}
```
