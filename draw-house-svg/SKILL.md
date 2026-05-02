---
name: draw-house-svg
description: |
  Produces a stroke-only 2D front-elevation house drawing as a single self-contained SVG file.
  Pinterest-style aspirational aesthetic: CAD-level proportional precision + ballpoint pen warmth.
  Use when: user asks to draw a house, generate a house illustration, create an architectural elevation.
  Example triggers: "draw me a house", "ev çiz", "generate a house SVG", "traditional cottage elevation".
---

# SVG Architectural Elevation Drawing

> **Core aesthetic**: CAD-level precision in proportions and geometry, rendered with the warmth of a ballpoint pen sketch on paper. This is not a tension to resolve — it IS the skill.

The result must feel **trustworthy** (correct proportions, buildable), **personal** (human line quality), **inviting** (life elements, context), and **not surreal** (no floating parts, no impossible geometry).

Mental test: imagine the drawing printed on cream paper and pinned to a corkboard in a café. IKEA instruction → too clean. Napkin doodle → too rough. Aim for: "someone who can draw lovingly drew this careful thing."

---

## Phase 0: Decisions (MANDATORY — write as SVG comments before any element)

Skipping this is the #1 reason drawings look generic. Declare ALL five before writing `<svg>`:

```
<!-- TYPOLOGY: 2-story, rectangular plan, no garage -->
<!-- STYLE: Traditional gabled -->
<!-- FACADE: 3-bay symmetric, door center, windows 20% ratio -->
<!-- MATERIALS: horizontal siding + shingle roof, stone plinth -->
<!-- SITE: flat ground, grass, low garden wall -->
```

### Style → Roof pitch reference

| Style | Roof pitch | Window proportion | Ornament |
|-------|-----------|-------------------|----------|
| Modern/cubic | ≤15° | Horizontal / large | None |
| Traditional gabled | 30–45° | Vertical, 1:1.5 | Simple trim |
| Victorian | 45–60° | Vertical, tall | Dense |
| Tudor / half-timber | 50–60° | Vertical, small mullions | Timber frame |
| Anadolu kırsal | 15–25°, tile | Vertical + shutters | Minimal |
| Mediterranean | 15–25°, tile | Arched or rect | Arches |

---

## Phase 1: Constants

### 1a. Typology → Dimensions (MANDATORY FIRST STEP)

**Before any px coordinate, convert your typology to realistic meters:**

| Typology | Typical facade width | Typical wall height |
|----------|---------------------|---------------------|
| Small forest cabin | 4–6m | 2.5–3m |
| Urban rowhouse | 5–7m | 3–3.5m per floor |
| Suburban house | 8–12m | 3–3.5m per floor |
| Villa / detached | 10–16m | 3–4m per floor |

Then convert to px immediately: `meters × SCALE = px`

**Footprint validation — run before placing a single element:**
```
total_wall_px / SCALE = meters → is this realistic for the typology?
```

Example:
```
<!-- TYPOLOGY: small forest cabin → realistic width ~5m -->
<!-- 5m × 40 = 200px -->
<!-- WALL_LEFT=200, WALL_RIGHT=400 → 200px / 40 = 5m ✓ -->
```

**NEVER copy px coordinates from a different typology drawing without recalculating from scratch.** A suburban house is 10m wide; a forest cabin is 5m wide — the same WALL_LEFT/WALL_RIGHT values produce a completely wrong building.

---

Define once, reference everywhere. Never hardcode raw numbers.

```svg
<!--
  SCALE     = 40        (1m = 40px)
  PAPER     = #F5EFE3   (cream journal paper)
  INK       = #2A2620   (warm black-brown ballpoint)
  INK_LIGHT = #5C504A   (faded secondary strokes)

  Pick ONE ink family: black-brown OR blue (#1F3B5C). Never mix.
-->
```

### Standard measurements at SCALE=40

| Element | Real | px |
|---------|------|----|
| Door width | 90cm | 36 |
| Door height | 210cm | 84 |
| Window width | 100cm | 40 |
| Window height | 130cm | 52 |
| Wall height (1 story) | 300cm | 120 |
| Basement height | 75cm | 30 |
| Step riser | 17.5cm | 7 |
| Window sill from floor | 90cm | 36 |
| Railing height | 80cm | 32 |
| Frame strip width | 8cm | 3 |
| Floor band thickness | 15cm | 6 |
| Timber thickness | 15cm | 6 |

**Validation rule — apply after EVERY element placement:**
```
element_px / SCALE * 100 = cm → is this realistic?
```
A 175cm-wide door or 200cm-tall window is wrong. Check immediately, not at the end.

---

## Phase 2: SVG Boilerplate + Defs

```svg
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 800 600">
  <!-- No width/height — viewBox only for responsive scaling -->

  <defs>
    <!-- Paper texture filter — ONE filter for the whole drawing -->
    <filter id="paper">
      <feTurbulence type="fractalNoise" baseFrequency="0.9"
                    numOctaves="2" seed="5"/>
      <feDisplacementMap in="SourceGraphic" scale="0.4"/>
      <!-- CRITICAL: scale ≤ 0.5. Above 1.0 = drunk drawing. -->
    </filter>

    <!-- Window symbol — define once, use many times -->
    <!-- All coords relative to 0,0 top-left of frame -->
    <symbol id="win-std" viewBox="0 0 40 52">
      <!-- Lintel -->
      <rect x="-4" y="-4" width="48" height="4"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.1"/>
      <!-- Frame -->
      <rect x="0" y="0" width="40" height="52"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.4"/>
      <!-- Miter joints — mandatory at all 4 corners -->
      <line x1="0"  y1="0"  x2="3"  y2="3"  stroke="#2A2620" stroke-width="0.9"/>
      <line x1="40" y1="0"  x2="37" y2="3"  stroke="#2A2620" stroke-width="0.9"/>
      <line x1="0"  y1="52" x2="3"  y2="49" stroke="#2A2620" stroke-width="0.9"/>
      <line x1="40" y1="52" x2="37" y2="49" stroke="#2A2620" stroke-width="0.9"/>
      <!-- Two panes side by side (NOT a + cross) -->
      <rect x="3"  y="3" width="16" height="46" fill="#F5EFE3" stroke="#2A2620" stroke-width="0.9"/>
      <rect x="21" y="3" width="16" height="46" fill="#F5EFE3" stroke="#2A2620" stroke-width="0.9"/>
      <!-- Sill -->
      <rect x="-4" y="52" width="48" height="4"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.1"/>
    </symbol>

    <!-- Basement window symbol (single pane, shorter) -->
    <symbol id="win-basement" viewBox="0 0 40 24">
      <rect x="-4" y="-4" width="48" height="4"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.0"/>
      <rect x="0" y="0" width="40" height="24"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.2"/>
      <line x1="0"  y1="0"  x2="3"  y2="3"  stroke="#2A2620" stroke-width="0.8"/>
      <line x1="40" y1="0"  x2="37" y2="3"  stroke="#2A2620" stroke-width="0.8"/>
      <line x1="0"  y1="24" x2="3"  y2="21" stroke="#2A2620" stroke-width="0.8"/>
      <line x1="40" y1="24" x2="37" y2="21" stroke="#2A2620" stroke-width="0.8"/>
      <rect x="3" y="3" width="34" height="18" fill="#F5EFE3" stroke="#2A2620" stroke-width="0.8"/>
      <rect x="-4" y="24" width="48" height="4"
            fill="#F5EFE3" stroke="#2A2620" stroke-width="1.0"/>
    </symbol>

    <!-- ClipPath per roof slope — prevents texture overflow -->
    <!-- Define after computing roof coordinates -->
    <clipPath id="clip-roof-left">
      <polygon points="LEFT_OVERHANG,WALL_TOP PEAK_X,PEAK_Y WALL_LEFT,WALL_TOP"/>
    </clipPath>
    <clipPath id="clip-roof-right">
      <polygon points="PEAK_X,PEAK_Y RIGHT_OVERHANG,WALL_TOP WALL_RIGHT,WALL_TOP"/>
    </clipPath>
  </defs>

  <!-- All strokes inside this group get the paper filter -->
  <g filter="url(#paper)">
    <!-- drawing content here -->
  </g>
</svg>
```

**Using window symbols:**
```svg
<!-- <use> x,y = top-left of the frame (NOT including the lintel offset) -->
<use href="#win-std" x="120" y="180"/>   <!-- ground floor left -->
<use href="#win-std" x="280" y="180"/>   <!-- ground floor right -->
<use href="#win-std" x="120" y="60"/>    <!-- upper floor — SAME x, aligned -->

<!-- Instance-specific additions drawn separately -->
<line x1="121" y1="200" x2="158" y2="200"   <!-- curtain inside left window -->
      stroke="#2A2620" stroke-width="0.6" opacity="0.5"/>
```

---

## Phase 3: Drawing Order (SVG renders last-on-top)

Execute in this exact order — wrong order causes masking failures:

1. Background rect (`fill=PAPER`, full viewBox)
2. Scale reference line (side of drawing, always visible)
3. **Chimney body** ← drawn BEFORE roof (roof covers its base)
4. Roof masking polygon (`fill=PAPER, stroke=none` — hides chimney base + wall-top)
5. Roof timber outlines (the `/\` with thickness)
6. Roof surface texture (inside clipPath — see §Roof)
7. Gable wall lines
8. Eaves (small L-shapes, fascia + soffit)
9. House body — 3 lines only (left, bottom, right — **NO top line**)
10. Wall surface texture (before openings — their paper fills mask it)
11. Floor band / string course (multi-story only)
12. Basement / plinth rect
13. Ground line + texture
14. Shutters (before windows — windows overlap shutters)
15. Ground floor windows (`<use href="#win-std" .../>`)
16. Upper floor windows (`<use href="#win-std" .../>`)
17. Door (complete: lintel, frame, miter, panels, knob, threshold)
18. Basement windows (`<use href="#win-basement" .../>`)
19. Life elements (doorbell, light, number, smoke, curtain, mat)
20. Steps + railings
21. Rain gutter + downpipes
22. Foreground context (plants, fence, wall)
23. **Shadows — ALWAYS last**

---

## Phase 4: Core Elements

### House Body
```svg
<!-- 3 lines, NO top border (roof sits there) -->
<line x1="LEFT"  y1="TOP"    x2="LEFT"  y2="BOTTOM" stroke="#2A2620" stroke-width="2.1"/>
<line x1="LEFT"  y1="BOTTOM" x2="RIGHT" y2="BOTTOM" stroke="#2A2620" stroke-width="2.0"/>
<line x1="RIGHT" y1="TOP"    x2="RIGHT" y2="BOTTOM" stroke="#2A2620" stroke-width="1.9"/>
<!-- Note: vary stroke-width ±0.2 — real pen pressure variation -->
```

### Roof

**Timber has thickness.** Inner and outer edges must be parallel. Inner peak offset downward by thickness:

```
Timber thickness = SCALE * 0.15  (6px at 40px/m)

Left slope outer: (LEFT_OVERHANG, WALL_TOP) → (PEAK_X, PEAK_Y)
Left slope inner: (WALL_LEFT,     WALL_TOP) → (PEAK_X, PEAK_Y + thickness)
                                                        ↑ never same point as outer peak
```

**Masking polygon** (hides chimney base and wall-top line):
```svg
<polygon points="LEFT_OVERHANG,WALL_TOP PEAK_X,PEAK_Y RIGHT_OVERHANG,WALL_TOP"
         fill="#F5EFE3" stroke="none"/>
```

**Roof texture with clipPath** (prevents overflow past timber edges):
```svg
<!-- Ceramic tile: rows parallel to SLOPE, not to page horizontal -->
<g clip-path="url(#clip-roof-left)">
  <!-- rows at 6px intervals along slope, wavy path per row -->
  <path d="M x1,y1 Q cx,cy x2,y2" stroke="#2A2620" stroke-width="0.5" fill="none" opacity="0.6"/>
  <!-- repeat for each row -->
</g>
<g clip-path="url(#clip-roof-right)">
  <!-- mirror for right slope -->
</g>
```

### Chimney — sitting on the roof slope

**The most common error**: chimney bottom floating above or sinking below the roof line.

```python
# Roof line from (x1, y1) to (x2, y2)
# Given chimney center_x, find the y where it intersects the slope:

roof_slope       = (y2 - y1) / (x2 - x1)
chimney_bottom_y = y1 + roof_slope * (chimney_center_x - x1)

# chimney_bottom_y is where the chimney body MEETS the roof
# The chimney body rect bottom = chimney_bottom_y
# Draw chimney BEFORE the roof masking polygon so roof covers the base
```

**Why it keeps going wrong**: The masking polygon hides the chimney base, creating the illusion it's floating. Check:
1. Is the chimney body drawn BEFORE step 4 (masking polygon)? If after → chimney appears to start at roof surface
2. Is `chimney_bottom_y` calculated with the slope formula above? If using a fixed y → chimney won't align

```svg
<!-- Correct order: -->
<!-- Step 3: chimney body -->
<rect x="chimney_x" y="chimney_top_y"
      width="chimney_w" height="(chimney_bottom_y - chimney_top_y)"
      fill="#F5EFE3" stroke="#2A2620" stroke-width="1.5"/>

<!-- Step 4: masking polygon — covers chimney base, leaving cap visible -->
<polygon points="..."  fill="#F5EFE3" stroke="none"/>

<!-- Step 5+: roof timber, texture drawn on top -->
```

### Door
```
Components (all mandatory):
1. Lintel   — rect, wider than frame by SCALE*0.1 each side, height SCALE*0.10
2. Frame    — 45° miter joints at ALL 4 corners
3. Leaf     — inside frame, has internal structure (not flat rect)
4. Panels   — upper panel (35% height), middle rail, two lower panels side by side
5. Knob     — at knob_y = door_bottom - SCALE*1.0, knob_x = door_right - SCALE*0.08
6. Threshold— bottom rect, same width as lintel
```

### Multi-story floor band
```
band_y      = wall_top + SCALE * 3.0
band_height = SCALE * 0.15

Upper floor window frame_y:
  = band_y + band_height + SCALE * 0.9   ← sill height above upper floor
```

---

## Phase 5: Material Patterns

### Wall materials
**Horizontal siding**: lines every `SCALE * 0.25`, `stroke-width="0.5"`, `opacity="0.6"`

**Brick (running bond)**:
```
horizontal lines: every SCALE * 0.07 (7cm course)
vertical joints:  every SCALE * 0.22 (22cm brick)
offset odd rows:  by SCALE * 0.11 (half brick)
stroke-width: 0.4, opacity: 0.7
```

**Half-timber**: timber rects `SCALE * 0.15` wide at corners + intermediates + diagonals. Plaster infill between (no texture).

**Stucco**: no line texture. Sparse stipple dots only: `<circle r="0.3" fill="#5C504A" opacity="0.3"/>` ~1 per 30px².

### Roof materials
**Ceramic tile**: wavy horizontal paths parallel to slope, every ~6px along slope length:
```svg
<path d="M x1,y1 q 5,-1 10,0 q 5,1 10,0 q 5,-1 10,0"
      stroke="#2A2620" stroke-width="0.5" fill="none" opacity="0.6"/>
```

**Shingle**: rows every ~5px, staggered tile bottom edges, each tile ~8px wide:
```svg
<!-- For each row at y_row, tiles at x = start, start+8, start+16... offset odd rows by 4px -->
<line x1="tile_x" y1="y_row" x2="tile_x+8" y2="y_row" stroke="#2A2620" stroke-width="0.5"/>
```

**Standing-seam metal**: straight lines following slope direction, every `SCALE * 0.45`.

---

## Phase 6: Shadow System

**Light direction**: top-left at 45°. Consistent throughout.

**Rule**: protrusions → shadow right+down. Recesses → shadow left+top inner edges.

**All shadows = hatching, never flat fill.**

```svg
<!-- Hatching pattern for shadows -->
<!-- 45° diagonal lines, 2-3px spacing, stroke-width 0.4-0.6 -->
<!-- ALWAYS use clipPath to bound the hatch area -->

<defs>
  <clipPath id="clip-shadow-eaves">
    <rect x="shadow_x" y="shadow_y" width="shadow_w" height="shadow_h"/>
  </clipPath>
</defs>

<g clip-path="url(#clip-shadow-eaves)">
  <!-- lines at 45°, spaced 2.5px, covering bounding box generously -->
  <line x1="sx-20" y1="sy"    x2="sx"    y2="sy-20" stroke="#2A2620" stroke-width="0.5"/>
  <line x1="sx-20" y1="sy+3"  x2="sx+3"  y2="sy-20" stroke="#2A2620" stroke-width="0.5"/>
  <!-- etc. -->
</g>
```

**Roof shadow thickness** (two slopes differ — calculate, don't guess):
```python
import math
alpha = math.atan2(rise, run)   # roof pitch in radians
shadow_right = 3                # px, minimum readable
shadow_left  = round(3 / math.tan(alpha))  # shallower roof → thicker shadow
# Example: alpha=22.4° → tan=0.412 → shadow_left ≈ 7px
```

**Validation**: every shadow must have a named physical cause. No cause → delete it.

---

## Phase 7: Rendering Mode — Choose ONE

Declare at the top with other decisions: `<!-- RENDER MODE: ballpoint | pencil -->`

The two modes share the same proportions, shadows, and structure. Only the filter and stroke treatment differ.

---

### Mode A: Ballpoint Pen

Warm, confident strokes. Slight wobble, fiber feel. Like a Bic on cream journal paper.

**Filter** (one filter, whole drawing):
```svg
<filter id="render">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5"/>
  <feDisplacementMap in="SourceGraphic" scale="0.4"/>
  <!-- CRITICAL: scale ≤ 0.5. Above 1.0 = drunk drawing. -->
</filter>
```

**Ink colors**:
- Default: `#2A2620` (black-brown ballpoint)
- Alternative: `#1F3B5C` (ballpoint blue — journal/notebook feel)
- Secondary: `#5C504A`
- Pick ONE family per drawing, never mix.

**Stroke treatment**:
- Stroke-width jitter ±0.2 from nominal
- Corner overshoot on ~30% of corners (1–2px past intersection)
- Double-stroke on silhouette: house body + outer roof edges get a second line offset 0.5–1px at 40% opacity

**Scatter marks**: 20–40 tiny marks (2–3px) across drawing area. `stroke="#5C504A"` `opacity="0.3"`.

---

### Mode B: Pencil / Karakalem

Softer, textured strokes. Graphite density — darker where strokes overlap, lighter at edges. Like an HB pencil on cartridge paper.

**Source**: reverse-engineered from the [Here Dragons Abound](https://heredragonsabound.blogspot.com/2020/02/creating-pencil-effect-in-svg.html) technique. The exact working filters are below — verified from the author's Codepen source.

**How it works**: 3 separate noise sources displace the source graphic in different directions. `feBlend mode="multiply"` stacks them — where displaced copies overlap → darker (simulates pencil pressure). At edges they diverge → lighter (simulates pencil lift).

The author provides 4 progressively more complex filters. Use `pencilTexture4` — it's the most complete:

**Filter** (copy verbatim, replace `id` with `render`):
```svg
<filter id="render" x="-20%" y="-20%" width="140%" height="140%"
        filterUnits="objectBoundingBox">

  <!-- Three noise sources with different seeds = different displacement directions -->
  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3"
                seed="1" result="f1"/>
  <feDisplacementMap xChannelSelector="R" yChannelSelector="G"
                     scale="5" in="SourceGraphic" in2="f1" result="d1"/>

  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3"
                seed="10" result="f2"/>
  <feDisplacementMap xChannelSelector="R" yChannelSelector="G"
                     scale="5" in="SourceGraphic" in2="f2" result="d2"/>

  <!-- Fine grain — higher baseFrequency = fine graphite texture -->
  <feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2"
                seed="100" result="f3"/>
  <feDisplacementMap xChannelSelector="R" yChannelSelector="G"
                     scale="3" in="SourceGraphic" in2="f3" result="d3"/>

  <!-- Multiply blend: overlap = darker (pencil density) -->
  <feBlend mode="multiply" in="d1" in2="d2" result="blend1"/>
  <feBlend mode="multiply" in="blend1" in2="d3"/>
</filter>
```

For a subtler effect (lighter pencil), also use `pencilTexture3` which adds interior grain via `feColorMatrix`:
```svg
<filter id="render-subtle" x="-2%" y="-2%" width="104%" height="104%"
        filterUnits="objectBoundingBox">
  <feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="5"
                stitchTiles="stitch" result="f1"/>
  <feColorMatrix type="matrix"
                 values="0 0 0 0 0, 0 0 0 0 0, 0 0 0 0 0, 0 0 0 -1.5 1.5"
                 result="f2"/>
  <!-- Clips source to noise mask — creates fibrous interior texture -->
  <feComposite operator="in" in="SourceGraphic" in2="f2" result="f3"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="3"
                result="noise"/>
  <feDisplacementMap xChannelSelector="R" yChannelSelector="G"
                     scale="2.5" in="f3"/>
</filter>
```

**Paper texture** — use `roughPaper` filter on the background rect separately for the paper feel:
```svg
<filter id="roughPaper" x="0%" y="0%" width="100%" height="100%"
        filterUnits="objectBoundingBox">
  <feTurbulence type="fractalNoise" baseFrequency="128" numOctaves="1"
                result="noise"/>
  <feDiffuseLighting in="noise" lighting-color="white" surfaceScale="1"
                     result="diffLight">
    <feDistantLight azimuth="45" elevation="55"/>
  </feDiffuseLighting>
  <feGaussianBlur in="diffLight" stdDeviation="0.75" result="dlblur"/>
  <feComposite operator="arithmetic" k1="1.2" k2="0" k3="0" k4="0"
               in="dlblur" in2="SourceGraphic"/>
</filter>

<!-- Apply to background rect only -->
<rect x="..." y="..." width="..." height="..." fill="#F7F4EE"
      filter="url(#roughPaper)"/>
```

**Ink colors** — pencil mode uses grey-graphite, not warm brown:
- Primary: `#3A3835` (dark graphite)
- Secondary: `#6B6560` (mid graphite, for texture lines)
- Paper: `#F7F4EE` (slightly cooler than ballpoint paper — cartridge paper feel)

**Stroke treatment**:
- Slightly thinner nominal strokes — multiply blend already adds visual weight
  - Silhouette: 1.6–1.8
  - Secondary: 1.1–1.3
  - Texture: 0.3–0.4
- Corner overshoot more generous — up to 3px, ~40% of corners
- NO double-stroke silhouette — the multiply blend handles this
- Scatter marks denser: 40–60, slightly longer (3–5px), `opacity="0.25"`

**Shadows in pencil mode**:
- Same hatching rules (§Phase 6), but cross-hatching reads more naturally — use freely
- Spacing can be denser: 1.5–2px instead of 2–3px

**Known limitation**: `scale` values (5, 5, 3) are absolute pixel offsets — they don't scale with viewBox. For large viewBoxes (>800px wide), increase scale proportionally. Rule of thumb: `scale ≈ viewBox_width / 160`.

---

### Shared rules (both modes)

- **Paper filter applied to outer `<g>`**: `<g filter="url(#render)">` wraps all strokes
- **All closed shapes**: `fill="PAPER_COLOR"` not `fill="none"`
- **Subtle path curves**: lines >80px use `<path d="M x1,y1 Q mx,my x2,y2"/>` with 1px arc
- **Stipple texture**: stucco, stone plinth, ground — sparse dots, viewer senses not sees
- **Flat shadow fills**: never — always hatch with clipPath

---

## Phase 8: Ground + Context

House does not float. Minimum viable context:

```svg
<!-- Ground: wavy path (subtle 1px arc) -->
<path d="M LEFT,GROUND_Y Q MID_X,GROUND_Y-1 RIGHT,GROUND_Y"
      stroke="#2A2620" stroke-width="1.5" fill="none"/>

<!-- Grass: short vertical strokes, irregular spacing -->
<line x1="x" y1="GROUND_Y" x2="x" y2="GROUND_Y-3" stroke="#2A2620" stroke-width="0.6"/>
<!-- repeat ~30 times with irregular x spacing -->
```

**Life elements** (pick 1–3 total — more clutters):

| Element | Position | Notes |
|---------|----------|-------|
| Doorbell | right of door frame, y = door_bottom - SCALE*1.2 | daily use signal |
| House number | near door, eye level | identification |
| Smoke from chimney | rising from cap, wavy path | "home is heated" |
| Curtain | wavy line inside window pane | "someone lives here" |
| Welcome mat | at threshold, ground level | |

Best combinations: doorbell + number (minimal) | smoke + curtain (cozy/lived-in) | mat + flower box (welcoming).

---

## Phase 9: Final Validation Checklist

Run through this before outputting. Each `[ ]` is a failure mode caught before delivery.

**Decisions**
- [ ] All 5 declarations written as SVG comments
- [ ] Style is internally consistent (pitch matches style table)

**Scale**
- [ ] 1m reference line visible on drawing
- [ ] Every element validated: `px / SCALE * 100 = cm` is realistic

**Roof**
- [ ] No base line (`/_\` = wrong, `/\` = correct)
- [ ] Timber has thickness, inner peak offset from outer peak
- [ ] Roof texture inside clipPath (no overflow)
- [ ] Both slope shadows different thickness (calculated)

**Chimney**
- [ ] Body drawn BEFORE masking polygon (step 3, not step 5+)
- [ ] Bottom y calculated with slope intersection formula
- [ ] Material matches wall material

**Openings**
- [ ] All windows use `<symbol>` + `<use>` (or manually have all 5 components)
- [ ] Upper floor windows x-aligned with ground floor windows
- [ ] Basement windows have full treatment (not bare rects)
- [ ] Door has panels, knob at 100cm, miter joints

**Ground level**
- [ ] Plinth/basement drawn
- [ ] Steps equal width (no perspective)
- [ ] Gutter + downpipes present

**Rendering**
- [ ] Render mode declared: `ballpoint` or `pencil`
- [ ] Correct filter for chosen mode in `<defs>`, applied to outer `<g>`
- [ ] Correct ink color family for chosen mode (warm brown OR graphite — not mixed)
- [ ] All shadows = hatching with clipPath
- [ ] At least 1 life element
- [ ] Scatter marks present
- [ ] Ballpoint: `feDisplacementMap scale ≤ 0.5` | Pencil: coarse scale ≈ viewBox_width / 300

**Fills**
- [ ] All closed shapes: `fill="#F5EFE3"` (not `fill="none"`)
