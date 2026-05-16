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
  prevalence?: number;
  display_value?: string;
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

type Payload = {
  metadata: {
    name: string;
    seed: number;
    cases: number;
    description: string;
  };
  nodes: GraphNode[];
  links: GraphLink[];
  aggregate: Record<string, any>;
};

const typeColor: Record<NodeType, string> = {
  signal: "#7a6f63",
  collision: "#ff2a00",
  obligation: "#101010",
  mitigation: "#f59e0b",
};

const storySteps = [
  {
    title: "1. Signals enter the system",
    body: "Agent workflows emit signals such as jailbreak risk, self-harm disclosure, fraud risk, language barriers, privacy sensitivity, or compute pressure.",
  },
  {
    title: "2. Obligations activate",
    body: "Each signal may trigger one or more governance obligations: security, care, privacy, accessibility, safeguarding, safety, or environmental efficiency.",
  },
  {
    title: "3. Collisions appear",
    body: "A boundary collision occurs when valid obligations recommend incompatible actions over the same case, such as block versus escalate or safety review versus compute reduction.",
  },
  {
    title: "4. Mitigations route the case",
    body: "EdgeCase selects bounded strategies such as constrain-and-escalate, adaptive verification, split logging, or adaptive-depth review.",
  },
  {
    title: "5. Audit evidence is exported",
    body: "The framework records triggered obligations, selected mitigation, and externalities so evaluation does not hide displaced harms.",
  },
];

export default function CollisionNetwork() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const zoomRef = useRef<any>(null);
  const gRef = useRef<any>(null);

  const [data, setData] = useState<Payload | null>(null);
  const [selectedType, setSelectedType] = useState<NodeType | "all">("all");
  const [hovered, setHovered] = useState<GraphNode | null>(null);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [storyIndex, setStoryIndex] = useState(0);

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

    root
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("rx", 28)
      .attr("fill", "#fffaf0");

    const g = root.append("g");
    gRef.current = g;

    const zoom = d3
      .zoom()
      .scaleExtent([0.35, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    zoomRef.current = zoom;
    root.call(zoom);

    const link = g
      .append("g")
      .attr("stroke", "#101010")
      .attr("stroke-opacity", 0.16)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", (d) => Math.max(1, Math.sqrt(d.weight)));

    const node = g
      .append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => Math.min(26, 5 + Math.sqrt(d.weight) * 2.5))
      .attr("fill", (d) => typeColor[d.type])
      .attr("stroke", "#fffaf0")
      .attr("stroke-width", 2)
      .style("cursor", "grab")
      .on("mouseenter", (_, d) => setHovered(d))
      .on("mouseleave", () => setHovered(null))
      .on("click", (_, d) => setSelected(d))
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

    const label = g
      .append("g")
      .selectAll("text")
      .data(nodes.filter((d) => d.type === "collision" || d.weight > 18))
      .join("text")
      .text((d) =>
        d.type === "collision" && d.display_value
          ? `${d.label} · ${d.display_value}`
          : d.label
      )
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
      .force("charge", d3.forceManyBody().strength(-220))
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
    };
  }, [filtered]);

  function zoomBy(factor: number) {
    if (!svgRef.current || !zoomRef.current) return;
    d3.select(svgRef.current)
      .transition()
      .duration(250)
      .call(zoomRef.current.scaleBy, factor);
  }

  function resetZoom() {
    if (!svgRef.current || !zoomRef.current) return;
    d3.select(svgRef.current)
      .transition()
      .duration(300)
      .call(zoomRef.current.transform, d3.zoomIdentity);
  }

  if (!data) {
    return (
      <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-8">
        Loading simulation…
      </div>
    );
  }

  const activeNode = selected || hovered;
  const step = storySteps[storyIndex];

  return (
    <div className="rounded-[2rem] border border-[#101010]/15 bg-[#fffaf0] p-5">
      <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-[#ff2a00]">
            Interactive simulation
          </p>

          <h3 className="mt-3 text-4xl font-semibold tracking-[-0.05em]">
            How signals become obligations, collisions, and mitigations.
          </h3>

          <p className="mt-4 text-lg leading-8 text-[#51473d]">
            This network introduces the internal mechanics of EdgeCase. Signals enter from agent workflows, activate governance obligations, form boundary collisions, and route toward bounded mitigations. Collision percentages indicate how often each collision family appears across simulated workflow traces.
          </p>

          <div className="mt-5 rounded-[1.5rem] bg-[#f6f1e7] p-5">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
              Story mode
            </p>

            <h4 className="mt-3 text-2xl font-semibold tracking-[-0.03em]">
              {step.title}
            </h4>

            <p className="mt-3 leading-7 text-[#51473d]">{step.body}</p>

            <div className="mt-5 flex gap-2">
              {storySteps.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setStoryIndex(i)}
                  className={`h-2.5 rounded-full transition-all ${
                    storyIndex === i ? "w-9 bg-[#ff2a00]" : "w-2.5 bg-[#101010]/20"
                  }`}
                  aria-label={`Story step ${i + 1}`}
                />
              ))}
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            {Object.entries(data.aggregate).map(([kind, value]) => (
              <button
                key={kind}
                onClick={() => setSelectedType("collision")}
                className="rounded-2xl border border-[#101010]/15 bg-[#fffaf0] p-4 text-left transition hover:border-[#ff2a00]"
              >
                <div className="font-mono text-xs uppercase text-[#ff2a00]">
                  {kind.replaceAll("_", " ")}
                </div>
                <div className="mt-2 text-2xl font-semibold">{value.count}</div>
                <div className="text-xs text-[#51473d]">
                  observed traces · avg severity {value.avg_severity}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
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

            <div className="flex gap-2">
              <button
                onClick={() => zoomBy(1.25)}
                className="rounded-full border border-[#101010]/20 px-3 py-2 text-xs"
              >
                +
              </button>
              <button
                onClick={() => zoomBy(0.8)}
                className="rounded-full border border-[#101010]/20 px-3 py-2 text-xs"
              >
                −
              </button>
              <button
                onClick={resetZoom}
                className="rounded-full border border-[#101010]/20 px-3 py-2 text-xs"
              >
                Reset
              </button>
            </div>
          </div>

          <svg ref={svgRef} className="min-h-[460px] w-full rounded-[1.5rem]" />

          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_260px]">
            <div className="rounded-[1.5rem] bg-[#f6f1e7] p-5">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                How to read this
              </p>
              <p className="mt-3 text-sm leading-6 text-[#51473d]">
                Read the graph from grey signals to black obligations, then to red collision nodes and amber mitigation nodes. Percentages on collision nodes indicate prevalence across simulated workflow traces.
              </p>
            </div>

            <aside className="rounded-[1.5rem] bg-[#f6f1e7] p-5">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#ff2a00]">
                Node detail
              </p>

              {activeNode ? (
                <div className="mt-4">
                  <div className="text-xl font-semibold">{activeNode.label}</div>
                  <div className="mt-2 font-mono text-xs uppercase text-[#51473d]">
                    {activeNode.type}
                  </div>
                  <div className="mt-4 text-sm text-[#51473d]">
                    Frequency weight: {activeNode.weight}
                  </div>
                </div>
              ) : (
                <p className="mt-4 text-sm leading-6 text-[#51473d]">
                  Hover or click a node to inspect its role in the simulated
                  governance conflict network.
                </p>
              )}

              <div className="mt-5 space-y-3">
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
      </div>
    </div>
  );
}
