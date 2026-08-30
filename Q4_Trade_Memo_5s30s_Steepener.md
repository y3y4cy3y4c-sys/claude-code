# Q4 — Trade: Put Your Money Where Your Macro View Is

**Trade memo — as of Friday, August 28, 2026 (entry Monday, August 31)**

**The trade: DV01-neutral 5s30s Treasury curve steepener — long 5y UST / short 30y UST, entered around +75–80bp (H.15 Aug 27 close: +81), initial target +110–120bp with a +150bp stretch, stop +45–50bp, 6–12 month horizon, positive carry.**

*(Revised Aug 29 after quant validation — see the Addendum at the end for the mechanics check, the 2s30s/5s30s/10s30s comparison, and the eight-cycle backtest behind the revised targets.)*

This memo is structured the way the assignment demands: the trade is not chosen until the research conclusions from Q1–3 force it. Sections 1–3 restate those conclusions with the current data behind them. Sections 4–9 run the required chain: **View → Mispricing → Instrument → Catalyst → Payoff → Risk**. If any of the Q1–3 conclusions is wrong, Section 8 says exactly which market observation would falsify it and what happens to the position.

---

## 1. Where the research from Q1–3 landed

### Q1 — The Fed's reaction function: hawkish words, constrained hands

The surface reading of the Fed is hawkish. The July 28–29 FOMC held at **3.50–3.75%** on a 9–3 vote, with three regional presidents — Hammack (Cleveland), Kashkari (Minneapolis), Logan (Dallas) — dissenting **in favor of a hike**, the first unified three-way dissent in one direction since 2016. Chair Kevin Warsh, 100 days into the job after replacing Powell in May, used his first Jackson Hole keynote (Friday, Aug 28) to say inflation is running too high and the Fed may "have work to do," while refusing to give forward guidance. The front end repriced immediately: the 2y jumped ~6–11bp to ~4.30–4.34%, its highest in a month, and futures now put September hike odds around 30–38% (Polymarket is above 50%), with roughly one full hike priced cumulatively by end-2026.

The research conclusion from Q1 is that **this hawkishness is rhetoric the committee cannot convert into a sustained hiking cycle**, for three reasons:

1. **The labor market is already contracting.** July payrolls printed **–23k** with negative revisions — outright job losses in retail (–19k), leisure/hospitality (–40k), financial activities (–14k), and local government education (–50k). The unemployment rate fell to 4.1% only because participation fell. Average hourly earnings are up just **3.2% y/y, the slowest since May 2021** and *below* current inflation — real wages are falling. There is no wage-price spiral to break with hikes; hiking into negative payrolls is the policy mistake, and the committee knows it.
2. **The committee's political center of gravity blocks hikes.** All three hike dissents came from regional presidents. The Board — reshaped by the administration that installed Warsh precisely because it wants easier policy — is not going to supply votes for a tightening cycle into a midterm year. Warsh's dominant strategy is hawkish *talk* as a substitute for hawkish *action*: rebuild inflation-fighting credibility rhetorically while never actually delivering the hikes.
3. **The inflation impulse is a supply shock, not a demand overheat.** The stall in disinflation dates to the late-February closure of the Strait of Hormuz (see Q3 context below). Central banks look through supply shocks when wages are decelerating — and wages are decelerating.

**Q1 conclusion: on a 12-month view, the next durable move in the front end is down, not up.** The hiking-cycle scenario requires Trump-appointed governors to vote for higher rates into a shrinking labor market. That is a tail, not a base case.

### Q2 — Inflation: stuck above 3%, but not accelerating — and not going to 2% quickly either

July core PCE held at **3.3% y/y** (headline **3.7%**), hotter than expected, and the disinflation trend has visibly stalled; headline CPI is **3.4%**. But composition matters. The gap between headline PCE (3.7%) and core (3.3%) is energy — the Iran war premium. Core CPI's monthly run-rate in July returned to its February, pre-conflict pace. The demand side is disinflating on its own: wage growth at 3.2% and falling, payrolls negative, participation declining.

**Q2 conclusion: inflation grinds from the mid-3s toward the high-2s as the energy shock fades and labor income weakens — but it does not return to 2% on any near horizon**, because the tariff level-shift is still passing through, the Hormuz risk premium can reignite, and (per Q1) the Fed will not impose the demand destruction required to force it there. Sticky-3s, drifting slowly lower. Neither the hawks' spiral nor a clean glide to target.

### Q3 — Fiscal, supply, and the long end: structural pressure is no longer a thesis, it's the news flow

This was the structural leg of the research, and 2026 has made it explicit:

- The 30y traded to its **highest yield since 2007** (~5.27%) this summer, driven by war escalation risk and — the market's own stated concern — a deteriorating fiscal picture with a "tidal wave" of maturing debt to refinance on top of ongoing deficits.
- Treasury's response was not to term out less — the August refunding still sold $125bn including $25bn of 30y — but to **buy its own long bonds**: Secretary Bessent doubled long-end liquidity-support buybacks to at least **$4bn per operation** ($69bn total Aug 6–Nov 5, upsized long-end operations beginning Sept 9), and is floated in the press as considering tapping the ~$1T Treasury General Account to fund more.
- Each buyback-driven rally in the long end has **fizzled within days** — the Aug 19 rally was fully retraced by Aug 21. The flow problem (issuance + maturing stock) overwhelms the buyback capacity.

Treasury frames the buybacks as liquidity support, not yield management — but their timing and upsizing around long-end selloffs show how sensitive the fiscal authority has become to long-end yields, and they have not held the level. The point is not a fiscal crisis: fiscal supply, real term premium and structural demand for capital (an AI investment boom raises long real rates even when it is productive) are increasingly what the 30y prices, over and above the Fed's path.

**Q3 conclusion: relative to the 5y, the 30y's ability to *rally* is constrained by supply, term premium and capital demand — its risks skew toward staying elevated, with further term-premium widening the fatter tail.**

---

## 2. VIEW

> **The market may be overpricing the persistence of Fed hawkishness — a contracting labor market and a divided committee argue the hawkish path erodes — while underpricing the persistence of structural pressure at the long end, where fiscal supply, term premium and capital demand increasingly set the price. The claim is not that the Fed is wrong; it is that the *relative* pricing of the 5y versus the 30y is wrong, and post-Jackson-Hole (~35% September hike priced, 5s30s flattened to ~+75–80bp) is an attractive level to take the other side.**

Note the contrast with the naive version of this view. "The Fed will eventually ease, but fiscal pressure keeps the long end elevated" was easy to say a year ago when the Fed was already cutting. Today the same *structural* view has a much better *entry*: the market has swung all the way to pricing **hikes**, so the front leg of the trade is no longer "how fast do cuts come" but "does the hiking cycle that is now priced actually exist" — a cheaper, more falsifiable bet.

## 3. MISPRICING

Two relative mispricings, and the asymmetry that ties them together:

1. **The front end prices a phantom hiking cycle.** The 2y at 4.24% (4.31–4.36 post-speech) and 5y at 4.38% sit ~60–75bp above the funds midpoint (3.625%), embedding ~35% odds of a September hike and roughly a full hike by end-2026, with essentially no probability weight on the labor-driven cutting scenario within 12 months. Against –23k payrolls, falling participation, and 3.2% wage growth, that distribution is skewed the wrong way. You are being paid to fade it — at post-speech levels, at a local extreme in hike pricing.
2. **The long end prices too little structural risk premium relative to the fiscal path** — or at minimum, no compression is on offer. At 5.19% (real yield 2.96%) the 30y is not "cheap to short" on level, but the flow backdrop (refinancing wall, fizzled buybacks, TGA gimmicks that *add* future supply) means its risks remain one-sided versus the front end. The point of shorting it here is not that it must sell off; it is that it **cannot rally far**, which is exactly what a curve trade needs from its short leg.
3. **The asymmetry that ties them together.** No claim of logical inconsistency in market prices is needed — hike odds and 2.28% breakevens can coexist coherently (the market can expect a hike delivered precisely to keep medium-term expectations anchored). The trade's case is the asymmetry: *either weaker growth eventually removes the hike pricing, helping the 5y — or persistent inflation and fiscal pressure remain concentrated at the long end, hurting the 30y.* **Both resolutions steepen; only credible delivered tightening flattens.** That is what makes it a relative-value expression rather than a directional coin flip.

## 4. INSTRUMENT — derived by elimination, not picked

The assignment's menu, scored against the three research conclusions (✔ = expresses it, ✗ = exposed to it, ○ = neutral):

| Instrument | Q1: no hikes / eventual cuts | Q2: sticky-3s inflation | Q3: long end pinned by fiscal | Carry | Verdict |
|---|---|---|---|---|---|
| **Outright duration** (long 5y) | ✔ | ✗ (sticky inflation hurts) | ✗ (term premium leaks into belly) | + | Right direction, unhedged against Q2/Q3 — incomplete |
| **Rates: curve — 5s30s steepener** | ✔ (long 5y) | ○/✔ (sticky inflation hits 30y hardest) | ✔ (short 30y) | + | **Expresses all three. The trade.** |
| **Cross-market rates** (US vs bunds/JGBs) | ○ | ○ | ○ | ○ | Dilutes a domestic mispricing with foreign legs we have no edge on |
| **FX** (short USD "debasement") | ✔ | ✔ | ✔ | – | Right theme, wrong vehicle: war-haven USD bid and any delivered hike both fight it |
| **Credit** (short IG/HY on labor) | ✔ | ○ | ○ | – | Negative carry, fights AI-capex earnings strength, timing-dependent |
| **Breakevens** (long 5y BE at 2.28%) | ✔ | ✔✔ | ✔ | ++ | Best *alternative* — but dies in the hard-landing scenario that Q1 makes live (see §9) |
| **Commodities** (long oil) | ○ | ✔ | ○ | ○ | A Hormuz-negotiation binary, not a macro view |

Why the curve dominates the outright: a DV01-neutral steepener is long the front end's mispricing while **immunized against the level of yields** — the thing Q2 and Q3 say we cannot forecast with confidence. And it is the rare trade that wins in *both* of the opposed macro resolutions:

- **Bull steepening** (base case): hike pricing bleeds out, labor keeps softening, cuts get priced → 5y rallies hard, 30y anchored by supply.
- **Bear steepening** (stagflation escalation): Hormuz stays shut, oil re-spikes, Fed under-reacts (per Q1) → inflation/term premium hits the 30y hardest.

It loses only in **bear flattening** — hikes actually delivered *and* believed, restoring credibility and compressing term premium — which is precisely the scenario Q1's research rejects. The trade is therefore a pure, falsifiable expression of the research: if the political appointees vote for hikes into negative payrolls, the thesis was wrong and the position is stopped out. One structural note: 5s over 2s for the long leg because the 2y is dominated by the next few FOMC meetings, whereas the 5y has more exposure to how the entire medium-term policy path reprices over the 6–12-month horizon — the repricing this thesis is actually about; 5s30s rather than 10s30s because dropping the front leg would discard the Q1 alpha and keep only the crowded term-premium short.

## 5. TRADE SPECIFICATION

**Structure.** Long 5y UST / short 30y UST, DV01-neutral, on a $100mm mock-fund NAV.

| Leg | Instrument | Face | DV01 |
|---|---|---|---|
| Long | 5y Treasury note (4.38%, H.15 Aug 27) | +$44.9mm | +$20.0k/bp |
| Short | 30y Treasury bond (5.19%, H.15 Aug 27) | –$13.2mm | –$20.0k/bp |

*(DV01 per $1mm face: 5y ≈ $445, 30y ≈ $1,520.)*

**Futures implementation** (no repo lines needed for the mock book): long **FV** (5y note future) vs short **WN** (Ultra Bond — deliverable remaining maturity ≥25y, so it tracks the 30y; the classic bond contract's 15–25y basket does not). Legs are sized **dynamically to equalize DV01 off the current cheapest-to-deliver securities and conversion factors** — CTD switches change the ratio, so no fixed contract ratio is quoted. Swap alternative: receive 5y SOFR / pay 30y SOFR, same DV01s, cleaner rolldown math, adds swap-spread basis.

**Entry: 5s30s ≈ +75–80bp (H.15 Aug 27 close: +81).** Friday's hawkish-speech reaction (2y up 6–11bp, long end *lower* — a bear-flattening) handed the trade a better entry than midweek. We are fading the market at a local extreme in hike pricing, not chasing steepening.

**Entry, statistically** (monthly closes; `spread_stats_5s30s.py`, which upgrades itself to daily FRED data when run with network access):

| Spread | Window | Current | Mean | Stdev | Z | Percentile | Min–Max | Δm vol |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **5s30s** | **1y** | **81** | 96.4 | 12.0 | **−1.28** | **4%** | 81–110 | 5.0 |
| 5s30s | 3y | 81 | 61.0 | 36.2 | +0.55 | 57% | 7–110 | 9.8 |
| 2s30s | 1y | 95 | 107.3 | 9.6 | −1.28 | 4% | 95–125 | 7.2 |
| 2s30s | 3y | 95 | 55.2 | 55.7 | +0.71 | 56% | −31–125 | 14.9 |
| 10s30s | 1y | 52 | 56.8 | 4.0 | −1.21 | 12% | 52–65 | 4.7 |
| 10s30s | 3y | 52 | 36.9 | 19.0 | +0.80 | 61% | 11–65 | 6.0 |

The two windows tell one story. The 3-year Z (+0.55, 57th percentile) says the level is only mid-range — that window mixes the flat 2023–24 regime with the steep 2025 one, so no claim of generational flatness is available (or needed). The 1-year Z (**−1.28, 4th percentile — the flattest monthly close of the past year**) says the 2026 hike-repricing retraced roughly a quarter of the 2024–25 steepening (+7 in Apr-24 → +110 late-25 → +81 now), and *that retracement is what the entry buys*: a re-entry into an established steepening regime at its local flattest, not a chase. (Basis: month-end CMTs, Sep-23…Aug-26; 2023–25 reconstructed ±5–10bp, H1-2026 interpolated between documented anchors ±10–15bp, Aug-26 official H.15; monthly closes smooth intra-month extremes, so percentiles are conservative.)

**Carry and rolldown — the trade pays you to wait:**

- Computed by aging both legs one year and repricing them on today's (unchanged) curve, financed at repo ≈ 3.65% — not the coupon-minus-repo shortcut (`carry_roll_tenor_comparison.py`):
- Running: +$125k/yr net (long 5y earns 73bp over repo on $44.9mm; short 30y costs 154bp on $13.2mm)
- Rolldown: +$71k/yr (5y rolls to a ~4.34% 4y point; the 30y roll is ~zero because 20s30s is flat at 5.18/5.19)
- **Net carry + roll ≈ +$196k/yr ≈ +9.8bp of curve per year (≈ +0.8bp/month).** Magnitude is assumption-sensitive (repo specialness, financing spreads, futures calendar rolls); the *sign* is robust while funds sit below the entire coupon curve.

This is the quiet edge of doing the trade *now* rather than in 2025: with the funds rate below the entire coupon curve (no inversion at the front), the steepener is **positive carry** — the position no longer bleeds while waiting for the Fed, which is what killed early steepeners in prior cycles.

**Sizing.** Risk budget: 60bp of NAV at the stop → $600k / 30bp adverse move → **$20k/bp curve DV01** (the table above). Checks against the fund's risk limits: 5s30s daily vol ≈ 3–3.5bp → 95% 1-day VaR ≈ $100–115k ≈ **0.10–0.12% of NAV** (limit 2%); net duration ≈ 0 (level-immunized). Sizing is risk-budget-based only — no Kelly-style optimization is claimed, because the scenario probabilities in §7 are subjective priors, not estimated frequencies.

## 6. CATALYST — what closes the gap, and when

The mispricing is a probability distribution over FOMC outcomes; the catalysts are the events that collapse it:

| Date | Event | Expected effect |
|---|---|---|
| **Fri Sep 4** | August payrolls | Second negative/weak print breaks "solid economy" premise of the hike case → front leg rallies |
| Thu Sep 10 | August CPI | Core m/m at ~0.2% with energy fading starves the September-hike argument |
| **Tue–Wed Sep 15–16** | **FOMC** | Base case: hold, hawkish words, no delivered hike. ~35% priced hike premium starts bleeding out of the whites/reds. The dissent count is the tell (see §8) |
| Sep 9 → Nov 5 | Upsized long-end buyback operations | Test of Q3: rallies that fizzle (like Aug 19–21) confirm the supply floor under the short leg |
| Late Oct / Nov 4 | Q4 refunding (QRA) | Coupon sizes at the long end reprice term premium; any TGA-funded buyback scheme = more future supply → steepener-positive |
| Nov / Dec | Hormuz negotiation | A deal drops headline energy → kills the hike case faster (front leg) while easing the war-premium bid for long bonds — net steepener-positive |
| **Dec 15–16** | **FOMC + SEP** | If cumulative 2026 hike pricing dies unfulfilled here, the front end has to re-center on the 2027 cut path |
| Q1 2027 | Labor data cycle | The slow-burn catalyst: each month of sub-50k payrolls drags the priced path from hikes → hold → cuts |

Time horizon: the front-end repricing (hikes → hold) is a 1–4 month story; the cut-pricing and fiscal legs run 6–12 months. Positive carry means the position is not paying for the long tail of that window.

## 7. PAYOFF

Scenario tree, 6–12 month horizon, from +75bp entry (curve P&L at $20k/bp; carry ≈ +$150–300k over the horizon on top):

| Scenario | Prob. | 5y | 30y | 5s30s | Curve P&L |
|---|---|---|---|---|---|
| **A. Base — hawkish hold, hike premium bleeds, labor softens; partial cut-pricing by Q1-27** | ~45% | 4.00 | 5.10 | **+110 → +133** | +$0.6–1.1mm |
| **B. Hard landing — payrolls go deeply negative; even this Fed cuts** | 20% | 3.30 | 4.95 | **+165** | +$1.8mm |
| **C. Stagflation — Hormuz re-shuts, oil $110+; Fed hikes once but long end blows out** | 10% | 4.80 | 5.70 | **+90** | +$0.3mm |
| **D. Credible tightening — hikes delivered and believed; bear flattening** | ~20% | 4.85 | 5.25 | +40 → **stopped at +45–50** | –$0.6mm |
| **E. Bull flattening — global risk-off haven bid to 30y while Fed refuses to ease** | 5% | 4.30 | 4.85 | +55 | –$0.4mm |

- **Probabilities are subjective priors that rank the scenarios — no point-estimate EV is claimed from them.** What can be stated: risk to the stop is –30bp (–$0.6mm, –0.6% NAV); the initial target (+110–120) is +32–42bp of curve — regaining the 2025 steepness, which the backtest shows the median cut-delivering cycle achieved within 12 months; the +150 stretch (+72bp, ~2.4:1) sits below every deep-cycle peak level on record (+170 to +295).
- **The shape that matters:** the trade wins in opposed macro resolutions (A and B are disinflationary, C is inflationary) and loses only where the thesis is genuinely wrong (D, and the small E tail).
- **Take-profit plan:** scale out through +110–120; hold a stretch tranche for +150 only while the labor data keeps deteriorating (the deep-cycle condition).

## 8. RISK — where the view is wrong, and what it costs

**The stop: 5s30s +45–50bp (–30bp from entry), ≈ –$600k, –0.6% NAV.** That is roughly where a delivered September hike plus hawkish guidance (scenario D) would take the spread. The stop is placed where the *thesis* is falsified, not at an arbitrary distance: a curve flattening through the band means the market believes in the hiking cycle, which means Q1's political-constraint argument was wrong. The 1998 precedent (insurance cuts → re-hike) flattened 5s30s 50bp in a year; the stop caps this trade's version of that path at –30.

**Thesis falsifiers — exit on the information, before the stop if they hit:**

1. **A Board governor votes to hike.** The Q1 argument rests on the hike faction being regional presidents only. If Bowman, Waller, Miran — or Warsh himself forcing a vote — deliver a Board majority for a hike into negative payrolls, the political-constraint premise is dead. Exit.
2. **Labor re-accelerates.** Two consecutive payroll prints >+150k with participation recovering, or AHE back above ~3.5% y/y, kills the "no spiral, labor cracking" leg. Exit or halve.
3. **Term premium genuinely compresses.** If long-end rallies *stop fizzling* — 30y sustainably through ~4.90% absent a hard-landing panic — the structural supply floor (Q3) is failing and the short leg is wrong.

**Known hazards that are *not* falsifiers (manage, don't exit):**

- **Buyback squeeze on the short leg (sharpest tactical risk).** Treasury's upsized operations start Sept 9, and the TGA-funded escalation ($1T headline) would target exactly the sector we are short. Mitigants: capacity is small against a refinancing wall Treasury itself concedes; both August rallies fizzled inside a week; and TGA-funded buybacks are debt-financed purchases of debt — supply displaced into the future plus an inflation-credibility cost that ultimately *cheapens* the long end. Playbook: treat fizzling buyback rallies as adds, but never average down through the stop.
- **The Warsh paradox.** His no-guidance doctrine raises headline volatility around every speech (Friday: 11bp on the 2y). Position is sized so a 2σ rhetoric day (~$120k) is noise.
- **AI-productivity disinflation** (Warsh's own Jackson Hole theme): fast disinflation with solid growth → Fed credibly holds, term premium compresses slowly → the trade bleeds rather than breaks. Positive carry (+1.2bp/mo) is the cushion; the +45bp stop is the backstop.
- **Convexity/tails:** the position is long the front end into any crisis (the right tail to be long) and short the instrument with the worst supply story (the right tail to be short); the genuinely bad tail — global deflationary shock with a Fed on strike (E) — is real but 30y haven rallies into a 5.2% yield with this issuance calendar have repeatedly failed.

**Monitoring cadence:** payrolls/CPI/FOMC dates above; weekly buyback operation results (bid-to-cover on long-end ops); dissent composition in the September statement; 5y5y breakevens as the fiscal-credibility thermometer.

## 9. The alternative the research also supports — and why it's the complement, not the core

The same three conclusions justify **long 5y TIPS breakevens at 2.28%**: a politically constrained Fed easing into 3%+ inflation is the textbook breakeven-widening regime, and the carry is enormous (TIPS accrue realized CPI at 3.4% vs. 2.28% priced ≈ +110bp/yr if inflation merely stays put). It is the purest expression of the view that inflation settles in the high-2s rather than gliding back to 2% — a standalone bet on Q2's conclusion.

It is not the core position for one reason: **scenario B.** The hard-landing outcome that Q1's labor data makes live (–23k payrolls) is the scenario where breakevens historically collapse (5y BE reached ~0% in 2008 and 2020) — and it is simultaneously the steepener's best scenario. The steepener wins in A, B, and C; breakevens win in A and C but die in B. A book running both (e.g., 2/3 steepener, 1/3 breakevens) is better diversified across the inflation axis, but forced to one instrument per the assignment, the steepener is the internally consistent choice — it is the only expression on the menu that does not require taking a side on the one question the research left genuinely open (does the labor crack become a recession?).

---

## Appendix — Market data snapshot (as of Aug 27–28, 2026)

| Item | Level | Item | Level |
|---|---|---|---|
| Fed funds target | 3.50–3.75% (held 9–3, three hike dissents) | July payrolls | –23k (U3 4.1%, participation-driven) |
| 2y UST | 4.31–4.36% (post-Warsh) | AHE y/y | +3.2% (slowest since May 2021) |
| 5y UST | 4.38% (H.15 Aug 27) | Core PCE y/y (Jul) | 3.3% (headline 3.7%) |
| 10y UST | 4.67–4.68% | CPI y/y (Jul) | 3.4% |
| 30y UST | 5.18–5.27% (2026 high: highest since 2007) | 5y / 10y breakeven | 2.28% / 2.32% |
| **5s30s** | **≈ +75bp (post-speech)** | WTI / Brent | ~$82–87 / ~$89 (Hormuz flows 15–16mmbd vs 22–24 pre-war) |
| Sep-26 hike odds | ~30–38% futures; ~53% Polymarket | Buybacks | $69bn Aug 6–Nov 5; long-end ops doubled to ≥$4bn; TGA (~$1T) floated |

**Primary sources:** July FOMC decision and dissents ([CNBC](https://www.cnbc.com/2026/07/29/fed-rate-decision-july-2026.html), [Federal Reserve statement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm)); Warsh Jackson Hole keynote and market reaction ([Federal Reserve](https://www.federalreserve.gov/newsevents/speech/warsh20260828a.htm), [CNBC](https://www.cnbc.com/2026/08/28/kevin-warsh-jackson-hole-federal-reserve-inflation.html), [CNBC yields](https://www.cnbc.com/2026/08/28/treasury-yields-jackson-hole.html), [Washington Post](https://www.washingtonpost.com/business/2026/08/28/fed-chair-warsh-speaks-jackson-hole-conference/)); Warsh confirmation ([NPR](https://www.npr.org/2026/05/13/nx-s1-5816235/kevin-warsh-federal-reserve-chair-jerome-powell)); July jobs report ([CNBC](https://www.cnbc.com/2026/08/07/jobs-report-july-2026.html), [NBC](https://www.nbcnews.com/business/economy/july-2026-jobs-report-rcna591138), [BLS](https://www.bls.gov/news.release/empsit.nr0.htm)); July CPI/PCE ([TD Economics](https://economics.td.com/us-cpi), [Kiplinger](https://www.kiplinger.com/investing/economy/cpi-report-july-2026-what-to-expect)); yields ([Advisor Perspectives snapshot](https://www.advisorperspectives.com/dshort/updates/2026/08/14/treasury-yields-snapshot-august-14-2026), [CNBC](https://www.cnbc.com/2026/08/21/treasury-yields-bonds-inflation-rates.html), [FRED DGS2/DGS5/DGS10/DGS30](https://fred.stlouisfed.org/series/DGS30)); breakevens ([FRED T5YIE](https://fred.stlouisfed.org/series/T5YIE), [T10YIE](https://fred.stlouisfed.org/series/T10YIE)); hike odds ([KuCoin/Polymarket](https://www.kucoin.com/news/flash/polymarket-prices-53-odds-of-fed-rate-hike-in-september-2026-vs-32-in-futures), [Chase](https://www.chase.com/personal/investments/learning-and-insights/article/september-2026-rate-hike-now-expected-amid-energy-shocks)); refunding and buybacks ([Treasury QRA](https://home.treasury.gov/news/press-releases/sb0590), [buyback upsizing](https://home.treasury.gov/news/press-releases/sb0607), [Reuters via Yahoo](https://finance.yahoo.com/economy/policy/articles/us-treasury-double-sizes-debt-134308742.html), [CNBC TGA report](https://www.cnbc.com/2026/08/24/bessent-1-trillion-treasury-general-account-bond-buybacks.html), [Bloomberg](https://www.bloomberg.com/news/articles/2026-08-19/long-dated-treasuries-rally-as-treasury-boosts-bond-buybacks)); oil/Hormuz ([CNBC](https://www.cnbc.com/2026/08/10/oil-prices-today-brent-wti-hormuz-trump-iran.html), [Al Jazeera](https://www.aljazeera.com/economy/2026/8/10/oil-prices-climb-as-iranian-demands-cloud-outlook-for-strait-of-hormuz)).

---

## Addendum (Aug 29, 2026) — Quant validation: mechanics, tenor choice, and the backtest

*Added after a quant-consistency review of the Aug-28 memo. Changes made to the memo above: entry restated as +75–80bp (H.15 Aug 27 close: +81); initial target restructured to +110–120 with +150 as a stretch; stop widened to a +45–50 band; carry recomputed by aged-bond repricing (+9.8bp/yr, previously +15); the fixed futures ratio replaced by dynamic CTD-based DV01 sizing; the Kelly calculation and point-estimate EV removed as false precision.*

### A1. What the position actually bets on

DV01-neutral, the P&L is **P&L ≈ DV01 × (Δy30 − Δy5)** — the win condition is simply Δy30 > Δy5. The 5y does not need to rally and the 30y does not need to sell off:

| Scenario | Δ5y | Δ30y | Result |
|---|---:|---:|---|
| Bull steepener | −50bp | −10bp | +40bp → win |
| Bear steepener | +20bp | +60bp | +40bp → win |
| Bear flattener | +60bp | +20bp | −40bp → lose |
| Bull flattener | −20bp | −60bp | −40bp → lose |

### A2. Why the 5y, not the 2y (or the 10y) — quantified on the Aug-27 curve

The purest Fed instrument is the 2y; the answer to "why not 2s30s?" is horizon: this is a 6–12-month view about the **medium-term policy path**, not the next FOMC. Quantified (DV01-neutral at $20k/bp per leg; carry+roll by aged-bond repricing on the unchanged curve; beta = median deep-cycle peak steepening vs 5s30s from the backtest):

| Pair | Front yield | Gross notional | Static carry+roll, 12m | Deep-cycle peak beta | Character |
|---|---:|---:|---:|---:|---|
| 2s30s | 4.24% | $118.6mm | +29bp | 1.62× | Purest next-FOMC bet; the "carry" IS the hike premium (realized only if no hikes); ~2× the balance sheet |
| **5s30s** | 4.38% | $58.2mm | **+9.8bp** | 1.00× | ~62% of 2s30s's payoff on ~half the gross; carry positive without being purely the Fed bet |
| 10s30s | 4.67% | $38.5mm | +7.5bp | 0.33× | Both legs term-premium duration; keeps a third of the payoff — RV, not the macro trade |

> "I chose 5s30s because five years is long enough to capture a repricing of the medium-term Fed path, while thirty years gives the cleanest exposure to the fiscal, term-premium and structural capital-demand pressures that are increasingly independent of monetary policy."

### A3. Backtest — 5s30s through eight easing cycles (entry at first cut, bp of curve)

Reconstructed quarterly checkpoints from the historical record (underlying series: FRED H.15 daily CMTs; this environment's network policy blocked a live pull — levels ±10–15bp, the 1984-86 cycle ±25–30bp, 30y after Feb-2002 is a long-bond proxy; peaks cross-checked against published anchors). Code and data: `backtest_5s30s_easing_cycles.py`; workbook: `5s30s_Backtest_TenorComparison.xlsx`.

| Cycle | Kind | Cuts (bp) | @T0 | +12m | +24m | Peak Δ | @mo | Worst |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1984–86 | deep, disinflation, no recession | 562 | +30 | +90 | +40 | +90 | 12 | 0 |
| 1989–92 | deep, recession | 681 | −10 | +10 | +70 | +180 | 36 | −15 |
| 1995–96 | shallow, insurance | 75 | +60 | −5 | −10 | +5 | 6 | −10 |
| 1998–99 | shallow → re-hiked | 75 | +80 | **−50** | — | 0 | 0 | −50 |
| 2001–03 | deep, recession | 550 | +55 | +55 | +140 | +195 | 30 | 0 |
| 2007–10 | deep, GFC | 512 | +65 | +70 | +110 | +230 | 38 | 0 |
| 2019–21 | mid-cycle → COVID | 225 | +69 | +30 | +52 | +80 | 20 | −4 |
| 2024–26 | gradual → paused (live) | 175 | +55 | +55 | — | +60 | 15 | −10 |

**Findings that changed the trade above:**

1. **Hit rate 6/8 positive at 12m (median +43bp)**; deep cycles peaked at a median **+180bp**, but at a median **~18 months** — steepeners are marathon trades, which is why positive carry matters.
2. **The failure mode is the shallow cycle**: 1995 went nowhere; 1998 (insurance cuts → re-hike) lost **50bp in a year** — today's bear case, and the reason the stop and the Board-vote falsifier exist.
3. **Target calibration**: +110–120 = regaining the 2025 steepness (the curve traded +101 in Jun-2025, ~+110 late 2025, before 2026 hike pricing flattened it to +81) — it requires cuts to resume, not a recession. +150 sits **below every deep-cycle peak level** (+170 to +295).
4. **Entry context, honestly**: pre-positioning 6 months before first cuts was the historical sweet spot (median +33bp into T0). Entering 23 months in, mid-pause, leans on the 1990-style resolution (pause → recession → mega-steepening) over the 1998-style one (re-hike → flattening). The labor market is what distinguishes them — which is Q1's argument.

### A4. Files

- `backtest_5s30s_easing_cycles.py` — dataset + cycle/tenor analytics (auto-upgrades to daily FRED CSVs when run with network access)
- `carry_roll_tenor_comparison.py` — DV01 sizing and carry+roll by aged-par-bond repricing for 2s30s / 5s30s / 10s30s
- `spread_stats_5s30s.py` — Z-scores / percentiles for the three spreads on 1y and 3y windows (monthly closes; auto-upgrades to daily FRED CSVs)
- `backtest_5s30s_results.csv` — full per-cycle, per-spread results
- `5s30s_Backtest_TenorComparison.xlsx` — Dashboard, Cycle Backtest, Yield Data, Tenor Comparison (all formulas live; computed on open)
