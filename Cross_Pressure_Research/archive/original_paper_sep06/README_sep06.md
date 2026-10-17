# Cross Pressure Research

Measurement-validity study: honesty under pressure (Stage 1) and whether explicit evaluation framing widens the social-pressure gap (Stage 2).

**Paper (submit copy):** [`arxiv_pack/main.pdf`](arxiv_pack/main.pdf)  
**Title:** Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama 3.3 70B  
**Author:** Jack Lakkapragada (Independent researcher)

## Status

Empirical core is **frozen**. Do **not** re-run Colab notebooks to “get results” for the paper — tables come from the frozen artifacts below and the PDF.

## Layout

| Path | Contents |
|------|----------|
| `notebooks/` | Stage 1 / Stage 2 Colab notebooks (recipe + audit trail) |
| `pilot02_artifacts/` | Frozen Stage 2 config, tables, bootstrap, review/adjudicated CSVs, final scored |
| `pilot02_adjudication/` | Blinded adjudication SOP, scoring sheet, blind texts |
| `arxiv_pack/` | `main.tex`, `references.bib`, `main.bbl`, `main.pdf`, metadata |

## How to read results

1. Read the PDF.
2. Cross-check numbers in `pilot02_artifacts/pilot02_canonical_table.json` and `pilot02_clustered_bootstrap.json`.
3. Notebooks document generation/scoring; re-execution needs an API key and can drift from the freeze.

## Model

`meta-llama/llama-3.3-70b-instruct` (OpenRouter)  
Model card: https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct

## License / cite

See `arxiv_pack/ARXIV_METADATA.md`. Prefer citing the arXiv version once posted.
