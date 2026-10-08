# AI control when agents find each other

<p align="center">
  <a href="https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/"><img src="docs/images/slides/cover-en.jpg" width="100%" alt="Cover slide: AI control when agents find each other. One-eyed agents in many colours and shapes mill around a hexagonal message board while a single monitor on a stand watches one of them."></a>
</p>

<p align="center"><b><a href="https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/">View the slides</a></b> · <a href="https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/es/">Ver en español</a></p>

Slides, drawing code, character art, sources and draft scripts for a 15-minute introduction to AI control and multi-agent systems, given in English and Spanish (*Control de IA cuando los agentes se encuentran*). The talk was prepared in the In-the-Wild AI Control project at [SPAR](https://sparai.org/projects/f26/rec8RybPH2kNV6qDa) (Fall 2026), mentored by Sree Sharvesh and Thao Pham.

The running example is the July 2026 OpenAI–Hugging Face incident, in which sandboxed agents found each other on an unsanctioned message board and attacked Hugging Face. The talk has four parts: the incident, a short tour of AI control, the multi-agent gap, and the project's LOC-Arena setting. An appendix (A1–A7) covers seven open research directions: white-box monitoring, agent monitors, scalable monitoring, multi-agent monitoring, spy agents, deals with AIs and automated red teaming. Each appendix slide has its own drawing and sources.

## The slides

<p align="center">
  <img src="docs/images/slides/04-incident-map.jpg" width="49%" alt="Slide 4, Sandboxed agents found each other, then broke into Hugging Face: about 1,200 agents in the OpenAI evaluation reach a message board, the internet, Hugging Face tokens, 41 workers and cluster admin in under 13 hours.">
  <img src="docs/images/slides/07-premise.jpg" width="49%" alt="Slide 7, Assume the model is trying to beat you, and get useful work anyway: a protocol in which a human auditor H and a trusted monitor T watch an untrusted model U do useful work.">
  <img src="docs/images/slides/11-kill-chain.jpg" width="49%" alt="Slide 11, Attacks are chains; one caught link is enough: the incident's five steps drawn as chain links, with a monitor catching link 3, and high-stakes versus diffuse threats below.">
  <img src="docs/images/slides/15-swarms.jpg" width="49%" alt="Slide 15, Swarms break monitors built to watch one agent at a time: too many trajectories, fragments that stay under the threshold, permissions that pool up, and speed that outruns review.">
  <img src="docs/images/slides/18-loc-arena.jpg" width="49%" alt="Slide 18, LOC-Arena: a fake AI lab where agents may attempt a rogue deployment, with sub-agents, seven repositories, sync and async monitors and a sealed verifier that measures the gap between caught and happened.">
  <img src="docs/images/slides/24-app-scalable.jpg" width="49%" alt="Appendix slide A3, How do you watch a thousand agents without stalling them: a cheap filter, a costly monitor and a human audit in a funnel, with auto mode false positives falling from 8.5% to 0.4%.">
</p>

The [website](https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/) shows each deck full screen with its build steps: → or Space moves forward, ← back, G shows all slides, N the speaker notes and sources, F full screen. A link like [`#11`](https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/#11) opens one slide. All 28 slides on one page: [English](docs/images/slides/deck-en.jpg) · [Español](docs/images/slides/deck-es.jpg).

## Characters and icons

Every drawing in the talk is original and free to reuse under CC BY 4.0: one-eyed agents in six shapes and ten colours, attacking and rogue agents, the monitor robot, swarms, and the icons for the control setting (U, T, H, the message board, the kill chain, the suspicion meter).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/characters-dark.png">
  <img src="docs/images/characters-light.png" width="100%" alt="Character lineup: six one-eyed agents (chip, round, tall, drop, hex and ghost shapes), an attacking agent with a red eye and an attack badge, a hooded rogue, a glitching rogue and the monitor robot.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/icons-dark.png">
  <img src="docs/images/icons-light.png" width="100%" alt="Icon set: the untrusted model U, the trusted monitor T, the human auditor H, the watched message board, a kill chain, the suspicion meter, a breached sandbox and a swarm with attackers.">
</picture>

Each drawing comes as SVG and as a 512 px PNG, in an on-dark version and an outlined on-light version. The `v2/` folders hold the look the decks use (black eye, red for attacks). The packs are documented in [`assets/characters/`](assets/characters/README.md) and [`assets/icons/`](assets/icons/README.md).

## What is here

| Path | Contents |
|---|---|
| `sources.bib` | Every source cited on the slides, main deck and appendix |
| `talks/ai-control-intro/slides/{en,es}/project/` | The decks as presented: `deck.json` (slide order and sections) and one `<section>` per slide in `slides/`, speaker notes in each slide's `<aside>` |
| `talks/ai-control-intro/slides/preview.py` | Renders a deck into one HTML page (see [Previewing](#previewing)) |
| `talks/ai-control-intro/slides/build_site.py` | Builds the website: a full-screen viewer per language, deployed by `.github/workflows/pages.yml` on every push to `main` |
| `talks/ai-control-intro/script/` | Draft talk scripts, English and Spanish (`[click]` / `[clic]` marks a build step) |
| `talks/ai-control-intro/build/` | The generator that drew the first version of the deck (`glyphs.py` holds every character and glyph, `gen.py` the slide helpers, `act*.py` the slides), plus `MANIFEST.md` and the facts tables used to check every number |
| `talks/ai-control-intro/*.py` | Later edits applied to the published decks: the appendix (`appendix.py`), the closing-slide QR codes (`closing_repo.py`), animated embeds (`cover_embed.py`), the v2 look (`v2_transform.py`) and layout fixes |
| `talks/ai-control-intro/DESIGN.md` | Design system: palette, type scale, glyph recipes, slide archetypes and the accessibility checks |
| `talks/ai-control-intro/design-research.md` | The evidence behind the design choices (multimedia learning, projection constraints, an expert audience, turning content into drawings), with references |
| `talks/ai-control-intro/specimen.html` | The first build of the deck, written by `build/gen.py` |
| `talks/ai-control-intro/es/GLOSARIO.md` | Terms and style rules for the Spanish version |
| `assets/characters/`, `assets/icons/` | The character pack and the deck's icons, as SVG and PNG, with their generators |
| `tools/headless.py` | Finds headless Chrome, Chromium or Edge on any OS and takes screenshots, for `screenshots.py` and the asset generators |
| `docs/images/` | The images in this README |

The slides use the format of a Claude Slides artifact: a fixed 1920×1080 canvas, inline styles only, with the Outfit and JetBrains Mono fonts from Google Fonts.

## Previewing

```bash
cd talks/ai-control-intro/slides
python3 preview.py en
```

Open `preview-en.html` in a browser; `preview-en.html?solo=N` shows slide N alone at 1920×1080.

To save slides as PNGs, as for the images in this README:

```bash
python3 screenshots.py en          # every slide
python3 screenshots.py es 1 4 7    # only these slides
```

The PNGs land in `screenshots/`. The script finds Chrome, Chromium or Edge on macOS, Linux or Windows; if it finds none, set `CHROME` to the browser's path. The asset generators in `assets/` use the same helper, `tools/headless.py`.

To build the website and serve it locally at <http://localhost:8000/>:

```bash
python3 build_site.py _site
python3 -m http.server --directory _site 8000
```

## Rebuilding

`python3 talks/ai-control-intro/appendix.py <EN deck root> <ES deck root>` regenerates the eight appendix slides into decks laid out like `slides/en` and `slides/es`. The QR scripts need `segno` (`uv run --with segno python3 closing_repo.py …`). The decks were edited by hand after the first build, so `slides/` is the source of truth; rerunning `build/build_deck.py` produces the earlier version. The appendix slides were also adjusted by hand after `appendix.py` last ran, and rerunning it overwrites those adjustments.

## Not included

- The Kurzgesagt video thumbnail and channel logo shown on slide 6 belong to Kurzgesagt – In a Nutshell. The slides reference them as uploaded files (`/_blob/…`), so they appear as empty boxes in a local preview. The visual style is inspired by their video on the incident; all characters and drawings here are original.
- Copies of the papers and posts. `sources.bib` links to each one.

## Licence

Code is under the MIT licence (`LICENSE`). Slides, drawings, character art and scripts are under CC BY 4.0 (`LICENSE-CONTENT.md`).
