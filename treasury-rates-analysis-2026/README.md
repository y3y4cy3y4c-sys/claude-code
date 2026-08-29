# Treasury Rates Analysis — Summer 2026 (late June → Aug 28, 2026)

Research deliverable answering: **what happened to US and global rates over the last ~2 months, and why** — with a decomposition distinguishing a monetary-policy repricing from a long-end / fiscal / term-premium repricing.

## Contents

- `report.html` — the full charted report ("The 5.33% Summer"): US 2Y/5Y/10Y/30Y moves, curve shape, real-vs-breakeven decomposition, global comparison (Europe/UK/Japan/Korea), driver scorecard, event timeline, and verdict. Published as a Claude artifact.
- `findings/` — raw research notes from the multi-agent sweep (one file per topic + three verification passes), each with dated data points and sources.

## Headline conclusions

1. **What happened:** a bear steepening led by the long end. 2Y 4.15%→4.34% (+19bp), 10Y 4.44%→4.73% (+29bp), 30Y 4.93%→5.17% (+24bp; **peak 5.33% on Aug 18 — highest since June 2007**). 2s10s ~29→39–44bp; 30Y–2Y peaked ~38bp steeper before partially unwinding on Treasury's Aug 19 buyback expansion and Warsh's hawkish Jackson Hole speech (Aug 28).
2. **Real yields did all the work:** 10Y breakeven flat (~2.34%→2.34%); 10Y real +~24bp; 30Y real to ~3.0% (30Y TIPS auction at 2.973%, highest since 2001). Long-run inflation expectations stayed anchored despite the Iran/oil shock (Brent briefly $100.69 on Jul 23).
3. **Cause = joint repricing:** a genuine hawkish Fed-path repricing (June SEP erased the 2026 cut; 3 hike dissents at the July FOMC; Sept-hike odds 55%→82%→42%→58%) **plus** a fiscal/term-premium repricing concentrated in 20s–30s (ACM 10Y term premium +~35bp; $432B July deficit — largest since Mar 2021; $40T debt; costliest 30Y auction since 2001; two 20Y tails; Treasury doubled long-end buybacks). AI capex (~$725B hyperscaler 2026 capex; +$474B net AI-linked bond supply) is the structural new demand for capital behind higher real yields — and why equities sat near records while the long bond sold off.
4. **The tell:** Aug 7–18 — the front end *rallied* on −23k payrolls while 30s made 19-year highs. A pure Fed story can't produce that divergence; a term-premium/supply story predicts it.
5. **Global:** synchronized long-end milestones the same week — UK 30Y ~5.85% (reported 1998 highs), 30Y JGB >4% for the first time ever, German 30Y funding costliest since 2011, OAT–Bund ~90bp (widest since 2012), Korea's curve steepest since 2021 with the BOK hiking back-to-back to 3.00%.

## Method & caveats

Compiled Aug 29, 2026 from ~340 live web searches (14 parallel research agents + adversarial verification). All figures are dated observations from cited public reporting (CNBC, Bloomberg, Treasury, FRED/NY Fed, CBO, CRFB, TIPS Watch, etc.); closes and intraday prints are mixed where noted, so 1–5bp discrepancies between outlets survive. One agent's cut-pricing claim was identified as 2025-coverage contamination and discarded (see `findings/res_verify_thesis.md`). Not investment advice.
