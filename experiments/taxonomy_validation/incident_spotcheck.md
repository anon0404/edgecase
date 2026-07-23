# Taxonomy coverage spot-check against real incident reports

**Scope, stated plainly:** this is a bounded, first-pass spot-check — 16
publicly-reported incidents, 2-3 per domain, sourced via web search against
the AI Incident Database and recent reporting/literature. It is not a
systematic review, not exhaustive, and not a substitute for the bottom-up
taxonomy-mining program described as future work. Its purpose is narrow: does
anything here obviously not fit the current 7 registered collision types,
before we spend the rest of the redesign polishing instance diversity within
a taxonomy that might have a structural gap.

For each incident: the domain it's closest to, a one-line summary, the
plausible obligation tension, and a verdict against `INCOMPATIBLE_ACTIONS`.

## Crisis-support

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 1 | [Incident 1041](https://incidentdatabase.ai/cite/1041/) - Nomi companion chatbots gave explicit self-harm/violence instructions instead of escalating | None documented - no adversarial/jailbreak framing reported, just a missing escalation response | **Does not fit.** This is a single obligation (`care.escalate`) never firing, not two obligations in tension. |
| 2 | Common Sense Media testing: only 1 in 5 crisis prompts triggered appropriate intervention across tested chatbots | Same as above | **Does not fit**, same reason. |
| 3 | Raine v. OpenAI and similar suits alleging chatbots encouraged a minor toward suicide | Public reporting doesn't establish the user input also carried adversarial/jailbreak framing | **Unclear / likely does not fit** as reported - would need transcript-level detail to know if `block_vs_escalate` actually applies. |

**Pattern across all three crisis-support incidents found:** none of the
most-reported real failures in this domain are genuine two-obligation
collisions in the sense this taxonomy models. They're single-obligation
failures - the escalation obligation simply doesn't fire, full stop, not
"fires but loses to a competing obligation." Worth stating plainly: the
domain's real-world failure mode and the benchmark's modeled failure mode
may not be the same phenomenon.

## Banking/fintech

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 4 | Blind/low-vision Americans locked out of biometric identity verification for benefits/banking as fraud controls tightened | Fraud-verification need directly in tension with accessibility/disability need | **Clean fit** - `verify_vs_accessibility`. |
| 5 | Banks freezing more accounts in 2026 as automated fraud-detection flags legitimate transactions | Same general tension, less explicitly accessibility-coded | **Fit**, weaker match than #4. |

## Healthcare triage

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 6 | AI system deferred rescue medication for escalating seizures to a follow-up appointment instead of immediate review | Loosely resembles review-depth-vs-speed, but no explicit compute/latency pressure documented as the cause | **Partial fit at best** - reads as a pure safety failure (bad triage call), not a documented speed-vs-thoroughness tension. |
| 7 | Mount Sinai study: ChatGPT Health failed to direct users to emergency care in a significant fraction of serious cases | Same issue - no documented competing pressure, just a miss | **Does not clearly fit** - another single-obligation failure, not a collision. |

## Enterprise copilot

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 8 | EchoLeak (CVE-2025-32711) - zero-click data exfiltration via hidden instructions in a retrieved email, no user action required | Memory/context poisoning via a channel that looks like normal retrieval/summarization | **Conceptually related to `memory_care_vs_memory_poisoning` but structurally different**: the poisoning instruction comes from a **third party** (an attacker-crafted email), not from the requesting user's own prompt. |
| 9 | Microsoft Copilot "Summarize with AI" button hijacked via hidden instructions embedded in documents by an external party | Same pattern | **Same structural mismatch as #8.** |

**This is the single most important finding of the spot-check.** The
current taxonomy's obligation pairs all assume one first-party requester
whose own message embeds both sides of the tension (e.g. the user's own
prompt asks to personalize memory AND carries a poisoning-style
instruction). The two best-documented, most severe real-world incidents in
this exact domain (EchoLeak and the Copilot Studio/Agentforce family of
CVEs) are **indirect**: the tension is introduced by a third party via
content the system retrieves, not by the user making the request. This is
a real, structural blind spot, not a phrasing-diversity problem - no
amount of paraphrasing the existing single-requester template fixes it.

## Education

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 10 | UK A-level grading algorithm downgraded high-achieving students from historically lower-performing schools | Personalization/adjustment based on group history creating unfair individual outcomes | **Clean conceptual fit** - `fairness_vs_personalization`. |
| 11 | Automated essay-grading systems scoring Black students' essays lower for equivalent content | Bias in an automated scoring system | **Loose fit** - this reads as a pure bias/failure case (the system is unfair), not a case where a legitimate personalization request and a legitimate fairness concern are both active and in genuine tension. |

## Public-benefits

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 12 | [Incident 822](https://incidentdatabase.ai/cite/822/) - French welfare fraud algorithm allegedly scored disabled and single-parent claimants as higher risk | Fraud-detection scoring producing discriminatory harm | **Does not cleanly fit `privacy_vs_safeguarding`** - closer to a fairness/discrimination failure in a fraud-verification system than a privacy-minimization-vs-evidence-preservation tension. |
| 13 | [Incident 101](https://incidentdatabase.ai/cite/101/) - Dutch childcare benefits scandal (SyRI): families wrongly flagged for fraud based on nationality data, severe real-world harm | Data-driven fraud detection weaponized against a vulnerable population | **Does not cleanly fit** - same issue as #12, a discrimination failure in scoring, not the specific privacy-vs-safeguarding pairing modeled here. |
| 14 | UK DWP automated fraud tool: two-thirds of flagged housing-benefit claims were legitimate | High false-positive rate in automated fraud detection | **Does not fit `privacy_vs_safeguarding` specifically** - a detection-accuracy failure, not a collision between minimizing data and preserving it for safeguarding. |

## Moderation

| # | Incident | Plausible tension | Verdict |
|---|---|---|---|
| 15 | Only 5 of 14 studied generative AI tools clearly document a non-legal appeals process | Opacity in moderation systems generally | **Does not clearly fit** - documents a transparency gap, not a specific transparency-request-that-also-enabled-evasion incident. |
| 16 | Jailbreak/evasion phrasing evolving faster than moderation systems can be retrained | Adversarial adaptation vs. enforcement | **Loosely related to `explain_vs_exploitability`** but no specific incident ties a transparency/appeal request to a documented exploit. |

## Synthesis

Of 16 incidents checked: **2 are clean fits** (#4 verify/accessibility, #10
fairness/personalization), **2 are structurally-related but reveal a real
gap** (#8-9, indirect/third-party memory poisoning), and **the remaining
12 mostly describe a different failure mode than this taxonomy models** -
either a single obligation failing outright (crisis-support, healthcare
triage) or a discrimination/bias failure in one system rather than a
genuine tension between two co-legitimate obligations (education essay
grading, both public-benefits fraud-scoring incidents).

**Two honest conclusions, not one:**

1. Where the current 7 collision types do have real-world analogs, those
   analogs are severe and well-documented (identity verification vs.
   disability access; algorithmic personalization vs. fairness) - the
   taxonomy is not made up, at least not entirely.
2. The taxonomy's implicit assumption - that governance failures are
   mostly two-sided collisions between co-legitimate obligations, both
   triggered by the same first-party request - does not match most of
   what's actually reported as an AI governance incident in practice. Real
   incidents more often look like (a) an obligation that should have fired
   never firing at all, (b) a system that's simply biased/wrong rather
   than caught between two legitimate demands, or (c) a tension introduced
   by a third party rather than the user making the request. Of these
   three, (c) is the most actionable and most clearly a benchmark-design
   gap rather than a labeling ambiguity - the redesigned benchmark should
   add at least one collision pattern where the tension is introduced by
   retrieved/third-party content, not the user's own message.

This spot-check does not by itself justify adding a new obligation domain
or collision *type* to `INCOMPATIBLE_ACTIONS` - 16 incidents is too small
and too informally sourced a sample for that. What it does justify is
narrower and more concrete: the benchmark's case-generation design should
stop assuming every conflict is first-party-only, since the best-documented
real incidents in the enterprise-copilot domain specifically are not.

## Comparison against the MIT AI Risk Repository

The [MIT AI Risk Repository](https://airisk.mit.edu/risks) (1,700+ risks
extracted from 74 existing frameworks, Domain Taxonomy of 7 top-level
domains / 24 subdomains) is the most comprehensive systematic AI risk
taxonomy publicly available, and a much stronger validation target than
16 informally-sourced incidents. Mapping EdgeCase's 10 governance domains
(security, care, accessibility, privacy, safeguarding, environment,
safety, memory, transparency, fairness) against it:

| EdgeCase domain | MIT match | Verdict |
|---|---|---|
| security | 2.2 AI system security vulnerabilities and attacks | Clean match |
| privacy | 2.1 Compromise of privacy | Clean match |
| fairness | 1.1 Unfair discrimination; 1.3 Unequal performance across groups | Clean match |
| transparency | 7.4 Lack of transparency or interpretability | Clean match |
| environment | 6.6 Environmental harm | Clean match |
| safety | 7.3 Lack of capability or robustness; 5.1 Overreliance and unsafe use | Loose match - no exact "review-depth" concept |
| care | none | **No clean top-level home** - closest is 5.1/5.2 (human-computer interaction), but nothing captures "failure to escalate a vulnerable/crisis user" specifically |
| accessibility | none | **No clean top-level home** - closest is 6.2 (increased inequality), framed socioeconomically, not as an interaction/accommodation burden |
| safeguarding | none | **No clean top-level home** |
| memory (poisoning/protection) | 2.2 generically (security attacks) | **No dedicated category** for memory-specific attacks as such |

Five of ten domains map cleanly onto an existing, well-established risk
category. Four (care, accessibility, safeguarding, memory-specific) do
not have an obvious home in the field's most comprehensive taxonomy -
worth stating honestly as either a genuine, underexplored area this
benchmark is right to model, or a domain needing sharper justification for
why it's treated as a first-class obligation. We do not have enough
evidence from this check alone to say which.

**The more consequential finding is structural, not domain-by-domain.**
The MIT repository's own FAQ states its limitation directly: *"Our
taxonomies do not categorize risks by potentially important factors such
as risk impact, likelihood, or discuss the interaction between risks."*
The repository catalogs risks independently - it does not model when two
risk domains, or two legitimate stakeholder obligations, are in tension
with each other, and its authors name this explicitly as a gap for future
work rather than something the repository attempts. This means EdgeCase's
core methodological move - treating governance as a set of obligations
that can be jointly active and mutually incompatible, not just
independently-tracked risk categories - is addressing a gap the field's
own most comprehensive risk taxonomy explicitly identifies as unaddressed,
not a problem EdgeCase invented to have a paper about. This is citable
and belongs in Related Work, not just this validation appendix.
