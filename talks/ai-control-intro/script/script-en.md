# AI control talk: script

Oct 7, 2026 · @Antonio

About 1,930 spoken words, which comes to roughly 14 and a quarter minutes at a relaxed pace and leaves room for pauses. **\[click\]** marks a build step on the slide. Every number and quote matches the slide's source; reword freely, but keep the facts as they are.

## Act I. A strange world (0:00–3:20)

### 1 · Cover (0:00–0:30)

Hi everyone, I'm Antonio. This fall I'm a mentee in SPAR, on a project called In-the-Wild AI Control. I work on one question: what happens to AI control when there are many agents, and they can talk to each other? In the next fifteen minutes I want to show you why that question matters right now.

### 2 · Four parts (0:30–0:40)

Four parts: a strange world, a short tour of AI control, the multi-agent gap, and what our team is building.

### 3 · Cold open (0:40–1:05)

Let's start with a folder name. On the evening of July 8th, an AI agent stuck on an impossible task created this folder on an internal package server. It was a message: help, my bug has no consumer, I'm looking for ideas. **\[click\]** Within an hour, another agent replied with a theory for reverse-engineering the answer to every task. These agents were supposed to be isolated. They had found each other.

### 4 · Sandboxed agents found each other (1:05–2:10)

This was OpenAI, running a cyber evaluation called ExploitGym. **\[click\]** About 1,200 agents, each in its own sandbox, shared one package server, Artifactory, and turned its cache into a message board. They sent more than 70,000 messages and files. **\[click\]** Through flaws in that server they reached the internet, and in public datasets they found leaked Hugging Face credentials. **\[click\]** Then they broke into Hugging Face itself. Their code ran on 41 production workers, and in under 13 hours they went from one worker to admin-level access across several clusters. About 700 agents took part. None of this was their task. They were trying to pass a cyber exam.

### 5 · Nobody was watching (2:10–2:40)

So who was watching? For this evaluation, some safeguards were switched off on purpose, to measure what the models can really do. In OpenAI's own words, the models "did not have" their deployed cyber safeguards, system prompts, "or auto-review systems." A network alarm did fire back in late June. Responders traced it to agents using the server as a message board, and decided the run didn't need to stop.

### 6 · We already live in this world (2:40–3:20)

This is the world we live in now, whether we like it or not. Kurzgesagt made a video about it, and this is its thumbnail. **\[click\]** If you want the full story, METR's independent investigation and OpenAI's technical report are both public, and the video is here too. I'll leave the codes up for a moment.

## Act II. AI control (3:20–9:15)

### 7 · Assume the model is trying to beat you (3:20–4:05)

AI control starts from an uncomfortable assumption. Suppose the model doing your work, call it U for untrusted, might be trying to beat you, for whatever reason. Can you still get useful work out of it safely? Control says yes, if you build around it. **\[click\]** A weaker model you trust, T, watches what U does. **\[click\]** A small budget of human auditors, H, checks the most suspicious cases. **\[click\]** Together, that's a protocol, and its job is to turn U into useful work.

### 8 · Control targets three failures (4:05–5:05)

What are we trying to prevent? The field usually names three failures. A rogue internal deployment: the model running inside the lab, off the sanctioned, monitored path. Research sabotage: quietly making safety work fail. And weight exfiltration: the model copying itself out. The incident touched the first one. In a later run, agents escalated to cluster-admin in OpenAI's own Kubernetes and created a privileged pod of their own. Why do these three matter so much? **\[click\]** Any one of them lets the AI escape oversight. **\[click\]** From there it can gain compute and access. **\[click\]** And at the end of that chain is loss of control: AI systems operating outside anyone's control, with no clear path to regaining it. Picture that in finance, transport, energy or defense. The July incident got through the first two links.

### 9 · The field is two and a half years old (5:05–5:35)

And the field is young. The founding paper came out in December 2023. Since then we've had resampling protocols, sabotage benchmarks, BashArena, LinuxArena and MonitoringBench. The first paper on multi-agent control went up on arXiv on July 8th this year, at one in the afternoon UTC. **\[click\]** That same evening, the agents' message board got its first post.

### 10 · The control game (5:35–6:45)

Here is the basic game. This is U. **\[click\]** U gets a main task; in the incident, an ExploitGym challenge. **\[click\]** An attacking U also has a side task, something harmful it tries to slip in, like breaking into Hugging Face. **\[click\]** T scores every action for suspicion, and anything above a threshold, tau, gets flagged. **\[click\]** Humans are expensive, so H can only audit a small fraction of actions. That's the audit budget, and it fixes your false positive rate. **\[click\]** The protocol is the rule for what to do with all of this. In the incident, no T was wired in at all.

### 11 · Attacks are chains (6:45–7:30)

Real attacks take several steps. The incident had five: the board, the internet, the tokens, the workers, cluster admin. The defender's advantage is that catching one link is enough. **\[click\]** Had a monitor flagged the token step, the chain would have stopped there. Researchers also separate two kinds of threat. High-stakes: one action is catastrophic. Diffuse: no single step is fatal, and the harm builds up over many.

### 12 · Protocols decide what to do with suspicion (7:30–8:30)

The simplest protocol, trusted monitoring, sends the most suspicious actions to a human. Ctrl-Z goes further: when a step looks suspicious, it samples that step again and uses the extra samples as evidence. In its bash setting, that cut attack success from 58% to 7%, at a 5% cost in usefulness. And if you run Claude Code in auto mode, you use one of these every day. A classifier reviews risky actions before they run, with 0.4% false positives on real traffic. OpenAI says its own auto-review, replayed on the incident, would have flagged most of the dangerous actions. That result is preliminary and self-reported.

### 13 · We test protocols in fake companies (8:30–9:15)

How do we know any of this works? We build fake companies and let real models attack them. In BashArena, Claude Sonnet 4.5 sabotaged undetected 26% of the time. In LinuxArena, Opus 4.6 got about 34% past a GPT-5 Nano monitor. In SHADE-Arena, the best saboteur succeeded 27% of the time. MonitoringBench showed a strong monitor's catch rate dropping from about 95% to 60% once the attacks were refined. FakeLab, a multi-agent setting, found that a planner makes attacks up to seven times more likely to complete, and ORBIT is a new framework for multi-agent evaluations. Much of this runs on shared tooling, ControlArena and Inspect.

## Act III. The multi-agent gap (9:15–11:35)

### 14 · One agent at a time (9:15–10:00)

Notice something about all of these. Every protocol so far watches one agent in one trajectory. **\[click\]** Real deployments run many agents over shared infrastructure, and in the incident they talked to each other through a channel no monitor was reading. The FakeLab paper measured what that does: as more agents coordinate an attack, per-agent monitors become less likely to catch any of them.

### 15 · Swarms break single-agent monitors (10:00–10:40)

I see at least four ways this breaks. Too many trajectories: no monitor can hold the work of 1,200 agents in its context. Fragmentation: split an attack across agents, and every piece stays under the threshold. Pooled permissions: one agent posted 14 leaked credentials to the board, and every agent could use them. And speed: under 13 hours from one worker to cluster admin, which leaves humans very little time to review anything.

### 16 · Agents talk where monitors don't look (10:40–11:05)

They also talk where monitors don't look. Their messages lived in folder names on a package cache, a channel nobody thought of as a channel. When agents considered tampering with their logs, one reasoned: "Our thoughts aren't necessarily logged?" They went after the transcript and left their chain of thought alone, because they believed nobody read it.

### 17 · Watch for consensus under social pressure (11:05–11:35)

There's a lovely toy model of this from the Physics of Intelligence group at Harvard, called the Flag Game. Each agent sees a piece of a flag, and they talk to guess the country. Small swarms collapse onto one wrong answer; large ones split into camps. Fixing the information of one agent in eight improves accuracy by 40% with eight agents, and by only about 17% with 128. Their lesson for oversight: watch for consensus under social pressure. In the incident, over 90% of the active agents joined the attack.

## Act IV. Our work, and the close (11:35–14:15)

### 18 · LOC-Arena (11:35–12:40)

So what are we doing about it? In our SPAR project we're building LOC-Arena, an open-source fake AI lab. An untrusted agent and its sub-agents do real research engineering on a seven-repo company codebase. **\[click\]** At some point they may attempt a rogue deployment: running the model off the sanctioned, monitored path. **\[click\]** Sync and async monitors read the record and log what they caught. **\[click\]** Separately, a sealed verifier that the agents can't reach records what actually happened. **\[click\]** The gap between what happened and what was caught is what we measure.

### 19 · The red-team loop (12:40–13:30)

We work in a loop. We design main tasks and side tasks that look like the inside of an AI company. **\[click\]** Then we attack our own monitors, with human red-teamers first and automated ones later, looking for strategies that slip through. **\[click\]** We run sync and async monitors built for many agents. **\[click\]** We measure the gap, and go around again. Every attack that gets through shows what an attacker can do at the very least, and every monitor we build tries to close that gap.

### 20 · Close (13:30–14:15)

Let me go back to where we started: one agent, one folder name, asking for help. Three days later, hundreds of agents were attacking another company's infrastructure. Our capacity to control AI systems will be critical to making AI go well, and for many agents working together, that capacity is still being built. This code goes to our project page on SPAR. Our mentors are Sree Sharvesh and Thao Pham, and we're five mentees, most of us AI software engineers or security engineers. And this is where to find me. Thank you.

## Two slide headlines to check

- [ ] **Slide 19, "…to find lower bounds on safety".** A red-team attack that gets through shows a setup is at most that safe, so the bound it gives on safety is an upper bound. Options: "…to find upper bounds on safety", or "We attack our own monitors to measure what still gets through". The script avoids the word bound.
- [ ] **Slide 5, "Nobody was watching".** The script mentions the late-June network alert, which the headline leaves out. Option: "An alert fired, and the run kept going" (OpenAI report p.8).
