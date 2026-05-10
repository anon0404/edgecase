import Image from "next/image";
import {
  ArrowRight,
  FileJson,
  GitBranch,
  Package,
  Server,
  ShieldCheck,
  Zap,
} from "lucide-react";

const collisions = [
  {
    title: "Block vs Escalate",
    body: "A jailbreak-like signal also indicates crisis, coercion, or self-harm risk.",
  },
  {
    title: "Verify vs Accessibility",
    body: "Fraud controls burden disabled, distressed, or non-native users.",
  },
  {
    title: "Privacy vs Safeguarding",
    body: "Minimization removes context needed for intervention or protected review.",
  },
  {
    title: "Safety vs Energy",
    body: "Multi-pass safety improves robustness while increasing cost, latency, and emissions.",
  },
];

const metrics = [
  "Collision rate",
  "Suppressed-care rate",
  "Escalation precision",
  "Over-refusal rate",
  "Mitigation externality score",
  "Safety-energy profile",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f6f1e7] text-[#101010]">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
        <a href="#" className="flex items-center gap-4">
          <Image
            src="/edgecase-logo.png"
            alt="EdgeCase logo"
            width={72}
            height={72}
            className="h-16 w-16 object-contain"
            priority
          />
          <span className="font-mono text-2xl tracking-tight">
            EdgeCase
          </span>
        </a>

        <div className="hidden gap-7 text-sm md:flex">
          <a href="#framework">Framework</a>
          <a href="#python">Python</a>
          <a href="#api">API</a>
          <a href="#experiments">Experiments</a>
        </div>
      </nav>

      <section className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:grid-cols-[1.15fr_0.85fr] md:py-28">
        <div>
          <p className="mb-5 font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Conflict-aware assurance for agentic AI
          </p>

          <h1 className="max-w-5xl text-5xl font-semibold leading-[0.92] tracking-[-0.06em] md:text-8xl">
            When safety objectives collide.
          </h1>

          <p className="mt-8 max-w-2xl text-lg leading-8 text-[#51473d]">
            EdgeCase detects boundary collisions where legitimate governance
            obligations recommend incompatible actions: block versus escalate,
            verify versus accessibility, privacy versus safeguarding, and safety
            versus energy efficiency.
          </p>

          <div className="mt-10 flex flex-wrap gap-3">
            <a
              href="#python"
              className="rounded-full bg-[#101010] px-5 py-3 text-sm text-white transition hover:bg-[#2a2a2a]"
            >
              Install Python package
            </a>

            <a
              href="#api"
              className="rounded-full border border-[#101010]/25 px-5 py-3 text-sm transition hover:bg-[#101010] hover:text-white"
            >
              Explore API <ArrowRight className="ml-1 inline h-4 w-4" />
            </a>
          </div>
        </div>

        <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6 shadow-sm">
          <div className="mb-4 font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Example audit artifact
          </div>

          <pre className="overflow-x-auto rounded-2xl bg-[#101010] p-6 text-sm leading-6 text-[#f6f1e7]">
{`{
  "case_id": "block_vs_escalate_001",
  "triggered_obligations": [
    "security.block",
    "care.escalate"
  ],
  "collision": "block_vs_escalate",
  "selected_mitigation": "constrain_and_escalate",
  "externalities": {
    "care_suppression_risk": 0.72,
    "security_risk": 0.41,
    "energy_cost": "medium"
  }
}`}
          </pre>
        </div>
      </section>

      <section id="framework" className="mx-auto max-w-7xl px-6 py-16">
        <div className="border-y border-[#101010]/15 py-14">
          <h2 className="max-w-3xl text-4xl font-semibold tracking-[-0.04em] md:text-6xl">
            From single-objective safety to obligation conflict detection.
          </h2>

          <div className="mt-10 grid gap-4 md:grid-cols-4">
            {[
              ["Obligation registry", ShieldCheck],
              ["Workflow traces", GitBranch],
              ["Collision detector", Zap],
              ["Audit artifacts", FileJson],
            ].map(([title, Icon]) => (
              <div
                key={title as string}
                className="rounded-3xl border border-[#101010]/15 bg-[#fffaf0] p-6"
              >
                {(() => {
                  const C = Icon as any;
                  return <C className="mb-10 h-6 w-6 text-[#ff2a00]" />;
                })()}

                <h3 className="text-xl font-medium">
                  {title as string}
                </h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
          Boundary collisions
        </p>

        <h2 className="mt-4 text-4xl font-semibold tracking-[-0.04em] md:text-6xl">
          The same signal can trigger incompatible duties.
        </h2>

        <div className="mt-10 grid gap-4 md:grid-cols-2">
          {collisions.map((item) => (
            <div
              key={item.title}
              className="rounded-3xl border border-[#101010]/15 bg-[#fffaf0] p-7"
            >
              <h3 className="font-mono text-sm uppercase tracking-widest">
                {item.title}
              </h3>

              <p className="mt-5 text-lg leading-7 text-[#51473d]">
                {item.body}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section
        id="python"
        className="mx-auto grid max-w-7xl gap-8 px-6 py-16 md:grid-cols-2"
      >
        <div>
          <Package className="mb-5 h-8 w-8 text-[#ff2a00]" />

          <h2 className="text-4xl font-semibold tracking-[-0.04em] md:text-6xl">
            Python package.
          </h2>

          <p className="mt-6 text-lg leading-8 text-[#51473d]">
            Instrument agent workflows, register governance obligations,
            detect collisions, score externalities, and export audit logs.
          </p>
        </div>

        <pre className="overflow-x-auto rounded-3xl bg-[#101010] p-6 text-sm leading-6 text-[#f6f1e7]">
{`pip install edgecase

from edgecase import Registry, Trace, detect

registry = Registry.default()

trace = Trace(
    signals=["jailbreak", "self_harm"],
    workflow="assistant_response"
)

report = detect(trace, registry)

print(report.collision_type)
print(report.recommended_mitigation)`}
        </pre>
      </section>

      <section
        id="api"
        className="mx-auto grid max-w-7xl gap-8 px-6 py-16 md:grid-cols-2"
      >
        <div>
          <Server className="mb-5 h-8 w-8 text-[#ff2a00]" />

          <h2 className="text-4xl font-semibold tracking-[-0.04em] md:text-6xl">
            Hosted API.
          </h2>

          <p className="mt-6 text-lg leading-8 text-[#51473d]">
            Send workflow traces to EdgeCase and receive conflict reports,
            mitigation recommendations, and governance-ready JSON evidence.
          </p>
        </div>

        <pre className="overflow-x-auto rounded-3xl bg-[#101010] p-6 text-sm leading-6 text-[#f6f1e7]">
{`curl -X POST https://api.edgecase.dev/v1/detect \\
  -H "Content-Type: application/json" \\
  -d '{
    "signals": ["fraud_risk", "accessibility_need"],
    "workflow": "identity_verification"
  }'`}
        </pre>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16">
        <div className="rounded-[2rem] bg-[#101010] p-6 text-[#f6f1e7] md:p-10">
          <p className="mb-4 font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Audit artifact
          </p>

          <pre className="overflow-x-auto text-sm leading-6">
{`{
  "case_id": "block_vs_escalate_001",
  "triggered_obligations": [
    "security.block",
    "care.escalate"
  ],
  "collision": "block_vs_escalate",
  "selected_mitigation": "constrain_and_escalate",
  "externalities": {
    "care_suppression_risk": 0.72,
    "security_risk": 0.41,
    "energy_cost": "medium"
  }
}`}
          </pre>
        </div>
      </section>

      <section id="experiments" className="mx-auto max-w-7xl px-6 py-16">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
          Experiments
        </p>

        <h2 className="mt-4 max-w-4xl text-4xl font-semibold tracking-[-0.04em] md:text-6xl">
          Measuring harms displaced by single-objective optimization.
        </h2>

        <div className="mt-10 flex flex-wrap gap-3">
          {metrics.map((metric) => (
            <span
              key={metric}
              className="rounded-full border border-[#101010]/20 bg-[#fffaf0] px-4 py-2 text-sm"
            >
              {metric}
            </span>
          ))}
        </div>
      </section>

      <footer className="mx-auto flex max-w-7xl flex-col gap-4 border-t border-[#101010]/15 px-6 py-10 text-sm text-[#6f675f] md:flex-row md:items-center md:justify-between">
        <p className="font-mono">EdgeCase</p>
        <p>Anonymous research artifact for double-anonymous review.</p>
      </footer>
    </main>
  );
}
