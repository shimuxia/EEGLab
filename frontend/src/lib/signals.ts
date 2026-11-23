// Deterministic "channel" traces for the seven research directions.
// Each trace sketches the kind of data the direction works with, so the
// research index reads like a multi-channel recording rather than decoration.

export const TRACE_W = 600;
export const TRACE_H = 64;

export interface Trace {
  /** Main stroke. */
  d: string;
  /** Optional dashed continuation (forecasts, projected paths). */
  dashed?: string;
  /** Points worth marking (anomalies, waypoints). */
  marks: [number, number][];
}

const mid = TRACE_H / 2;
const fmt = (n: number) => Math.round(n * 10) / 10;
const line = (pts: [number, number][]) =>
  pts.map(([x, y], i) => `${i ? "L" : "M"}${fmt(x)} ${fmt(y)}`).join("");

// Small seeded PRNG so every build draws identical traces.
function rng(seed: number) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

function sample(fn: (t: number) => number, from = 0, to = 1, step = 3): [number, number][] {
  const pts: [number, number][] = [];
  for (let x = from * TRACE_W; x <= to * TRACE_W + 0.01; x += step) {
    pts.push([x, mid - fn(x / TRACE_W)]);
  }
  return pts;
}

function fault(): Trace {
  const r = rng(11);
  const spikeAt = 0.71;
  const pts = sample((t) => {
    const base = Math.sin(t * 64) * 3.2 + (r() - 0.5) * 2.4;
    const d = (t - spikeAt) * 60;
    return base + (Math.abs(d) < 1 ? (1 - Math.abs(d)) * 24 * (d < 0 ? 1 : -0.7) : 0);
  });
  return { d: line(pts), marks: [[spikeAt * TRACE_W, mid - 22]] };
}

function eeg(): Trace {
  const r = rng(7);
  let drift = 0;
  const pts = sample((t) => {
    drift += (r() - 0.5) * 1.6;
    drift *= 0.92;
    const burst = 0.55 + 0.45 * Math.sin(t * 9.5 - 1.2) ** 2;
    return (Math.sin(t * 132) * 9 + Math.sin(t * 57 + 1) * 5) * burst + drift * 3;
  }, 0, 1, 2);
  return { d: line(pts), marks: [] };
}

function forecast(): Trace {
  const f = (t: number) => Math.sin(t * Math.PI * 4 - 1.3) * 11 + Math.sin(t * Math.PI * 8) * 4 - (t - 0.5) * 6;
  const pts = sample(f, 0, 0.68);
  const ahead = sample(f, 0.68, 1);
  return { d: line(pts), dashed: line(ahead), marks: [[0.68 * TRACE_W, mid - f(0.68)]] };
}

function opinion(): Trace {
  const bursts = [0.16, 0.22, 0.47, 0.52, 0.56, 0.83];
  const pts = sample((t) => {
    let v = 0;
    for (const b of bursts) {
      const d = t - b;
      if (d >= 0) v += 22 * Math.exp(-d * 55) * (b === 0.52 ? 1.2 : 0.75);
    }
    return v - 12;
  }, 0, 1, 2);
  return { d: line(pts), marks: [] };
}

function optimize(): Trace {
  const pts = sample((t) => 24 * Math.exp(-t * 4.8) * Math.cos(t * 38) - 2);
  return { d: line(pts), marks: [[TRACE_W, mid + 2]] };
}

function digital(): Trace {
  const pts: [number, number][] = [];
  const hi = mid - 12;
  const lo = mid + 12;
  const pattern = [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1];
  const w = TRACE_W / pattern.length;
  let level = lo;
  pts.push([0, level]);
  pattern.forEach((bit, i) => {
    const next = bit ? hi : lo;
    if (next !== level) {
      pts.push([i * w, level], [i * w, next]);
      level = next;
    }
  });
  pts.push([TRACE_W, level]);
  return { d: line(pts), marks: [] };
}

function trajectory(): Trace {
  const pts = sample((t) => Math.sin(t * Math.PI * 2.2) * 15 + Math.sin(t * Math.PI * 5.5 + 0.6) * 5);
  const marks: [number, number][] = [0.12, 0.38, 0.64, 0.9].map((t) => {
    const x = t * TRACE_W;
    return [x, mid - (Math.sin(t * Math.PI * 2.2) * 15 + Math.sin(t * Math.PI * 5.5 + 0.6) * 5)];
  });
  return { d: line(pts), marks };
}

const builders = [fault, eeg, forecast, opinion, optimize, digital, trajectory];
const cache = new Map<number, Trace>();

export function traceFor(index: number): Trace {
  const i = ((index % builders.length) + builders.length) % builders.length;
  if (!cache.has(i)) cache.set(i, builders[i]());
  return cache.get(i)!;
}
