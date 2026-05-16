"use client";

import { useState } from "react";
import { domains } from "@/data/domains";
import {
  GitBranch,
  ShieldCheck,
  Zap,
  Route,
  FileJson,
  ArrowRight,
} from "lucide-react";

const architecture = [
  {
    title: "Workflow trace",
    body: "Capture routing, validators, memory, tools, model calls, and escalation decisions.",
    icon: GitBranch,
  },
  {
    title: "Obligation registry",
    body: "Represent security, care, privacy, accessibility, fairness, compliance, and energy as triggerable obligations.",
    icon: ShieldCheck,
  },
  {
    title: "Collision detector",
    body: "Detect when valid obligations recommend incompatible actions over the same case.",
    icon: Zap,
  },
  {
    title: "Mitigation router",
    body: "Choose bounded responses such as adaptive verification, split logging, or constrain-and-escalate.",
    icon: Route,
  },
  {
    title: "Audit artifact",
    body: "Export evidence showing signals, obligations, conflict type, mitigation, and externalities.",
    icon: FileJson,
  },
];

const collisions = [
  {
    name: "Block vs Escalate",
    signals: ["policy_evasion", "self_harm"],
    obligations: ["security.block", "care.escalate"],
    mitigation: "constrain_and_escalate",
  },
  {
    name: "Verify vs Accessibility",
    signals: ["fraud_risk", "language_barrier"],
    obligations: ["fraud.verify", "accessibility.reduce_burden"],
    mitigation: "adaptive_verification",
  },
  {
    name: "Privacy vs Safeguarding",
    signals: ["sensitive_data", "abuse_disclosure"],
    obligations: ["privacy.minimize", "safeguarding.preserve_context"],
    mitigation: "split_logging",
  },
  {
    name: "Safety vs Energy",
    signals: ["high_risk", "compute_pressure"],
    obligations: ["safety.increase_review", "energy.reduce_compute"],
    mitigation: "adaptive_depth",
  },
  {
    name: "Explain vs Exploitability",
    signals: ["transparency_request", "policy_evasion"],
    obligations: ["transparency.explain", "security.limit_exploitability"],
    mitigation: "layered_explanation",
  },
  {
    name: "Memory Care vs Memory Poisoning",
    signals: ["memory_update", "memory_poisoning_risk"],
    obligations: ["memory.personalize", "memory.protect"],
    mitigation: "typed_memory",
  },
];

export default function FrameworkExplorer() {
  const [selectedCollision, setSelectedCollision] = useState(collisions[0]);
  const [selectedDomain, setSelectedDomain] = useState(domains[0]);

  return (
    <section id="framework" className="mx-auto max-w-7xl px-6 py-8">
      <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
        Framework
      </p>

      <h2 className="mt-4 max-w-5xl text-4xl font-semibold tracking-[-0.05em] md:text-6xl">
        Conflict-aware assurance for agentic systems.
      </h2>

      <p className="mt-6 max-w-3xl text-lg leading-8 text-[#51473d]">
        EdgeCase connects workflow traces to governance obligations, detects
        boundary collisions, routes bounded mitigations, and exports audit
        evidence for downstream evaluation.
      </p>

      <div className="mt-5 grid gap-4 md:grid-cols-5">
        {architecture.map((item, index) => (
          <div
            key={item.title}
            className="relative rounded-3xl border border-[#101010]/15 bg-[#fffaf0] p-5"
          >
            <item.icon className="mb-8 h-6 w-6 text-[#ff2a00]" />
            <div className="font-mono text-xs text-[#ff2a00]">0{index + 1}</div>
            <h3 className="mt-2 text-xl font-semibold tracking-[-0.03em]">
              {item.title}
            </h3>
            <p className="mt-3 text-sm leading-6 text-[#51473d]">{item.body}</p>

            {index < architecture.length - 1 && (
              <ArrowRight className="absolute -right-3 top-1/2 hidden h-6 w-6 text-[#ff2a00] md:block" />
            )}
          </div>
        ))}
      </div>

      <div className="mt-5 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
            Boundary collision explorer
          </p>

          <h3 className="mt-3 text-3xl font-semibold tracking-[-0.04em]">
            The same signal can trigger incompatible duties.
          </h3>

          <div className="mt-6 grid gap-2">
            {collisions.map((collision) => (
              <button
                key={collision.name}
                onClick={() => setSelectedCollision(collision)}
                className={`rounded-2xl border p-4 text-left transition ${
                  selectedCollision.name === collision.name
                    ? "border-[#101010] bg-[#101010] text-[#f6f1e7]"
                    : "border-[#101010]/15 bg-[#fffaf0]"
                }`}
              >
                <div className="font-mono text-xs uppercase tracking-[0.15em]">
                  {collision.name}
                </div>
                <div
                  className={`mt-2 text-sm ${
                    selectedCollision.name === collision.name
                      ? "text-[#d6cfc4]"
                      : "text-[#51473d]"
                  }`}
                >
                  {collision.signals.join(" + ")}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
            Selected collision
          </p>

          <h3 className="mt-3 text-3xl font-semibold tracking-[-0.04em]">
            {selectedCollision.name}
          </h3>

          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl bg-[#f6f1e7] p-4">
              <div className="font-mono text-xs uppercase tracking-[0.15em] text-[#ff2a00]">
                Signals
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {selectedCollision.signals.map((signal) => (
                  <span key={signal} className="rounded-full bg-[#101010] px-3 py-1 text-xs text-[#f6f1e7]">
                    {signal}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-2xl bg-[#f6f1e7] p-4">
              <div className="font-mono text-xs uppercase tracking-[0.15em] text-[#ff2a00]">
                Obligations
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {selectedCollision.obligations.map((obligation) => (
                  <span key={obligation} className="rounded-full border border-[#101010]/20 px-3 py-1 text-xs">
                    {obligation}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-2xl bg-[#f6f1e7] p-4">
              <div className="font-mono text-xs uppercase tracking-[0.15em] text-[#ff2a00]">
                Mitigation
              </div>
              <div className="mt-3 rounded-full bg-[#ff2a00] px-3 py-1 text-xs text-[#f6f1e7]">
                {selectedCollision.mitigation}
              </div>
            </div>
          </div>

          <div className="mt-5">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
              Application domains
            </p>

            <div className="mt-4 flex flex-wrap gap-2">
              {domains.map((domain) => (
                <button
                  key={domain.name}
                  onClick={() => setSelectedDomain(domain)}
                  className={`rounded-full border px-3 py-2 text-xs transition ${
                    selectedDomain.name === domain.name
                      ? "border-[#101010] bg-[#101010] text-[#f6f1e7]"
                      : "border-[#101010]/20"
                  }`}
                >
                  {domain.name}
                </button>
              ))}
            </div>

            <div className="mt-5 rounded-2xl bg-[#101010] p-5 text-[#f6f1e7]">
              <div className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                {selectedDomain.collision}
              </div>
              <div className="mt-2 text-2xl font-semibold">
                {selectedDomain.name}
              </div>
              <p className="mt-3 text-sm leading-6 text-[#d6cfc4]">
                {selectedDomain.description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
