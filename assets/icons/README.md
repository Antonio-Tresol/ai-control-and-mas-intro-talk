# Icon assets

The talk's icons as standalone assets to paste into any presentation. `index.html` shows them all.

| Folder | Contents |
|---|---|
| `png/on-dark/` | 22 icons, transparent PNG, longest side 512 px, for dark slides |
| `png/on-light/` | the same 22 with ink outlines, for white or light slides |
| `svg/on-dark/`, `svg/on-light/` | the same drawings as SVG (scale without blur) |
| `app-icon/` | a 512 × 512 icon (rounded square and round), PNG and SVG: an agent watched by the monitor robot |

The icons: the untrusted model U, an attacking agent, the trusted monitor T (lens), the absent monitor, the human auditor H, a swarm (plain and with attackers), a sandbox (closed and breached), the message board (unwatched with a dashed rim, and watched), task mazes (with side task, main task only, impossible), main-task and side-task flags, the suspicion meter with τ, a kill chain, a document, a server rack, and flagged versions of the document and rack.

The more cartoon-like agents in many colours and shapes, and the small monitor robot, are in `../characters/`.

Rebuild everything (needs Chrome, Chromium or Edge for the PNGs, found by `tools/headless.py`):

```bash
uv run make_icons.py
```

The drawings come from the deck's generator in `talks/ai-control-intro/build/glyphs.py`, so they match the slides exactly.

## v2: black eyes, red attacks

`v2/` holds the same 22 icons and the app icon in the look the talk now uses: agents with a black eye and a white centre, and red for everything attack-related (attack badge, side-task flag, kill-chain links). The top-level files keep the classic look. Rebuild with `uv run make_icons.py v2`.
