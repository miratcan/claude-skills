# Troubleshooting: draw-house-svg

## Chimney appears to float through the roof

**Symptom**: chimney body visually passes through the roof surface, starting from inside the roof triangle instead of sitting on the slope.

**Root cause**: almost always a drawing order problem, not a math problem.

The correct order is:
1. Chimney body rect (before the masking polygon)
2. Masking polygon (`fill=PAPER, stroke=none`) — this HIDES the chimney base below roof level
3. Roof timber outlines drawn on top

If the chimney is drawn AFTER the masking polygon, the masking polygon covers it and the chimney appears to float up from the roof surface.

**Fix**:
```svg
<!-- CORRECT ORDER -->
<!-- 1. Chimney body — including the part that goes below roof line -->
<rect id="chimney-body" .../>

<!-- 2. Masking polygon — hides everything below roof triangle -->
<polygon points="..." fill="#F5EFE3" stroke="none"/>

<!-- 3. Roof timber, texture etc. drawn on top of masking polygon -->
```

**Second cause**: `chimney_bottom_y` calculated incorrectly (fixed y instead of slope-intersected y).

```python
# WRONG — fixed y that doesn't follow the slope
chimney_bottom_y = wall_top  # ← this ignores roof pitch

# CORRECT — calculate intersection with slope
roof_slope       = (y2 - y1) / (x2 - x1)
chimney_bottom_y = y1 + roof_slope * (chimney_center_x - x1)
```

---

## Roof texture overflows past the timber edges

**Symptom**: tile or shingle lines extend beyond the roof outline, appearing on the sky or wall area.

**Fix**: wrap texture group in a `<clipPath>` defined by the exact roof polygon:

```svg
<defs>
  <clipPath id="clip-roof-left">
    <polygon points="LEFT_OVERHANG,WALL_TOP PEAK_X,PEAK_Y WALL_LEFT,WALL_TOP"/>
  </clipPath>
</defs>

<g clip-path="url(#clip-roof-left)">
  <!-- all tile/shingle lines here — safe, can't overflow -->
</g>
```

---

## Shadow hatching looks messy / extends beyond shadow area

**Symptom**: hatching lines visually spill beyond the intended shadow region.

**Fix**: same clipPath technique as roof texture — define a clipPath for the shadow bounding shape:

```svg
<defs>
  <clipPath id="clip-shadow-sill">
    <rect x="sx" y="sy" width="sw" height="sh"/>
  </clipPath>
</defs>

<g clip-path="url(#clip-shadow-sill)">
  <!-- hatch lines — can be drawn generously, only visible inside shape -->
</g>
```

---

## Upper floor windows don't align with ground floor windows

**Symptom**: upper windows appear shifted left or right relative to lower ones.

**Fix**: `<use x="...">` x value must be IDENTICAL for same-column windows across floors. Define as a named constant:

```
win_left_x  = wall_left + bay_width * 0.5 - win_w/2
win_right_x = wall_left + bay_width * 2.5 - win_w/2

<!-- Both floors use the same x values -->
<use href="#win-std" x="win_left_x"  y="ground_floor_y"/>
<use href="#win-std" x="win_left_x"  y="upper_floor_y"/>   <!-- same x -->
```

---

## Drawing looks like a CAD export (too clean)

Missing ballpoint pen layer. Check:
- Is `<filter id="paper">` defined in `<defs>` and applied to the outer `<g>`?
- Is `feDisplacementMap scale` set to 0.4 (not 0 or 1+)?
- Are stroke-widths varying (2.1, 1.9, 1.4... not all exactly 2.0)?
- Are there scatter marks present?
- Is ink color `#2A2620` not `#000000`?

---

## Drawing looks drunk / wobbly

`feDisplacementMap scale` is too high. Set to exactly `0.4`. Never above `0.5`.

---

## `fill="none"` transparency issues (elements behind show through)

Replace all `fill="none"` on closed shapes with `fill="#F5EFE3"`. The paper color is visually "empty" but opaque — elements behind won't bleed through.

---

## Building looks too wide / wrong scale for the typology

**Symptom**: a "small forest cabin" renders 10m wide, or a "rowhouse" looks like a villa.

**Root cause**: px coordinates were copied or adapted from a different typology drawing without recalculating from real dimensions. The previous drawing's WALL_LEFT/WALL_RIGHT happen to be in the file — they get reused uncritically.

**Fix**: Phase 1 must start with typology → meters → px, not with px from a previous drawing:

```
<!-- After Phase 0 typology decision: -->
<!-- Typology: small forest cabin → realistic width 4–6m, pick 5m -->
<!-- 5m × 40px/m = 200px -->
<!-- WALL_LEFT = (viewBox_width - 200) / 2 = 200 -->
<!-- WALL_RIGHT = WALL_LEFT + 200 = 400 -->
<!-- Validation: (400 - 200) / 40 = 5m ✓ -->
```

Footprint check to run before any element:
```
(WALL_RIGHT - WALL_LEFT) / SCALE = meters → realistic for this typology?
```

Typical widths:
- Small cabin: 4–6m
- Urban rowhouse: 5–7m
- Suburban house: 8–12m
- Villa: 10–16m

**Source**: session 2026-04-20 (house_pencil.svg was 10m wide instead of ~5m)
