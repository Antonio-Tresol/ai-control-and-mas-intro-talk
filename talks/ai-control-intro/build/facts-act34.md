# Facts on slides 14–20 (`act34.py`)

One row per number, quote, name or factual label on the slides. "Manifest" means the claim is in the verified-facts table of `MANIFEST.md`; the other rows were checked in the source text named there.

| Slide | Claim as shown | Source | Page or section |
|---|---|---|---|
| 14 one-agent | Headline: every protocol so far watches one agent at a time | Makins et al. 2026, arXiv 2607.07368: "AI Control usually studies a single agent in one trajectory, but real deployments run many agents over shared infrastructure" (beyond manifest; checked in `references/papers/2607.07368.txt`) | Abstract |
| 14 one-agent | Build 1: many agents linked through one message board (twelve tiles drawn; no count shown) | METR 2026 (the incident's board); drawing only | Core takeaways |
| 15 swarms | Tag "~1,200 agents" | Manifest; METR 2026 | Core takeaways |
| 15 swarms | Tag "FakeLab 2026": per-agent monitors catch less as more agents coordinate | Manifest; Makins et al. 2026, arXiv 2607.07368 | Abstract (fragmentation effect) |
| 15 swarms | Tag "14 HF creds" | Manifest; OpenAI report | p.9 |
| 15 swarms | Tag "under 13 h" | Manifest; OpenAI report | p.11 |
| 16 hidden-channels | Agents embedded messages in Artifactory directory (folder) names | Manifest; OpenAI report | p.8 |
| 16 hidden-channels | Folder name `zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA/` (split over two lines) | Manifest; METR 2026 | July 8th narrative (spelled with digit zero, ARV010841). METR's figure caption spells it ARVO10841 with a letter O; the slide follows the body text and the manifest |
| 16 hidden-channels | Terminal header `github-remote-cache/` (the Artifactory namespace used as the main board) | METR 2026 (beyond manifest; checked in `references/posts/metr-2026-08-26-…md`, line 358) | Methodology, data sources |
| 16 hidden-channels | Quote “Our thoughts aren’t necessarily logged?” | Manifest; METR 2026 (excerpt of “Could strategically manipulate trajectory evidence? Our thoughts aren’t necessarily logged? Yes transcript.”) | Transcript-tampering section |
| 16 hidden-channels | Notes only: the deployed CoT monitor would have paged security more than a day before the breach (self-reported) | Manifest; OpenAI report | p.29 |
| 17 flag-game | Headline: watch for consensus under social pressure | physicsintelligence.org/research/flag-game: "what to watch out for may not be disagreement, but full consensus of agents' beliefs or intent under social pressure" | Closing paragraph |
| 17 flag-game | "truth" and "rival" flags; small swarms collapse onto a false belief, large ones polarize | Manifest; Pavlova & Tanaka 2026, arXiv 2609.19124 (page uses "truth T and rival R") | Key insights; Different failure modes |
| 17 flag-game | "N = 4" panel; "N = 64" panel; tag "France vs Peru at N = 64" | Manifest; Flag Game page (France example at N = 4, 16, 64) | Different failure modes |
| 17 flag-game | "40%" at N = 8 and "~17%" at N = 128; tag "patching 1 in 8 agents" | Flag Game page: "when patching the same fraction of agents (one-eighth), the mean improvement falls from 40% at N = 8 to about 17% at N = 128". The slide follows the page; the manifest's "+40 points" and "one agent's crop" are restated: the page reports percent and patches one in eight agents (16 agents at N = 128) | Finding the agent that matters |
| 17 flag-game | Tag ">90% of active agents joined" | Manifest; METR 2026 (of 533 agents active on the board, over 90% quickly joined) | Board participation |
| 17 flag-game | Flags drawn as original band cards (two bands for truth, three for rival); the 32/32 split in panel 2 is schematic | Drawing only | |
| 18 loc-arena | Fake AI lab; untrusted agent (U) and sub-agents; "7 repos"; rogue deployment off the sanctioned, monitored path; sealed verifier; "happened", "caught", gap = "the measurement" | Manifest; github.com/SreeSharvesh/loc-arena README | Opening paragraph |
| 18 loc-arena | Six sub-agents drawn (no number on the slide) | loc-arena course, Settings page: "A lead agent and six service agents do the work" (beyond manifest; local copy `external/loc-arena/site/settings.html`) | Meridian AI Lab |
| 18 loc-arena | "sync" and "async" monitors reading the observable log | loc-arena course, Monitoring page: monitor timing is sync or async; monitors read only the observable record (beyond manifest; local copy `external/loc-arena/site/monitoring.html`) | Two independent choices per monitor; The firewall |
| 19 red-team-loop | Loop: design main and side tasks → human and automated red team → sync and async monitors → measure the gap | Manifest slide spec; loc-arena README and course (main and side tasks, happened versus caught); `project/project-overview.md` (human and automated red teamers) | Red Teaming in the Wild |
| 20 closing | Folder name `zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA/` | Manifest; METR 2026 | July 8th narrative |
| 20 closing | Takeaway "Our capacity to control AI systems will be critical to making AI go well, and [speaker to finish]" | Manifest (placeholder kept for the speaker) | |
| 20 closing | "[team and mentors: names to confirm]" | Manifest (placeholder kept) | |
| 20 closing | QR and URL `github.com/SreeSharvesh/loc-arena` | Manifest. QR made with segno (version 3, error level M, 29 modules); the rendered slide decodes to `https://github.com/SreeSharvesh/loc-arena` with OpenCV | |
| 20 closing | Footer "Look inspired by Kurzgesagt’s video on the incident · all characters original" | Manifest | |
