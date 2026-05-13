// @ts-nocheck
"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

type Point = {
  policy: string;
  security: number;
  care: number;
  accessibility: number;
  privacy: number;
  energy_penalty: number;
};

const colors: Record<string, string> = {
  strict_block: "#101010",
  always_escalate: "#ff2a00",
  always_verify: "#f59e0b",
  maximum_review: "#7c3aed",
  edgecase_adaptive: "#0f766e",
};

const descriptions: Record<string, string> = {
  strict_block:
    "Prioritizes security robustness but suppresses care and accessibility.",
  always_escalate:
    "Optimizes escalation and support pathways while increasing security exposure.",
  always_verify:
    "Reduces fraud risk at the cost of accessibility burden and user friction.",
  maximum_review:
    "Maximizes review depth and oversight while increasing energy and latency.",
  edgecase_adaptive:
    "Attempts to balance competing obligations through conflict-aware mitigation routing.",
};

export default function TradeoffFrontier() {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const [points, setPoints] = useState<Point[]>([]);
  const [hovered, setHovered] = useState<Point | null>(null);

  useEffect(() => {
    fetch("/data/tradeoff_frontier.json")
      .then((res) => res.json())
      .then(setPoints);
  }, []);

  useEffect(() => {
    if (!points.length || !svgRef.current) return;

    const width = 920;
    const height = 560;
    const margin = { top: 40, right: 40, bottom: 70, left: 70 };

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

    const x = d3
      .scaleLinear()
      .domain([0, 1])
      .range([margin.left, width - margin.right]);

    const y = d3
      .scaleLinear()
      .domain([0, 1])
      .range([height - margin.bottom, margin.top]);

    const grid = svg.append("g");

    grid
      .selectAll("line.horizontal")
      .data(d3.range(0, 1.01, 0.2))
      .join("line")
      .attr("x1", margin.left)
      .attr("x2", width - margin.right)
      .attr("y1", (d) => y(d))
      .attr("y2", (d) => y(d))
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.08);

    grid
      .selectAll("line.vertical")
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
      .attr("y", height - 18)
      .attr("text-anchor", "middle")
      .attr("font-size", 14)
      .attr("font-family", "monospace")
      .text("Security robustness");

    svg
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", 22)
      .attr("text-anchor", "middle")
      .attr("font-size", 14)
      .attr("font-family", "monospace")
      .text("Care + accessibility preservation");

    svg
      .append("text")
      .attr("x", width - 210)
      .attr("y", 32)
      .attr("font-size", 12)
      .attr("font-family", "monospace")
      .attr("fill", "#51473d")
      .text("Bubble size = energy penalty");

    const bubbles = svg
      .append("g")
      .selectAll("circle")
      .data(points)
      .join("circle")
      .attr("cx", (d) => x(d.security))
      .attr("cy", (d) => y((d.care + d.accessibility) / 2))
      .attr("r", (d) => 16 + d.energy_penalty * 28)
      .attr("fill", (d) => colors[d.policy] || "#101010")
      .attr("fill-opacity", 0.85)
      .attr("stroke", "#fffaf0")
      .attr("stroke-width", 3)
      .style("cursor", "pointer")
      .on("mouseenter", (_, d) => setHovered(d))
      .on("mouseleave", () => setHovered(null));

    svg
      .append("g")
      .selectAll("text.labels")
      .data(points)
      .join("text")
      .attr("x", (d) => x(d.security))
      .attr("y", (d) => y((d.care + d.accessibility) / 2) - 24)
      .attr("text-anchor", "middle")
      .attr("font-size", 11)
      .attr("font-family", "monospace")
      .attr("fill", "#101010")
      .text((d) => d.policy.replaceAll("_", " "));

    svg
      .append("path")
      .datum(
        [...points].sort((a, b) => a.security - b.security)
      )
      .attr("fill", "none")
      .attr("stroke", "#0f766e")
      .attr("stroke-width", 2.5)
      .attr("stroke-dasharray", "7 5")
      .attr(
        "d",
        d3
          .line<Point>()
          .x((d) => x(d.security))
          .y((d) => y((d.care + d.accessibility) / 2))
      );

    bubbles.raise();
  }, [points]);

  return (
    <section className="mx-auto max-w-7xl px-6 py-16">
      <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-6 md:p-8">
        <div className="grid gap-10 lg:grid-cols-[0.85fr_1.15fr]">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
              Interactive tradeoff frontier
            </p>

            <h2 className="mt-4 text-4xl font-semibold tracking-[-0.05em] md:text-6xl">
              Single-objective optimization externalizes harm.
            </h2>

            <p className="mt-6 text-lg leading-8 text-[#51473d]">
              This visualization compares governance policies across competing
              objectives. Moving toward stronger security controls often reduces
              accessibility or suppresses care, while deeper review increases
              energy and latency costs.
            </p>

            <div className="mt-8 rounded-[1.5rem] bg-[#f6f1e7] p-5">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                How to interpret
              </p>

              <ul className="mt-4 space-y-3 text-sm leading-6 text-[#51473d]">
                <li>
                  • Rightward movement improves security robustness.
                </li>
                <li>
                  • Upward movement preserves care and accessibility.
                </li>
                <li>
                  • Larger bubbles indicate greater energy overhead.
                </li>
                <li>
                  • The dashed frontier approximates balanced governance trade-offs.
                </li>
              </ul>
            </div>

            <div className="mt-8 rounded-[1.5rem] bg-[#101010] p-5 text-[#f6f1e7]">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                Selected policy
              </p>

              {hovered ? (
                <>
                  <div className="mt-4 text-2xl font-semibold">
                    {hovered.policy.replaceAll("_", " ")}
                  </div>

                  <p className="mt-4 text-sm leading-6 text-[#d6cfc4]">
                    {descriptions[hovered.policy]}
                  </p>

                  <div className="mt-6 grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <div className="text-[#ff2a00]">Security</div>
                      <div>{hovered.security}</div>
                    </div>

                    <div>
                      <div className="text-[#ff2a00]">Care</div>
                      <div>{hovered.care}</div>
                    </div>

                    <div>
                      <div className="text-[#ff2a00]">Accessibility</div>
                      <div>{hovered.accessibility}</div>
                    </div>

                    <div>
                      <div className="text-[#ff2a00]">Energy penalty</div>
                      <div>{hovered.energy_penalty}</div>
                    </div>
                  </div>
                </>
              ) : (
                <p className="mt-4 text-sm leading-6 text-[#d6cfc4]">
                  Hover over a policy bubble to inspect how it shifts governance trade-offs.
                </p>
              )}
            </div>
          </div>

          <div>
            <svg
              ref={svgRef}
              className="min-h-[560px] w-full rounded-[1.5rem]"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
