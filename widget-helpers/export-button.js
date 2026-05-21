/**
 * In-widget Export button — drop-in for any explanatory-animations widget.
 *
 * Adds a floating "Export" button to the bottom-right of the page. Click it,
 * pick resolution / fps / duration / aspect, and the widget records itself
 * frame-by-frame in the browser. No server, no Playwright, no Remotion.
 *
 * REQUIREMENTS the widget must meet:
 *   - Expose its master timeline as `window.timeline` (already the skill convention).
 *   - Have a "stage" element (the area to record) — auto-detected, see TARGET below.
 *
 * USAGE (one line in the widget HTML):
 *   <script src="../widget-helpers/export-button.js" defer></script>
 *
 * Then the user clicks the floating button. Output: a WebM file in Downloads/.
 * The skill's render.py can convert WebM → MP4 if MP4 is required.
 *
 * Engine: CCapture.js (lazy-loaded from cdnjs on first export click). Records by
 * stepping window.timeline.seek(t_ms) frame-by-frame so the capture is
 * deterministic + frame-perfect regardless of host hardware.
 */

(function () {
  if (window.__exportButtonLoaded) return;
  window.__exportButtonLoaded = true;

  // ── Stage detector ────────────────────────────────────────────────────
  // Priority list of selectors. First match wins. The widget can override
  // by setting window.exportTarget = HTMLElement OR setting data-export-target
  // on the desired element.
  const TARGET_SELECTORS = [
    "[data-export-target]",
    ".bbg2-stage",
    ".bbg-flow-container",
    ".state-machine",
    ".stage",
    ".sm > svg",
    ".layered-animations",
    "#stage",
    "main",
    "body",
  ];

  function resolveStage() {
    if (window.exportTarget instanceof HTMLElement) return window.exportTarget;
    for (const sel of TARGET_SELECTORS) {
      const el = document.querySelector(sel);
      if (el) return el;
    }
    return document.body;
  }

  // ── Styles ────────────────────────────────────────────────────────────
  const css = `
.eb-fab {
  position: fixed; right: 20px; bottom: 20px; z-index: 99998;
  width: 48px; height: 48px; border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.12);
  background: #ffffff; color: #18181b;
  font-family: 'Geist', system-ui, sans-serif; font-size: 11px; font-weight: 600;
  cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.18);
  display: inline-flex; align-items: center; justify-content: center;
  transition: transform 120ms, box-shadow 120ms, width 180ms;
  overflow: hidden; gap: 6px; padding: 0 14px;
}
.eb-fab:hover { transform: translateY(-1px); box-shadow: 0 10px 28px rgba(0,0,0,0.24); width: 110px; }
.eb-fab .eb-fab-icon { font-size: 16px; }
.eb-fab .eb-fab-label { display: none; white-space: nowrap; }
.eb-fab:hover .eb-fab-label { display: inline; }
.eb-fab.recording { background: #dc2626; color: #fff; width: 130px; }
.eb-fab.recording .eb-fab-label { display: inline; }

.eb-modal-backdrop {
  position: fixed; inset: 0; z-index: 99999;
  background: rgba(15,15,18,0.55); backdrop-filter: blur(4px);
  display: none; align-items: center; justify-content: center;
}
.eb-modal-backdrop.open { display: flex; }
.eb-modal {
  width: 420px; max-width: calc(100vw - 32px);
  background: #ffffff; border-radius: 14px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.30);
  font-family: 'Geist', system-ui, sans-serif; color: #09090b;
  padding: 18px 20px 16px;
}
.eb-modal h3 { margin: 0 0 4px; font-size: 16px; font-weight: 600; letter-spacing: -0.01em; }
.eb-modal .eb-sub { font-size: 12px; color: #71717a; margin-bottom: 14px; }
.eb-row { display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; }
.eb-row label { font-family: 'Geist Mono', monospace; font-size: 10.5px; color: #52525b; text-transform: uppercase; letter-spacing: .08em; }
.eb-row .eb-pill { display: inline-flex; background: #f4f4f5; border: 1px solid #e4e4e7; border-radius: 8px; padding: 2px; gap: 1px; }
.eb-row .eb-pill button {
  border: 0; background: transparent; cursor: pointer;
  font-family: 'Geist Mono', monospace; font-size: 11.5px; color: #52525b;
  padding: 5px 9px; border-radius: 6px; line-height: 1; flex: 1;
}
.eb-row .eb-pill button.active { background: #eab308; color: #fff; font-weight: 600; }
.eb-row .eb-pill button:hover:not(.active) { background: #fafaf7; }
.eb-row input[type="number"] {
  width: 100%; padding: 7px 9px; font-family: 'Geist Mono', monospace; font-size: 12.5px;
  border: 1px solid #d4d4d8; border-radius: 6px; background: #ffffff;
}
.eb-footer { display: flex; gap: 8px; margin-top: 8px; align-items: center; }
.eb-btn-primary {
  flex: 1; padding: 10px 14px; background: #eab308; color: #fff;
  border: 0; border-radius: 8px; font-family: 'Geist Mono', monospace;
  font-size: 12.5px; font-weight: 600; cursor: pointer;
}
.eb-btn-primary:hover { background: #ca8a04; }
.eb-btn-primary:disabled { opacity: .5; cursor: not-allowed; }
.eb-btn-cancel {
  padding: 10px 14px; background: transparent; color: #71717a;
  border: 1px solid #d4d4d8; border-radius: 8px;
  font-family: 'Geist Mono', monospace; font-size: 12.5px; cursor: pointer;
}
.eb-btn-cancel:hover { background: #fafaf7; color: #18181b; }
.eb-progress {
  width: 100%; height: 6px; background: #f4f4f5; border-radius: 3px;
  overflow: hidden; margin: 12px 0 6px; display: none;
}
.eb-progress.active { display: block; }
.eb-progress > .eb-progress-bar { height: 100%; background: #eab308; width: 0%; transition: width 120ms; }
.eb-status {
  font-family: 'Geist Mono', monospace; font-size: 10.5px; color: #71717a;
  text-align: center; min-height: 14px;
}
@media (max-width: 460px) {
  .eb-modal { width: calc(100vw - 24px); }
}`;

  function injectStyles() {
    if (document.getElementById("eb-style")) return;
    const s = document.createElement("style");
    s.id = "eb-style"; s.textContent = css;
    document.head.appendChild(s);
  }

  // ── DOM ───────────────────────────────────────────────────────────────
  function buildUI() {
    const fab = document.createElement("button");
    fab.className = "eb-fab";
    fab.title = "Export this animation as video";
    fab.innerHTML = '<span class="eb-fab-icon">⬇</span><span class="eb-fab-label">Export</span>';
    document.body.appendChild(fab);

    const backdrop = document.createElement("div");
    backdrop.className = "eb-modal-backdrop";
    backdrop.innerHTML = `
      <div class="eb-modal" role="dialog" aria-modal="true">
        <h3>Export animation</h3>
        <div class="eb-sub">Records this widget frame-by-frame and downloads a WebM file. Use the skill's <code>render.py</code> to convert to MP4 if needed.</div>

        <div class="eb-row">
          <label>Aspect ratio</label>
          <div class="eb-pill" data-group="aspect">
            <button data-value="16:9" class="active">16:9</button>
            <button data-value="9:16">9:16</button>
            <button data-value="1:1">1:1</button>
            <button data-value="current">Current</button>
          </div>
        </div>

        <div class="eb-row">
          <label>Resolution</label>
          <div class="eb-pill" data-group="res">
            <button data-value="720">720p</button>
            <button data-value="1080" class="active">1080p</button>
            <button data-value="1440">1440p</button>
            <button data-value="2160">4K</button>
          </div>
        </div>

        <div class="eb-row">
          <label>Frame rate</label>
          <div class="eb-pill" data-group="fps">
            <button data-value="30">30 fps</button>
            <button data-value="60" class="active">60 fps</button>
          </div>
        </div>

        <div class="eb-row">
          <label>Duration (seconds)</label>
          <input type="number" id="eb-duration" min="1" max="60" step="0.5" value="6">
        </div>

        <div class="eb-progress"><div class="eb-progress-bar"></div></div>
        <div class="eb-status">Ready</div>

        <div class="eb-footer">
          <button class="eb-btn-cancel">Cancel</button>
          <button class="eb-btn-primary">▶ Start recording</button>
        </div>
      </div>`;
    document.body.appendChild(backdrop);

    return { fab, backdrop };
  }

  // ── State ────────────────────────────────────────────────────────────
  const choice = { aspect: "16:9", res: 1080, fps: 60, duration: 6 };

  function applyChoice(group, val, modal) {
    if (group === "aspect" || group === "fps" || group === "res") choice[group] = (group === "aspect") ? val : parseInt(val, 10);
    modal.querySelectorAll(`[data-group="${group}"] button`).forEach(b => {
      b.classList.toggle("active", b.dataset.value === val);
    });
  }

  function resolveResolution(stage) {
    const heightLabels = { 720: 720, 1080: 1080, 1440: 1440, 2160: 2160 };
    const h = heightLabels[choice.res] ?? 1080;
    let w;
    if (choice.aspect === "16:9") w = Math.round(h * 16 / 9);
    else if (choice.aspect === "9:16") { const ww = h; w = Math.round(ww * 9 / 16); return { w, h: ww }; }
    else if (choice.aspect === "1:1") w = h;
    else {
      const r = stage.getBoundingClientRect();
      const ratio = r.width / r.height;
      w = Math.round(h * ratio);
    }
    return { w, h };
  }

  // ── Engines ──────────────────────────────────────────────────────────
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src; s.defer = false;
      s.onload = () => resolve();
      s.onerror = (e) => reject(new Error("failed to load " + src));
      document.head.appendChild(s);
    });
  }

  let ccaptureLoaded = false;
  async function ensureCCapture() {
    if (ccaptureLoaded || window.CCapture) { ccaptureLoaded = true; return; }
    await loadScript("https://cdnjs.cloudflare.com/ajax/libs/ccapture.js/1.0.9/CCapture.all.min.js");
    ccaptureLoaded = true;
  }

  let html2canvasLoaded = false;
  async function ensureHtml2Canvas() {
    if (html2canvasLoaded || window.html2canvas) { html2canvasLoaded = true; return; }
    await loadScript("https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js");
    html2canvasLoaded = true;
  }

  // ── Recording ─────────────────────────────────────────────────────────
  async function record(stage, statusEl, progressBar) {
    const { w, h } = resolveResolution(stage);
    const fps = choice.fps;
    const totalFrames = Math.max(1, Math.round(choice.fps * choice.duration));

    statusEl.textContent = `Preparing… (${w}×${h}, ${fps}fps, ${choice.duration}s)`;

    await ensureCCapture();
    // We use html2canvas to rasterize SVG/HTML widgets into a canvas the same
    // size as our target resolution, so the WebM has exact pixel dimensions.
    await ensureHtml2Canvas();

    const stageRect = stage.getBoundingClientRect();
    const scale = Math.min(w / stageRect.width, h / stageRect.height);

    // Off-screen canvas at the target resolution.
    const canvas = document.createElement("canvas");
    canvas.width = w; canvas.height = h;
    const ctx = canvas.getContext("2d");

    const capturer = new window.CCapture({ format: "webm", framerate: fps, verbose: false, quality: 99 });
    capturer.start();

    // Pause and rewind the timeline.
    if (window.timeline) {
      try { window.timeline.pause(); window.timeline.seek(0); } catch {}
    }

    for (let i = 0; i <= totalFrames; i++) {
      const tMs = (i / fps) * 1000;
      if (window.timeline) {
        try { window.timeline.seek(tMs); } catch {}
      }
      // Wait one rAF so the seek paints.
      await new Promise(r => requestAnimationFrame(r));

      // Snapshot stage to canvas at native size, then draw into output canvas centered.
      let snapshot;
      try {
        snapshot = await window.html2canvas(stage, {
          backgroundColor: null,
          logging: false,
          scale: Math.max(1, devicePixelRatio || 1),
          useCORS: true,
          allowTaint: true,
        });
      } catch (e) {
        // Skip frame on error but keep recording.
        continue;
      }
      ctx.clearRect(0, 0, w, h);
      // letterbox / pillarbox if aspect ratios differ
      const sw = snapshot.width, sh = snapshot.height;
      const k = Math.min(w / sw, h / sh);
      const dw = sw * k, dh = sh * k;
      const dx = (w - dw) / 2, dy = (h - dh) / 2;
      // background fill — use page background if detected
      const bg = getComputedStyle(document.body).backgroundColor || "#ffffff";
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, w, h);
      ctx.drawImage(snapshot, dx, dy, dw, dh);
      capturer.capture(canvas);

      const pct = Math.round((i / totalFrames) * 100);
      progressBar.style.width = pct + "%";
      statusEl.textContent = `Recording… ${pct}% (frame ${i}/${totalFrames})`;
    }

    statusEl.textContent = "Encoding WebM…";
    return new Promise((resolve) => {
      capturer.stop();
      capturer.save(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
        a.href = url;
        a.download = `animation-${w}x${h}-${ts}.webm`;
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
        statusEl.textContent = `Saved ${a.download} (${(blob.size / 1024).toFixed(0)} KB)`;
        resolve();
      });
    });
  }

  // ── Wire up ──────────────────────────────────────────────────────────
  function init() {
    injectStyles();
    const { fab, backdrop } = buildUI();
    const modal = backdrop.querySelector(".eb-modal");
    const statusEl = modal.querySelector(".eb-status");
    const progress = modal.querySelector(".eb-progress");
    const progressBar = modal.querySelector(".eb-progress-bar");
    const startBtn = modal.querySelector(".eb-btn-primary");
    const cancelBtn = modal.querySelector(".eb-btn-cancel");
    const durationInput = modal.querySelector("#eb-duration");

    fab.addEventListener("click", () => {
      backdrop.classList.add("open");
      // Try to read window.timeline.duration to pre-fill
      try {
        if (window.timeline && window.timeline.duration && Number.isFinite(window.timeline.duration)) {
          const d = window.timeline.duration / 1000;
          if (d > 0 && d < 60) { durationInput.value = d.toFixed(1); choice.duration = d; }
        }
      } catch {}
    });

    cancelBtn.addEventListener("click", () => backdrop.classList.remove("open"));
    backdrop.addEventListener("click", (e) => { if (e.target === backdrop) backdrop.classList.remove("open"); });

    modal.querySelectorAll(".eb-pill button").forEach(b => {
      b.addEventListener("click", () => {
        const group = b.closest(".eb-pill").dataset.group;
        applyChoice(group, b.dataset.value, modal);
      });
    });

    durationInput.addEventListener("input", () => {
      choice.duration = Math.max(0.5, Math.min(60, parseFloat(durationInput.value) || 6));
    });

    startBtn.addEventListener("click", async () => {
      const stage = resolveStage();
      progress.classList.add("active");
      progressBar.style.width = "0%";
      startBtn.disabled = true;
      cancelBtn.disabled = true;
      fab.classList.add("recording");
      fab.querySelector(".eb-fab-label").textContent = "Recording…";
      try {
        await record(stage, statusEl, progressBar);
      } catch (e) {
        statusEl.textContent = "Error: " + e.message;
        console.error("[export-button]", e);
      } finally {
        startBtn.disabled = false;
        cancelBtn.disabled = false;
        fab.classList.remove("recording");
        fab.querySelector(".eb-fab-label").textContent = "Export";
        setTimeout(() => progress.classList.remove("active"), 1500);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
