# arXiv packaging metadata — SUBMIT COPY

**Status:** Paper review PASS. Do not rewrite sections, add citations, or change claims/empirics.

## Title
Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama 3.3 70B

## Authors
Jack Lakkapragada (Independent researcher)

## Abstract
Pressure effects on model honesty are hard to interpret when task content, wrapper language, and evaluation cues are confounded. I study this as a measurement-validity problem on a cleaned 20-item honesty bank with gold answers and final-commitment scoring. Stage 1 holds the task fixed and varies only pressure wrappers (Neutral / Social / Training). For Llama 3.3 70B, adjudicated maintain rates were 96.2% Neutral, 76.9% Social, and 93.7% Training (Neutral−Social 19.2 pp). A locked ≥95% usable gate excluded GPT-OSS from any cross-model table (full-run usable 94.2%). Stage 2 reuses the same frozen Llama instrument and crosses Neutral/Social with explicit evaluation framing OFF vs ON (160 generations). Post-adjudication, the Neutral−Social gap widened from 13.0 to 29.9 pp under ON—an interaction of +16.9 pp (item-clustered 95% CI 5.1–30.8). Neutral remained high under ON (97.5%), so the effect is not a global honesty collapse; the interaction concentrates under social pressure and in a minority of items. Blinded adjudication mattered (26/30 review rows were B→A recoveries). I do not claim evaluation awareness as a mechanism or generalize across models. Stage 2 OFF directionally tracks Stage 1’s social-pressure cost without reproducing its point estimate. 1

## Categories
- **Primary:** cs.AI (Artificial Intelligence)
- **Secondary:** cs.CL (Computation and Language)

## Comments line (suggested)
7 pages. Code: https://github.com/lvjr3383/AI_Safety · Model: meta-llama/llama-3.3-70b-instruct

## License
Choose on submit (e.g., CC BY 4.0). Not set in TeX.

## Links (preserve)
- Code: https://github.com/lvjr3383/AI_Safety
- Series: https://lvjr3383.substack.com
- Model card: https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct

## Build
```bash
cd arxiv_pack
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

## Submit package contents
`cross_pressure_arxiv_submit.zip`:
- `main.tex`
- `references.bib`
- `main.bbl`
- `main.pdf`

No separate figure assets (tables are TeX-native).

## Empirical freeze
Do not reopen analysis, sample counts, H08/H19, model scope, or claims.
Stage 2 = 2 samples · 160 gens; Stage 1 = 4 samples · 480 grid; Stage 1 usable 78/80, 78/80, 79/80.
