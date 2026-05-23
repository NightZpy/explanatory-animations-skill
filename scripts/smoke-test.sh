#!/usr/bin/env bash
# Smoke test for explanatory-animations
#
# Validates the end-to-end flow on a clean machine:
#   1. Plugin manifest + skill structure exists
#   2. doctor.py reports a non-BLOCKED status
#   3. render.py can produce an MP4 from a bundled example widget
#   4. (optional, with --in-browser) opens the resulting MP4 in the default viewer
#
# Exit codes:
#   0  all good
#   1  plugin / skill structure broken
#   2  doctor reports BLOCKED
#   3  render failed
#
# This is what the CI workflow runs after the structural checks; it's also
# what a maintainer should run before publishing a release.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$(mktemp -d)"
OUT_MP4="$OUT_DIR/smoke.mp4"
WIDGET="$REPO_ROOT/plugin/skills/animate/examples/lifecycle.html"

echo "▶ smoke-test  ($REPO_ROOT)"

# 1. Structure check
[[ -f "$REPO_ROOT/.claude-plugin/plugin.json" ]] || { echo "FAIL: missing .claude-plugin/plugin.json"; exit 1; }
[[ -f "$REPO_ROOT/plugin/skills/animate/SKILL.md"     ]] || { echo "FAIL: missing plugin/skills/animate/SKILL.md"; exit 1; }
[[ -f "$WIDGET" ]]                                || { echo "FAIL: missing example widget at $WIDGET"; exit 1; }
echo "✓ structure"

# 2. Doctor
DOCTOR_OUT="$(python3 "$REPO_ROOT/plugin/skills/animate/scripts/doctor.py" 2>/dev/null)" || true
STATUS="$(echo "$DOCTOR_OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])')"
echo "✓ doctor → status=$STATUS"
[[ "$STATUS" != "BLOCKED" ]] || { echo "FAIL: doctor reports BLOCKED — inspect:"; echo "$DOCTOR_OUT"; exit 2; }

# 3. Render
echo "▶ render.py → $OUT_MP4 (this triggers bootstrap on first run)"
python3 "$REPO_ROOT/plugin/skills/animate/scripts/render.py" \
    --widget "$WIDGET" \
    --out "$OUT_MP4" \
    --resolution 1280x720 \
    --fps 30 \
    --duration 3 \
    --yes 2>&1 | tail -10

[[ -f "$OUT_MP4" ]] || { echo "FAIL: render did not produce $OUT_MP4"; exit 3; }
SIZE_KB=$(( $(stat -f%z "$OUT_MP4" 2>/dev/null || stat -c%s "$OUT_MP4") / 1024 ))
echo "✓ render → $OUT_MP4 (${SIZE_KB} KB)"

# 4. Optional open
if [[ "${1:-}" == "--in-browser" ]]; then
    if command -v open >/dev/null 2>&1; then
        open "$OUT_MP4"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$OUT_MP4"
    fi
fi

echo "✅ smoke-test PASS"
echo "   plugin manifest OK · doctor=$STATUS · MP4=$OUT_MP4 (${SIZE_KB} KB)"
