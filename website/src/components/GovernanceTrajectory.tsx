// @ts-nocheck
"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";

type Step = {
  step: number;
  event: string;
  description: string;
  security: number;
  care_accessibility: number;
  privacy_exposure: number;
  energy: number;
  signals: string[];
  obligations: string[];
  collision: string | null;
  mitigation: string | null;
};

type Trajectory = {
  id: string;
  title: string;
  domain: string;
  steps: Step[];
};

export default function GovernanceTrajectory() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [trajectories, setTrajectories] = useState<Trajectory[]>([]);
  const [activeId, setActiveId] = useState<string>("");
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    fetch("/data/governance_trajectories.json")
      .then((res) => res.json())
      .then((payload) => {
        setTrajectories(payload.trajectories);
        setActiveId(payload.trajectories[0].id);
      });
  }, []);

  const active = useMemo(
    () => trajectories.find((t) => t.id === activeId),
    [trajectories, activeId]
  );

  const currentStep = active?.steps[stepIndex];

  useEffect(() => {
    if (!active || !svgRef.current) return;

    const width = 900;
    const height = 560;
    const margin = { top: 44, right: 46, bottom: 74, left: 76 };

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    svg.attr("viewBox", `0 0 ${width} ${height}`);

    svg
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("rx", 28)
      .attr("fill", "#fffaf0");

    const x = d3
      .scaleLinear()
      .domain([0, 1])
      .range([margin.left, width - margin.right]);

    const y = d3
      .scaleLinear()
      .domain([0, 1])
      .range([height - margin.bottom, margin.top]);

    const r = d3
      .scaleLinear()
      .domain([0, 1])
      .range([10, 34]);

    const color = d3
      .scaleLinear<string>()
      .domain([0, 1])
      .range(["#101010", "#ff2a00"]);

    svg
      .append("g")
      .selectAll("line.h")
      .data(d3.range(0, 1.01, 0.2))
      .join("line")
      .attr("x1", margin.left)
      .attr("x2", width - margin.right)
      .attr("y1", (d) => y(d))
      .attr("y2", (d) => y(d))
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.08);

    svg
      .append("g")
      .selectAll("line.v")
      .data(d3.range(0, 1.01, 0.2))
      .join("line")
      .attr("y1", margin.top)
      .attr("y2", height - margin.bottom)
      .attr("x1", (d) => x(d))
      .attr("x2", (d) => x(d))
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.08);

    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(5));

    svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y).ticks(5));

    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", height - 22)
      .attr("text-anchor", "middle")
      .attr("font-family", "monospace")
      .attr("font-size", 18)
      .text("Security strictness");

    svg
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", 24)
      .attr("text-anchor", "middle")
      .attr("font-family", "monospace")
      .attr("font-size", 18)
      .text("Care + accessibility preservation");

    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", 24)
      .attr("text-anchor", "middle")
      .attr("font-family", "monospace")
      .attr("font-size", 16)
      .attr("font-weight", 600)
      .attr("fill", "#51473d")
      .text("Size = energy cost · Color = privacy exposure");

    const shown = active.steps.slice(0, stepIndex + 1);

    const line = d3
      .line<Step>()
      .x((d) => x(d.security))
      .y((d) => y(d.care_accessibility))
      .curve(d3.curveCatmullRom.alpha(0.5));

    svg
      .append("path")
      .datum(shown)
      .attr("fill", "none")
      .attr("stroke", "#101010")
      .attr("stroke-width", 2.5)
      .attr("stroke-dasharray", "6 5")
      .attr("d", line);

    svg
      .append("g")
      .selectAll("circle.history")
      .data(shown)
      .join("circle")
      .attr("cx", (d) => x(d.security))
      .attr("cy", (d) => y(d.care_accessibility))
      .attr("r", (d) => r(d.energy))
      .attr("fill", (d) => color(d.privacy_exposure))
      .attr("fill-opacity", (d, i) => (i === stepIndex ? 0.95 : 0.35))
      .attr("stroke", (d) => (d.collision ? "#ff2a00" : "#fffaf0"))
      .attr("stroke-width", (d) => (d.collision ? 4 : 2));

    svg
      .append("g")
      .selectAll("text.step-label")
      .data(shown)
      .join("text")
      .attr("x", (d) => x(d.security))
      .attr("y", (d) => y(d.care_accessibility) - r(d.energy) - 9)
      .attr("text-anchor", "middle")
      .attr("font-family", "monospace")
      .attr("font-size", 11)
      .attr("fill", "#101010")
      .text((d) => `S${d.step}`);

    const current = active.steps[stepIndex];

    svg
      .append("circle")
      .attr("cx", x(current.security))
      .attr("cy", y(current.care_accessibility))
      .attr("r", r(current.energy) + 8)
      .attr("fill", "none")
      .attr("stroke", "#ff2a00")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", "4 4")
      .append("animate")
      .attr("attributeName", "r")
      .attr("values", `${r(current.energy) + 5};${r(current.energy) + 14};${r(current.energy) + 5}`)
      .attr("dur", "1.6s")
      .attr("repeatCount", "indefinite");
  }, [active, stepIndex]);

  if (!active || !currentStep) {
    return (
      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-8">
          Loading trajectory simulator…
        </div>
      </section>
    );
  }

  return (
    <section id="trajectory" className="mx-auto max-w-7xl px-6 py-8">
      <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6 md:p-8">
        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
              Governance trajectory simulator
            </p>

            <h2 className="mt-4 text-4xl font-semibold tracking-[-0.05em] md:text-6xl">
              Watch obligations collide during agent execution.
            </h2>

            <p className="mt-6 text-lg leading-8 text-[#51473d]">
              Each trajectory shows how an agentic workflow moves through
              governance state space as signals, obligations, collisions, and
              mitigations activate over time.
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              {trajectories.map((trajectory) => (
                <button
                  key={trajectory.id}
                  onClick={() => {
                    setActiveId(trajectory.id);
                    setStepIndex(0);
                  }}
                  className={`rounded-full border px-4 py-2 text-xs transition ${
                    activeId === trajectory.id
                      ? "border-[#101010] bg-[#101010] text-[#f6f1e7]"
                      : "border-[#101010]/20"
                  }`}
                >
                  {trajectory.domain}
                </button>
              ))}
            </div>

            <div className="mt-5 rounded-[1.5rem] bg-[#f6f1e7] p-5">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                Current step
              </p>

              <h3 className="mt-3 text-2xl font-semibold tracking-[-0.03em]">
                S{currentStep.step}: {currentStep.event}
              </h3>

              <p className="mt-3 leading-7 text-[#51473d]">
                {currentStep.description}
              </p>

              <div className="mt-5 flex gap-2">
                {active.steps.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setStepIndex(i)}
                    className={`h-2.5 rounded-full transition-all ${
                      stepIndex === i
                        ? "w-10 bg-[#ff2a00]"
                        : "w-2.5 bg-[#101010]/20"
                    }`}
                    aria-label={`Step ${i + 1}`}
                  />
                ))}
              </div>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <div className="rounded-[1.5rem] bg-[#101010] p-5 text-[#f6f1e7]">
                <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                  Active obligations
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {currentStep.obligations.length ? (
                    currentStep.obligations.map((o) => (
                      <span key={o} className="rounded-full bg-[#f6f1e7]/10 px-3 py-1 text-xs">
                        {o}
                      </span>
                    ))
                  ) : (
                    <span className="text-sm text-[#d6cfc4]">None yet</span>
                  )}
                </div>
              </div>

              <div className="rounded-[1.5rem] bg-[#101010] p-5 text-[#f6f1e7]">
                <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                  Collision / mitigation
                </p>
                <div className="mt-4 text-sm leading-6 text-[#d6cfc4]">
                  <div>
                    Collision:{" "}
                    <span className="text-[#f6f1e7]">
                      {currentStep.collision || "none"}
                    </span>
                  </div>
                  <div>
                    Mitigation:{" "}
                    <span className="text-[#f6f1e7]">
                      {currentStep.mitigation || "pending"}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setStepIndex(Math.max(0, stepIndex - 1))}
                className="rounded-full border border-[#101010]/20 px-4 py-2 text-sm"
              >
                Previous
              </button>
              <button
                onClick={() =>
                  setStepIndex(Math.min(active.steps.length - 1, stepIndex + 1))
                }
                className="rounded-full bg-[#101010] px-4 py-2 text-sm text-[#f6f1e7]"
              >
                Next step
              </button>
            </div>
          </div>

          <div>
            <svg ref={svgRef} className="min-h-[560px] w-full rounded-[1.5rem]" />

            <div className="mt-4 rounded-[1.5rem] bg-[#f6f1e7] p-5">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                How to read this
              </p>
              <p className="mt-3 text-sm leading-6 text-[#51473d]">
                Movement to the right means stricter security control. Movement
                upward means better care and accessibility preservation. Larger
                bubbles mean greater energy or review cost. Redder bubbles mean
                higher privacy exposure. A red outline marks a boundary
                collision.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
