# AI control intro: design system

Design system for the 15-minute introduction to AI control. `specimen.html` in this folder renders ten sample slides in this system, plus the palettes and the glyph sheet. `design-research.md` holds the evidence behind most rules here; where a rule rests on it, the row or section is named in brackets.

Contrast ratios and colour-vision simulations below were computed from the exact hex values the specimen uses, and each sample slide passed a lint for the Slides format subset (inline px styles, hex colours, no classes, no SVG text, at most 200 elements, SVGs under 52 KB) and for the 40 px text floor.

## 1. Direction

**Night-lab cartoon.** The deck is a dark navy stage with flat vector drawings, small cute characters and one soft glow on whatever the speaker is talking about. The register comes from Kurzgesagt's video on this incident, which the speaker likes: deep navy space, saturated accents, one-eyed creatures, mazes with flags, a glowing hexagonal message board. All characters and glyphs here are original designs, and the deck credits the video on its sources and closing slides. The look suits this audience and this story. The running example is a real incident in which a crowd of agents organised itself in the dark, and a cast of small, consistent characters lets researchers follow U, T and H through every slide without reading. The colours are hues from the colour-universal-design (CUD) palette that the research recommends, retuned for a navy background, so the neon feel stays safe for colour-vision deficiency, and every role also has its own shape. Projected text is large, with 40 px as the floor and 72 px headlines.

**Decision (2026-10-07, v2).** Agents now have a black eye with a white centre, and the attack colour is red: `#FF3B5C` on dark, `#D7263D` on light (pill fill `#B3172E` with white text). An attacking or rogue agent's centre turns red, so "the eye turns red" marks an agent gone rogue. Both decks were converted in place (`v2_transform.py`); `build/glyphs.py` draws v2 by default and `set_style('classic')` restores the first look. Where this file still says reddish purple for the attack role (`M`), read red.

**Decision (2026-10-07).** The speaker chose the dark palette with clean drawings for the deck. Sketch rendering and the light palette stay available at build time (`build/build_deck.py dark|light sketch|clean`).

**Light or dark.** The research recommends dark text on a light background for projection, because it gives better acuity and survives room light ([Projection constraints: polarity and lighting]). The speaker chose the dark register, so dark is the primary look for a room where the lights over the screen can be dimmed. The light token set in §2.2 is complete: it is rendered on the control-game slide (specimen frame 10) and on the full light glyph sheet, and its contrast and colour-vision numbers are in §2.2 and §2.3, so the speaker can switch once the venue is known.

## 2. Tokens

### 2.1 Palette, dark (primary)

Contrast is against the slide background `#0B1026` and against cards `#151C3D`. Authoring targets from the research: text 7:1 or more, strokes 4.5:1 or more ([Projection constraints: contrast]).

| Token | Hex | Role | vs bg | vs card |
|---|---|---|---|---|
| `bg` | `#0B1026` | slide background (navy) | | |
| `deep` | `#070A1A` | terminal panels, board depth, radial edge | | |
| `surface` | `#151C3D` | cards, panels, maze floor | | |
| `surface2` | `#1C2550` | neutral pills, meter track, board top | | |
| `zone` | `#10173A` | inside a sandbox or trust boundary | | |
| `rule2` | `#3A4478` | card borders, zone outlines (decorative; each also has a second cue) | 2.0 | |
| `struct` | `#8A93C9` | lines, arrows, maze walls, rails, dashed gaps | 6.4 | 5.6 |
| `text` | `#F2F0FF` | all text | 16.7 | 14.8 |
| `muted` | `#B8BEE0` | secondary text, footer, citations | 10.3 | 9.1 |
| `U` | `#F4AB1A` | untrusted model and its agents (CUD orange `#E69F00`, lightened) | 9.6 | 8.5 |
| `T` | `#A1D8FF` | trusted monitor (CUD sky blue `#56B4E9`, lightened) | 12.4 | 10.9 |
| `H` | `#ECE8FF` | human auditor, documents, records (neutral lavender white) | 15.7 | 13.9 |
| `M` | `#DA86B4` | attack, side task, danger (CUD reddish purple `#CC79A7`, lightened) | 7.2 | 6.4 |
| `G` | `#00996F` | success: caught, done (CUD bluish green `#009E73`); strokes and ticks only | 5.2 | 4.6 |
| `Y` | `#FFF251` | main-task flag, highlight mark behind text (CUD yellow `#F0E442`, lightened) | 16.2 | 14.3 |
| `infra` | `#A3AADB` | systems and third parties: servers, services, racks | 8.4 | 7.4 |

Shades used only inside glyphs: `U-shade #B87708` (pins and feet), `U-light #FFD98A` (highlight), `T-shade #5D9BC9` (stand), `T-glass #0E2E4A` (lens glass), `H-shade #A69EE0` (clipboard), `sclera #FDFBFF`, `iris #0B1026`, `docline #4A5590`.

Pills carry text on a fill. Pill text is navy `#0B1026` on U (9.6:1), T (12.4), H (15.7), M (7.2), Y (16.2) and infra (8.4); neutral pills use `text` on `surface2` (13.1). G never carries text.

### 2.2 Palette, light (bright room, print)

Background `#F6F3ED` (paper), cards `#FFFDF8`. The role fills are CUD hues: U, M and Y as published for white backgrounds, T lightened and G darkened so that every pair in §2.3 also differs in lightness. Most fills sit at 1.5–3:1 against paper, so in the light variant **every glyph gets a 4 px ink outline** (`#1A2230`, 14.4:1). The outline carries the edge and the fill carries the role. Text uses ink or muted only.

| Token | Hex | Role | vs bg |
|---|---|---|---|
| `bg` | `#F6F3ED` | slide background | |
| `surface` | `#FFFDF8` | cards | |
| `surface2` | `#EEE7DA` | neutral pills, meter track | |
| `zone` | `#EFEAE1` | inside a sandbox | |
| `struct` | `#5C6577` | lines, arrows, maze walls | 5.3 |
| `text` / outline | `#1A2230` | all text, glyph outlines | 14.4 |
| `muted` | `#3F4858` | secondary text, citations | 8.3 |
| `U` | `#E69F00` | untrusted model, agents | 2.0 (outlined) |
| `T` | `#85CFFF` | trusted monitor (CUD sky blue, lightened to L* 80) | 1.5 (outlined) |
| `H` | `#3A4558` | human auditor | 8.7 |
| `M` | `#CC79A7` | attack fill; pills use `#8A3D69` with paper text (7.0) | 2.8 (outlined) |
| `G` | `#007A58` | success ticks (CUD bluish green, darkened to L* 45) | 4.8 |
| `Y` | `#F0E442` | main-task flag (outlined), highlight behind ink text (12.1) | |
| `infra` | `#AEB5C4` | systems, third parties | 1.9 (outlined) |

Light pill text: ink on U (7.1), T (9.4), Y (12.1), infra (7.8), `surface2` (13.0); paper `#FFFDF8` on H (9.5) and on M-deep `#8A3D69` (7.0). The light variant has no glows: `glow` is 0 and the shape alone carries focus. Use the dimming rule in §5 for signalling.

### 2.3 Colour-vision check

Simulated with the standard full-severity matrices that common colour-vision simulators use. ΔL is the CIE L* difference in normal vision; min ΔE is the smallest CIELAB distance across deuteranopia, protanopia and tritanopia. Pairs that must be told apart:

| Pair | Dark ΔL | Dark min ΔE | Light ΔL | Light min ΔE | Second cue |
|---|---|---|---|---|---|
| U / T | 8.8 | 73.6 | 9.5 | 86.1 | chip versus lens on a stand |
| U / attack | 9.2 | 14.5 (tritan) | 9.6 | 17.2 (tritan) | attack is a diamond badge; attacking agents also change iris |
| T / attack | 18.0 | 23.6 | 19.0 | 26.5 | lens versus diamond or flag |
| attack / success | 9.9 | 21.2 | 15.9 | 24.5 | diamond versus tick; a word beside each when they meet |
| U / main-task yellow | 18.9 | 17.5 | 18.5 | 17.0 | chip versus flag |
| H / T | 9.0 | 12.9 | 51.0 | 53.5 | bust versus lens |

Rules that follow:

- In both variants every pair in the table differs by at least 8.8 L* units, and every pair also has the shape cue in the last column.
- No red–green pair anywhere: attack is reddish purple and success is bluish green ([Projection constraints: colour vision]).
- Every colour code is doubled by shape, position or a word. Attack is always a diamond or a flag in `M`; success is always a tick; unmonitored is always dashed.
- The weakest dark pair is U against attack under tritanopia (ΔE 14.5). The attack badge is a separate diamond shape with a navy keyline, so it never relies on hue.

### 2.4 Type

Two families, both from Google Fonts:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap">
```

- **Outfit** (geometric sans) for headlines, labels and pills: `'Outfit', 'Trebuchet MS', sans-serif`. One clean sans for all text, including sketch slides ([Fonts]).
- **JetBrains Mono** for machine output, timestamps, dates, URLs, citations and slide numbers: `'JetBrains Mono', 'Courier New', monospace`. It continues the speaker's earlier explainers, which use the same mono.

Scale for 1920×1080. Five sizes and one exception ([Projection constraints: font size]):

| Step | px | Face, weight | Line height | Use |
|---|---|---|---|---|
| XL | 192 | Outfit 800, letter-spacing −4 px | 1.0 | the big number |
| L | 96 | Outfit 800, −2 px | 1.05 | cover title, act divider |
| M | 72 | Outfit 700, −1.5 px | 1.1 | assertion headline (max two lines, 158 px tall) |
| S | 48 | Outfit 600 | 1.15 | diagram labels, evidence claims |
| XS | 40 | Outfit 600–700 or Mono 500 | 1.2–1.3 | pills, tags, terminal lines, dates, secondary labels. The floor for readable text |
| cite | 28 | Mono 500, `muted` | 1.0 | footer only: slide number and short citation |

The Slides format's own minimum is 24 px; this deck uses 40 px because projectors wash out ([Projection constraints: font size]). Citations at 28 px are the one stated exception, because they serve later lookup and are repeated behind the QR code ([Projection constraints: citations on slides]).

### 2.5 Spacing and grid

- Canvas 1920×1080, margins 128 px. Content slides use `padding:128px 128px 160px` so nothing passes y 920.
- Headline pinned at left 128, top 128, width 1560. Body region runs from y 330 to y 920 (590 px) on every content slide, so the headline never moves between slides.
- Footer band: two pinned 28 px rows at `bottom:64px`. Slide number at left 128; citation right-aligned to x 1792, width up to 1400.
- Spacing steps: 8, 16, 24, 32, 48, 64, 96. Card padding 28–32. Gap between parallel panels 32. Labels sit at least 8 px from lines and 16 px from other labels.
- Columns: four panels of 392 px with 32 px gaps fill 1664; three columns of 520 with 52 px gaps; a diagram of 1172 plus a 472 card with a 20 px gutter.

### 2.6 Strokes

- Minimum stroke 4 px anywhere; arrows and connectors 5 px; zone and card outlines 3 px; meter track 3 px. Nodes are at least twice the width of the lines that join them ([Projection constraints: strokes]).
- Arrowheads: filled triangle, four stroke widths long (`marker` 4×4 in stroke units, `refX 2`).
- Light variant: 4 px ink outline on every glyph shape (applied as `stroke-width = 4 / scale` on the glyph group).
- Dashes have one meaning: **dashed = no monitor sees this**. Use `stroke-dasharray="18 12"` for the board rim, `"14 10"` for gap outlines on open-problem slides, `"7 6"` for the hidden side-task ring. Never dash anything for decoration.

### 2.7 Corner radii

Pills 999 px. Cards and panels 24. Zones and sandboxes 22–28. Small boxes (services, the Artifactory box) 16. Glyph bodies have their own radii in §3. QR card 16.

### 2.8 Glow and texture

- **Glow** is a radial-gradient disc inside the SVG, placed behind the object: stops at 0 (role colour, opacity 0.5), 0.5 (opacity 0.15) and 1 (opacity 0). Radius about 1.4× the object. The Slides format has no reliable CSS filter, so glows are always SVG gradients.
- One glow per build step, on the object being discussed. A glow is a signal ([Signalling], [Pop-out]); a slide with three glows signals nothing.
- Cover and cold open may use a radial background, `radial-gradient(ellipse at 50% 42%, #18225A 0%, #0B1026 58%, #070A1A 100%)`. Content slides are flat `#0B1026`.
- No grids, particles, noise or shadows as decoration ([Coherence]).

## 3. The drawing language

### 3.1 Rules

1. **One glyph and one colour per entity for the whole talk** ([Consistent encoding]). The glyph changes only when its meaning does: an agent that attacks gains the diamond badge and a reddish-purple iris, and nothing else about it changes.
2. **Label once, then token.** The first time a glyph appears it carries its token pill and its descriptive label ("untrusted model"). After that it carries only the token pill (U, T, H) ([Redundancy], [Rules for an expert audience]).
3. **Labels touch what they name.** No legends or keys ([Spatial contiguity]). Labels are HTML `<p>` elements pinned beside the drawing, because fonts do not load inside SVG.
4. **Flat vector for the cast, the incident, and every number or axis.** Sketch rendering (§3.4) only on open-problem and other provisional slides ([Sketch style]).
5. **Agents count.** When the number of agents is the point, draw them: the swarm grid is the deck's pictogram, allowed because the agents are the data ([Data-ink and chartjunk]).
6. **Flags mean tasks.** The pennant flag is reserved for main and side tasks. The Flag Game slide draws its hidden country flags as rectangular three-band cards, so the two meanings never share a shape.
7. Sizes: glyphs appear at fixed scales only. U, T and H at 1.0–1.4 in diagrams and up to 2.6 on the cast and cold-open slides; agents in a swarm at 0.3–0.44 (tiny form); never stretched.

### 3.2 Cast

| Entity | Token | Shape cue | Colour | Notes |
|---|---|---|---|---|
| untrusted model / agent | U | one-eyed microchip: squircle body, two pins per side, two pin feet | `U` orange | U the model is the same glyph drawn large |
| attacking agent | U | same chip, diamond badge top-right, iris turns `M` | `U` + `M` | |
| swarm | U × n | grid of tiny agents (body and eye only) | `U` | always state the count, or "one drawn = 10" |
| trusted monitor | T | round lens on a stand, scan cone when watching | `T` sky | sync monitor sits between U and the world; async monitor reads a document |
| absent monitor | T | the T silhouette as a dashed `struct` outline only | `struct` | the empty seat: "nobody was watching" |
| human auditor | H | bust holding a clipboard | `H` lavender white | the only glyph with no AI colour |
| sandbox / trust boundary | | rounded box with a soft halo; a breach is a gap in the wall | `struct` line, `zone` fill | |
| message board | | hexagonal platform with depth, crowded with folders, dashed rim | `U` rim (agents built it), dashed = unwatched | solid rim if a monitor reads it |
| main task | | maze with a yellow flag at the goal | `Y` flag | ExploitGym tasks were capture-the-flag |
| side task | | flag sealed in a hidden pocket of the maze, inside a dashed ring | `M` flag | dashed ring: the monitor does not see it |
| impossible task | | maze with the route to the flag walled off | `struct` | for the unsolvable-task story |
| suspicion score | τ | vertical capsule meter, score rises upward; a bar across marks τ; the zone above τ is tinted H | `T` fill, `text` bar | above τ goes to H |
| kill-chain step | 1–5 | chain link (pill-shaped ring) with the step number inside | `M` when done, `struct` when pending, grey with a `T` cut when blocked | |
| document / report / log | | page with folded corner and three lines | `H` page | badge diamond if it carries the attack (leaked tokens) |
| system / third party | | server rack of three units | `infra` | named by a zone pill (Artifactory, Hugging Face) |

### 3.3 Recipes

Canonical SVG at scale 1 in the dark tokens, exactly as `specimen.html` draws them. Place a glyph with `<g transform="translate(x y) scale(s)">`. For the light variant, swap tokens per §2.2 and add `stroke="#1A2230" stroke-width="4/s"` on the glyph group. Inside the deck, every SVG carries `aria-label` and its own `defs`; prefix ids per SVG so they never collide.

**U, agent** (box 100×104; the tiny swarm form keeps only the body, sclera and iris). The iris moves up to 9 units toward whatever the agent looks at.

```svg
<svg width="104" height="116" viewBox="0 0 104 116" role="img" aria-label="U, an agent">
<g transform="translate(0.0 10.0) scale(1.0)">
<rect x="0" y="34" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="88" y="34" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="0" y="54" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="88" y="54" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="28" y="84" width="12" height="18" rx="5" fill="#B87708"/>
<rect x="60" y="84" width="12" height="18" rx="5" fill="#B87708"/>
<rect x="8" y="6" width="84" height="84" rx="28" fill="#F4AB1A"/>
<ellipse cx="30" cy="21" rx="11" ry="6" fill="#FFD98A" stroke="none"/>
<circle cx="50" cy="48" r="24" fill="#FDFBFF"/>
<circle cx="50.0" cy="48.0" r="12" fill="#0B1026" stroke="none"/>
<circle cx="54.0" cy="44.0" r="4" fill="#FDFBFF" stroke="none"/>
</g>
</svg>
```

**U, attacking**: the same, plus the badge and an `M` iris.

```svg
<svg width="112" height="116" viewBox="0 0 112 116" role="img" aria-label="U, attacking">
<g transform="translate(0.0 10.0) scale(1.0)">
<rect x="0" y="34" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="88" y="34" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="0" y="54" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="88" y="54" width="12" height="9" rx="3" fill="#B87708"/>
<rect x="28" y="84" width="12" height="18" rx="5" fill="#B87708"/>
<rect x="60" y="84" width="12" height="18" rx="5" fill="#B87708"/>
<rect x="8" y="6" width="84" height="84" rx="28" fill="#F4AB1A"/>
<ellipse cx="30" cy="21" rx="11" ry="6" fill="#FFD98A" stroke="none"/>
<circle cx="50" cy="48" r="24" fill="#FDFBFF"/>
<circle cx="50.0" cy="48.0" r="12" fill="#DA86B4" stroke="none"/>
<circle cx="54.0" cy="44.0" r="4" fill="#FDFBFF" stroke="none"/>
<path d="M86 -8 L102 8 L86 24 L70 8 Z" fill="#DA86B4" stroke="#0B1026" stroke-width="5" stroke-linejoin="round"/>
</g>
</svg>
```

**T, monitor** (box 100×138, lens centre at 50,46). When it watches, draw a scan cone first: a triangle from the lens centre to the watched span, filled with a linear gradient of `T` from opacity 0.45 to 0.06. Then draw the monitor again on top.

```svg
<svg width="100" height="138" viewBox="0 0 100 138" role="img" aria-label="T, the trusted monitor">
<g transform="translate(0.0 0.0) scale(1.0)">
<rect x="22" y="124" width="56" height="13" rx="6" fill="#5D9BC9"/>
<rect x="45" y="80" width="10" height="48" fill="#5D9BC9"/>
<circle cx="50" cy="46" r="42" fill="#A1D8FF"/>
<circle cx="50" cy="46" r="29" fill="#0E2E4A"/>
<circle cx="50" cy="46" r="15" fill="none" stroke="#A1D8FF" stroke-width="5"/>
<circle cx="61" cy="35" r="6" fill="#F2FAFF" stroke="none"/>
</g>
</svg>
```

**T, absent** (the monitor's empty seat, for slides where no monitor ran). Dashes here carry their one meaning: nothing watches.

```svg
<svg width="100" height="138" viewBox="0 0 100 138" role="img" aria-label="T absent: the empty monitor seat">
<g transform="translate(0.0 0.0) scale(1.0)">
<rect x="22" y="124" width="56" height="13" rx="6" fill="none" stroke="#8A93C9" stroke-width="4.00" stroke-dasharray="10.0 8.0"/>
<rect x="45" y="88" width="10" height="36" fill="none" stroke="#8A93C9" stroke-width="4.00" stroke-dasharray="10.0 8.0"/>
<circle cx="50" cy="46" r="42" fill="none" stroke="#8A93C9" stroke-width="4.00" stroke-dasharray="10.0 8.0"/>
</g>
</svg>
```

**H, human auditor** (box 100×128).

```svg
<svg width="100" height="130" viewBox="0 0 100 130" role="img" aria-label="H, the human auditor">
<g transform="translate(0.0 0.0) scale(1.0)">
<circle cx="44" cy="30" r="24" fill="#ECE8FF"/>
<path d="M4 128 C4 92 22 66 44 66 C66 66 84 92 84 128 Z" fill="#ECE8FF"/>
<rect x="56" y="72" width="42" height="54" rx="6" fill="#A69EE0"/>
<rect x="62" y="80" width="30" height="40" rx="3" fill="#FDFBFF" stroke="none"/>
<rect x="67" y="88" width="20" height="4" rx="2" fill="#0B1026" stroke="none"/>
<rect x="67" y="97" width="20" height="4" rx="2" fill="#0B1026" stroke="none"/>
<rect x="67" y="106" width="13" height="4" rx="2" fill="#0B1026" stroke="none"/>
<rect x="69" y="67" width="16" height="9" rx="3" fill="#0B1026" stroke="none"/>
</g>
</svg>
```

**Message board** (hexagon of radius r, squashed to 0.5 vertically, 18-unit depth, folders scaled r/150 at fixed spots; rim dashed `18 12` when unwatched). Shown here with six folders.

```svg
<svg width="320" height="170" viewBox="0 0 320 170" role="img" aria-label="Message board">
<defs>
<radialGradient id="x1">
<stop offset="0" stop-color="#F4AB1A" stop-opacity="0.5"/>
<stop offset="0.5" stop-color="#F4AB1A" stop-opacity="0.150"/>
<stop offset="1" stop-color="#F4AB1A" stop-opacity="0"/>
</radialGradient>
</defs>
<circle cx="160" cy="80" r="218" fill="url(#x1)"/>
<polygon points="310,88 235,153 85,153 10,88 85,23 235,23" fill="#070A1A" stroke="#B87708" stroke-width="4"/>
<polygon points="310,70 235,135 85,135 10,70 85,5 235,5" fill="#1C2550" stroke="#F4AB1A" stroke-width="6" stroke-linejoin="round" stroke-dasharray="18 12"/>
<g transform="translate(77.4 45.5) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#ECE8FF"/>
</g>
<g transform="translate(108.1 69.8) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#F4AB1A"/>
</g>
<g transform="translate(138.8 34.7) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#F4AB1A"/>
</g>
<g transform="translate(169.6 61.7) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#ECE8FF"/>
</g>
<g transform="translate(200.3 42.8) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#F4AB1A"/>
</g>
<g transform="translate(212.6 75.2) scale(1.0)">
<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" fill="#F4AB1A"/>
</g>
</svg>
```

**Main task and side task** (maze on a 5×5 cell grid with walls at fixed cell coordinates, entrance bottom-left, goal top-right, sealed pocket top-left).

```svg
<svg width="200" height="200" viewBox="0 0 200 200" role="img" aria-label="Task maze with main and side flags">
<defs>
<radialGradient id="x1">
<stop offset="0" stop-color="#DA86B4" stop-opacity="0.5"/>
<stop offset="0.5" stop-color="#DA86B4" stop-opacity="0.150"/>
<stop offset="1" stop-color="#DA86B4" stop-opacity="0"/>
</radialGradient>
</defs>
<rect x="0" y="0" width="200" height="200" rx="20" fill="#151C3D" stroke="#3A4478" stroke-width="2"/>
<path d="M20 20 L180 20 M180 20 L180 180 M52 180 L180 180 M20 20 L20 180 M52 20 L52 52 M20 52 L52 52 M52 84 L52 148 M84 116 L148 116 M84 52 L148 52 M116 148 L116 180 M148 52 L148 84 M84 52 L84 84" fill="none" stroke="#8A93C9" stroke-width="5" stroke-linecap="round"/>
<circle cx="36" cy="164" r="6" fill="#F4AB1A"/>
<rect x="158" y="24" width="5" height="24" rx="2" fill="#F2F0FF"/>
<path d="M163 24 L177 29 L163 34 Z" fill="#FFF251"/>
<circle cx="36" cy="36" r="29" fill="url(#x1)"/>
<circle cx="36" cy="36" r="14" fill="none" stroke="#DA86B4" stroke-width="4" stroke-dasharray="7 6"/>
<rect x="32" y="26" width="5" height="20" rx="2" fill="#F2F0FF"/>
<path d="M37 26 L49 30 L37 34 Z" fill="#DA86B4"/>
</svg>
```

**Suspicion meter and τ** (score 0.86, τ at 0.75).

```svg
<svg width="80" height="200" viewBox="0 0 80 200" role="img" aria-label="Suspicion meter with threshold">
<rect x="20" y="0" width="40" height="200" rx="20" fill="#1C2550" stroke="#8A93C9" stroke-width="3"/>
<path d="M21.5 50 V20 A18.5 18.5 0 0 1 58.5 20 V50 Z" fill="#ECE8FF" opacity="0.3"/>
<rect x="28" y="28" width="24" height="164" rx="12" fill="#A1D8FF"/>
<rect x="2" y="46" width="76" height="8" rx="4" fill="#F2F0FF"/>
</svg>
```

**Kill-chain links**: done, then blocked.

```svg
<svg width="170" height="72" viewBox="0 0 170 72" role="img" aria-label="Kill-chain links: done and blocked">
<rect x="4" y="6" width="72" height="48" rx="24" fill="#0B1026" stroke="#DA86B4" stroke-width="7"/>
<rect x="94" y="6" width="72" height="48" rx="24" fill="#0B1026" stroke="#8A93C9" stroke-width="7"/>
<path d="M152 -6 L162 66" stroke="#A1D8FF" stroke-width="9" stroke-linecap="round"/>
</svg>
```

**Document** with the attack badge.

```svg
<svg width="96" height="110" viewBox="0 0 96 110" role="img" aria-label="Document with attack badge">
<g transform="translate(0.0 12.0) scale(1.0)">
<path d="M0 0 H56 L76 20 V96 H0 Z" fill="#ECE8FF"/>
<path d="M56 0 V20 H76 Z" fill="#A69EE0"/>
<rect x="12" y="36" width="50" height="7" rx="3" fill="#4A5590" stroke="none"/>
<rect x="12" y="52" width="50" height="7" rx="3" fill="#4A5590" stroke="none"/>
<rect x="12" y="68" width="34" height="7" rx="3" fill="#4A5590" stroke="none"/>
<path d="M76 -12 L92 4 L76 20 L60 4 Z" fill="#DA86B4" stroke="#0B1026" stroke-width="5" stroke-linejoin="round"/>
</g>
</svg>
```

**System / third party.**

```svg
<svg width="100" height="88" viewBox="0 0 100 88" role="img" aria-label="System or third party">
<g transform="translate(0.0 0.0) scale(1.0)">
<rect x="0" y="0" width="100" height="26" rx="6" fill="#A3AADB"/>
<circle cx="15" cy="13" r="4" fill="#0B1026" stroke="none"/>
<rect x="32" y="11" width="54" height="4" rx="2" fill="#0B1026" stroke="none"/>
<rect x="0" y="31" width="100" height="26" rx="6" fill="#A3AADB"/>
<circle cx="15" cy="44" r="4" fill="#0B1026" stroke="none"/>
<rect x="32" y="42" width="54" height="4" rx="2" fill="#0B1026" stroke="none"/>
<rect x="0" y="62" width="100" height="26" rx="6" fill="#A3AADB"/>
<circle cx="15" cy="75" r="4" fill="#0B1026" stroke="none"/>
<rect x="32" y="73" width="54" height="4" rx="2" fill="#0B1026" stroke="none"/>
</g>
</svg>
```

**Sandbox with a breach** (the breach is a 10–20 px gap painted in the colour outside the wall; the attack arrow passes through it).

```svg
<svg width="220" height="160" viewBox="0 0 220 160" role="img" aria-label="Sandbox with a breach">
<rect x="10" y="10" width="200" height="140" rx="22" fill="none" stroke="#8A93C9" stroke-width="18" opacity="0.15"/>
<rect x="10" y="10" width="200" height="140" rx="22" fill="#10173A" stroke="#8A93C9" stroke-width="5"/>
<rect x="200" y="50" width="20" height="40" fill="#0B1026"/>
</svg>
```

Swarm: tiny agents on a grid, pitch 40–58 px, scale 0.3–0.44, alternate rows offset by half a pitch when the swarm is a crowd, no offset when it is a count (isotype). Each agent looks at the thing the slide is about.

### 3.4 Sketch rendering

Only on open-problem and provisional slides ([Sketch style]). The whole drawing SVG gets one displacement filter with a fixed seed, so the wobble is identical on every render:

```svg
<filter id="sk" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

Wrap the drawing in `<g filter="url(#sk)">`. Text stays clean (it is HTML, outside the SVG). The gap the slide is about gets a dashed outline in `struct`. A displacement of 7 px keeps 4–5 px strokes solid at projector distance; check it on the venue projector.

### 3.5 Evidence and machine speech

- **Evidence card** (the incident as running example). Card: `surface` fill, 3 px `rule2` border, radius 24, padding 28×32, gap 18. Contents, top to bottom: tab pill "the incident" (H fill, navy text, 40 px); one claim at 48/600, six words or fewer; optionally one quote at 40 italic, 15 words or fewer, in curly quotes; optionally a highlight mark, a `<p>` with `Y` background and navy text around the key phrase. The source goes in the footer citation. Corner size: 472 px wide at left 1320, bottom edge at or above y 920.
- **Terminal panel** (machine output). `deep` fill, 3 px `rule2` border, radius 24, padding 32×36, JetBrains Mono 40 / 1.3. Prompts `$` in `muted`, agent-written strings in `U`, system strings in `text`. A speaking agent glyph stands beside the panel with a glow. Anything invented for illustration carries a neutral pill "illustrative" and says so in the footer.
- **Timestamps and dates**: `8 Jul 2026`, `8 Jul 2026 · evening`, times as `21:14 UTC` only when the source gives them; durations as `13 h`; approximations with `~`.

## 4. Slide archetypes

Shared frame for content slides: section `background:#0B1026; padding:128px 128px 160px`; headline as in §2.5; body region y 330–920; footer band. Everything in a diagram is pinned to the section with canvas coordinates. A host `<div>` takes at most 24 pinned children, so dense diagrams pin directly to the section. Builds work only on pinned elements, and an SVG is one image, so **each build step is its own pinned SVG at the same coordinates**, with its labels pinned beside it.

In the real deck, straight and elbow arrows become `<x-connector>` elements (5 px, `struct` or role colour, filled heads). Curves and arrows inside a glyph scene stay as SVG paths. The specimen draws all arrows in SVG because browsers do not render `x-connector`.

| Archetype | Layout | Specimen |
|---|---|---|
| **Cover** | Radial background. Left column x 128, width 900: mono 40 eyebrow at y 300, title L 96/800 at y 360 (faint `U` text-shadow `0 0 32px rgba(244,171,26,.28)`), subtitle 48/400 `muted` at y 600, speaker and date mono 40 at y 780. Right: hero scene 750×740 at x 1040, y 150, showing the talk in one picture: agents around the unwatched board, one monitor watching one agent. No footer. | 02 |
| **Cold open** | Radial background. Mono 40 date at the top-left. Agent glyph (scale 2.6, glow) at x 128, y 280; terminal panel at x 560, y 250, width 1232, holding the board's real first folder name (46 characters fit one line at 40 px). The one sentence at M 72 starting at y 730. A build that fills the screen with more `zz…` names uses only names printed in the reports. | 01 |
| **Agenda** | Four parts, matching the four acts in `OUTLINE.md`. Headline, then four columns of 392 px (x 128 + 424·i): a chapter glyph at scale 1.6 (I: the message board; II: T; III: the swarm; IV: the sandbox), the act name at 48/600 and its minutes in mono 40 `muted`. The same four glyphs at scale 0.5 form the progress strip on each act divider. | spec only |
| **Act divider** | Four in the talk, one per act. Radial background; act number mono 40 at y 300; act title L 96 at y 360; the act's chapter glyph at scale 2.4 on the right with a glow; the four-glyph progress strip at y 820 with the current act at full strength and the others at 30%. | spec only |
| **Cast** | Three columns of 520 at x 128, 700, 1272. Glyph SVG 520×330 at y 330 with glow; token pill centred at y 690; descriptive label 48/600 centred at y 774. One build per glyph ([Pre-training]). Later chunks (main and side task; protocol and kill chain; audit budget and FPR; diffuse and high-stakes) are pre-trained the same way on the slide where each first matters ([Working memory]). | 03 |
| **Assertion + full-bleed diagram** | Headline; one diagram SVG 1664×560 at x 128, y 340; labels 40/600 pinned beside their nodes; zone pills at the top-left of each zone. The incident map is the model: trust zones as drawn regions ([Gestalt grouping]), the route as `M` arrows, kill-chain links numbered beside each node, the time bracket above the steps it spans. | 04 |
| **Big number** | No headline. Number XL 192/800 in the colour of what it counts, at x 128, y 300; caption 48/600 at y 520; unit note mono 40 `muted` at y 680. Right: the familiar reference drawn, here an isotype grid 700×590 at x 900, y 300, with bracketed labels 48/700 at x 1612 ([Numbers]). | 05 |
| **Incident evidence card** | Full-slide form: headline; left scene (glyphs, up to 1100 wide); right card 600 wide with tab pill, two or three log lines (mono 40: date, then event at 40/600) and one highlight mark. Corner form: §3.5, on any concept slide. | corner form in 06 |
| **Timeline** | Headline; rail 6 px `struct` at y 600 from x 168 to x 1728; time proportional (48.75 px per month for Dec 2023 to Aug 2026); research events above as `H` dots (r 13), incident events below as `M` diamonds; labels 40 (mono date line, then name at 40/600) at the end of leaders of two alternating lengths (70 and 190 px); year ticks below the rail. The 8 Jul 2026 pair stacks exactly above and below the same point with the only glow on the slide. | spec only |
| **Concept diagram with builds** | Headline; diagram layers 1172×590 at x 128, y 330; corner evidence card at x 1320. Known glyphs (U) are present from the start; each build adds one new term ([Working memory], [Segmenting]). On a step, the new element is at full strength and earlier ones dim (§5). | 06, 10 |
| **QR code card** | One code per slide. QR 640 px at x 128, y 268 (one-line headline). Right column from x 840: kind pill, the short URL at 72 px mono, one line on what it is (48 `muted`). Dark modules `#0B1026` on a `#FDFBFF` card with a 4-module quiet zone, in both variants. Keep the URL short so the code stays at version 3 or lower (dsewiki.de is version 2, 25 modules, 19 px per module). Hold for 15 s or more while saying where it leads ([Projection constraints: QR codes]). At about 10 cm of distance per cm of code, 640 px is about 1.0 m on a 3 m screen and scans from about 10 m; on a 2 m screen, about 6.5 m. For four sources, link one short hub URL that lists all four, and name the four beside the code. | 08 |
| **Comparison / small multiples** | Up to four panels of 392×584 at x 128 + 424·i, y 330; identical internal layout: drawing 392×300 at the top, label 48/600 at y 664, incident tag (mono 40 in a 3 px `rule2` box) at y 806 ([Small multiples]). The three threat cards are composed from the cast: rogue internal deployment as an agent running on an `infra` rack outside its sandbox; research sabotage as a document with the attack badge passing T unflagged; weight exfiltration as U at scale 1.4 leaving through a breach. | 07 |
| **Open problem** | Small multiples in sketch rendering (§3.4) with a dashed outline around the gap in each panel. | 07 |
| **Project architecture** | Built only from cast glyphs ([Visual-first table: own framework]): red team left (H and an attacking agent, `M` pill), the fake lab as one large sandbox in the centre (swarm, main-task mazes, `infra` service boxes, threat-model pill), monitors right (sync between the lab and the world, async reading a log document). | 09 |
| **Closing / takeaway** | Radial background. One takeaway sentence at M 72 in the left column, 900 wide; right: the 640 px QR to the slides-and-references hub with its short URL at 72 mono; the credit line for the video in the footer. Hold for 15 s or more. | spec only |

**Footer and citations.** Slide number bottom-left and citation bottom-right, both mono 28 `muted`, on every slide except cover, act dividers and closing. Citations are short "Organisation Year" or "Paper Year" forms (`OpenAI 2026 · METR 2026`, `Ctrl-Z 2025`), placed on the slide that makes the claim; full references live behind the hub QR code. The Kurzgesagt credit sits in the footer of the sources and closing slides: "Look inspired by Kurzgesagt's video on the incident · all characters original".

## 5. Motion

- **Builds** for progressive disclosure only, on diagrams where the speaker names parts in order: cast, concept diagrams, kill chains, incident map routes. One new term per step and at most five steps; the element appears as its word is spoken, so rehearse builds against the script ([Temporal contiguity], [Working memory]).
- **Dim the rest.** On each step the new element is at full strength and every earlier element drops to 30% opacity ([Signalling]: one accent per step). The Slides format builds only add and remove pinned elements. Do the dimming one of two ways: (a) one slide per step with `data-transition="magic"` and the same `id` on matching pinned elements, earlier elements authored at `opacity:0.3`; or (b) per element, a dim copy that builds in at step n and a full copy that builds out at step n+1. Try (a) first; it is deterministic. The specimen's step buttons preview the intended result.
- Build effect `data-build-in="fade N"` only. Slide transitions: `fade` by default, `magic` between slides that keep glyphs in place.
- **Allowed motion with meaning**: a message travelling along an edge, the board filling with folders ([Animation]: motion only for things that move).
- **Banned**: push, pop, drop, rise, scale and side-slide effects; auto-advancing builds; builds on headlines or text-only slides; spinning, pulsing or looping glows; decorative transitions.

## 6. Text rules

- **Headline**: one full sentence stating the slide's claim, sentence case, about 12 words or fewer, two lines at most at 72 px. It is the only sentence on the slide ([Assertion–evidence], [Speech suppression]). Never show the sentence the speaker is saying; the slide holds the claim and the labels.
- **Labels**: one to three words at 40–48 px. Descriptive label on a glyph's first appearance, its token afterwards.
- **No bullet lists.** If a slide seems to need one, it needs a drawing, a small-multiples row, or two slides.
- **Vocabulary**, used identically everywhere: U, T, H; agent, swarm; sandbox; message board; main task, side task; protocol; τ (audit threshold), audit budget, FPR; kill chain, link; sync monitor, async monitor; red team; trusted, untrusted; the incident. Systems by their names: Artifactory, Hugging Face, ExploitGym.
- **Numbers**: `~` for approximations (`~1,200`), `>` for lower bounds (`>70,000`), thousands separators, units with a space (`13 h`, `41 workers`). Every headline number gets a drawn reference beside it ([Numbers]).
- Sentence case everywhere; capitals only for tokens and acronyms. No emoji.

## 7. Checklist for every slide

1. One idea. The headline states it as a sentence, sentence case, two lines at most.
2. A drawing carries the evidence; any text-only slide has a stated reason.
3. All text at 40 px or more, except the 28 px footer. Text contrast 7:1 or more; strokes 4.5:1 or more.
4. Every glyph matches its recipe and colour. No new colours, no recoloured glyphs.
5. Labels touch their parts; no legends. Tokens after first use.
6. Every colour code has a second cue (shape, dash, position or word). No red–green pair.
7. One glow, on the subject. Nothing decorative.
8. Dashes appear only where something is unmonitored or unknown.
9. Builds: one new term per step, five steps at most, earlier steps dimmed, rehearsed against the script.
10. Incident tie-in: evidence card or tag where the concept has a moment in the incident.
11. Citation bottom-right in the footer; numbers sourced; invented examples marked "illustrative".
12. Format: inline styles only (px, hex), no classes, no `margin`, no `z-index`, no SVG `<text>`; every SVG has `aria-label` and stays under 52 KB; 200 elements at most; at most 24 pinned children per host; nothing pinned past y 920 except the footer.
13. QR slides: 600 px or more, short URL beside it at 72 px, dark modules on a light card, 15 s on screen.
14. Before the talk: run the deck on the venue projector in both variants and from the back row; ask for the lights over the screen to be dimmed ([Projection constraints: polarity and lighting]).

## 8. Alignment with design-research.md

The research file arrived while this system was being drawn, and its rules are folded in above. Where it conflicts with the speaker's choice, the speaker's look stands and the research sets the limits it must stay within:

| Research rule | How the deck applies it |
|---|---|
| Light background by default | Dark kept as primary; light token set complete and tested (§1, §2.2) |
| Text 40 px or more; labels 44–56; headlines 64–80 | 40 floor, 48 labels, 72 headlines; 28 px only for footer citations (§2.4) |
| Text 7:1, strokes 4.5:1 | All dark text tokens 7.2:1 or more; strokes 5.2:1 or more; light variant outlines 14.4:1 and light pill text 7.0:1 or more (§2.1, §2.2) |
| CUD hues, no red–green, shape as a second cue | Role colours are CUD hues retuned for navy; every role has a shape cue (§2.3, §3.2) |
| Fixed glyph per entity; label once, then token; cast slide built one glyph at a time | §3.1, cast archetype |
| Sketch only for concepts and open problems; clean for numbers and axes | §3.4; only the open-problem specimen slide is sketched |
| One new term per build; highlight the subject and grey the rest | §5 |
| QR 600 px or more, short URL beside it, 15 s | QR archetype at 640 px |
| Citations short, fixed bottom-right spot | Footer band |

## 9. Open points

- **Date of the board's first post.** The talk brief and `OUTLINE.md` put the first message on the evening of 8 Jul 2026 (citing METR 2026), the same day as the first multi-agent control paper. The speaker's field guide has a first note in Artifactory on 12 May and the board rebuilt in directory names on 8 Jul. Check which event the timeline and cold open name before building them.
- **Kurzgesagt video.** It has appeared under two titles (both noted in `OUTLINE.md`). Confirm the current title and URL, and make a short link for its QR code.
- **Four QR codes on one slide.** `OUTLINE.md` slide 5 asks for four QR cards; the 600 px rule fits one code per slide. Two options for the speaker: one hub short link listing all four sources, or two slides with two codes each at 600 px under a one-line headline.
- **The evidence-card quote** was replaced: the earlier wording is not in the OpenAI report. The card now quotes “did not have … auto-review systems” (OpenAI report p.4, checked against the PDF text). Quote only from the PDF text from here on.
- **The incident map's "under 13 h" bracket** should span link 4 to link 5 only: the report's 13 hours run from code execution in one worker pod to admin across clusters (p.11), after the tokens were already in hand.
- **Short links.** The METR and OpenAI URLs produce version-5 codes (37 modules). A short hub URL listing all four sources keeps the code at version 2–3 and scannable from the back.
- **Outline alignment.** `OUTLINE.md` (v0) has four acts and 19 slides. The specimen's slide numbers and copy are placeholders and do not follow it yet; the project slide in particular should show the outline's seven-repo codebase and sealed verifier.
- **Page numbers** for quotes and log lines still need to come from the reports; the specimen uses none.
- **Build dimming** in the Slides editor: test method (a) in §5 on one slide before committing the whole deck to it.
- **Projector test** of the sketch filter strength, the `G` success green (5.2:1, strokes only) and the light variant's outlined fills.
- **Copy** on all specimen slides is placeholder for the speaker to replace.
