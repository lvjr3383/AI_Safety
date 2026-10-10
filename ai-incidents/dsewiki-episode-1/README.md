# The country relay (DSEWiki, Episode 1): check files

Companion files for the article "The country relay" by Jack Lakkapragada. The
article follows one page of the DSEWiki export, `dse/HealthdataCVDSequenceCollab`,
and a second page, `dse/PolandSeeker2`.

## Files

| File | What it is |
|---|---|
| `verify_episode1.py` | Recomputes the counts, timestamps, labels, quotations and body hashes the article uses. Standard library only. |
| `r6_slovenia_review.tsv` | All 191 fragments that mention R6 or Slovenia, each with how it was read. |
| `CHECKS.md` | Record of the script run, the fragment reading and the phone-width check. |
| `figures/` | The six figures at full resolution. |
| `figure-captions-and-alt-text.md` | Caption and alt text for each figure. |

## Run the checks

```
python3 verify_episode1.py /path/to/export-folder
python3 verify_episode1.py /path/to/export-folder --review-list fragments.tsv
```

The folder must hold `revisions.jsonl` (or `.gz`). With `pages.jsonl`,
`labels.jsonl` and `events.jsonl` present, all 30 checks run.

## Which export

- Publisher's export: https://collusion.wiki/explorer/download
  Expanded `revisions.jsonl` SHA-256
  `60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793`
- Privacy-sanitized copy: https://github.com/intentionallydense/fast-follow-question-trajectories
  at commit `952d0d94e72af69c42d3792198954d8cc64a32cb`, file `full-wiki-logs.zip`.
  Expanded `revisions.jsonl` SHA-256
  `de241d012cc620bfaa0f44f3f0205d7c778f16d7ed816edbf2230bc6fd93b2e2`

The two pages can also be read on the publisher's site:

- https://collusion.wiki/explorer/page/dse~HealthdataCVDSequenceCollab
- https://collusion.wiki/explorer/page/dse~PolandSeeker2

## What a pass means

The script checks counts, timestamps, selected quotations and body hashes. It
does not decide what a post means. The conclusion that no post reports round 6
arriving comes from reading the page text; that reading is recorded fragment by
fragment in `r6_slovenia_review.tsv`.
