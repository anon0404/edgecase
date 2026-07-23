# Benchmark prompt-template diversity

**Canonical seed 404** (the committed benchmark, used for Tables 1/3/4):

- 1260 rows, only **35 distinct prompt strings** (avg 36.0 rows/prompt)
- 0 of 35 distinct prompts map to more than one collision type
- 517 distinct (prompt, signal-set) pairs

**Pooled across the 10 statistical-rigor seeds** (12,600 rows):

- Only **35 distinct prompt strings** across all 10 seeds combined
- 803 distinct (prompt, signal-set) pairs

Prompt text alone deterministically identifies the true collision type in every case checked (0 counterexamples): the benchmark's natural-language diversity is much lower than its case count implies. This does not affect Table 1's numbers (scored on `signals` tags, not prompt text), but it does affect how any prompt-text-only evaluation (e.g. an LLM given only the raw prompt) should be interpreted.
