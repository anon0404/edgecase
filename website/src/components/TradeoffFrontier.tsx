// @ts-nocheck
"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";

type Point = {
  policy: string;
  security: number;
  care: number;
  accessibility: number;
  privacy: number;
  energy_penalty: number;
};

const policyDescriptions: Record<string, string> = {
  strict_block:
    "Prioritizes security aggressively but suppresses care and accessibility.",
  always_escalate:
    "Routes uncertain cases toward human review while increasing security exposure.",
  always_verify:
    "Improves fraud resistance but creates heavy accessibility burden.",
  maximum_review:
    "Maximizes oversight depth but significantly increases energy and latency costs.",
  edgecase_adaptive:
    "Balances competing obligations through conflict-aware mitigation routing.",
};

const colors: Record<string, string> = {
  strict_block: "#101010",
  always_escalate: "#ff2a00",
  always_verify: "#7a6f63",
  maximum_review: "#f59e0b",
  edgecase_adaptive: "#0f766e",
};

export default function TradeoffFrontier() {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const [data, setData] = useState<Point[]>([]);
  const [hovered, setHovered] = useState<Point | null>(null);

  const [xMetric, setXMetric] = useState("security");
  const [yMetric, setYMetric] = useState("care");

  useEffect(() => {
    fetch("/data/tradeoff_frontier.json")
      .then((res) => res.json())
      .then(setData);
  }, []);

  const metricOptions = [
    { value: "security", label: "Security robustness" },
    { value: "care", label: "Care preservation" },
    { value: "accessibility", label: "Accessibility support" },
    { value: "privacy", label: "Privacy preservation" },
  ];

  const processed = useMemo(() => {
    return data.map((d) => ({
      ...d,
      x: d[xMetric],
      y: d[yMetric],
    }));
  }, [data, xMetric, yMetric]);

  useEffect(() => {
    if (!processed.length || !svgRef.current) return;

    const width = 920;
    const height = 540;
    const margin = {
      top: 40,
      right: 40,
      bottom: 70,
      left: 80,
    };

    const svg = d3.select(svgRef.current);

    svg.selectAll("*").remove();

    svg
      .attr("viewBox", `0 0 ${width} ${height}`)
      .style("overflow", "visible");

    svg
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("rx", 28)
      .attr("fill", "#fffaf0");

    const x = d3.scaleLinear()
      .domain([0, 1])
      .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
      .domain([0, 1])
      .range([height - margin.bottom, margin.top]);

    const grid = svg.append("g");

    grid.selectAll("line.horizontal")
      .data(d3.range(0, 1.01, 0.2))
      .join("line")
      .attr("x1", margin.left)
      .attr("x2", width - margin.right)
      .attr("y1", d => y(d))
      .attr("y2", d => y(d))
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.08);

    grid.selectAll("line.vertical")
      .data(d3.range(0, 1.01, 0.2))
      .join("line")
      .attr("y1", margin.top)
      .attr("y2", height - margin.bottom)
      .attr("x1", d => x(d))
      .attr("x2", d => x(d))
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.08);

    svg.append("g")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg.append("g")
      .attr("transform", `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(y));

    svg.append("text")
      .attr("x", width / 2)
      .attr("y", height - 18)
      .attr("text-anchor", "middle")
      .attr("font-size", 13)
      .attr("fill", "#51473d")
      .text(metricOptions.find(m => m.value === xMetric)?.label || xMetric);

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -(height / 2))
      .attr("y", 24)
      .attr("text-anchor", "middle")
      .attr("font-size", 13)
      .attr("fill", "#51473d")
      .text(metricOptions.find(m => m.value === yMetric)?.label || yMetric);

    svg.selectAll("circle.policy")
      .data(processed)
      .join("circle")
      .attr("cx", d => x(d.x))
      .attr("cy", d => y(d.y))
      .attr("r", d => 10 + d.energy_penalty * 24)
      .attr("fill", d => colors[d.policy])
      .attr("stroke", "#fffaf0")
      .attr("stroke-width", 3)
      .style("cursor", "pointer")
      .on("mouseenter", (_, d) => setHovered(d))
      .on("mouseleave", () => setHovered(null));

    svg.selectAll("text.label")
      .data(processed)
      .join("text")
      .attr("x", d => x(d.x))
      .attr("y", d => y(d.y) - 18)
      .attr("text-anchor", "middle")
      .attr("font-size", 11)
      .attr("font-family", "monospace")
      .attr("fill", "#101010")
      .text(d => d.policy);

  }, [processed, xMetric, yMetric]);

  return (
    <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6">
      <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Tradeoff frontier
          </p>

          <h3 className="mt-3 text-4xl font-semibold tracking-[-0.05em]">
            Single-objective optimization displaces harm.
          </h3>

          <p className="mt-5 text-lg leading-8 text-[#51473d]">
            The frontier visualizes how governance strategies optimize one
            objective while externalizing cost into another domain. Larger nodes
            indicate higher energy and oversight cost.
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-2 block font-mono text-xs uppercase tracking-[0.18em] text-[#51473d]">
                X-axis
              </label>

              <select
                value={xMetric}
                onChange={(e) => setXMetric(e.target.value)}
                className="w-full rounded-2xl border border-[#101010]/15 bg-[#fffaf0] p-3"
              >
                {metricOptions.map((m) => (
                  <option key={m.value} value={m.value}>
                    {m.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="mb-2 block font-mono text-xs uppercase tracking-[0.18em] text-[#51473d]">
                Y-axis
              </label>

              <select
                value={yMetric}
                onChange={(e) => setYMetric(e.target.value)}
                className="w-full rounded-2xl border border-[#101010]/15 bg-[#fffaf0] p-3"
              >
                {metricOptions.map((m) => (
                  <option key={m.value} value={m.value}>
                    {m.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-8 rounded-[1.5rem] bg-[#f6f1e7] p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-[#ff2a00]">
              Interpretation
            </p>

            {hovered ? (
              <>
                <h4 className="mt-3 text-2xl font-semibold">
                  {hovered.policy}
                </h4>

                <p className="mt-3 leading-7 text-[#51473d]">
                  {policyDescriptions[hovered.policy]}
                </p>

                <div className="mt-6 grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <div className="font-mono text-[#51473d]">
                      Security
                    </div>
                    <div>{hovered.security.toFixed(3)}</div>
                  </div>

                  <div>
                    <div className="font-mono text-[#51473d]">
                      Care
                    </div>
                    <div>{hovered.care.toFixed(3)}</div>
                  </div>

                  <div>
                    <div className="font-mono text-[#51473d]">
                      Accessibility
                    </div>
                    <div>{hovered.accessibility.toFixed(3)}</div>
                  </div>

                  <div>
                    <div className="font-mono text-[#51473d]">
                      Privacy
                    </div>
                    <div>{hovered.privacy.toFixed(3)}</div>
                  </div>
                </div>
              </>
            ) : (
              <p className="mt-3 leading-7 text-[#51473d]">
                Hover over a policy to inspect its governance tradeoff profile.
              </p>
            )}
          </div>
        </div>

        <div>
          <svg
            ref={svgRef}
            className="w-full rounded-[1.5rem]"
          />

          <div className="mt-5 grid gap-3 md:grid-cols-2">
            {processed.map((d) => (
              <div
                key={d.policy}
                className="rounded-2xl border border-[#101010]/12 bg-[#f6f1e7] p-4"
              >
                <div className="flex items-center gap-3">
                  <span
                    className="h-3 w-3 rounded-full"
                    style={{ background: colors[d.policy] }}
                  />

                  <div className="font-mono text-xs uppercase">
                    {d.policy}
                  </div>
                </div>

                <div className="mt-3 text-sm leading-6 text-[#51473d]">
                  {policyDescriptions[d.policy]}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
