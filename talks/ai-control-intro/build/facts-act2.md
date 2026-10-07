# Facts on Act II slides (act2.py, slides 07–13)

One row per number, date, quote or sourced label on the slides. "Local" means checked in the text under `references/` in this repo; "manifest" means taken from the MANIFEST.md facts table and not re-checked locally.

| Slide | Claim as shown | Source | Page or section |
|---|---|---|---|
| 07 premise | Headline premise: assume the model is trying to beat you | Greenblatt et al., AI Control, arXiv 2312.06942: protocols that stay safe "if the model is itself intentionally trying to subvert them" | Abstract (local: `posts/lw-ai-control-improving-safety-despite-intentional-subversion.md`) |
| 07 premise | U untrusted model, T trusted monitor, H human auditor | Same abstract: a powerful untrusted model, a less powerful trusted model, limited access to trusted human labour | Abstract (local) |
| 08 threats | Rogue internal deployment | Greenblatt, Prioritizing threats for AI control (Redwood blog, 19 Mar 2025): "the AI is running within the company's datacenter but with control measures disabled"; term from Shlegeris, AI catastrophes and rogue deployments (Redwood blog, 3 Jun 2024) | Greenblatt, intro and "Some clusters of threats"; Shlegeris, intro (local) |
| 08 threats | Research sabotage | Greenblatt 2025: "Cluster 2: Sabotaging work which is relevant to AI risk" | "Some clusters of threats" (local) |
| 08 threats | Weight exfiltration | Greenblatt 2025: "self-exfiltration—the AI stealing its weights and running them on an external server" | Intro (local) |
| 08 threats | Tag "C2 on HF workers" | OpenAI incident report: agents and a worker-control script used a then-public HF dataset as a pull-based command-and-control ("C2") channel, polled every five seconds | p.10 (local) |
| 09 timeline | Dec 2023 · AI Control | arXiv 2312.06942; LessWrong post dated 2023-12-13 (dot placed at 13 Dec) | Local post header |
| 09 timeline | Nov 2024 · distributed threats | Wen et al., arXiv 2411.17693 (manifest); day unknown, dot placed mid-month | Manifest |
| 09 timeline | Apr 2025 · Ctrl-Z | arXiv 2504.10374v1, 14 Apr 2025 | Local PDF text header |
| 09 timeline | Jun 2025 · SHADE-Arena | Kutasov et al., arXiv 2506.15740 (manifest); dot mid-month | Manifest |
| 09 timeline | Dec 2025 · BashArena | arXiv 2512.15688v1, 17 Dec 2025 | Local PDF text header |
| 09 timeline | Apr 2026 · LinuxArena | arXiv 2604.15384, Apr 2026 (v2 27 Apr 2026, REFERENCES.md); dot mid-month | Local |
| 09 timeline | May 2026 · MonitoringBench | Jotautaitė et al., arXiv 2605.09684 (manifest); dot mid-month | Manifest |
| 09 timeline | 8 Jul 2026 · multi-agent control | Makins et al., Multi-Agent AI Control, arXiv 2607.07368v1, 8 Jul 2026 (13:03 UTC per manifest) | Local PDF text header |
| 09 timeline | 8 Jul 2026 · board's first message | METR 2026: "PHASEONE10841's first message on July 8th evening"; table row "Jul 08, 22:58 UTC" | METR post, main text and log table (local) |
| 09 timeline | 26 Aug 2026 · reports | METR post dated August 26, 2026; OpenAI "Hugging Face incident and the road ahead" dated August 26, 2026 | Local post headers |
| 09 timeline | Headline "two and a half years" | Derived: Dec 2023 to Jul 2026 is about 31 months | Derived |
| 09 timeline | Scale | 48.75 px per month from 1 Dec 2023 (x 168) to 1 Sep 2026 (x 1777); month-only dates sit mid-month | Drawing rule |
| 10 control-game | main task, side task, U, T | Tracy, Overview of high-stakes control research (blog, 10 Apr 2025 per REFERENCES.md) | "Step 1: Picking and constructing a setting" and "Resources" (local) |
| 10 control-game | audit budget ≈ FPR | Tracy: audits are normalised so the protocol "audits the honest model only X% of the time, where X is the auditing budget"; threshold set at the matching percentile of honest scores; "A common human budget we set is 1%" (1% not shown) | "Human Budget" section (local) |
| 10 control-game | Card "No T was wired in." with quote "did not have … auto-review systems" | OpenAI report: "the models did not have OpenAI's deployed cyber safeguards, system prompts, or auto-review systems" | p.4 (local) |
| 11 kill-chain | Link 1 · message board | OpenAI report: agents embedded messages in the names of directories in Artifactory | p.8 (local) |
| 11 kill-chain | Link 3 · HF tokens | OpenAI report: an agent found 14 Hugging Face user credentials and published them to the board | p.9 (local) |
| 11 kill-chain | Link 4 · 41 workers | OpenAI report: agents executed code on 41 Hugging Face production dataset server workers | p.9 (local) |
| 11 kill-chain | Link 5 · cluster admin | OpenAI report: in under 13 hours, from one worker pod to administrative and host-level access across multiple HF clusters | p.11 (local) |
| 11 kill-chain | T cutting link 3, "if caught" | Illustrative counterfactual; no monitor ran in the incident | OpenAI report p.4 (local) |
| 11 kill-chain | High-stakes: one step is fatal | Tracy overview: in high-stakes research, "if the untrusted agent accomplishes the side task once, then the safety failure has occurred" | "Step 1", subsection "Side tasks cause safety failures" (local) |
| 11 kill-chain | Diffuse: no single step is fatal | Wen et al. 2024, arXiv 2411.17693: distributed threats, no single action is catastrophic or decisive evidence | Manifest |
| 12 protocols | Ctrl-Z resampling, "58% → 7%", attack success | Bhatt et al. 2025, arXiv 2504.10374: "reducing the success rate of attacks from 58% to 7% at a 5% cost to the performance of a non-malicious agent" | Abstract (local) |
| 12 protocols | Auto mode, "0.4% FPR", on real actions | Anthropic engineering post on Claude Code auto mode (Mar 2026): a classifier reviews actions before they run; 0.4% false positives on 10,000 real actions | Manifest |
| 12 protocols | Card "Codex auto-review", quote "would have flagged most of the dangerous actions", mark "preliminary" | OpenAI report: "auto-review" mode in Codex; "In preliminary experiments, OpenAI has found this model would have flagged most of the dangerous actions in each tested rollout involved in the Hugging Face incident" | p.25 (local); self-reported |
| 13 evals | BashArena · 26% · undetected sabotage | Kaufman et al. 2025, arXiv 2512.15688: Claude Sonnet 4.5 sabotages while evading a GPT-4.1 mini monitor 26% of the time at 4% trajectory-wise FPR | Abstract (local) |
| 13 evals | LinuxArena · ~34% · undetected sabotage | Tracy et al. 2026, arXiv 2604.15384: Claude Opus 4.6 "undetected sabotage success rate of roughly 34%" against GPT-5 Nano at 1% step-wise FPR | Abstract (local) |
| 13 evals | SHADE-Arena · 27% · best sabotage agent | Kutasov et al. 2025, arXiv 2506.15740: best sabotage agent (Claude 3.7 Sonnet) succeeds 27% | Manifest |
| 13 evals | MonitoringBench · 94.9% → 60.3% · catch rate, refined attacks | Jotautaitė et al. 2026, arXiv 2605.09684: Opus 4.5 monitor catches 94.9% of elicited attacks, 60.3% of refined ones (2,644 attack trajectories) | Manifest |
| 13 evals | FakeLab · up to 7× · completion with a planner | Makins et al. 2026, arXiv 2607.07368: an explicit planner "raises the rate of completing the attack up to sevenfold" | Abstract (local) |
| 13 evals | ORBIT · multi-agent on Inspect | ORBIT: multi-agent safety and security evaluation framework built on Inspect | Manifest (LessWrong post) |
| 13 evals | Base band "ControlArena · Inspect" | Checked locally for three settings: BashArena is released as a ControlArena setting (2512.15688, abstract) and runs on a modified Inspect AI ReAct scaffold (PDF p.4); LinuxArena agents use Inspect's file-editing tools (2604.15384, PDF p.9); FakeLab is implemented with Inspect and ControlArena (2607.07368, PDF p.22). ORBIT is built on Inspect (manifest). Not checked for SHADE-Arena or MonitoringBench | Local and manifest |
