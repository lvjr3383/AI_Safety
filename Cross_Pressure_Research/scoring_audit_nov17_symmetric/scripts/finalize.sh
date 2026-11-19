#!/bin/bash
# HISTORICAL RECORD of the Reader 3 run. Not runnable outside the original workspace (absolute paths, incoming CSVs not shipped).
# To reproduce results use the commands in README.md.
# Run once, after the third reader's three CSVs arrive. Nothing here edits a label.
# Usage: finalize.sh <chunk1.csv> <chunk2.csv> <chunk3.csv> "<model name/version>" <packet: v1|v2|unknown>
set -e
SYM=/home/claude/sym; R=/home/claude/lvjr3383/ai_safety/Cross_Pressure_Research
python3 -I $SYM/scripts/ingest_reader3.py $SYM "$1" "$2" "$3" "$4" "$5"            # validate + FREEZE (hash) before unblinding
python3 -I $SYM/scripts/second_reader_repro.py $R $SYM/out > /dev/null
python3 -I $SYM/scripts/analyze_final.py $R $SYM $SYM/out reader3 FINAL | tee $SYM/out/run_FINAL.log
python3 -I $SYM/scripts/check_explicit_commitment.py $R $SYM/out/final_labels_unblinded_FINAL.csv
python3 -I $SYM/scripts/make_tables.py $SYM $R $SYM/paper_v9/v9_generated.tex
python3 -I $SYM/scripts/build_v9.py $R/paper/cross_pressure_v8_review.tex $SYM/paper_v9/cross_pressure_v9_review.tex
cd $SYM/paper_v9 && pdflatex -interaction=nonstopmode -halt-on-error cross_pressure_v9_review.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error cross_pressure_v9_review.tex >/dev/null && echo "v9 PDF rebuilt with third reader"
