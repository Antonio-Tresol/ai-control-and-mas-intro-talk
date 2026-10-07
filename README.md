# AI control when agents find each other

Slides, drawing code, character art, sources and draft scripts for a 15-minute introduction to AI control and multi-agent systems, given in English and Spanish (*Control de IA cuando los agentes se encuentran*). The talk was prepared in the In-the-Wild AI Control project at [SPAR](https://sparai.org/projects/f26/rec8RybPH2kNV6qDa) (Fall 2026), mentored by Sree Sharvesh and Thao Pham.

The running example is the July 2026 OpenAI–Hugging Face incident, in which sandboxed agents found each other on an unsanctioned message board and attacked Hugging Face. The talk has four parts: the incident, a short tour of AI control, the multi-agent gap, and the project's LOC-Arena setting. An appendix (A1–A7) covers seven open research directions: white-box monitoring, agent monitors, scalable monitoring, multi-agent monitoring, spy agents, deals with AIs and automated red teaming. Each appendix slide has its own drawing and sources.

## What is here

| Path | Contents |
|---|---|
| `sources.bib` | Every source cited on the slides, main deck and appendix |
| `talks/ai-control-intro/slides/{en,es}/project/` | The decks as presented: `deck.json` (slide order and sections) and one `<section>` per slide in `slides/`, speaker notes in each slide's `<aside>` |
| `talks/ai-control-intro/slides/preview.py` | Renders a deck into one HTML page: `python3 preview.py en` |
| `talks/ai-control-intro/script/` | Draft talk scripts, English and Spanish (`[click]` / `[clic]` marks a build step) |
| `talks/ai-control-intro/build/` | The generator that drew the first version of the deck (`glyphs.py` holds every character and glyph, `gen.py` the slide helpers, `act*.py` the slides), plus `MANIFEST.md` and the facts tables used to check every number |
| `talks/ai-control-intro/*.py` | Later edits applied to the published decks: the appendix (`appendix.py`), the closing-slide QR codes (`closing_repo.py`), animated embeds and layout fixes |
| `talks/ai-control-intro/DESIGN.md` | Design system: palette, type scale, glyph recipes, slide archetypes and the accessibility checks |
| `assets/characters/`, `assets/icons/` | The character pack (one-eyed agents, the monitor robot, rogue agents and swarms) and the deck's icons, as SVG and PNG, with their generators |

The slides use the format of a Claude Slides artifact: a fixed 1920×1080 canvas, inline styles only, with the Outfit and JetBrains Mono fonts from Google Fonts.

## Rebuilding

`python3 talks/ai-control-intro/appendix.py <EN deck root> <ES deck root>` regenerates the eight appendix slides into decks laid out like `slides/en` and `slides/es`. The QR scripts need `segno` (`uv run --with segno python3 closing_repo.py …`). The decks were edited by hand after the first build, so `slides/` is the source of truth; rerunning `build/build_deck.py` produces the earlier version.

## Not included

- The Kurzgesagt video thumbnail and channel logo shown on slide 6 belong to Kurzgesagt – In a Nutshell. The slides reference them as uploaded files (`/_blob/…`), so they appear as empty boxes in a local preview. The visual style is inspired by their video on the incident; all characters and drawings here are original.
- Copies of the papers and posts. `sources.bib` links to each one.

## Licence

Code is under the MIT licence (`LICENSE`). Slides, drawings, character art and scripts are under CC BY 4.0 (`LICENSE-CONTENT.md`).
