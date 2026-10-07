# Evidence-based design for the AI control introduction

Design research for a 15-minute talk to AI safety researchers, built as 1920×1080 HTML slides with inline SVG and shown live on a projector.

## Summary

- The voice carries the explanation; the screen carries drawings with short labels. Narrated graphics beat captioned graphics (d = 1.00), and text-heavy slides make audiences miss what is said aloud (Mayer 2023; Wecker 2012).
- Cutting extraneous material helped in 18 of 19 tests (d = 0.86), and irrelevant detail does most harm when the presenter sets the pace, as in a live talk (Mayer 2023).
- Each label touches the part it names and appears as the speaker says it (spatial contiguity d = 0.82, temporal contiguity d = 1.31).
- U, T, H, agents and monitors keep one glyph and one colour all talk, because audiences read any change in appearance as new meaning (Kosslyn et al. 2012).
- Expertise reversal applies concept by concept: pre-train only the control vocabulary, give each glyph its descriptive label once, then keep only its token, such as U (Kalyuga et al. 1998, 2003).
- The July 2026 incident is the running example; narratives are understood and recalled better than exposition (Mar et al. 2021).
- Sketch style suits concepts and open problems because it reads as provisional; numbers and results are drawn cleanly (Schumann et al. 1996; Wood et al. 2012).
- Authoring targets a washed-out projector: text of 40 px or more, high contrast, a colour-blind-safe palette with shape as a second cue, and a short URL beside a large QR code.

## Evidence and rules

The Mayer medians come from Mayer (2023), which summarises Mayer (2021). They pool one lab's experiments, mostly with novices in short, system-paced lessons; independent meta-analyses, where listed, usually give smaller estimates. A live talk is system-paced, the condition in which coherence, modality and temporal contiguity effects are strongest.

| Principle | Evidence (source; effect and boundary) | Rule for this deck |
|---|---|---|
| Multimedia and dual coding | Words plus graphics beat words alone in 13 tests, d = 1.35 (Mayer 2023). Pictures are recognised and recalled better than words (Standing 1973; Paivio & Csapo 1973), which dual coding theory attributes to separate verbal and imagery representations (Clark & Paivio 1991). | Every content slide carries a drawing. A words-only slide needs a stated reason. |
| Coherence | 18 of 19 tests, d = 0.86 (Mayer 2023). Seductive details hurt learning (Sundararajan & Adesope 2020), most when system-paced and highly interesting (Mayer & Fiorella 2014). | No logos, stock photos, textures or decorative icons. Incident imagery appears only where it carries a concept. |
| Signalling | 26 of 28 tests, d = 0.70 (Mayer 2023); positive in a separate meta-analysis (Schneider et al. 2018). Works best used sparingly. Integration signals helped only low-prior-knowledge learners (Richter et al. 2016) and hurt high-knowledge learners in a field study (Richter et al. 2018). | One accent per build step, on the element being discussed; the rest drops to grey. |
| Redundancy | Now the weakest principle: 8 of 12 tests, d = 0.10 (Mayer 2023), down from d = 0.86 in Mayer & Fiorella (2014). It weakens or reverses for short text, slow pacing and second-language listeners. Two-to-three-word labels inside a diagram raised retention (d = 0.47, 0.70) at no cost to transfer (Mayer & Johnson 2008); key terms beat verbatim text (Adesope & Nesbit 2012). | Never show the sentence being spoken. The jargon token (U, T, H, FPR) is part of its glyph and stays on every slide; the descriptive label ("untrusted model") appears once, and the explanation is spoken. |
| Speech suppression | With 209 students, regular slides reduced retention of information given only orally; concise slides avoided the loss (Wecker 2012). | One sentence (the headline) plus labels per slide. The assertion–evidence slides that tested well averaged 21 words (Garner & Alley 2013). |
| Spatial contiguity | 9 of 9 tests, d = 0.82 (Mayer 2023); g = 0.63 over 58 comparisons (Schroeder & Cenkci 2018). Strongest for low prior knowledge. | Labels touch what they name. No legends or keys. |
| Temporal contiguity | 8 of 8 tests, d = 1.31 (Mayer 2023); strongest in longer, system-paced lessons. | Each element appears as its word is spoken; builds are rehearsed against the script. |
| Segmenting | 7 of 7 tests, d = 0.67 (Mayer 2023). System-paced segmenting also works, and high-prior-knowledge learners gained more on retention (Rey et al. 2019). | One idea per slide or build step, with a short pause at each. |
| Pre-training | 10 of 10 tests, d = 0.78 (Mayer 2023; Mayer et al. 2002). May not apply to high prior knowledge or simple material. | A cast slide builds up U, T and H one glyph at a time before any protocol diagram; the other term chunks are pre-trained the same way on the slide where each first matters. |
| Modality | 18 of 19 tests, d = 1.00 (Mayer 2023); moderated by element interactivity and strongest under system pacing (Ginns 2005). Printed words can help for technical terms. | Narration carries explanations; the screen carries drawings and jargon tokens. |
| Personalisation | 13 of 15 tests, d = 1.00 (Mayer 2023); may not hold for experienced learners. | Conversational spoken script. Low priority for slide design. |
| Working memory | About four chunks (Cowan 2001). Novel information passes through limited working memory; stored schemas remove the limit (Sweller 1988; Sweller et al. 2019). | One new term per build step and three or four per slide. The ten control terms arrive in chunks: U, T and H; main and side task; protocol and kill chain; audit budget and FPR; diffuse and high-stakes. A known glyph counts as one chunk. |
| Assertion–evidence | Sentence headlines raised recall of slide assertions from 69% to 79% in a live course (Alley et al. 2006). For 110 novices with recorded narration, assertion–evidence slides gave better comprehension, fewer misconceptions and lower load than topic–bullet slides (Garner & Alley 2013). An informal critique cites weak control slides and modest effects, and notes the speaker can carry the assertion (Farkas 2010). | The headline states the slide's claim in at most two lines and is the only sentence on the slide; the body is a drawing. |
| Data-ink and chartjunk | Tufte (2001) argues for maximising data-ink. Embellished charts were read as accurately and recalled better after two to three weeks, n = 20 (Bateman et al. 2010), a result Few (2011) disputes. Colour and recognisable objects raised memorability (Borkin et al. 2013); titles stating the message drive recall, and pictograms did not hurt understanding (Borkin et al. 2016). | Strip gridlines, borders and shadows. A pictogram is allowed when it is the data's subject (agent glyphs counting agents). Chart titles state the takeaway. |
| Small multiples | Tufte (1990). For trends, small multiples were more accurate than animation, which viewers enjoyed and misread (Robertson et al. 2008). | Protocols and results are compared in side-by-side panels with identical layout and axes. |
| Graphical perception | Position on a common scale is judged most accurately, then length; angle, area and saturation rank lower (Cleveland & McGill 1984). | Key quantities are encoded as position or length. No pies or area bubbles. |
| Pop-out | A target differing in one feature, such as colour, is found in parallel; conjunctions need serial search (Treisman & Gelade 1980; Ware 2013; Healey & Enns 2012). | The one thing to look at differs from its neighbours in a single feature, the accent colour. |
| Gestalt grouping | Proximity, similarity and common region group elements (Wagemans et al. 2012; Palmer 1992). Viewers group automatically and attach a label to the nearest element (Kosslyn et al. 2012). | Each trust boundary or sandbox is a drawn region. Unrelated elements keep clear space between them. |
| Consistent encoding | Audiences assume every change in appearance carries information (Kosslyn et al. 2012). Inconsistent encodings across views slow reading and cause errors (Qu & Hullman 2018). | Fixed glyph and colour for U, T, H, agents and monitors. Appearance changes only when meaning does, for example U turning accent when it attacks. |
| Animation | Animation helps only when congruent with the concept and easy to perceive; many reported wins came from extra information or interactivity (Tversky et al. 2002). Mean d = 0.37 over static pictures, higher for realistic and procedural-motor content (Höffler & Leutner 2007). | Processes advance in discrete builds. Motion is reserved for things that move, such as messages between agents. No decorative transitions. |
| Drawing while talking | Watching an instructor draw improved transfer for low-knowledge learners (d = 0.58) and not for high-knowledge learners (d = −0.24); computer-animated drawing gave a non-significant d = 0.33 (Fiorella & Mayer 2016). | Builds add strokes in step with speech. Expected gain for this audience is small. |
| Narrative and examples | Narratives were understood and recalled better than expository texts across 33,000+ participants (Mar et al. 2021). Concrete examples aid learning (Weinstein et al. 2018). Worked examples help novices and become redundant with experience (Atkinson et al. 2000; Kalyuga et al. 2001). Comparing two cases aids abstraction (Gentner et al. 2003). | Each concept returns to the incident. One contrasting case appears where an abstraction needs it. None of the studies found here tests a single running example directly; this rule is an inference. |
| Numbers | Perspective sentences (ratios, ranks, unit changes) improved recall, estimation and error detection in 3,200+ participants (Barrio et al. 2016); familiar-object re-expressions helped estimation (Hullman et al. 2018). | Every headline number gets a familiar reference drawn beside it. |
| Sketch style | Among CAD users in a questionnaire of 54 architects, 53% picked the sketch rendering for a first draft and 8% for a final presentation; the study measured preference only (Schumann et al. 1996). Sketchiness compromised area judgement and may raise engagement (Wood et al. 2012). Whiteboard animations beat narrated slides on comprehension, N = 299 (Türkay 2022); a drawing hand raised motivation without a learning effect (Krieglstein et al. 2023). Comprehension evidence is thin and confounded with the act of drawing. | Sketch style for concepts, threat models and open problems. Clean geometry for any quantity, evaluation result or timeline axis. |
| Fonts | Hard-to-read fonts had no effect on recall (d = −0.01) or transfer and lengthened reading time (Xie et al. 2018). | One clean sans-serif for all text, including sketch-style slides. |

## Projection constraints

- **Font size.** Kosslyn et al. (2012) score text of 20 points or less as a legibility violation, noting their rules rest on face validity. The default PowerPoint slide is 540 points tall, so 20 points is 3.7% of its height, about 40 px at 1080 px. Rule: readable text at 40 px or more, labels 44–56 px, headlines 64–80 px.
- **Strokes.** Kosslyn et al. (2012) also flag points less than twice as thick as their connecting lines. Rule: nodes at least twice the stroke width, strokes of 4 px or more (the floor is an untested inference for washout).
- **Contrast.** WCAG 2.2 sets 4.5:1 for text, 3:1 for large text and graphical objects, 7:1 for enhanced contrast, and forbids colour as the only cue (W3C 2024). These apply to authored colour pairs. Room light lowers on-screen contrast; the InfoComm standard asks 15:1 for basic decision making and 50:1 for analytical viewing, measured in the room (rAVe 2012, on ANSI/INFOCOMM 3M-2011, since superseded). Rule, inferred from both: text at 7:1 or more, strokes at 4.5:1 or more.
- **Polarity and lighting.** Dark text on light backgrounds gave better acuity and proofreading on displays (Piepenbrock et al. 2013). The InfoComm article reports that switching off lights above the screen can double contrast. Rule: light background by default, a request to dim the lights over the screen, and a test run on the venue projector.
- **Colour vision.** About 8% of men and 0.4% of women of European descent have red–green deficiency (Birch 2012). Rule: Okabe–Ito hues (Okabe & Ito 2008; Wong 2011), no red–green pairs, every colour code doubled by shape, position or label.
- **QR codes.** Scanning needs about 1 cm of code per 10 cm of distance and at least 15 s; label the destination, and prefer a short URL when viewers have under 15 s (Kohler 2024). The guideline comes from print, so projection use is an extrapolation. On a 3 m wide screen one slide pixel is 1.56 mm, so a back row at 8 m needs about 510 px and one at 12 m about 770 px. Rule: the closing slide shows a QR code of 600 px or more with the short URL under it at headline size, held for at least 15 s while the speaker says what it links to.
- **Citations on slides.** No study found here tests citation formats. Rule, derived from coherence and consistent encoding: a short "Author Year" in a fixed bottom-right spot on the slide that makes the claim, with full references behind the QR code. Citations are the one stated exception to the 40 px floor (28 px or more), because they serve later lookup and are repeated behind the QR code.

## Rules for an expert audience

Under the expertise reversal effect, techniques that help novices lose their benefit, or harm learning, for experienced learners (Kalyuga et al. 2003; Kalyuga 2007). Expertise is specific to a concept: this audience is expert on LLMs and agents and uneven on control.

- **Skip LLM and agent basics.** No slide explains agents, scaffolds or tool calls.
- **Pre-train control terms once.** Each term chunk gets one short build, about a minute in total for the cast; pre-training gains fade with prior knowledge (Mayer 2023).
- **Describe once, then keep only the token.** Each glyph carries its descriptive label ("trusted model") on first appearance and only its token (T) afterwards. As expertise grew, the best design dropped text from diagrams (Kalyuga et al. 1998).
- **Signal only what changes.** Extra integration signals hurt high-knowledge learners (Richter et al. 2018).
- **Keep segmenting.** Segmenting helped high-prior-knowledge learners more on retention (Rey et al. 2019).
- **Use prompts for familiar material.** Worked examples become redundant with experience (Kalyuga et al. 2001). A protocol diagram can appear before its explanation, with the audience asked where U would attack.
- **Put depth behind the link.** Detail lives on the referenced page, so each slide keeps one claim.

## Visual-first: how to turn each kind of content into a drawing

Every row reuses the same glyph set.

| Content | Drawing | Example in this deck | Basis |
|---|---|---|---|
| Term or role | Glyph with its token and a fixed colour; descriptive label on first use only | U, T, H, monitor, agent | Pre-training, consistent encoding |
| Definition with parts | Glyph with two or three callouts touching their parts | Main task and side task as two paths out of one U | Spatial contiguity |
| Process or protocol | Left-to-right flow, one build per step | Action from U, score from T, threshold, audit by H | Congruence, temporal contiguity |
| Kill chain | Horizontal chain of links; the monitor's catch drawn as one broken link | Steps of a side task | Congruence |
| Single number | One large figure with a familiar reference drawn beside it | About 1,200 agents as a grid of 1,200 dots; over 70,000 messages against a familiar volume | Numbers |
| Rate or budget | Unit grid, or a score distribution with a threshold line and the tail shaded | A 1% audit budget as 1 lit square in 100; FPR as the tail past the threshold | Graphical perception |
| Comparison | Small multiples with identical layout and axes | Monitors or protocols side by side; diffuse and high-stakes as two panels | Small multiples |
| Trade-off between two quantities | Two-axis plot, one point per option | Protocols placed on two axes | Graphical perception |
| Timeline | One horizontal axis with few labelled ticks and event glyphs | History of the field | Congruence, coherence |
| Multi-agent system | Node-link graph; motion only for messages travelling along edges | The unsanctioned message board | Animation |
| Claim | Sentence headline over one drawing | Every slide | Assertion–evidence |
| Evidence from a paper or report | Cropped figure or screenshot with one highlight box | State-of-the-art evaluations | Signalling, coherence |
| Open problem | Sketch-style drawing of the known parts, dashed outline where the gap is | Multi-agent open problems | Sketch style |
| Own framework | Architecture drawing built from the same glyphs | Multi-agent loss-of-control eval | Consistent encoding |

## References

- Adesope, O. O., & Nesbit, J. C. (2012). Verbal redundancy in multimedia learning environments: A meta-analysis. *Journal of Educational Psychology*, 104(1), 250–263. https://doi.org/10.1037/a0026147
- Alley, M., Schreiber, M., Ramsdell, K., Muffo, J., & Borrego, M. (2006). Testing the effect of sentence headlines in teaching slides. *ASEE Annual Conference*, paper 2006-852. https://peer.asee.org/testing-the-effect-of-sentence-headlines-in-teaching-slides
- Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D. (2000). Learning from examples: Instructional principles from the worked examples research. *Review of Educational Research*, 70(2), 181–214. https://doi.org/10.3102/00346543070002181
- Barrio, P. J., Goldstein, D. G., & Hofman, J. M. (2016). Improving comprehension of numbers in the news. *CHI 2016*, 2729–2739. https://doi.org/10.1145/2858036.2858510
- Bateman, S., Mandryk, R. L., Gutwin, C., Genest, A., McDine, D., & Brooks, C. (2010). Useful junk? The effects of visual embellishment on comprehension and memorability of charts. *CHI 2010*, 2573–2582. https://doi.org/10.1145/1753326.1753716
- Birch, J. (2012). Worldwide prevalence of red-green color deficiency. *Journal of the Optical Society of America A*, 29(3), 313. https://doi.org/10.1364/JOSAA.29.000313
- Borkin, M. A., Vo, A. A., Bylinskii, Z., Isola, P., Sunkavalli, S., Oliva, A., & Pfister, H. (2013). What makes a visualization memorable? *IEEE TVCG*, 19(12), 2306–2315. https://doi.org/10.1109/TVCG.2013.234
- Borkin, M. A., Bylinskii, Z., Kim, N. W., Bainbridge, C. M., Yeh, C. S., Borkin, D., Pfister, H., & Oliva, A. (2016). Beyond memorability: Visualization recognition and recall. *IEEE TVCG*, 22(1), 519–528. https://doi.org/10.1109/TVCG.2015.2467732
- Clark, J. M., & Paivio, A. (1991). Dual coding theory and education. *Educational Psychology Review*, 3(3), 149–210. https://doi.org/10.1007/BF01320076
- Cleveland, W. S., & McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *Journal of the American Statistical Association*, 79(387), 531–554. https://doi.org/10.1080/01621459.1984.10478080
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87–114. https://doi.org/10.1017/S0140525X01003922
- Farkas, D. K. (2010). A brief assessment of Michael Alley's ideas regarding the design of PowerPoint slides. Informal report, University of Washington. https://faculty.washington.edu/farkas/dfpubs/Farkas-Assessment%20Of%20Alleys%20Slide%20Design.pdf
- Few, S. (2011). The chartjunk debate: A close examination of recent findings. *Visual Business Intelligence Newsletter*, Perceptual Edge. https://webspace.science.uu.nl/~telea001/uploads/VACourse/Few11.pdf
- Fiorella, L., & Mayer, R. E. (2016). Effects of observing the instructor draw diagrams on learning from multimedia messages. *Journal of Educational Psychology*, 108(4), 528–546. https://doi.org/10.1037/edu0000065
- Garner, J. K., & Alley, M. P. (2013). How the design of presentation slides affects audience comprehension: A case for the assertion–evidence approach. *International Journal of Engineering Education*, 29(6), 1564–1579. https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf
- Gentner, D., Loewenstein, J., & Thompson, L. (2003). Learning and transfer: A general role for analogical encoding. *Journal of Educational Psychology*, 95(2), 393–408. https://doi.org/10.1037/0022-0663.95.2.393
- Ginns, P. (2005). Meta-analysis of the modality effect. *Learning and Instruction*, 15(4), 313–331. https://doi.org/10.1016/j.learninstruc.2005.07.001
- Healey, C. G., & Enns, J. T. (2012). Attention and visual memory in visualization and computer graphics. *IEEE TVCG*, 18(7), 1170–1188. https://doi.org/10.1109/TVCG.2011.127
- Höffler, T. N., & Leutner, D. (2007). Instructional animation versus static pictures: A meta-analysis. *Learning and Instruction*, 17(6), 722–738. https://doi.org/10.1016/j.learninstruc.2007.09.013
- Hullman, J., Kim, Y.-S., Nguyen, F., Speers, L., & Agrawala, M. (2018). Improving comprehension of measurements using concrete re-expression strategies. *CHI 2018*, 1–12. https://doi.org/10.1145/3173574.3173608
- Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. *Educational Psychology Review*, 19(4), 509–539. https://doi.org/10.1007/s10648-007-9054-3
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist*, 38(1), 23–31. https://doi.org/10.1207/S15326985EP3801_4
- Kalyuga, S., Chandler, P., & Sweller, J. (1998). Levels of expertise and instructional design. *Human Factors*, 40(1), 1–17. https://doi.org/10.1518/001872098779480587
- Kalyuga, S., Chandler, P., Tuovinen, J., & Sweller, J. (2001). When problem solving is superior to studying worked examples. *Journal of Educational Psychology*, 93(3), 579–588. https://doi.org/10.1037/0022-0663.93.3.579
- Kohler, T. (2024). 13 QR-code usability guidelines. Nielsen Norman Group. https://www.nngroup.com/articles/qr-code-guidelines/
- Kosslyn, S. M., Kievit, R. A., Russell, A. G., & Shephard, J. M. (2012). PowerPoint presentation flaws and failures: A psychological analysis. *Frontiers in Psychology*, 3, 230. https://doi.org/10.3389/fpsyg.2012.00230
- Krieglstein, F., Meusel, F., Rothenstein, E., Scheller, N., Wesenberg, L., & Rey, G. D. (2023). How to insert visual information into a whiteboard animation with a human hand? Effects of different insertion styles on learning. *Smart Learning Environments*, 10, 39. https://doi.org/10.1186/s40561-023-00258-6
- Mar, R. A., Li, J., Nguyen, A. T. P., & Ta, C. P. (2021). Memory and comprehension of narrative versus expository texts: A meta-analysis. *Psychonomic Bulletin & Review*, 28(3), 732–749. https://doi.org/10.3758/s13423-020-01853-1
- Mayer, R. E. (2023). Research-based principles for designing multimedia instruction. In C. E. Overson, C. M. Hakala, L. L. Kordonowy, & V. A. Benassi (Eds.), *In their own words: What scholars and teachers want you to know about why and how to apply the science of learning in your academic setting*. Society for the Teaching of Psychology, APA Division 2. https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf
- Mayer, R. E., & Fiorella, L. (2014). Principles for reducing extraneous processing in multimedia learning: Coherence, signaling, redundancy, spatial contiguity, and temporal contiguity principles. In R. E. Mayer (Ed.), *The Cambridge handbook of multimedia learning* (2nd ed., pp. 279–315). Cambridge University Press. https://doi.org/10.1017/CBO9781139547369.015
- Mayer, R. E., & Johnson, C. I. (2008). Revising the redundancy principle in multimedia learning. *Journal of Educational Psychology*, 100(2), 380–386. https://doi.org/10.1037/0022-0663.100.2.380
- Mayer, R. E., Mathias, A., & Wetzell, K. (2002). Fostering understanding of multimedia messages through pre-training: Evidence for a two-stage theory of mental model construction. *Journal of Experimental Psychology: Applied*, 8(3), 147–154. https://doi.org/10.1037/1076-898X.8.3.147
- Okabe, M., & Ito, K. (2008). Color Universal Design (CUD): How to make figures and presentations that are friendly to colorblind people. Jfly. https://jfly.uni-koeln.de/color/
- Paivio, A., & Csapo, K. (1973). Picture superiority in free recall: Imagery or dual coding? *Cognitive Psychology*, 5(2), 176–206. https://doi.org/10.1016/0010-0285(73)90032-7
- Palmer, S. E. (1992). Common region: A new principle of perceptual grouping. *Cognitive Psychology*, 24(3), 436–447. https://doi.org/10.1016/0010-0285(92)90014-S
- Piepenbrock, C., Mayr, S., Mund, I., & Buchner, A. (2013). Positive display polarity is advantageous for both younger and older adults. *Ergonomics*, 56(7), 1116–1124. https://doi.org/10.1080/00140139.2013.790485
- Qu, Z., & Hullman, J. (2018). Keeping multiple views consistent: Constraints, validations, and exceptions in visualization authoring. *IEEE TVCG*, 24(1), 468–477. https://doi.org/10.1109/TVCG.2017.2744198
- rAVe [PUBS] (2012). InfoComm: Designing for high contrast: How one university uses InfoComm's projected image standard. https://www.ravepubs.com/infocomm-designing-for-high-contrast-how-one-university-uses-infocomms-projected-image-standard
- Rey, G. D., Beege, M., Nebel, S., Wirzberger, M., Schmitt, T. H., & Schneider, S. (2019). A meta-analysis of the segmenting effect. *Educational Psychology Review*, 31(2), 389–419. https://doi.org/10.1007/s10648-018-9456-4
- Richter, J., Scheiter, K., & Eitel, A. (2016). Signaling text-picture relations in multimedia learning: A comprehensive meta-analysis. *Educational Research Review*, 17, 19–36. https://doi.org/10.1016/j.edurev.2015.12.003
- Richter, J., Scheiter, K., & Eitel, A. (2018). Signaling text–picture relations in multimedia learning: The influence of prior knowledge. *Journal of Educational Psychology*, 110(4), 544–560. https://doi.org/10.1037/edu0000220
- Robertson, G., Fernandez, R., Fisher, D., Lee, B., & Stasko, J. (2008). Effectiveness of animation in trend visualization. *IEEE TVCG*, 14(6), 1325–1332. https://doi.org/10.1109/TVCG.2008.125
- Schneider, S., Beege, M., Nebel, S., & Rey, G. D. (2018). A meta-analysis of how signaling affects learning with media. *Educational Research Review*, 23, 1–24. https://doi.org/10.1016/j.edurev.2017.11.001
- Schroeder, N. L., & Cenkci, A. T. (2018). Spatial contiguity and spatial split-attention effects in multimedia learning environments: A meta-analysis. *Educational Psychology Review*, 30(3), 679–701. https://doi.org/10.1007/s10648-018-9435-9
- Schumann, J., Strothotte, T., Raab, A., & Laser, S. (1996). Assessing the effect of non-photorealistic rendered images in CAD. *CHI '96*, 35–41. https://doi.org/10.1145/238386.238398
- Standing, L. (1973). Learning 10,000 pictures. *Quarterly Journal of Experimental Psychology*, 25(2), 207–222. https://doi.org/10.1080/14640747308400340
- Sundararajan, N., & Adesope, O. (2020). Keep it coherent: A meta-analysis of the seductive details effect. *Educational Psychology Review*, 32(3), 707–734. https://doi.org/10.1007/s10648-020-09522-4
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257–285. https://doi.org/10.1207/s15516709cog1202_4
- Sweller, J., van Merriënboer, J. J. G., & Paas, F. (2019). Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review*, 31(2), 261–292. https://doi.org/10.1007/s10648-019-09465-5
- Treisman, A. M., & Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, 12(1), 97–136. https://doi.org/10.1016/0010-0285(80)90005-5
- Tufte, E. R. (1990). *Envisioning information*. Graphics Press.
- Tufte, E. R. (2001). *The visual display of quantitative information* (2nd ed.). Graphics Press.
- Türkay, S. (2022). Comparison of dynamic visuals to other presentation formats when learning social science topics in an online setting. *Australasian Journal of Educational Technology*, 22–36. https://doi.org/10.14742/ajet.7639
- Tversky, B., Morrison, J. B., & Bétrancourt, M. (2002). Animation: Can it facilitate? *International Journal of Human-Computer Studies*, 57(4), 247–262. https://doi.org/10.1006/ijhc.2002.1017
- W3C (2024). *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/
- Wagemans, J., Elder, J. H., Kubovy, M., Palmer, S. E., Peterson, M. A., Singh, M., & von der Heydt, R. (2012). A century of Gestalt psychology in visual perception: I. Perceptual grouping and figure–ground organization. *Psychological Bulletin*, 138(6), 1172–1217. https://doi.org/10.1037/a0029333
- Ware, C. (2013). *Information visualization: Perception for design* (3rd ed.), chapter 5, "Visual attention and information that pops out". Morgan Kaufmann.
- Wecker, C. (2012). Slide presentations as speech suppressors: When and why learners miss oral information. *Computers & Education*, 59(2), 260–273. https://doi.org/10.1016/j.compedu.2012.01.013
- Weinstein, Y., Madan, C. R., & Sumeracki, M. A. (2018). Teaching the science of learning. *Cognitive Research: Principles and Implications*, 3, 2. https://doi.org/10.1186/s41235-017-0087-y
- Wong, B. (2011). Points of view: Color blindness. *Nature Methods*, 8(6), 441. https://doi.org/10.1038/nmeth.1618
- Wood, J., Isenberg, P., Isenberg, T., Dykes, J., Boukhelifa, N., & Slingsby, A. (2012). Sketchy rendering for information visualization. *IEEE TVCG*, 18(12), 2749–2758. https://doi.org/10.1109/TVCG.2012.262
- Xie, H., Zhou, Z., & Liu, Q. (2018). Null effects of perceptual disfluency on learning outcomes in a text-based educational context: A meta-analysis. *Educational Psychology Review*, 30(3), 745–771. https://doi.org/10.1007/s10648-018-9442-x
