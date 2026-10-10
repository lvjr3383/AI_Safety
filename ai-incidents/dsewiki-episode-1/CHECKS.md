# Checks record: The country relay (DSEWiki, Episode 1)

Recorded 10 October 2026.

## 1. Script run

- `verify_episode1.py`, this version, on the privacy-sanitized copy of the export
  (`revisions.jsonl` SHA-256 `de241d01...b2e2`): 30 of 30 checks passed, 0 skipped.
- A reviewer ran this version on the publisher's export
  (`revisions.jsonl` SHA-256 `60df4a51...f793`) and reported 30 of 30.
- The same reviewer regenerated the 191-fragment list from the publisher's export
  and reported that it matches `r6_slovenia_review.tsv`.
- In the sanitized copy, `pages.jsonl` and `labels.jsonl` have the same SHA-256 as
  the files listed on the publisher's download page.
- Tamper test: changing one character in save @99 or @102 makes the script fail.

## 2. Reading of the R6 and Slovenia fragments

Scope: every sentence-like fragment of added or changed text on
`dse/HealthdataCVDSequenceCollab` that contains "R6" or "Slovenia". The script
lists them; it does not judge them. There are 191: 170 mention R6 and 21 more
mention Slovenia without R6.

Method: each fragment was read in save order and given one reading. The reading
was done with AI assistance (Claude Code) and is recorded per fragment in
`r6_slovenia_review.tsv`, so anyone can disagree with a specific line. A second
reviewer separately inspected the R6 and Slovenia passages on an earlier pass.

Result: no fragment reports that round 6 arrived.

| Read as | Fragments |
|---|---|
| Schedule or countdown | 86 |
| Request or question | 43 |
| Timing reasoning | 18 |
| Prepared for Slovenia | 17 |
| Monitoring or promise to relay | 13 |
| Prediction or guess | 8 |
| Says R6 has not been seen | 6 |
| Total | 191 |

Other fragments use "arrive" or "arrival" inside a question, a request or a
prediction. Three say it in a way that could be mistaken for a report. Each was
read as a schedule:

- Fragment 41, save @32: "cooldown confirmed 1h22m02, our R6 arrives 07:01:05." Uses “arrives” for a scheduled time: the same save says round 5 was answered at 05:37:42 and the cooldown is 1h22m02.
- Fragment 70, save @50: "Our announced R6 arrival 07:01:05 = 7h12m41 after start, deadline ~7h14m04." “Announced R6 arrival” is the announced schedule, used in a timing calculation.
- Fragment 73, save @52: "our R6 arrives exactly task-clock 22:31:14." Uses “arrives” for a scheduled time: the same save says the next query was announced for 1h22m02s later.

Save @102 repeats one paragraph four times, so its two fragments each appear
four times in the list.

## 3. Phone-width check of the figures

The figures went through three sizes. The first put most labels at about 5 to
6 px on a phone. The second put main labels at 7.5 to 9.2 px. A reviewer judged
both too small, and judged a third attempt still too small in Figures 2 and 4.
The current versions are drawn on a canvas close to phone width. Counts, exact
times and label names that did not fit at a readable size were moved into keys
under the drawings or into the captions.

Method: the article page was rendered at viewport widths of 360, 390 and 430 px
and the on-screen size of every text element in each figure was measured. Each
image file was also scaled to the width it gets in a 360 px phone column and
looked at, at that size.

| Viewport | Main labels | Largest labels in Figures 2 and 4 | Smallest text in the drawings |
|---|---|---|---|
| 360 px | 10.9 px | 12.2 px | 8.8 to 9.5 px |
| 390 px | 11.9 px | 13.4 px | 9.7 to 10.4 px |
| 430 px | 13.4 px | 15.1 px | 10.9 to 11.7 px |

Result: no figure overflows the screen. Titles, main labels, numbers and keys can
be read at phone size. On a 360 px phone the main labels are about 11 px and the
smallest text is about 9 px, which is below a comfortable reading size. The
article therefore tells readers to tap a figure to enlarge it, and the figures
should be treated as needing that on small phones.

Trade-off: because the images are phone-shaped, they look large when shown at
full column width on a desktop.
