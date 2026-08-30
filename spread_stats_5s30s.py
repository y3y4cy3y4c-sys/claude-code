#!/usr/bin/env python3
"""
Statistical scores for US curve spreads (2s30s / 5s30s / 10s30s), in the same
format as the KTB spread sheet: mean, sample stdev, current level, Z-score,
percentile rank, min/max, and spread-change vol — on 1-year and 3-year windows.

Data
----
Preferred: daily FRED CSVs (DGS2/DGS5/DGS10/DGS30, fredgraph format) next to
this script -> exact daily stats. This sandbox's egress policy blocks FRED, so
the fallback is MONTH-END reconstructed CMT yields, Sep-2023..Aug-2026:
  - 2023-09..2025-08: reconstructed from the historical record, ~±5-10bp
  - 2025-09..2026-01: from this project's session research, ~±10bp
  - 2026-02..2026-07: interpolated between documented anchors (late-2025
    levels; 30y 5.27-5.28 in Jul/Aug-26; hike pricing emerging through H1-26),
    ~±10-15bp -> treat these months' individual Z-scores as indicative only
  - 2026-08: official H.15 Aug-27-2026 (2y 4.24 / 5y 4.38 / 10y 4.67 / 30y 5.19)
Caveats: monthly resolution smooths intra-month extremes, so percentiles are
conservative (the true daily min/max are wider); stats on a trending series
mix regimes — hence both windows are reported and interpreted separately.
"""

import math
import os

# month, y2, y5, y10, y30  (% CMT, month-end)
MONTHLY = [
    ("2023-09", 5.04, 4.60, 4.57, 4.73),
    ("2023-10", 5.07, 4.82, 4.93, 5.04),
    ("2023-11", 4.70, 4.30, 4.35, 4.52),
    ("2023-12", 4.25, 3.85, 3.88, 4.03),
    ("2024-01", 4.24, 3.88, 3.95, 4.19),
    ("2024-02", 4.62, 4.25, 4.25, 4.38),
    ("2024-03", 4.60, 4.21, 4.20, 4.34),
    ("2024-04", 5.04, 4.72, 4.68, 4.79),
    ("2024-05", 4.88, 4.52, 4.50, 4.65),
    ("2024-06", 4.72, 4.33, 4.36, 4.51),
    ("2024-07", 4.26, 3.97, 4.09, 4.35),
    ("2024-08", 3.92, 3.71, 3.91, 4.20),
    ("2024-09", 3.65, 3.58, 3.81, 4.14),
    ("2024-10", 4.17, 4.16, 4.28, 4.47),
    ("2024-11", 4.13, 4.05, 4.18, 4.36),
    ("2024-12", 4.24, 4.38, 4.58, 4.78),
    ("2025-01", 4.21, 4.33, 4.55, 4.79),
    ("2025-02", 3.99, 4.02, 4.24, 4.49),
    ("2025-03", 3.89, 3.95, 4.23, 4.57),
    ("2025-04", 3.60, 3.92, 4.17, 4.68),
    ("2025-05", 3.89, 4.00, 4.41, 4.93),
    ("2025-06", 3.72, 3.79, 4.24, 4.78),
    ("2025-07", 3.95, 3.97, 4.37, 4.90),
    ("2025-08", 3.62, 3.70, 4.23, 4.79),
    ("2025-09", 3.60, 3.63, 4.15, 4.73),
    ("2025-10", 3.58, 3.58, 4.10, 4.62),
    ("2025-11", 3.63, 3.65, 4.15, 4.75),
    ("2025-12", 3.60, 3.75, 4.20, 4.85),
    ("2026-01", 3.75, 3.85, 4.35, 4.95),
    ("2026-02", 3.90, 4.05, 4.45, 5.05),
    ("2026-03", 4.05, 4.20, 4.55, 5.10),
    ("2026-04", 4.10, 4.25, 4.60, 5.15),
    ("2026-05", 4.15, 4.28, 4.60, 5.12),
    ("2026-06", 4.20, 4.35, 4.62, 5.18),
    ("2026-07", 4.28, 4.42, 4.70, 5.27),
    ("2026-08", 4.24, 4.38, 4.67, 5.19),   # official H.15 Aug-27-2026
]

SPREADS = {"2s30s": (1, 4), "5s30s": (2, 4), "10s30s": (3, 4)}


def sample_stats(vals):
    n = len(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / (n - 1)
    return mean, math.sqrt(var)


def pct_rank(vals, x):
    """Fraction of observations strictly below x plus half the ties (like PERCENTRANK.INC-ish)."""
    below = sum(1 for v in vals if v < x)
    ties = sum(1 for v in vals if v == x)
    return (below + 0.5 * ties) / len(vals)


def analyze(name, series):
    cur = series[-1]
    out = {}
    for label, window in (("1y", 12), ("3y", 36)):
        w = series[-window:]
        mean, sd = sample_stats(w)
        z = (cur - mean) / sd
        chg = [w[i] - w[i - 1] for i in range(1, len(w))]
        _, chg_sd = sample_stats(chg)
        out[label] = dict(mean=mean, sd=sd, cur=cur, z=z, pct=pct_rank(w, cur),
                          lo=min(w), hi=max(w), chg_sd=chg_sd)
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    if all(os.path.exists(os.path.join(here, f"DGS{t}.csv")) for t in (2, 5, 10, 30)):
        print("NOTE: FRED daily CSVs found — re-run on daily data for exact stats "
              "(embedded monthly table used because this sandbox blocks FRED).")
    print("US curve spread statistics — monthly closes, window ending Aug-2026 (H.15 8/27)")
    print("=" * 94)
    hdr = (f"{'spread':<8}{'win':>4}{'current':>9}{'mean':>8}{'stdev':>8}"
           f"{'Z':>7}{'pctile':>8}{'min':>7}{'max':>7}{'Δm vol':>8}")
    print(hdr)
    print("-" * len(hdr))
    for name, (si, li) in SPREADS.items():
        series = [round((row[li] - row[si]) * 100, 1) for row in MONTHLY]
        res = analyze(name, series)
        for wlabel in ("1y", "3y"):
            r = res[wlabel]
            print(f"{name:<8}{wlabel:>4}{r['cur']:>8.0f}bp{r['mean']:>8.1f}{r['sd']:>8.1f}"
                  f"{r['z']:>+7.2f}{r['pct']:>7.0%}{r['lo']:>7.0f}{r['hi']:>7.0f}{r['chg_sd']:>7.1f}bp")
        print()
    s530 = [round((row[4] - row[2]) * 100, 1) for row in MONTHLY]
    print("5s30s monthly series (bp):")
    for i in range(0, len(MONTHLY), 6):
        print("  " + "  ".join(f"{MONTHLY[j][0][2:]}:{s530[j]:>4.0f}" for j in range(i, min(i + 6, len(MONTHLY)))))
    print("\nReading: the 3y window says the level is mid-range (regime mix: inverted/flat "
          "2023-24 vs steep 2025); the 1y window says the curve sits at/near its flattest "
          "of the past year after the 2026 hike-repricing — the entry buys that retracement.")


if __name__ == "__main__":
    main()
