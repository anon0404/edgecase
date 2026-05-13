// @ts-nocheck
"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";

type NodeType = "signal" | "collision" | "obligation" | "mitigation";

type GraphNode = {
  id: string;
  label: string;
  type: NodeType;
  weight: number;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
};

type GraphLink = {
  source: string | GraphNode;
  target: string | GraphNode;
  type: string;
  weight: number;
};

type Aggregate = Record<
  string,
  {
    count: number;
    avg_severity: number;
    avg_ambiguity: number;
    avg_model_calls: number;
    avg_tokens: number;
    avg_latency_ms: number;
    avg_externalities: Record<string, number>;
  }
>;

type Payload = {
  metadata: {
    name: string;
    seed: number;
    cases: number;
    description: string;
  };
  nodes: GraphNode[];
  links: GraphLink[];
  aggregate: Aggregate;
};

const typeColor: Record<NodeType, string> = {
  signal: "#7a6f63",
  collision: "#ff2a00",
  obligation: "#101010",
  mitigation: "#f59e0b",
};

export default function CollisionNetwork() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [data, setData] = useState<Payload | null>(null);
  const [selectedType, setSelectedType] = useState<NodeType | "all">("all");
  const [hovered, setHovered] = useState<GraphNode | null>(null);

  useEffect(() => {
    fetch("/data/collision_network.json")
      .then((res) => res.json())
      .then(setData);
  }, []);

  const filtered = useMemo(() => {
    if (!data) return null;
    if (selectedType === "all") return data;

    const keep = new Set(
      data.nodes
        .filter((node) => node.type === selectedType || node.type === "collision")
        .map((node) => node.id)
    );

    return {
      ...data,
      nodes: data.nodes.filter((node) => keep.has(node.id)),
      links: data.links.filter((link) => {
        const source = typeof link.source === "string" ? link.source : link.source.id;
        const target = typeof link.target === "string" ? link.target : link.target.id;
        return keep.has(source) && keep.has(target);
      }),
    };
  }, [data, selectedType]);

  useEffect(() => {
    if (!filtered || !svgRef.current) return;

    const width = 980;
    const height = 620;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const nodes: GraphNode[] = filtered.nodes.map((d) => ({ ...d }));
    const links: GraphLink[] = filtered.links.map((d) => ({ ...d }));

    const root = svg
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("role", "img")
      .attr("aria-label", "Interactive EdgeCase collision network");

    const background = root
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("rx", 28)
      .attr("fill", "#fffaf0");

    const link = root
      .append("g")
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.16)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", (d) => Math.max(1, Math.sqrt(d.weight)));

    const node = root
      .append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => Math.min(24, 5 + Math.sqrt(d.weight) * 2.4))
      .attr("fill", (d) => typeColor[d.type])
      .attr("stroke", "#fffaf0")
      .attr("stroke-width", 2)
      .style("cursor", "grab")
      .on("mouseenter", (_, d) => setHovered(d))
      .on("mouseleave", () => setHovered(null))
      .call(
        d3
          .drag<SVGCircleElement, GraphNode>()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    const label = root
      .append("g")
      .selectAll("text")
      .data(nodes.filter((d) => d.type === "collision" || d.weight > 18))
      .join("text")
      .text((d) => d.label)
      .attr("font-size", 11)
      .attr("font-family", "monospace")
      .attr("fill", "#101010")
      .attr("paint-order", "stroke")
      .attr("stroke", "#fffaf0")
      .attr("stroke-width", 4)
      .attr("text-anchor", "middle");

    const simulation = d3
      .forceSimulation<GraphNode>(nodes)
      .force(
        "link",
        d3
          .forceLink<GraphNode, GraphLink>(links)
          .id((d) => d.id)
          .distance((d) => {
            if (d.type === "resolved_by") return 95;
            if (d.type === "activates") return 115;
            return 80;
          })
      )
      .force("charge", d3.forceManyBody().strength(-210))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide<GraphNode>().radius((d) => 18 + Math.sqrt(d.weight) * 2))
      .on("tick", () => {
        link
          .attr("x1", (d) => (d.source as GraphNode).x ?? 0)
          .attr("y1", (d) => (d.source as GraphNode).y ?? 0)
          .attr("x2", (d) => (d.target as GraphNode).x ?? 0)
          .attr("y2", (d) => (d.target as GraphNode).y ?? 0);

        node.attr("cx", (d) => d.x ?? 0).attr("cy", (d) => d.y ?? 0);

        label.attr("x", (d) => d.x ?? 0).attr("y", (d) => (d.y ?? 0) - 18);
      });

    return () => {
      simulation.stop();
      background.remove();
    };
  }, [filtered]);

  if (!data) {
    return (
      <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-8">
        Loading simulation…
      </div>
    );
  }

  return (
    <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-5">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Interactive simulation
          </p>
          <h3 className="mt-2 text-3xl font-semibold tracking-[-0.04em]">
            Boundary collision network
          </h3>
          <p className="mt-3 max-w-2xl text-[#51473d]">
            {data.metadata.cases} simulated agentic cases connect signals,
            obligations, collision types, and mitigation routes.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          {(["all", "signal", "collision", "obligation", "mitigation"] as const).map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`rounded-full border px-3 py-2 text-xs capitalize transition ${
                selectedType === type
                  ? "border-[#101010] bg-[#101010] text-[#f6f1e7]"
                  : "border-[#101010]/20 bg-transparent text-[#101010]"
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_280px]">
        <svg ref={svgRef} className="min-h-[420px] w-full rounded-[1.5rem]" />

        <aside className="rounded-[1.5rem] bg-[#f6f1e7] p-5">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
            Node detail
          </p>

          {hovered ? (
            <div className="mt-4">
              <div className="text-xl font-semibold">{hovered.label}</div>
              <div className="mt-2 font-mono text-xs uppercase text-[#51473d]">
                {hovered.type}
              </div>
              <div className="mt-4 text-sm text-[#51473d]">
                Frequency weight: {hovered.weight}
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-[#51473d]">
              Hover over a node to inspect its type and frequency in the
              simulated benchmark.
            </p>
          )}

          <div className="mt-8 space-y-3">
            {(Object.keys(typeColor) as NodeType[]).map((type) => (
              <div key={type} className="flex items-center gap-3 text-sm capitalize">
                <span
                  className="h-3 w-3 rounded-full"
                  style={{ backgroundColor: typeColor[type] }}
                />
                {type}
              </div>
            ))}
          </div>
        </aside>
      </div>
    </div>
  );
}
