export default function Methodology() {
  const items = [
    [
      "Benchmark generation",
      "Paired conflict scenarios are generated across crisis, banking, healthcare, support, moderation, enterprise, and education domains."
    ],
    [
      "Policy comparison",
      "Single-objective policies are compared against adaptive EdgeCase routing."
    ],
    [
      "Runtime traces",
      "Executable workflow DAGs record node activations, signals, obligations, collisions, mitigations, and externalities."
    ],
    [
      "Metrics",
      "Evaluation tracks mitigation accuracy, care suppression, security risk, accessibility burden, privacy exposure, and energy score."
    ],
    [
      "Model-backed evaluation",
      "Real-model runs compare governance conflict consistency across Anthropic Claude, Google Gemini, and Qwen open-model workflows."
    ]
  ];

  return (
    <section id="methodology" className="mx-auto max-w-7xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
        Methodology
      </p>

      <h2 className="mt-4 max-w-4xl text-4xl font-semibold tracking-[-0.05em] md:text-6xl">
        From traces to measurable governance trade-offs.
      </h2>

      <div className="mt-10 grid gap-4 md:grid-cols-2">
        {items.map(([title, body]) => (
          <div
            key={title}
            className="rounded-3xl border border-[#101010]/15 bg-[#fffaf0] p-6"
          >
            <h3 className="text-2xl font-semibold tracking-[-0.03em]">
              {title}
            </h3>
            <p className="mt-4 leading-7 text-[#51473d]">
              {body}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
