import json
from pathlib import Path

import matplotlib.pyplot as plt

OUT_DIR = Path("experiments/figures/paper")
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("ggplot")
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "axes.edgecolor": "#4d4d4d",
    "grid.color": "white",
    "grid.linewidth": 1.2,
})

POLICY_LABELS = {
    "strict_block": "Strict Block",
    "always_escalate": "Always Escalate",
    "always_verify": "Always Verify",
    "maximum_review": "Maximum Review",
    "edgecase_adaptive": "Adaptive\nEdgeCase",
    "llm_detected_edgecase_routed": "LLM-Detected +\nEdgeCase-Routed",
}
POLICY_COLORS = {
    "strict_block": "#4C72B0",
    "always_escalate": "#DD8452",
    "always_verify": "#8C8C8C",
    "maximum_review": "#937860",
    "edgecase_adaptive": "#C44E52",
    "llm_detected_edgecase_routed": "#64A65E",
}
PROVIDER_LABELS = {"anthropic": "Claude Sonnet", "gemini": "Gemini 2.5 Pro", "qwen": "Qwen2.5-7B\n(local)"}
PROVIDER_COLORS = {"anthropic": "#4C72B0", "gemini": "#DD8452", "qwen": "#55A868"}

def savefig(fig, name):
    fig.savefig(OUT_DIR / f"{name}.png", bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT_DIR / name}.{{png,pdf}}")

def bar_labels(ax, bars, fmt="{:.2f}"):
    for b in bars:
        h = b.get_height()
        ax.annotate(fmt.format(h), (b.get_x() + b.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.5)

# --- Figure 1: Governance tradeoffs across policies (Table 1), 10-seed bootstrap
# mean +/- 95% CI, small multiples. Uses the same statistical_summary.json data
# Table 1 itself reports (not the single-seed point estimate the previous
# version of this figure used), plus the new LLM-Detected + EdgeCase-Routed
# policy (original/"trust the detector" scoring, matching how the other five
# policies are scored, for visual consistency - see fig6 for the
# original-vs-penalized comparison specifically). ---
def _policy_ci_metrics():
    stats = json.loads(Path("experiments/results/statistical_summary.json").read_text())["ci_per_policy"]
    llm = json.loads(Path("experiments/results/llm_detected_edgecase_routed.json").read_text())
    by_policy = {p: {m["metric"]: m for m in metrics} for p, metrics in stats.items()}
    by_policy["llm_detected_edgecase_routed"] = {m["metric"]: m for m in llm["ci_original"]}
    return by_policy

def figure_governance_tradeoffs():
    by_policy = _policy_ci_metrics()
    policies = ["strict_block", "always_escalate", "maximum_review", "edgecase_adaptive", "llm_detected_edgecase_routed"]

    metrics = [
        ("mitigation_accuracy", "Mitigation Accuracy\n(higher is better)"),
        ("avg_care_suppression", "Care Suppression\n(lower is better)"),
        ("avg_security_risk", "Security Risk\n(lower is better)"),
        ("avg_accessibility_burden", "Accessibility Burden\n(lower is better)"),
        ("avg_privacy_exposure", "Privacy Exposure\n(lower is better)"),
        ("avg_energy_score", "Energy Score\n(lower is better)"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5))
    for ax, (metric, title) in zip(axes.flat, metrics):
        means = [by_policy[p][metric]["mean"] for p in policies]
        lo = [by_policy[p][metric]["mean"] - by_policy[p][metric]["ci_lower_95"] for p in policies]
        hi = [by_policy[p][metric]["ci_upper_95"] - by_policy[p][metric]["mean"] for p in policies]
        colors = [POLICY_COLORS[p] for p in policies]
        bars = ax.bar(
            range(len(policies)), means, color=colors, width=0.65, edgecolor="white", linewidth=0.8,
            yerr=[lo, hi], capsize=3, error_kw={"linewidth": 1, "ecolor": "#333333"},
        )
        ax.set_title(title)
        ax.set_xticks(range(len(policies)))
        ax.set_xticklabels([POLICY_LABELS[p] for p in policies], rotation=30, ha="right", fontsize=8)
        ax.set_ylim(0, 1.0)
        bar_labels(ax, bars)

    fig.suptitle(
        "Governance Tradeoffs Across Mitigation Policies\n(mean $\\pm$ 95% bootstrap CI, 10 seeds $\\times$ 1,260 cases)",
        fontsize=13.5, fontweight="bold", y=1.04,
    )
    fig.tight_layout()
    savefig(fig, "fig1_governance_tradeoffs")

# --- Figure 2: Aggregate externality (Xk), severity-weighted vs uniform ---
def figure_xk_weighting():
    rows = json.loads(Path("experiments/results/full_evaluation_summary.json").read_text())
    rows_by_policy = {r["policy"]: r for r in rows}
    policies = ["strict_block", "always_escalate", "maximum_review", "edgecase_adaptive"]

    x = range(len(policies))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5.5))
    severity = [rows_by_policy[p]["governance_externality"] for p in policies]
    uniform = [rows_by_policy[p]["governance_externality_uniform"] for p in policies]

    b1 = ax.bar([i - width / 2 for i in x], severity, width, label="Severity-weighted\n(care > security > privacy > access > energy)", color="#C44E52", edgecolor="white")
    b2 = ax.bar([i + width / 2 for i in x], uniform, width, label="Uniform weighting\n(1/5 each)", color="#8C8C8C", edgecolor="white")
    bar_labels(ax, b1)
    bar_labels(ax, b2)

    ax.set_ylabel("Aggregate Governance Externality ($X_k$), lower is better")
    ax.set_title("$X_k$ Is Weighting-Sensitive: Adaptive vs. Strict Block\nis Reversed Depending on Dimension Weighting", fontsize=12.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels([POLICY_LABELS[p] for p in policies])
    ax.legend(loc="upper left", fontsize=9, frameon=True, facecolor="white")
    ax.set_ylim(0, max(uniform + severity) * 1.25)
    fig.tight_layout()
    savefig(fig, "fig2_xk_weighting_sensitivity")

# --- Figure 3: Ablation analysis, step function ---
def figure_ablation():
    rows = json.loads(Path("experiments/results/ablation_analysis.json").read_text())
    labels = [r["configuration"] for r in rows]
    values = [r["mitigation_accuracy"] for r in rows]
    colors = ["#C44E52" if l == "Full EdgeCase" else "#4C72B0" for l in labels]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(range(len(labels)), values, color=colors, width=0.6, edgecolor="white", linewidth=0.8)
    bar_labels(ax, bars, fmt="{:.3f}")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("Mitigation Accuracy")
    ax.set_ylim(0, 1.0)
    ax.set_title("Ablation Analysis: Removing Registry or Detection Collapses\nto Zero; Runtime Instrumentation Has No Effect", fontsize=12.5)
    ax.annotate("no causal path to\nmitigation selection", xy=(4, 1.0), xytext=(3.3, 0.72),
                fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="->", color="#4d4d4d"))
    fig.tight_layout()
    savefig(fig, "fig3_ablation_analysis")

# --- Figure 4: Cross-model comparison (Table 3) ---
def figure_cross_model():
    providers = ["anthropic", "gemini", "qwen"]
    summaries = {}
    for p in providers:
        for f in Path("experiments/results/real_models").glob(f"summary_{p}_*.json"):
            summaries[p] = json.loads(f.read_text())

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))

    metrics = [
        ("governance_externality", "Governance Externality\n(lower is better)", "{:.2f}", 1),
        ("avg_response_alignment", "Response Alignment\n(higher is better)", "{:.2f}", 1),
        ("avg_latency_ms", "Avg Latency (s)", "{:.1f}s", 1 / 1000),
    ]
    for ax, (metric, title, fmt, scale) in zip(axes, metrics):
        values = [summaries[p][metric] * scale for p in providers]
        colors = [PROVIDER_COLORS[p] for p in providers]
        bars = ax.bar(range(len(providers)), values, color=colors, width=0.6, edgecolor="white")
        bar_labels(ax, bars, fmt=fmt)
        ax.set_title(title, fontsize=11)
        ax.set_xticks(range(len(providers)))
        ax.set_xticklabels([PROVIDER_LABELS[p] for p in providers], fontsize=9)

    fig.suptitle("Cross-Model Comparison (140 cases/provider, 20/domain, real API calls)", fontsize=13, fontweight="bold", y=1.04)
    fig.tight_layout()
    savefig(fig, "fig4_cross_model_comparison")

# --- Figure 5: External validity coverage (AgentHarm + Agent-SafetyBench) ---
def figure_external_validity():
    data = json.loads(Path("experiments/results/external_validity.json").read_text())

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, key, title in zip(
        axes,
        ("agentharm", "agent_safetybench"),
        ("AgentHarm\n(176 cases, 8/8 categories mapped)", "Agent-SafetyBench\n(2,000 cases, 4/8 categories mapped)"),
    ):
        by_cat = data[key]["by_category"]
        cats = sorted(by_cat.keys(), key=lambda c: -by_cat[c]["n_cases"])
        n_cases = [by_cat[c]["n_cases"] for c in cats]
        n_mapped = [by_cat[c]["n_mapped"] for c in cats]
        colors = ["#4C72B0" if m > 0 else "#C4C4C4" for m in n_mapped]

        y = range(len(cats))
        ax.barh(y, n_cases, color=colors, edgecolor="white", height=0.65)
        ax.set_yticks(list(y))
        ax.set_yticklabels(cats, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel("Cases")
        ax.set_title(title, fontsize=11)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color="#4C72B0", label="Mapped to an EdgeCase obligation"),
        plt.Rectangle((0, 0), 1, 1, color="#C4C4C4", label="No corresponding obligation (unmapped)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.04), frameon=False)
    fig.suptitle("External Validity: Registry Coverage of Independently-Authored\nAgent Safety Benchmarks", fontsize=13, fontweight="bold", y=1.05)
    fig.tight_layout()
    savefig(fig, "fig5_external_validity_coverage")

# --- Figure 6: Two failure modes, not a convergence story. A correctly-
# specified deterministic taxonomy (left panel) beats a capable LLM
# classifier on mitigation accuracy (1.000 vs 0.9915) -- but "correctly
# specified" was not free: the right panel shows the actual cost of
# getting it wrong, a phantom-signal bug that silently collapsed
# detection to 36-48% in two of seven domains until this revision's
# diversity-verification gate caught it. The LLM's own failure mode
# (bottom annotation) is smaller in aggregate but structurally different:
# bounded and concentrated in one explainable confusion pattern, rather
# than a silent domain-wide collapse. ---
def figure_detector_swap_convergence():
    orig_all = json.loads(Path("experiments/results/statistical_summary.json").read_text())["ci_per_policy"]
    llm = json.loads(Path("experiments/results/llm_detected_edgecase_routed.json").read_text())
    spec_bug = json.loads(Path("experiments/results/specification_bug_analysis.json").read_text())

    def get(metrics, name):
        return next(m for m in metrics if m["metric"] == name)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

    # Left: mitigation accuracy, rule-based (correctly specified) vs LLM.
    ax = axes[0]
    labels = ["Adaptive EdgeCase\n(rule-based, fixed)", "LLM-Detected +\nEdgeCase-Routed"]
    means = [get(orig_all["edgecase_adaptive"], "mitigation_accuracy")["mean"], get(llm["ci_original"], "mitigation_accuracy")["mean"]]
    m0, m1 = orig_all["edgecase_adaptive"], llm["ci_original"]
    lo = [means[0] - get(m0, "mitigation_accuracy")["ci_lower_95"], means[1] - get(m1, "mitigation_accuracy")["ci_lower_95"]]
    hi = [get(m0, "mitigation_accuracy")["ci_upper_95"] - means[0], get(m1, "mitigation_accuracy")["ci_upper_95"] - means[1]]
    bars = ax.bar(range(2), means, color=["#C44E52", "#64A65E"], width=0.55, edgecolor="white",
                   yerr=[lo, hi], capsize=4, error_kw={"linewidth": 1.2, "ecolor": "#333333"})
    bar_labels(ax, bars, fmt="{:.3f}")
    ax.set_xticks(range(2))
    ax.set_xticklabels(labels, fontsize=9.5)
    ax.set_ylim(0, 1.08)
    outcome = llm["outcome_counts"]
    ax.annotate(
        f"LLM: {outcome['wrong_type']}/{outcome['correct']+outcome['wrong_type']} errors,\n"
        f"one confusion pattern,\none domain (banking)",
        xy=(1, means[1]), xytext=(0.55, 0.55), fontsize=8.5, ha="center",
        arrowprops=dict(arrowstyle="->", color="#4d4d4d"),
    )
    ax.set_title("Mitigation Accuracy\n(same routing table, different detector)", fontsize=11.5)

    # Right: the cost of "correctly specified" - detection rate by domain,
    # before vs after the phantom-signal bug fix. Only the two affected
    # domains shown; the other five were 100% throughout.
    ax = axes[1]
    domains = list(spec_bug["before_fix"].keys())
    before_rates = [spec_bug["before_fix"][d]["rate"] * 100 for d in domains]
    after_rates = [spec_bug["after_fix"][d]["rate"] * 100 for d in domains]
    x = range(len(domains))
    width = 0.35
    b1 = ax.bar([i - width / 2 for i in x], before_rates, width, label="Before fix", color="#C4C4C4", edgecolor="white")
    b2 = ax.bar([i + width / 2 for i in x], after_rates, width, label="After fix", color="#4C72B0", edgecolor="white")
    bar_labels(ax, b1, fmt="{:.0f}%")
    bar_labels(ax, b2, fmt="{:.0f}%")
    ax.set_xticks(list(x))
    ax.set_xticklabels([d.replace("_", "\n") for d in domains], fontsize=9.5)
    ax.set_ylabel("Detection Rate")
    ax.set_ylim(0, 115)
    ax.legend(loc="upper left", fontsize=9, frameon=True, facecolor="white")
    ax.set_title("Cost of \"Correctly Specified\":\nSilent, Total Failure in the Affected Slice", fontsize=11.5)

    fig.suptitle(
        "Two Failure Modes: a Misspecified Deterministic System Fails Silently and\nTotally; an LLM Fails Rarely but Unpredictably",
        fontsize=13, fontweight="bold", y=1.06,
    )
    fig.tight_layout()
    savefig(fig, "fig6_detector_swap_convergence")

def main():
    figure_governance_tradeoffs()
    figure_xk_weighting()
    figure_ablation()
    figure_cross_model()
    figure_external_validity()
    figure_detector_swap_convergence()

if __name__ == "__main__":
    main()
