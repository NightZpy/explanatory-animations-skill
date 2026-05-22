/**
 * Pattern A — Lifecycle, ported to Remotion.
 *
 * The anime.js version drives the dot's position via createTimeline.add() per hop.
 * In Remotion we instead derive everything from useCurrentFrame() — the dot's
 * position at frame F is a function of F, the node list, and the path sequence.
 *
 * This is the bridge between the two engines:
 *
 *   anime.js                          Remotion
 *   --------                          --------
 *   timeline.add({duration:700})  →   hopFrames = (700 / 1000) * fps
 *   delay:200                     →   gapFrames = (200 / 1000) * fps
 *   ease:"inOutSine"              →   Easing.sin  (remotion's Easing API)
 *   anime.engine.speed = 2        →   set fps higher / duration shorter
 */

import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { z } from "zod";

const toneSchema = z.enum(["pending", "warn", "ok", "bad"]);
type Tone = z.infer<typeof toneSchema>;

const TONE_COLORS: Record<Tone, string> = {
  pending: "#a1a1aa",
  warn:    "#d97706",
  ok:      "#16a34a",
  bad:     "#dc2626",
};

const nodeSchema = z.object({
  id: z.string(),
  label: z.string(),
  tone: toneSchema,
  x: z.number(),
  y: z.number(),
});

export const lifecycleSchema = z.object({
  title:     z.string(),
  nodes:     z.array(nodeSchema),
  edges:     z.array(z.tuple([z.string(), z.string()])),
  path:      z.array(z.string()),
  hopDurationMs: z.number().default(700),
  hopDelayMs:    z.number().default(200),
  trailingFreezeMs: z.number().default(1500),
  vertical:  z.boolean().default(false),
});

export type LifecycleProps = z.infer<typeof lifecycleSchema>;

export const defaultLifecycle: LifecycleProps = {
  title: "Job lifecycle",
  nodes: [
    { id: "queued",    label: "queued",    tone: "pending", x: 200, y: 540 },
    { id: "active",    label: "active",    tone: "warn",    x: 700, y: 540 },
    { id: "completed", label: "completed", tone: "ok",      x: 1200, y: 380 },
  ],
  edges: [
    ["queued", "active"],
    ["active", "completed"],
  ],
  path: ["queued", "active", "completed"],
  hopDurationMs: 700,
  hopDelayMs: 200,
  trailingFreezeMs: 1500,
  vertical: false,
};

export function lifecycleDuration(props: LifecycleProps, fps: number): number {
  const hops = Math.max(0, props.path.length - 1);
  const totalMs = hops * (props.hopDurationMs + props.hopDelayMs) + props.trailingFreezeMs;
  return Math.ceil((totalMs / 1000) * fps);
}

export const Lifecycle: React.FC<LifecycleProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const { nodes, edges, path, hopDurationMs, hopDelayMs, title } = props;

  // Total ms elapsed at this frame.
  const ms = (frame / fps) * 1000;

  // Find which hop is in progress.
  const hopMs = hopDurationMs + hopDelayMs;
  const totalHops = path.length - 1;
  let hopIdx = Math.min(totalHops - 1, Math.floor(ms / hopMs));
  let withinHopMs = ms - hopIdx * hopMs;

  if (ms > totalHops * hopMs) {
    // Past the last hop — pin at end.
    hopIdx = totalHops - 1;
    withinHopMs = hopDurationMs;
  }

  // Travel happens after the delay phase.
  let travelT = 0;
  if (withinHopMs < hopDelayMs) {
    travelT = 0;
  } else {
    travelT = (withinHopMs - hopDelayMs) / hopDurationMs;
  }
  travelT = Math.max(0, Math.min(1, travelT));

  // Eased progress
  const eased = Easing.bezier(0.45, 0, 0.55, 1)(travelT);

  // Compute dot position at this frame.
  const fromNode = nodes.find(n => n.id === path[hopIdx]);
  const toNode   = nodes.find(n => n.id === path[hopIdx + 1]);
  const dotX = fromNode && toNode ? interpolate(eased, [0, 1], [fromNode.x, toNode.x]) : 0;
  const dotY = fromNode && toNode ? interpolate(eased, [0, 1], [fromNode.y, toNode.y]) : 0;

  // Mark which nodes have been visited.
  const visitedIds = new Set<string>();
  for (let i = 0; i <= hopIdx; i++) visitedIds.add(path[i]);
  if (eased > 0.5) visitedIds.add(path[hopIdx + 1]);

  // View box centering — fit within the viewport.
  const xs = nodes.map(n => n.x);
  const ys = nodes.map(n => n.y);
  const pad = 100;
  const minX = Math.min(...xs) - pad;
  const minY = Math.min(...ys) - pad;
  const w    = (Math.max(...xs) - Math.min(...xs)) + pad * 2;
  const h    = (Math.max(...ys) - Math.min(...ys)) + pad * 2;

  return (
    <AbsoluteFill style={{ background: "#fafaf7", fontFamily: "Geist, system-ui, sans-serif" }}>
      <h1 style={{
        position: "absolute", top: 60, left: 80, right: 80,
        fontSize: 56, fontWeight: 700, color: "#09090b", letterSpacing: "-0.02em",
        textAlign: props.vertical ? "center" : "left",
      }}>{title}</h1>

      <svg viewBox={`${minX} ${minY} ${w} ${h}`}
           preserveAspectRatio="xMidYMid meet"
           style={{ position: "absolute", inset: 0, width, height, padding: "200px 80px 120px" }}>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#71717a"/>
          </marker>
        </defs>
        {edges.map(([from, to], i) => {
          const a = nodes.find(n => n.id === from);
          const b = nodes.find(n => n.id === to);
          if (!a || !b) return null;
          const dx = b.x - a.x, dy = b.y - a.y;
          const len = Math.hypot(dx, dy) || 1;
          const ux = dx / len, uy = dy / len;
          const r = 80;
          const isOnPath = path.indexOf(from) >= 0 && path.indexOf(to) === path.indexOf(from) + 1;
          const reached = isOnPath && visitedIds.has(to);
          return (
            <line key={i}
              x1={a.x + ux * r} y1={a.y + uy * r}
              x2={b.x - ux * r} y2={b.y - uy * r}
              stroke={reached ? TONE_COLORS[b.tone] : "#d4d4d8"}
              strokeWidth={3}
              markerEnd="url(#arrow)"
            />
          );
        })}
        {nodes.map(n => {
          const active = visitedIds.has(n.id);
          return (
            <g key={n.id}>
              <rect x={n.x - 80} y={n.y - 30} width={160} height={60} rx={12}
                fill={active ? `${TONE_COLORS[n.tone]}1f` : "#ffffff"}
                stroke={active ? TONE_COLORS[n.tone] : "#d4d4d8"}
                strokeWidth={2}
              />
              <text x={n.x} y={n.y + 7} textAnchor="middle"
                    fontFamily="Geist Mono, monospace" fontSize={22} fill="#09090b">
                {n.label}
              </text>
            </g>
          );
        })}
        <circle cx={dotX} cy={dotY} r={14}
                fill="#eab308" stroke="#713f12" strokeWidth={3}
                style={{ filter: "drop-shadow(0 0 18px rgba(234,179,8,.6))" }}
                opacity={travelT > 0 || hopIdx > 0 ? 1 : 0} />
      </svg>
    </AbsoluteFill>
  );
};
