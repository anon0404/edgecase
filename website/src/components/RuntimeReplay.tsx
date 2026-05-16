// @ts-nocheck
"use client";

import { useEffect, useMemo, useState } from "react";

type Event = {
  timestamp: number;
  node_id: string;
  label: string;
  type: string;

  signals: string[];
  obligations: string[];

  collision: string | null;
  mitigation: string | null;

  metrics: {
    security: number;
    care: number;
    accessibility: number;
    privacy: number;
    energy: number;
  };
};

type Replay = {
  workflow: string;
  events: Event[];
};

const NODE_COLORS: Record<string, string> = {
  input: "#7a6f63",
  classifier: "#101010",
  validator: "#f59e0b",
  router: "#0f766e",
  audit: "#7c3aed",
};

export default function RuntimeReplay() {
  const [replays, setReplays] = useState<Replay[]>([]);

  const [workflow, setWorkflow] = useState("crisis");

  const [step, setStep] = useState(0);

  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    fetch("/data/runtime_replay.json")
      .then((r) => r.json())
      .then(setReplays);
  }, []);

  const replay = useMemo(
    () => replays.find((r) => r.workflow === workflow),
    [replays, workflow]
  );

  const current = replay?.events?.[step];

  useEffect(() => {
    if (!playing || !replay) return;

    const interval = setInterval(() => {
      setStep((s) => {
        if (s >= replay.events.length - 1) {
          setPlaying(false);
          return s;
        }

        return s + 1;
      });
    }, 1400);

    return () => clearInterval(interval);
  }, [playing, replay]);

  if (!replay || !current) {
    return (
      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-8">
          Loading runtime replay…
        </div>
      </section>
    );
  }

  return (
    <section
      id="runtime"
      className="mx-auto max-w-7xl px-6 py-8"
    >
      <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6 md:p-8">
        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
              Runtime governance replay
            </p>

            <h2 className="mt-4 text-4xl font-semibold tracking-[-0.05em] md:text-6xl">
              Observe governance state evolve during execution.
            </h2>

            <p className="mt-6 text-lg leading-8 text-[#51473d]">
              EdgeCase instruments workflow execution step-by-step, exposing
              obligation activation, collision emergence, mitigation routing,
              and externality drift in runtime.
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              {replays.map((r) => (
                <button
                  key={r.workflow}
                  onClick={() => {
                    setWorkflow(r.workflow);
                    setStep(0);
                    setPlaying(false);
                  }}
                  className={`rounded-full border px-4 py-2 text-xs transition ${
                    workflow === r.workflow
                      ? "border-[#101010] bg-[#101010] text-[#f6f1e7]"
                      : "border-[#101010]/20"
                  }`}
                >
                  {r.workflow}
                </button>
              ))}
            </div>

            <div className="mt-5 rounded-[1.5rem] bg-[#101010] p-5 text-[#f6f1e7]">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                Active runtime event
              </p>

              <div className="mt-4 text-2xl font-semibold">
                {current.label}
              </div>

              <div className="mt-2 font-mono text-xs uppercase text-[#d6cfc4]">
                {current.type}
              </div>

              <div className="mt-6 flex flex-wrap gap-2">
                {current.signals.map((s) => (
                  <span
                    key={s}
                    className="rounded-full bg-[#f6f1e7]/10 px-3 py-1 text-xs"
                  >
                    {s}
                  </span>
                ))}
              </div>

              {current.collision && (
                <div className="mt-6 rounded-xl border border-[#ff2a00] bg-[#ff2a00]/10 p-4">
                  <div className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                    Boundary collision detected
                  </div>

                  <div className="mt-2 text-sm">
                    {current.collision}
                  </div>

                  <div className="mt-4 text-sm text-[#d6cfc4]">
                    Mitigation:
                    {" "}
                    <span className="text-[#f6f1e7]">
                      {current.mitigation}
                    </span>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => {
                  setStep(0);
                  setPlaying(true);
                }}
                className="rounded-full bg-[#101010] px-5 py-2 text-sm text-[#f6f1e7]"
              >
                Replay workflow
              </button>

              <button
                onClick={() => setPlaying(false)}
                className="rounded-full border border-[#101010]/20 px-5 py-2 text-sm"
              >
                Pause
              </button>

              <button
                onClick={() =>
                  setStep((s) =>
                    Math.max(0, s - 1)
                  )
                }
                className="rounded-full border border-[#101010]/20 px-5 py-2 text-sm"
              >
                Prev
              </button>

              <button
                onClick={() =>
                  setStep((s) =>
                    Math.min(
                      replay.events.length - 1,
                      s + 1
                    )
                  )
                }
                className="rounded-full border border-[#101010]/20 px-5 py-2 text-sm"
              >
                Next
              </button>
            </div>
          </div>

          <div>
            <div className="rounded-[1.5rem] border border-[#101010]/10 bg-[#f6f1e7] p-6">
              <div className="flex items-center justify-between">
                {replay.events.map((event, idx) => {
                  const active = idx <= step;

                  const pulse =
                    idx === step && event.collision;

                  return (
                    <div
                      key={event.node_id}
                      className="flex flex-1 items-center"
                    >
                      <div className="relative flex flex-col items-center">
                        <div
                          className={`relative flex h-20 w-20 items-center justify-center rounded-2xl border-2 transition-all duration-700 ${
                            active
                              ? "scale-100 opacity-100"
                              : "scale-90 opacity-30"
                          }`}
                          style={{
                            background:
                              NODE_COLORS[event.type] || "#101010",
                            borderColor: pulse
                              ? "#ff2a00"
                              : "transparent",
                            boxShadow: pulse
                              ? "0 0 0 12px rgba(255,42,0,0.12)"
                              : "none",
                          }}
                        >
                          <div className="text-center text-xs font-medium text-[#f6f1e7]">
                            {event.label}
                          </div>

                          {pulse && (
                            <div className="absolute inset-0 animate-ping rounded-2xl border-2 border-[#ff2a00]" />
                          )}
                        </div>

                        <div className="mt-3 text-center text-xs text-[#51473d]">
                          step {idx + 1}
                        </div>
                      </div>

                      {idx < replay.events.length - 1 && (
                        <div
                          className={`mx-2 h-1 flex-1 rounded-full transition-all duration-700 ${
                            idx < step
                              ? "bg-[#101010]"
                              : "bg-[#101010]/10"
                          }`}
                        />
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {Object.entries(current.metrics).map(
                  ([key, value]) => (
                    <div
                      key={key}
                      className="rounded-2xl bg-[#fffaf0] p-4"
                    >
                      <div className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                        {key}
                      </div>

                      <div className="mt-2 text-3xl font-semibold tracking-[-0.04em]">
                        {value}
                      </div>

                      <div className="mt-3 h-2 rounded-full bg-[#101010]/10">
                        <div
                          className="h-2 rounded-full bg-[#101010] transition-all duration-700"
                          style={{
                            width: `${value * 100}%`,
                          }}
                        />
                      </div>
                    </div>
                  )
                )}
              </div>

              <div className="mt-5 rounded-[1.5rem] bg-[#fffaf0] p-5">
                <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                  Governance interpretation
                </p>

                <p className="mt-3 text-sm leading-7 text-[#51473d]">
                  As the workflow progresses, obligations activate dynamically.
                  Security interventions shift governance state toward stricter
                  control, while care and accessibility obligations pull toward
                  accommodation and escalation support. EdgeCase surfaces these
                  tensions before selecting bounded mitigations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
