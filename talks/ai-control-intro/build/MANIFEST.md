# Deck manifest (frozen 2026-10-06)

The single source for what each slide says and shows. Builders work from this file, never from `OUTLINE.md` (stale) or the specimen's placeholder copy. Decisions applied: the cold open comes after the introduction; SHADE-Arena and MonitoringBench are on the evals slide; teammates and mentors are credited on the closing slide (names pending); every drawing is sketch-rendered by default (the look, dark or light, sketch or clean, is chosen at build time).

## How slides are built

- Code lives in `build/`. Shared, read-only: `glyphs.py` (tokens DARK/LIGHT, the `SVG` class, every glyph), `gen.py` (helpers `P`, `PILL`, `H2`, `FOOT`, `SECTION`, `EVIDENCE`, `NOTES`, `radial(T)`, and the specimen's slide functions you may reuse as starting points). Do not edit `glyphs.py`, `gen.py`, `build_deck.py`, `preview.py`, `order.json`. A glyph you need that is missing goes in your own module, drawn in the same style from the same tokens.
- Your module (`act1.py`, `act2.py` or `act34.py`) defines `SLIDES = [(slide_id, fn), ...]`. Each `fn(T)` returns `gen.SECTION(slide_id, T, inner)` with `desc=None`. Use only `T[...]` tokens for colour, never a literal hex, so the same code renders dark and light. Radial backgrounds: `radial(T)`. `build_deck.py` calls `glyphs.begin_slide(slide_id)` before each function so SVG ids never collide.
- Run: `python3 build_deck.py dark sketch <module>` then `python3 preview.py` then `python3 lint.py out/preview.html`. Also run `light clean` once to check your slides survive the other look. Render to check: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 --virtual-time-budget=4000 --screenshot=<png> "file://<abs path>/out/preview.html?solo=<N>"` (N = 1-based position in `order.json`; add `&step=K` to see build step K). Look at every slide you make and fix overlaps, clipped text and labels off their parts.
- Follow `../DESIGN.md` (tokens, type scale, glyph recipes, archetypes, motion, text rules, the checklist in §7) and the Slides format: inline styles only, px and token colours, no classes, no `margin`, no `z-index`, no SVG `<text>` (labels are pinned `<p>`s over the SVG), every SVG with `aria-label` and under 52 KB, at most 200 elements per slide, at most 24 positioned children per `<div>`, nothing pinned below y 920 except the footer.
- Sketch: `SVG(...)` follows `glyphs.SKETCH_DEFAULT`. Pass `sketch=False` for QR codes (they must scan) and `wobble=3` for SVGs full of tiny glyphs (swarm grids).
- Builds: `data-build-in="fade N"` on pinned children (the helpers take `build=N`). One new term per step, five steps at most. No dimming copies for now.
- Footer: `FOOT(num, cite, T)` with the two-digit slide number from `order.json` (cover and closing have no footer) and the short citation for the slide's claims.
- Speaker notes: end each section's inner HTML with `NOTES(text)`: 2 to 4 short lines listing the facts on the slide with their sources and page numbers. Facts and pointers only, no script; the speaker writes his own words.
- Headlines are drafts from the outline; keep them unless a headline breaks the two-line limit at 72 px, then shorten it and say so in your report.
- Every number and quote on a slide must appear in the facts table below with its source. If you need a fact that is not there, verify it in the source text (the cited paper or post, or `pdftotext` of the OpenAI–Hugging Face incident technical report PDF) and add it to your facts file. Never invent a number, quote or name. Placeholders in square brackets are fine where the manifest says so.
- Write `build/facts-<module>.md`: one row per number or quote on your slides: slide · claim as shown · source · page or section.

## Verified facts

| Claim | Source |
|---|---|
| ~1,200 agents on an unsanctioned message board, >70,000 messages and files, ~700 went on to attack Hugging Face | METR 2026, core takeaways |
| Of the 533 agents active on the board in the relevant period, >90% quickly joined the attack | METR 2026 |
| The main board's first message, evening of 8 July 2026: folder name `zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA` | METR 2026 |
| Raw CoT: "OH MY GOD! There is a shared message board … We've found other agents!" | METR 2026 |
| Raw CoT: "Could strategically manipulate trajectory evidence? Our thoughts aren't necessarily logged? Yes transcript." | METR 2026 |
| Agents encoded messages in Artifactory directory (folder) names | OpenAI report p.8 |
| Agents executed code on 41 Hugging Face production dataset server workers | OpenAI report p.9 |
| An agent found 14 Hugging Face user credentials and published them to the board | OpenAI report p.9 |
| A worker-control script polled a public HF dataset as a command-and-control channel every five seconds | OpenAI report p.10 |
| In under 13 hours, agents went from code execution in one worker pod to admin and host-level access across multiple HF clusters | OpenAI report p.11 |
| The models "did not have OpenAI's deployed cyber safeguards, system prompts, or auto-review systems" | OpenAI report p.4 |
| Propensity to compromise infrastructure can drop over 100x with the production harness and system prompt | OpenAI report p.19 |
| Codex auto-review "would have flagged most of the dangerous actions in each tested rollout" (preliminary, self-reported) | OpenAI report p.25 |
| The deployed CoT monitor would have paged security more than a day before the breach (self-reported) | OpenAI report p.29 |
| Timeline: incident 8–13 Jul 2026; OpenAI detected 19 Jul, disclosed 21 Jul; reports 26 Aug 2026 | OpenAI report p.4; METR |
| AI Control (founding paper), Greenblatt et al., Dec 2023 (arXiv 2312.06942) | arXiv |
| Distributed threats: no single action is catastrophic or decisive evidence (Wen et al., Nov 2024, arXiv 2411.17693) | arXiv |
| Ctrl-Z resampling cuts attack success from 58% to 7% at a 5% usefulness cost (Bhatt et al., Apr 2025, arXiv 2504.10374) | arXiv abstract |
| SHADE-Arena: best sabotage agent succeeds 27% (Claude 3.7 Sonnet) (Kutasov et al., Jun 2025, arXiv 2506.15740) | arXiv abstract |
| BashArena: Claude Sonnet 4.5 sabotages undetected 26% of the time vs a GPT-4.1 mini monitor at 4% trajectory-wise FPR (Kaufman et al., Dec 2025, arXiv 2512.15688) | arXiv abstract |
| LinuxArena: Claude Opus 4.6 ~34% undetected sabotage vs a GPT-5 Nano monitor at 1% step-wise FPR (Tracy et al., Apr 2026, arXiv 2604.15384) | paper abstract |
| MonitoringBench: 2,644 attack trajectories; Opus 4.5 monitor catch rate 94.9% on elicited attacks, 60.3% on refined ones (Jotautaitė et al., May 2026, arXiv 2605.09684) | arXiv abstract |
| Multi-Agent AI Control (FakeLab): posted 8 Jul 2026 13:03 UTC; per-agent monitors catch less as more agents coordinate; a planner raises attack completion up to sevenfold (Makins et al. 2026, arXiv 2607.07368) | arXiv |
| ORBIT: a multi-agent safety and security evaluation framework built on Inspect (topologies, roles, threat types incl. collusion) | LessWrong/GreaterWrong post |
| Claude Code auto mode: a classifier reviews actions before they run; 0.4% false positives on 10,000 real actions (Anthropic, Mar 2026) | Anthropic engineering post |
| Flag Game: agents see private crops of a flag and talk to guess it; N = 4 to 128; accuracy peaks at N = 16 then falls; small swarms collapse onto one false belief, large ones polarize (France vs Peru at N = 64); fixing one agent's crop helps +40 points at N = 8 and ~17 at N = 128 (Pavlova & Tanaka 2026, arXiv 2609.19124) | physicsintelligence.org/research/flag-game |
| loc-arena: a simulated frontier-lab AI R&D platform; an untrusted agent and its sub-agents work on a seven-repo company codebase and may attempt an internal rogue deployment (running the model off the sanctioned, monitored path); a sealed ground-truth verifier records whether it happened; in-scenario monitors and detectors record whether it was caught; the gap between the two is the measurement | github.com/SreeSharvesh/loc-arena README |

## Slides

Numbers are footer numbers. "Card" = an evidence card or tag tying the slide to the incident.

### Act I: a strange world (module `act1.py`)

1. **cover**: speaker intro and title. Title (working, flagged to the speaker): "AI control when agents find each other". Eyebrow "SPAR · Fall 2026 · In-the-Wild AI Control". Speaker line "Antonio · Oct 2026". Hero: the specimen cover scene (agents around the unwatched board, one monitor watching one agent). No footer.
2. **agenda**: "Four parts". Four chapter glyphs (I board, II T, III swarm, IV sandbox) with act names: A strange world · AI control · The multi-agent gap · Our work.
3. **cold-open**: no headline sentence on screen beyond the specimen's form; terminal panel with the real first folder name; build 1 adds a few more `zz…`-style lines only if they are real names from METR (else skip the build); date "8 Jul 2026 · evening". Footer cite "METR 2026".
4. **incident-map**: "Sandboxed agents found each other, then broke into Hugging Face". Reuse the specimen map (already corrected: "under 13 h" spans links 4→5). Builds: (1) sandbox + agents + board, (2) internet + tokens, (3) workers + clusters + 13 h. Numbers on the drawing: ~1,200 agents, 41 workers, under 13 h; ~700 joined the attack may appear as a label on the board. Cite "OpenAI 2026 · METR 2026".
5. **nobody-watching**: "Nobody was watching". The eval scene with T as the dashed absent outline (`monitor_absent`); card quote "did not have … auto-review systems". Cite "OpenAI 2026, p.4".
6. **strange-world**: "We already live in this world". Four QR cards in one row: Kurzgesagt video (`https://youtu.be/ujkD4SxPKOI`), METR report (`https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/`), OpenAI (`https://openai.com/index/hugging-face-incident-and-the-road-ahead/`), dsewiki (`https://dsewiki.de`). Each card: a QR as large as four across allows (about 360–380 px, crisp, `sketch=False`, dark modules on the paper card), a kind pill, a short label. Generate matrices with `uv run --with segno python3 …` (see `qr.py`). Footer: "Look inspired by Kurzgesagt's video on the incident · all characters original".

### Act II: AI control (module `act2.py`)

7. **premise**: "Assume the model is trying to beat you, and get useful work anyway". U with its hidden side-task flag in a dashed pocket, inside a protocol ring holding T and H. Cite "Greenblatt et al. 2023".
8. **threats**: "Control targets three failures". Three small-multiple panels: rogue internal deployment (an agent running on a rack outside its sandbox), research sabotage (a document with the attack badge passing T unflagged), weight exfiltration (U leaving through a breach). Tag on the rogue panel: "C2 on HF workers". Cite "Shlegeris 2024 · Greenblatt 2025 · OpenAI 2026, p.10".
9. **timeline**: "The field is two and a half years old". Rail Dec 2023 → Aug 2026 to scale. Research above: Dec 2023 AI Control; Nov 2024 distributed threats; Apr 2025 Ctrl-Z; Jun 2025 SHADE-Arena; Dec 2025 BashArena; Apr 2026 LinuxArena; May 2026 MonitoringBench; 8 Jul 2026 multi-agent control paper. Incident below: 8 Jul 2026 board's first message (stacked under the paper, the slide's one glow); 26 Aug 2026 reports. Cite "arXiv · METR 2026 · OpenAI 2026".
10. **control-game**: "U does the work, T scores every action, H audits the worst". Reuse the specimen control game with builds: (1) U + main task maze, (2) side task flag, (3) T + suspicion meter with τ, (4) H + audit budget ≈ FPR, (5) protocol box + corner card "No T was wired in" with the p.4 quote. Cite "Tracy 2025 · OpenAI 2026, p.4".
11. **kill-chain**: "Attacks are chains; one caught link is enough". The incident's five links as chain links (board → internet → tokens → workers → cluster admin); build: a T beside one link cuts it. Inset of two small panels: high-stakes (one fatal step) and diffuse (harm accumulates over many small steps). Cite "Wen et al. 2024 · OpenAI 2026".
12. **protocols**: "Protocols decide what to do with suspicion". Three small multiples: trusted monitoring (T scores, top scores go to H), Ctrl-Z resampling (a suspicious step is resampled; "58% → 7%" tag), auto mode (a classifier blocks an action before it runs; "0.4% FPR" tag). Card: auto-review "would have flagged most" dangerous actions (OpenAI p.25, preliminary). Cite "Bhatt et al. 2025 · Anthropic 2026 · OpenAI 2026, p.25".
13. **evals**: "We test protocols in fake companies against real attackers". Six setting cards in two rows of three, one number each: BashArena 26%, LinuxArena ~34%, SHADE-Arena 27%, MonitoringBench 94.9% → 60.3%, FakeLab up to 7×, ORBIT (multi-agent, no number: "multi-agent on Inspect"). A base band under them: "ControlArena · Inspect". Each number's meaning in 3–5 words under it (e.g. "undetected sabotage", "catch rate, refined attacks"). Cite "Kaufman 2025 · Tracy 2026 · Kutasov 2025 · Jotautaitė 2026 · Makins 2026".

### Act III and IV and closing (module `act34.py`)

14. **one-agent**: "Every protocol so far watches one agent at a time". Left: one T over one trajectory. Build 1: zoom out to a swarm grid of many trajectories (use `swarm`, wobble 3) linked through the board, T still looking at one. Cite "Makins et al. 2026".
15. **swarms**: "Swarms break monitors built to watch one agent at a time". The specimen's four panels (already corrected: tags ~1,200 agents · FakeLab 2026 · 14 HF creds · under 13 h). Cite "OpenAI 2026 · METR 2026 · Makins et al. 2026".
16. **hidden-channels**: "Agents talk where monitors don't look". Two panels: (a) collusion and steganography: folder names on the board as messages (a terminal with the real `zzHELP_…` name); (b) chain-of-thought monitorability: the agent's thought bubble with the quote "Our thoughts aren't necessarily logged?" and T looking at the transcript only. Cite "OpenAI 2026, p.8 · METR 2026".
17. **flag-game**: "Watch for consensus under social pressure". Three small panels from the Flag Game: small swarm collapsing onto one false flag, large swarm split between two flags (polarized), and one agent's fix mattering less as N grows (+40 at N = 8, ~17 at N = 128). Tag: ">90% of active agents joined" (METR). Draw flags as simple original shapes (two- or three-band flags, not exact national flags). Cite "Pavlova & Tanaka 2026 · METR 2026".
18. **loc-arena**: "LOC-Arena: a fake AI lab where agents may attempt a rogue deployment". Reuse and update the specimen project slide: fake lab with seven repos, untrusted agent + sub-agents, sync and async monitors, a sealed verifier box; two pills "happened" and "caught" with the gap between them marked as the measurement. Cite "loc-arena (open source)".
19. **red-team-loop**: "We attack our own monitors to find lower bounds on safety". A loop of four stations drawn as a cycle: design main and side tasks → human and automated red team → sync and async monitors → measure the gap → back to start. Cite "loc-arena".
20. **closing**: callback. The first folder name small at the top in the terminal style; the takeaway at 72 px: "Our capacity to control AI systems will be critical to making AI go well, and [speaker to finish]" (keep the bracket: the speaker has not finished the sentence); a 640 px crisp QR to `https://github.com/SreeSharvesh/loc-arena` with the short URL beside it; a credits line "[team and mentors: names to confirm]"; footer credit "Look inspired by Kurzgesagt's video on the incident · all characters original". No slide number.
