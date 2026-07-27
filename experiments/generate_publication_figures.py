import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

OUT_DIR = Path("experiments/figures/paper")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Design system: fixed categorical palette, validated for CVD-safe
# adjacent contrast (see dataviz palette validator). Cool hues (blue/aqua/
# green) mark the EdgeCase family (adaptive router + its detector variants);
# warm hues (red/orange/violet) mark the four fixed-action baselines. This
# grouping is a reading aid, not the only identifier -- every series also
# carries a direct label, so color is never load-bearing alone. ---
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE_AXIS = "#c3c2b7"
SURFACE = "#ffffff"

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10.5,
    "text.color": INK_PRIMARY,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK_PRIMARY,
    "axes.labelsize": 9.5,
    "axes.labelcolor": INK_SECONDARY,
    "axes.edgecolor": BASELINE_AXIS,
    "axes.linewidth": 0.9,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "grid.color": GRIDLINE,
    "grid.linewidth": 0.8,
    "legend.frameon": False,
    "legend.fontsize": 8.5,
})

POLICY_LABELS = {
    "strict_block": "Strict\nBlock",
    "always_escalate": "Always\nEscalate",
    "always_verify": "Always\nVerify",
    "maximum_review": "Maximum\nReview",
    "edgecase_adaptive": "Adaptive\nEdgeCase",
    "oracle_tuned_fixed": "Oracle-Tuned\nFixed",
    "llm_detected_edgecase_routed": "LLM-Detected +\nHarness-Routed",
}
# Warm = fixed-action baselines. Cool = EdgeCase harness family (rule-based
# router, and the same router driven by an LLM detector instead).
POLICY_COLORS = {
    "strict_block": "#e34948",       # red
    "always_escalate": "#eb6834",    # orange
    "always_verify": "#8f8a7f",      # neutral (excluded from main comparison; kept for completeness)
    "maximum_review": "#4a3aa7",     # violet
    "edgecase_adaptive": "#2a78d6",  # blue (primary)
    "oracle_tuned_fixed": "#008300", # green
    "llm_detected_edgecase_routed": "#1baf7a",  # aqua
}
PROVIDER_LABELS = {"anthropic": "Claude\nSonnet", "gemini": "Gemini\n2.5 Pro", "qwen": "Qwen2.5-7B\n(local)"}
PROVIDER_COLORS = {"anthropic": "#2a78d6", "gemini": "#eb6834", "qwen": "#4a3aa7"}

MAPPED_COLOR = "#2a78d6"
UNMAPPED_COLOR = "#c3c2b7"


def savefig(fig, name):
    fig.savefig(OUT_DIR / f"{name}.png", bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT_DIR / name}.{{png,pdf}}")


def clean_axes(ax, y_grid=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE_AXIS)
    ax.tick_params(axis="both", length=0)
    if y_grid:
        ax.yaxis.grid(True, zorder=0)
        ax.set_axisbelow(True)
        ax.xaxis.grid(False)
    else:
        ax.grid(False)


def bar_labels(ax, bars, fmt="{:.2f}", color=INK_SECONDARY):
    for b in bars:
        h = b.get_height()
        ax.annotate(fmt.format(h), (b.get_x() + b.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center",
                    fontsize=8, color=color)


# --- Figure 1: Governance tradeoffs across policies, 10-seed bootstrap
# mean +/- 95% CI, small multiples. ---
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
        ("mitigation_accuracy", r"Mitigation accuracy $\uparrow$"),
        ("avg_care_suppression", r"Care suppression $\downarrow$"),
        ("avg_security_risk", r"Security risk $\downarrow$"),
        ("avg_accessibility_burden", r"Accessibility burden $\downarrow$"),
        ("avg_privacy_exposure", r"Privacy exposure $\downarrow$"),
        ("avg_energy_score", r"Energy score $\downarrow$"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.8))
    for ax, (metric, title) in zip(axes.flat, metrics):
        means = [by_policy[p][metric]["mean"] for p in policies]
        lo = [by_policy[p][metric]["mean"] - by_policy[p][metric]["ci_lower_95"] for p in policies]
        hi = [by_policy[p][metric]["ci_upper_95"] - by_policy[p][metric]["mean"] for p in policies]
        colors = [POLICY_COLORS[p] for p in policies]
        bars = ax.bar(
            range(len(policies)), means, color=colors, width=0.62, zorder=3,
            yerr=[lo, hi], capsize=2.5, error_kw={"linewidth": 0.9, "ecolor": INK_SECONDARY},
        )
        clean_axes(ax)
        ax.set_title(title, pad=8)
        ax.set_xticks(range(len(policies)))
        ax.set_xticklabels([POLICY_LABELS[p] for p in policies], fontsize=7.6)
        ax.set_ylim(0, 1.08)
        ax.yaxis.set_major_locator(mticker.MultipleLocator(0.25))
        bar_labels(ax, bars)

    fig.tight_layout(rect=(0, 0, 1, 1))
    savefig(fig, "fig1_governance_tradeoffs")


# --- Figure 2: Aggregate externality (Xk), severity-weighted vs uniform ---
def figure_xk_weighting():
    rows = json.loads(Path("experiments/results/full_evaluation_summary.json").read_text())
    rows_by_policy = {r["policy"]: r for r in rows}
    policies = ["strict_block", "always_escalate", "maximum_review", "edgecase_adaptive"]

    x = list(range(len(policies)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7, 4.6))
    severity = [rows_by_policy[p]["governance_externality"] for p in policies]
    uniform = [rows_by_policy[p]["governance_externality_uniform"] for p in policies]

    b1 = ax.bar([i - width / 2 for i in x], severity, width, label="Severity-weighted",
                color=[POLICY_COLORS[p] for p in policies], zorder=3)
    b2 = ax.bar([i + width / 2 for i in x], uniform, width, label="Uniform (1/5 each)",
                color=[POLICY_COLORS[p] for p in policies], alpha=0.42, zorder=3)
    bar_labels(ax, b1)
    bar_labels(ax, b2)

    clean_axes(ax)
    ax.set_ylabel("Aggregate externality $X_k$ (lower is better)")
    ax.set_title("Adaptive EdgeCase vs. Strict Block reverses\nunder uniform dimension weighting", pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels([POLICY_LABELS[p] for p in policies])
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=INK_SECONDARY, label="Severity-weighted (this paper)"),
        plt.Rectangle((0, 0), 1, 1, facecolor=INK_SECONDARY, alpha=0.42, label="Uniform (1/5 each)"),
    ]
    ax.legend(handles=handles, loc="upper left")
    ax.set_ylim(0, max(uniform + severity) * 1.3)
    fig.tight_layout()
    savefig(fig, "fig2_xk_weighting_sensitivity")


# --- Figure 3: Ablation analysis, step function ---
def figure_ablation():
    rows = json.loads(Path("experiments/results/ablation_analysis.json").read_text())
    labels = [r["configuration"] for r in rows]
    values = [r["mitigation_accuracy"] for r in rows]
    colors = [POLICY_COLORS["edgecase_adaptive"] if l == "Full EdgeCase" else INK_MUTED for l in labels]

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    bars = ax.bar(range(len(labels)), values, color=colors, width=0.58, zorder=3)
    bar_labels(ax, bars, fmt="{:.3f}")
    clean_axes(ax)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=18, ha="right")
    ax.set_ylabel("Mitigation accuracy")
    ax.set_ylim(0, 1.08)
    ax.set_title("Removing the registry or detector collapses accuracy;\nremoving instrumentation alone does not", pad=8)
    ax.annotate("instrumentation is not yet\nload-bearing for mitigation", xy=(4, 1.0), xytext=(3.05, 0.68),
                fontsize=8, ha="center", color=INK_SECONDARY,
                arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=0.9))
    fig.tight_layout()
    savefig(fig, "fig3_ablation_analysis")


# --- Figure 4: Cross-model comparison ---
def figure_cross_model():
    providers = ["anthropic", "gemini", "qwen"]
    summaries = {}
    for p in providers:
        for f in Path("experiments/results/real_models").glob(f"summary_{p}_*.json"):
            summaries[p] = json.loads(f.read_text())

    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    metrics = [
        ("governance_externality", r"Governance externality $\downarrow$", "{:.2f}", 1),
        ("avg_response_alignment", r"Response alignment $\uparrow$", "{:.2f}", 1),
        ("avg_latency_ms", "Avg. latency (s)", "{:.1f}s", 1 / 1000),
    ]
    for ax, (metric, title, fmt, scale) in zip(axes, metrics):
        values = [summaries[p][metric] * scale for p in providers]
        colors = [PROVIDER_COLORS[p] for p in providers]
        bars = ax.bar(range(len(providers)), values, color=colors, width=0.55, zorder=3)
        bar_labels(ax, bars, fmt=fmt)
        clean_axes(ax)
        ax.set_title(title, fontsize=9.5, pad=8)
        ax.set_xticks(range(len(providers)))
        ax.set_xticklabels([PROVIDER_LABELS[p] for p in providers], fontsize=8)
        ax.set_ylim(0, max(values) * 1.28)

    fig.tight_layout()
    savefig(fig, "fig4_cross_model_comparison")


# --- Figure 5: External validity coverage (AgentHarm + Agent-SafetyBench) ---
def figure_external_validity():
    data = json.loads(Path("experiments/results/external_validity.json").read_text())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, key, title in zip(
        axes,
        ("agentharm", "agent_safetybench"),
        ("AgentHarm (176 cases, 8/8 categories mapped)", "Agent-SafetyBench (2,000 cases, 4/8 mapped)"),
    ):
        by_cat = data[key]["by_category"]
        cats = sorted(by_cat.keys(), key=lambda c: -by_cat[c]["n_cases"])
        n_cases = [by_cat[c]["n_cases"] for c in cats]
        n_mapped = [by_cat[c]["n_mapped"] for c in cats]
        colors = [MAPPED_COLOR if m > 0 else UNMAPPED_COLOR for m in n_mapped]

        y = range(len(cats))
        ax.barh(y, n_cases, color=colors, height=0.62, zorder=3)
        ax.set_yticks(list(y))
        ax.set_yticklabels(cats, fontsize=8.5)
        ax.invert_yaxis()
        clean_axes(ax, y_grid=False)
        ax.xaxis.grid(True, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel("Cases")
        ax.set_title(title, fontsize=10, pad=8)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=MAPPED_COLOR, label="Mapped to an EdgeCase obligation"),
        plt.Rectangle((0, 0), 1, 1, color=UNMAPPED_COLOR, label="No corresponding obligation (unmapped)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout()
    savefig(fig, "fig5_external_validity_coverage")


# --- Figure 6: Two failure modes -- a correctly-specified deterministic
# harness vs. an LLM-driven one (left), and the cost of "correctly
# specified" when the registry's trigger vocabulary has a gap (right). ---
def figure_detector_swap_convergence():
    orig_all = json.loads(Path("experiments/results/statistical_summary.json").read_text())["ci_per_policy"]
    llm = json.loads(Path("experiments/results/llm_detected_edgecase_routed.json").read_text())
    spec_bug = json.loads(Path("experiments/results/specification_bug_analysis.json").read_text())

    def get(metrics, name):
        return next(m for m in metrics if m["metric"] == name)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

    ax = axes[0]
    labels = ["Rule-based\nharness", "LLM-detected,\nharness-routed"]
    means = [get(orig_all["edgecase_adaptive"], "mitigation_accuracy")["mean"], get(llm["ci_original"], "mitigation_accuracy")["mean"]]
    m0, m1 = orig_all["edgecase_adaptive"], llm["ci_original"]
    lo = [means[0] - get(m0, "mitigation_accuracy")["ci_lower_95"], means[1] - get(m1, "mitigation_accuracy")["ci_lower_95"]]
    hi = [get(m0, "mitigation_accuracy")["ci_upper_95"] - means[0], get(m1, "mitigation_accuracy")["ci_upper_95"] - means[1]]
    bars = ax.bar(range(2), means, color=[POLICY_COLORS["edgecase_adaptive"], POLICY_COLORS["llm_detected_edgecase_routed"]],
                   width=0.5, zorder=3, yerr=[lo, hi], capsize=3, error_kw={"linewidth": 1, "ecolor": INK_SECONDARY})
    bar_labels(ax, bars, fmt="{:.3f}")
    clean_axes(ax)
    ax.set_xticks(range(2))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.1)
    outcome = llm["outcome_counts"]
    ax.annotate(
        f"{outcome['wrong_type']}/{outcome['correct']+outcome['wrong_type']} errors,\none confusion pattern,\nconcentrated in banking",
        xy=(1, means[1]), xytext=(0.45, 0.52), fontsize=7.8, ha="center", color=INK_SECONDARY,
        arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=0.9),
    )
    ax.set_title("Same routing table, different detector", fontsize=10, pad=8)

    ax = axes[1]
    domains = list(spec_bug["before_fix"].keys())
    before_rates = [spec_bug["before_fix"][d]["rate"] * 100 for d in domains]
    after_rates = [spec_bug["after_fix"][d]["rate"] * 100 for d in domains]
    x = list(range(len(domains)))
    width = 0.34
    b1 = ax.bar([i - width / 2 for i in x], before_rates, width, label="Before fix", color=UNMAPPED_COLOR, zorder=3)
    b2 = ax.bar([i + width / 2 for i in x], after_rates, width, label="After fix", color=POLICY_COLORS["edgecase_adaptive"], zorder=3)
    bar_labels(ax, b1, fmt="{:.0f}%")
    bar_labels(ax, b2, fmt="{:.0f}%")
    clean_axes(ax)
    ax.set_xticks(x)
    ax.set_xticklabels([d.replace("_", "\n") for d in domains])
    ax.set_ylabel("Detection rate")
    ax.set_ylim(0, 118)
    ax.legend(loc="upper left")
    ax.set_title("Cost of an incomplete specification:\nsilent, total failure in the affected slice", fontsize=10, pad=8)

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
