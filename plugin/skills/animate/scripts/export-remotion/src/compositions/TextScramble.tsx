/**
 * Pattern M — Text scramble, ported to Remotion.
 *
 * Each character cycles through random glyphs before landing on its final
 * glyph. In anime.js this was driven by `text.split()` + `createTimeline`
 * with `ease: "steps(20)"`. In Remotion we compute the glyph per character
 * per frame from useCurrentFrame().
 */

import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { z } from "zod";

const GLYPHS = "█▓▒░@#$%&*+=<>?!~/\\|{}[]()01_-^X".split("");

export const scrambleSchema = z.object({
  text: z.string(),
  // ms per character to settle (from random → final)
  settleMs: z.number().default(700),
  // stagger between characters (ms)
  staggerMs: z.number().default(30),
  // hold time after all characters settled, before fade out
  holdMs: z.number().default(1500),
  background: z.string().default("#0f0f17"),
  foreground: z.string().default("#f4f4f5"),
  accent:     z.string().default("#22d3ee"),
  fontFamily: z.string().default("Geist Mono"),
  fontSize:   z.number().default(120),
});

export type ScrambleProps = z.infer<typeof scrambleSchema>;

export const defaultScramble: ScrambleProps = {
  text: "Make better stuff.",
  settleMs: 700,
  staggerMs: 30,
  holdMs: 1500,
  background: "#0f0f17",
  foreground: "#f4f4f5",
  accent: "#22d3ee",
  fontFamily: "Geist Mono",
  fontSize: 120,
};

export function scrambleDuration(props: ScrambleProps, fps: number): number {
  const totalMs = (props.text.length - 1) * props.staggerMs + props.settleMs + props.holdMs;
  return Math.ceil((totalMs / 1000) * fps);
}

// Deterministic pseudo-random so each render produces identical frames
// (Remotion requires deterministic renders for parallel rendering).
function det(seed: number): number {
  const x = Math.sin(seed * 9301 + 49297) * 233280;
  return x - Math.floor(x);
}
function glyphAt(charIndex: number, settleProgress: number): string {
  if (settleProgress >= 1) return ""; // caller knows the final
  // pick a glyph that mutates fast per frame at this character
  const tick = Math.floor(settleProgress * 16);
  const idx  = Math.floor(det(charIndex * 17 + tick * 23) * GLYPHS.length);
  return GLYPHS[idx];
}

export const TextScramble: React.FC<ScrambleProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const chars = Array.from(props.text);

  return (
    <AbsoluteFill style={{
      background: props.background,
      display: "flex", alignItems: "center", justifyContent: "center",
      padding: 80,
    }}>
      <h1 style={{
        margin: 0,
        fontFamily: `${props.fontFamily}, Geist Mono, monospace`,
        fontSize: props.fontSize,
        fontWeight: 700,
        color: props.foreground,
        letterSpacing: "-0.03em",
        textAlign: "center",
        lineHeight: 1.05,
        fontKerning: "none",
        whiteSpace: "pre-wrap",
      }}>
        {chars.map((finalChar, i) => {
          const charStartMs = i * props.staggerMs;
          const settleProgress = Math.max(0, Math.min(1, (ms - charStartMs) / props.settleMs));
          const showFinal = settleProgress >= 1 || finalChar === " ";
          const display = showFinal ? finalChar : glyphAt(i, settleProgress);
          const color = interpolate(settleProgress, [0, 0.5, 1], [props.accent, props.accent, props.foreground], { extrapolateRight: "clamp" });
          return <span key={i} style={{ display: "inline-block", color }}>{display}</span>;
        })}
      </h1>
    </AbsoluteFill>
  );
};
