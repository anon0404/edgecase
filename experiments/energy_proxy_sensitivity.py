"""Quantifies precisely what the paper's Limitations section currently
only asserts qualitatively: that the token/call-count energy proxy changes
the ranking of at least one cross-model comparison relative to wall-clock
latency.

Care suppression, accessibility burden, privacy exposure, and security
risk are identical across all three providers by construction (collision
detection runs on provider-invariant ground-truth signals - see Cross-
model Consistency), so energy is the only dimension that can move Xk
between providers under either proxy. This min-max normalizes each
provider's real observed avg_latency_ms onto the same [0.2, 0.9] range
the token/call-count ENERGY_SCORE dict already uses (low/high), so the two
proxies are on a comparable scale, and recomputes severity-weighted Xk
under both.
"""
import json
from pathlib import Path

from edgecase.metrics import SEVERITY_WEIGHTS, aggregate_governance_externality

PROVIDERS = ["anthropic_anthropic", "gemini_gemini", "qwen_qwen_ollama"]
LABELS = {"anthropic_anthropic": "Claude Sonnet", "gemini_gemini": "Gemini 2.5 Pro", "qwen_qwen_ollama": "Qwen2.5-7B (local)"}

OUT_JSON = Path("experiments/results/energy_proxy_sensitivity.json")
OUT_MD = Path("experiments/tables/energy_proxy_sensitivity.md")

def main():
    data = {p: json.load(open(f"experiments/results/real_models/summary_{p}.json")) for p in PROVIDERS}

    latencies = {p: data[p]["avg_latency_ms"] for p in PROVIDERS}
    lo, hi = min(latencies.values()), max(latencies.values())
    latency_energy = {p: round(0.2 + 0.7 * (latencies[p] - lo) / (hi - lo), 4) for p in PROVIDERS}

    results = {}
    for p in PROVIDERS:
        d = data[p]
        xk_token = aggregate_governance_externality(
            care_suppression=d["avg_care_suppression"],
            accessibility_burden=d["avg_accessibility_burden"],
            privacy_exposure=d["avg_privacy_exposure"],
            security_risk=d["avg_security_risk"],
            energy_score=d["avg_energy_score"],
            weights=SEVERITY_WEIGHTS,
        )
        xk_latency = aggregate_governance_externality(
            care_suppression=d["avg_care_suppression"],
            accessibility_burden=d["avg_accessibility_burden"],
            privacy_exposure=d["avg_privacy_exposure"],
            security_risk=d["avg_security_risk"],
            energy_score=latency_energy[p],
            weights=SEVERITY_WEIGHTS,
        )
        results[p] = {
            "label": LABELS[p],
            "avg_latency_ms": latencies[p],
            "token_call_energy_score": d["avg_energy_score"],
            "latency_normalized_energy_score": latency_energy[p],
            "Xk_token_proxy": round(xk_token, 4),
            "Xk_latency_proxy": round(xk_latency, 4),
        }

    token_rank = sorted(PROVIDERS, key=lambda p: results[p]["Xk_token_proxy"])
    latency_rank = sorted(PROVIDERS, key=lambda p: results[p]["Xk_latency_proxy"])

    out = {
        "results": results,
        "ranking_token_proxy_best_to_worst": [LABELS[p] for p in token_rank],
        "ranking_latency_proxy_best_to_worst": [LABELS[p] for p in latency_rank],
        "ranking_changed": token_rank != latency_rank,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Energy proxy sensitivity: token/call-count vs. latency-normalized\n\n")
        f.write("| Provider | Avg latency | Token-count energy | Latency-normalized energy | Xk (token proxy) | Xk (latency proxy) |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for p in PROVIDERS:
            r = results[p]
            f.write(
                f"| {r['label']} | {r['avg_latency_ms']:.0f}ms | {r['token_call_energy_score']} | "
                f"{r['latency_normalized_energy_score']} | {r['Xk_token_proxy']} | {r['Xk_latency_proxy']} |\n"
            )
        f.write(f"\nRanking (best/lowest Xk to worst) under token proxy: {' < '.join(out['ranking_token_proxy_best_to_worst'])}\n\n")
        f.write(f"Ranking under latency proxy: {' < '.join(out['ranking_latency_proxy_best_to_worst'])}\n\n")
        f.write(f"Ranking changed: {out['ranking_changed']}\n")

    print(json.dumps(out, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
