# EdgeCase Benchmark v2

`edgecase_benchmark_v2.jsonl` contains 1260 synthetic paired
governance-conflict workflow instances, generated from
132 distinct prompt templates across 7 domains
(up from v1's 35 total).

Two v1 findings motivated this redesign, both discovered as side effects
of building LLM-detector baselines against v1, not planned in advance:

1. v1's 1,260 instances came from only 35 distinct prompt strings.
2. Even with more templates, v1's design mapped each domain to exactly
   one collision type, so recognizing a domain's topic was sufficient
   regardless of template count - not the same task as reasoning about a
   genuinely novel or ambiguous tension.

v2 addresses (2) directly: crisis_support, moderation now each host
two collision types, grounded in real trigger-vocabulary overlaps already
present in the registry (`self_harm`/`coercion`/`abuse_disclosure` trigger
both `care.escalate` and `safeguarding.preserve_context`; `policy_evasion`
triggers both `security.block` and `security.limit_exploitability`) - not
invented ambiguity. Every crossover case's ground-truth label is verified
against the real `detect()` resolution logic before this file is written
(`verify_crossover_resolution()`), not assumed from the design intent.

`enterprise_copilot` additionally hosts an `indirect_third_party` pattern
(tension introduced via retrieved content, not the requester's own
message), added in response to a taxonomy-validation finding that the
best-documented real memory-poisoning incidents (EchoLeak and related
CVEs) are indirect in exactly this way - a pattern v1 did not represent.

`scenario_pattern` (primary / crossover / indirect_third_party)
distinguishes all three in every row. Same schema and `generate_rows(seed)`
contract as v1 otherwise.
