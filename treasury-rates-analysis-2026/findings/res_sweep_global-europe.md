# global-europe

## SUMMARY
Method note: the session's shared WebSearch budget was exhausted after 3 queries (2 returned data), and direct HTTPS egress is policy-blocked, so I pivoted to live, dated data pulled from auto-updating public GitHub datasets: (a) UK DMO daily reference prices (gilt-terminal repo, daily commits May 5-Aug 28; I computed YTMs for the 4.25% 2036 and 5.375% 2056 gilts), (b) the ECB Data Portal euro-area AAA yield-curve dataset (eur-curves repo, daily snapshots Jul 10-Aug 27, validated against ECB published rates), (c) a BoE-API-based UK 30Y tracker, and (d) two dated newsletter-digest archives (Boockvar, Authers/Bloomberg, Goldman, Robin Brooks). No number below is from memory. FINDINGS. Backdrop: the ECB HIKED its deposit rate 25bp to 2.25% on June 11, 2026 (first hike since Sept 2023, citing the Hormuz-linked energy shock) and then held it through the window - a hawkish hold, with some members wanting a further hike and markets pricing a possible September move (Aug 28). The BoE's only decision in the window was July 30: Bank Rate held at 3.75% by 6-3, with the three dissenters voting to HIKE; no August MPC decision appears through Aug 28, and markets priced hikes ahead of the BoE's on-hold baseline. Germany: 10Y Bund averaged 2.97% in June (FRED/OECD), rose 8bp to 3.07% on Jul 7, and printed 3.18% by Aug 25 (~+20bp net), at/near 15-year highs; the euro-area AAA 10Y spot went 3.11% (Jul 10) to 3.28% (Aug 27), with the jump concentrated Aug 14-18. On Aug 18 Germany syndicated EUR4bn of Aug-2056 debt at 3.783% - its highest 30Y funding cost since 2011 - amid record debt supply from the Merz defense/fiscal expansion (H1 sovereign issuance had already topped COVID-era H1 2020). France: 10Y OAT hit a 17-year high of 3.90% on Jul 8 and 4.06% by Aug 25; the OAT-Bund spread widened from ~83bp (Jul 8) to 85.7bp (Aug 21, widest since Jan 2025; Authers called it the widest since 2012) to ~88-90bp (Aug 25-28). French 10Y yields rose above Spain's and above/near Italy's - an inversion of the core-periphery hierarchy. The crisis is chronic-political, not an acute collapse: deficit revised up to 5.2% of GDP, hung three-way parliament since Macron's 2024 snap election, September budget talks looming, Goldman putting Le Pen at 68% for 2027; Fitch affirmed A+/Stable on Aug 28. UK: the biggest mover, driven by domestic politics (Starmer resigned Jun 22; Andy Burnham became PM Jul 20-21; Chancellor Healey's "fiscal flexibility" spooked gilts). 10Y gilt: 4.76% (Jun 30) to 5.11% (Aug 28), +35bp, breaking above the 2022 Truss-crisis peak (5.05-5.07% on Jul 21-23, highest since 2008, highest in the G7). 30Y gilt: 5.45% (Jun 30) to 5.81% (Aug 28), +36bp, peaking at ~5.85% on Aug 18 - reported by Authers/Bloomberg as the highest since 1998 (a BoE-based tracker shows a comparable ~5.90% print on May 15, 2026). GLOBAL VERDICT: yes, unambiguously a global long-end move, with the UK trading AHEAD of the US (July selloff on Burnham) and Europe selling off in sympathy: Jul 8 saw simultaneous multi-decade highs (JGB 10Y 2.87%, OAT 3.90%, gilts ~4.95%, Bunds 3.07%); the week of Aug 17-18 saw US 30Y >5.33% (19-year high), Japan 30Y >4% for the first time ever, UK gilts at 1998 highs and Germany's 2011-high 30Y auction together. Barclays: breakevens flat - it's deficits, AI-related issuance and a changed buyer base, not inflation. Net changes end-June to Aug 27/28: UK 30Y +36bp, UK 10Y +35bp, US 10Y +25bp (4.38 to 4.63), Bund 10Y ~+20bp, OAT ~+16bp with spread +5-7bp, euro AAA 30Y +12bp; policy rates unchanged in-window (ECB 2.25%, BoE 3.75%).

## DATA POINTS
- ECB deposit facility rate (hiked +25bp Jun 11, first since Sep 2023) = 2.25% (2026-06-11) [market-intelligence digest 2026-06-26 (Boockvar/McKinsey items), github.com/eric0205market-bit/market-intelligence]
- ECB deposit facility rate (hawkish pause; some members wanted hike; Sept hike priced) = 2.25% (2026-08-28) [market-intelligence digest 2026-08-28 (Dark Side of the Boom)]
- BoE Bank Rate decision (held, 6-3, 3 votes to hike) = 3.75% (2026-07-30) [market-intelligence digest 2026-07-30 (Boockvar substack)]
- Germany 10Y Bund yield (monthly average, June 2026) = 2.97% (2026-06-30) [FRED IRLTLT01DEM156N via WebSearch]
- Germany 10Y Bund yield (+8bp on day) = 3.07% (2026-07-07) [market-intelligence digest 2026-07-08]
- Germany 10Y Bund yield (vendor stamp) = 3.182% (2026-08-25) [mental-models-observatory daily update 2026-08-26]
- Germany 30Y syndication yield, EUR4bn Aug-2056 (highest since 2011) = 3.783% (2026-08-18) [Bloomberg 2026-08-18 via WebSearch]
- Euro-area AAA 10Y spot (ECB YC dataset) = 3.109% (2026-07-10) [github.com/0scarito/eur-curves (ECB Data Portal)]
- Euro-area AAA 10Y spot = 3.210% (2026-07-21) [github.com/0scarito/eur-curves]
- Euro-area AAA 10Y spot = 3.166% (2026-07-27) [github.com/0scarito/eur-curves]
- Euro-area AAA 10Y spot = 3.146% (2026-08-04) [github.com/0scarito/eur-curves]
- Euro-area AAA 10Y spot = 3.165% (2026-08-12) [github.com/0scarito/eur-curves]
- Euro-area AAA 10Y spot (post-selloff peak) = 3.289% (2026-08-18) [github.com/0scarito/eur-curves]
- Euro-area AAA 10Y spot = 3.277% (2026-08-27) [github.com/0scarito/eur-curves]
- Euro-area AAA 30Y spot = 3.605% (2026-07-10) [github.com/0scarito/eur-curves]
- Euro-area AAA 30Y spot = 3.656% (2026-07-21) [github.com/0scarito/eur-curves]
- Euro-area AAA 30Y spot = 3.594% (2026-08-04) [github.com/0scarito/eur-curves]
- Euro-area AAA 30Y spot = 3.738% (2026-08-18) [github.com/0scarito/eur-curves]
- Euro-area AAA 30Y spot = 3.727% (2026-08-27) [github.com/0scarito/eur-curves]
- France 10Y OAT yield (17-year high, +11bp on day) = 3.90% (2026-07-08) [market-intelligence digest 2026-07-08]
- France 10Y OAT yield (vendor stamp) = 4.064% (2026-08-25) [mental-models-observatory daily update 2026-08-26]
- OAT-Bund 10Y spread (computed from same-day 3.90 vs 3.07) = ~83bp (2026-07-08) [market-intelligence digest 2026-07-08 (computed)]
- OAT-Bund 10Y spread (widest since Jan 2025; Authers dated it widest since 2012) = 85.7bp (2026-08-21) [market-intelligence digests 2026-08-19/2026-08-23 (Dark Side of the Boom, Authers)]
- OAT-Bund 10Y spread (computed 4.064-3.182) = 88.2bp (2026-08-25) [mental-models-observatory 2026-08-26 (computed)]
- OAT-Bund 10Y spread; French spread wider than Italy's; Fitch affirms France A+/Stable = ~90bp (2026-08-28) [mental-models-observatory 2026-08-29; market-intelligence digest 2026-08-28]
- France deficit forecast revised up (budget minister: 'barrel of gunpowder') = 5.2% of GDP (2026-07-07) [market-intelligence digest 2026-07-07]
- UK 10Y gilt yield (YTM 4.25% Treasury Stock 2036, DMO clean mid) = 4.74% (2026-06-26) [github.com/chenjimeng01/gilt-terminal (UK DMO D10B), computed]
- UK 10Y gilt yield (2036 gilt) = 4.76% (2026-06-30) [UK DMO D10B via gilt-terminal, computed]
- UK 10Y gilt yield (2036 gilt) = 4.99% (2026-07-08) [UK DMO D10B via gilt-terminal, computed]
- UK 10Y gilt yield touched two-month high on Burnham becoming PM (above Truss-crisis peak, highest since 2008) = 5.05% (2026-07-21) [market-intelligence digests 2026-07-21]
- UK 10Y gilt yield (14-month high, highest in G7) = 5.07% (2026-07-23) [market-intelligence digest 2026-07-23; mental-models-observatory 2026-07-24]
- UK 10Y gilt yield (2036 gilt) = 4.94% (2026-08-05) [UK DMO D10B via gilt-terminal, computed]
- UK 10Y gilt yield (2036 gilt) = 5.12% (2026-08-18) [UK DMO D10B via gilt-terminal, computed]
- UK 10Y gilt yield (vendor benchmark stamp) = 4.967% (2026-08-25) [mental-models-observatory 2026-08-26]
- UK 10Y gilt yield (2036 gilt) = 5.11% (2026-08-28) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (YTM 5.375% Treasury Gilt 2056, DMO clean mid) = 5.43% (2026-06-26) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (2056 gilt) = 5.45% (2026-06-30) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (2056 gilt) = 5.69% (2026-07-08) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (2056 gilt) = 5.73% (2026-07-14) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield, July peak after Healey 'fiscal flexibility' (press reported 5.78%) = 5.79% (2026-07-23) [UK DMO D10B computed; mental-models-observatory 2026-07-24]
- UK 30Y gilt yield (2056 gilt) = 5.79% (2026-07-30) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (2056 gilt) = 5.66% (2026-08-05) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield (2056 gilt) = 5.79% (2026-08-11) [UK DMO D10B via gilt-terminal, computed]
- UK 30Y gilt yield - window high; Authers/Bloomberg: UK gilts highest since 1998 (multi-decade high). Caveat: BoE-based tracker shows comparable ~5.90% on 2026-05-15 = 5.85% (2026-08-18) [UK DMO D10B computed; Bloomberg Opinion (Authers) 2026-08-18; github.com/fairhurstbuckley/gilt-tracker (BoE IADB)]
- UK 30Y gilt yield (2056 gilt) = 5.81% (2026-08-28) [UK DMO D10B via gilt-terminal, computed]
- US 10Y Treasury yield = 4.38% (2026-06-30) [market-intelligence digest 2026-06-30]
- US 10Y Treasury yield (vendor stamp) = 4.634% (2026-08-25) [mental-models-observatory 2026-08-26]
- US 30Y Treasury yield (19-year/2007 high, same day as German 2011-high 30Y auction) = >5.33% (2026-08-18) [CNBC 2026-08-18 via WebSearch; Bloomberg Opinion (Authers)]
- Japan 30Y JGB yield above 4% for first time in its 27-year history = >4.00% (2026-08-18) [Bloomberg Opinion (Authers) via market-intelligence digest 2026-08-18]
- Japan 10Y JGB yield (29-year high, same global selloff day as OAT/gilt/Bund highs) = 2.87% (2026-07-07) [market-intelligence digest 2026-07-08]
- Net change UK 30Y gilt, Jun 30 - Aug 28 = +36bp (5.45 to 5.81; peak +40bp Aug 18) (2026-08-28) [computed from UK DMO D10B series]
- Net change UK 10Y gilt, Jun 30 - Aug 28 = +35bp (4.76 to 5.11) (2026-08-28) [computed from UK DMO D10B series]
- Net change Germany 10Y Bund, end-June - Aug 25 = ~+20bp (2.97-3.0 to 3.18); euro AAA 10Y +17bp Jul 10-Aug 27 (2026-08-27) [computed from FRED, digests, ECB YC dataset]
- Net change France 10Y OAT, Jul 8 - Aug 25, and OAT-Bund spread = +16bp (3.90 to 4.06); spread +5-7bp (83 to 88-90bp) (2026-08-28) [computed from digests and observatory stamps]

## SOURCES
- https://www.bloomberg.com/news/articles/2026-08-18/germany-is-set-to-sell-30-year-bonds-at-highest-yield-since-2011
- https://www.cnbc.com/2026/08/18/treasury-yields-.html
- https://fred.stlouisfed.org/series/IRLTLT01DEM156N
- https://tradingeconomics.com/germany/government-bond-yield
- https://github.com/chenjimeng01/gilt-terminal (UK DMO D10B daily reference prices, daily commits May 5-Aug 28, 2026; YTMs computed from clean mid prices)
- https://github.com/0scarito/eur-curves (ECB Data Portal dataset YC, euro-area AAA Svensson curve, daily snapshots Jul 10-Aug 27, 2026)
- https://github.com/fairhurstbuckley/gilt-tracker (Bank of England IADB 30Y gilt series, benchmark-adjusted to CNBC/FT quote, through Aug 26, 2026)
- https://github.com/eric0205market-bit/market-intelligence (dated daily digests of Boockvar, Authers/Bloomberg Opinion, Goldman, Rosenberg, Dark Side of the Boom; May 9-Aug 29, 2026)
- https://github.com/jacksonshapiro11/mental-models-observatory (daily updates incl. 2026-08-26 same-day yield stamps and 2026-08-29 Fitch/France item)
- https://www.bloomberg.com/opinion/newsletters/2026-08-18/the-30-year-itch-comes-for-bonds-and-brazil
- https://peterboockvar.substack.com/p/boe-scores-it-6-3-no-hikesavings
- https://thedarksideoftheboom.substack.com/p/hot-take-the-euros-problem-is-france
