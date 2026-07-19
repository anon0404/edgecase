# Human annotator agreement study

`build_annotation_sample.py` draws a stratified, blinded sample from
`datasets/splits/test.jsonl` for an independent human-annotator agreement
check against the benchmark's own template-generated labels.

## Files

- `annotation_blind.xlsx` — send this to annotators. 152 cases (22 per
  domain, capped at 20 for `moderation` since that's all `test.jsonl` has),
  sampled with a fixed seed (777) and shuffled to remove domain-order
  leakage. Contains only `prompt` and `signals` per case, plus a Rubric
  sheet defining the 7 collision types and their obligations/mitigations,
  and an Instructions sheet. Domain and the ground-truth `collision` /
  `expected_mitigation` labels are deliberately not shown anywhere in this
  file (verified programmatically — see below).
- `annotation_answer_key.csv` — **do not share with annotators.** Maps
  `row_number` (the neutral ID annotators see) back to the original
  dataset `id`, `domain`, and true `collision`/`expected_mitigation`
  labels. Used only for scoring returned annotations.

## Regenerating

```bash
python experiments/annotation/build_annotation_sample.py
```

Deterministic given the fixed seed; re-running overwrites both output
files with the same sample.

## Blinding verification

Before sending `annotation_blind.xlsx` to anyone, this was checked
programmatically: no column named `domain` or `id` exists on any sheet,
and none of the 189 original dataset `id` strings (e.g.
`crisis_support_0012`) appear anywhere in the workbook. Signal names that
happen to share a substring with a domain name (e.g. the real signal
`moderation_dispute` containing "moderation") are not a leak — they're
legitimate case evidence, not domain metadata.

## Once annotations come back

Each returned `annotation_blind.xlsx` (or its `Annotate` sheet) can be
joined to `annotation_answer_key.csv` on `row_number` to compare
`Your Collision Type` / `Your Expected Mitigation` against
`true_collision` / `true_expected_mitigation`. Cohen's kappa
(`sklearn.metrics.cohen_kappa_score`) is the natural agreement statistic
here — not built yet, since there's no real annotation data to write or
test a scoring script against. Ask for `experiments/annotation/score_agreement.py`
once at least one completed annotation file exists.
