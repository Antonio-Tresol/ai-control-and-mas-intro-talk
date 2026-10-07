# Character assets

Original one-eyed agents and a small monitor robot, drawn for the AI control talk and free to reuse in other projects. The register takes its cue from Kurzgesagt's video on the OpenAI–Hugging Face incident; every character here is an original design.

`index.html` shows everything on dark and light backgrounds.

## What's here

| Folder | Contents |
|---|---|
| `svg/on-dark/` | 82 drawings, no outline, for dark backgrounds |
| `svg/on-light/` | the same 82 drawings with a dark ink outline, for pale backgrounds |
| `png/on-dark/`, `png/on-light/` | 512 × 512 transparent PNGs of each SVG |

All drawings sit in a 140 × 140 viewBox with a transparent background, so they line up side by side.

- **Agents**: 6 shapes (`chip`, `round`, `tall`, `drop`, `hex`, `ghost`) × 10 colours (`orange`, `sky`, `pink`, `purple`, `teal`, `green`, `coral`, `yellow`, `lavender`, `slate`), named `agent-<shape>-<colour>`.
- **Accessories**: `antenna`, `cap`, `headset`, `sprout`, `crown`, `megaphone`, `attack-badge`. Shown on the orange chip and in six mixed examples.
- **Attacking agent**: `agent-chip-orange-attacking`, with a pink iris and the diamond attack badge.
- **Monitor robot**: `monitor-robot-idle`, `-scanning` (with a scan cone), `-alert` (pink scan line and lamp), four colour variants, and `monitor-robot-absent`, a dashed outline for "no monitor here".

## Rogue agents and swarms

`rogues-and-swarms.html` shows them; files sit in the same `svg/` and `png/` folders.

- **Three rogue agents**: `rogue-hooded` (dark hood, one glowing red eye), `rogue-visor` (faceless, red visor) and `rogue-glitch` (RGB split, glowing eye). These three were picked from ten iterations; the rest were dropped.
- **The same three looks in every body shape**: `rogue-hooded-<shape>`, `rogue-visor-<shape>`, `rogue-glitch-<shape>` for `chip`, `round`, `tall`, `drop`, `hex` and `ghost` (18 drawings; `rogue-hooded-chip` matches `rogue-hooded`).
- **Four swarms** (PNG 1200 px wide): `swarm-mixed` (all shapes and colours), `swarm-mixed-warm` (orange, yellow, coral only, so it still reads as "untrusted agents"), `swarm-with-rogues` (a few hooded, visor or glitch rogues hidden in the crowd), `swarm-rogue` (all rogue, in the same three styles).

Rebuild them with `python3 make_rogues_swarms.py` (it also exports their PNGs). The rogue parts (hood, visor, glowing eye, glitch, and the dropped lids, teeth, horns and spikes) are functions in that script.

## Changing them

`make_characters.py` draws everything. Each colour is a ramp of three hex values in `RAMPS` (body, shade, highlight); add a ramp or a shape function and run:

```bash
python3 make_characters.py
```

Then re-export the PNGs (uses headless Google Chrome):

```bash
python3 export_png.py
```

In the talk, colour carried meaning (orange = untrusted agent, sky blue = trusted monitor, pink = attack). If a new project uses roles the same way, keep one colour per role and vary shape and accessories within it.

## v2: black eyes, red attacks

`v2/` holds the same pack in the look the talk now uses: a black eye with a white centre, and red (`#FF3B5C`) for attacks (attack badge, attacking agent's eye, alert robot). Same names and folders (`v2/svg/…`, `v2/png/…`, `v2/index.html`, `v2/rogues-and-swarms.html`). The files at the top level keep the classic look (white eye, pink attacks) for later use.

Rebuild v2: `python3 make_characters.py v2 && python3 export_png.py v2 && python3 make_rogues_swarms.py v2`.
