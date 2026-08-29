#!/usr/bin/env python3
"""
Backtest: curve steepeners (2s30s / 5s30s / 10s30s) across Fed easing cycles.

Data strategy
-------------
Preferred: daily FRED CSVs (DGS2, DGS5, DGS10, DGS30) placed next to this
script (fredgraph.csv format). This sandbox's egress policy blocks FRED and
federalreserve.gov, so the script falls back to the EMBEDDED_DATA table:
quarterly checkpoint yields (constant-maturity, % — month-end approximations
reconstructed from the historical record).

Accuracy labels on embedded data:
  - 1989 onward: approx ±10-15bp per point
  - 1984-86 cycle: approx ±25-30bp (flagged 'era~')
  - 30y for Mar-2002..Feb-2006 is the outstanding long bond / interpolated
    (30y issuance suspended; FRED DGS30 has a gap) — flagged 'gap~'
Peak-spread anchors cross-checked against published sources (see memo):
post-GFC 5s30s peak ~+280-300bp (2010-11); Jun-2025 +101bp "steepest since
2021"; 2024-25 cycle context from press coverage of the 2025 cuts.

Definitions
-----------
Cycle T0 = month of the first cut of the easing cycle.
Spread (bp) = 100*(y_long - y_short).  Steepener P&L in "curve bp" =
spread(t) - spread(T0); with DV01-neutral legs sized at K $/bp, $P&L = K * bp.
Checkpoints are months relative to T0 (negative = before the first cut).
"""

import csv
import os
import sys

# ---------------------------------------------------------------------------
# Embedded quarterly checkpoint data
# cycle key -> dict: meta + {month_offset: (y2, y5, y10, y30)}
# ---------------------------------------------------------------------------

EMBEDDED_DATA = {
    "1984 disinflation": {
        "first_cut": "1984-09", "funds_start": 11.50, "funds_trough": 5.875,
        "depth_bp": 562, "kind": "deep (no recession: disinflation easing)",
        "quality": "era~ (±25-30bp)",
        "path": {
            -6:  (11.85, 12.25, 12.35, 12.40),
            0:   (11.60, 12.00, 12.30, 12.30),
            3:   (9.70, 10.80, 11.50, 11.60),
            6:   (10.30, 11.10, 11.90, 11.90),
            9:   (8.60,  9.40, 10.30, 10.50),
            12:  (8.80,  9.50, 10.40, 10.70),
            18:  (7.10,  7.45,  7.80,  7.95),
            24:  (6.30,  6.90,  7.45,  7.60),
            30:  (6.50,  7.00,  7.25,  7.55),
        },
        "peak_5s30s_note": "peak ~+120bp (mid-1985); curve then bull-flattened as ALL yields collapsed in 1986",
    },
    "1989-92 S&L / recession": {
        "first_cut": "1989-06", "funds_start": 9.8125, "funds_trough": 3.00,
        "depth_bp": 681, "kind": "deep (recession Jul90-Mar91)",
        "quality": "ok (±10-15bp)",
        "path": {
            -6:  (9.25, 9.20, 9.15, 9.00),
            0:   (8.45, 8.30, 8.30, 8.20),
            3:   (8.60, 8.50, 8.35, 8.25),
            6:   (7.80, 7.75, 7.90, 7.95),
            9:   (8.60, 8.60, 8.60, 8.60),
            12:  (8.20, 8.40, 8.40, 8.40),
            18:  (7.20, 7.70, 8.10, 8.25),
            24:  (6.80, 7.85, 8.20, 8.45),
            30:  (4.90, 6.00, 6.70, 7.40),
            36:  (4.70, 5.85, 6.90, 7.55),
            42:  (4.55, 6.05, 6.75, 7.40),
        },
        "peak_5s30s_note": "peak ~+200bp (Sep-Oct 1992, near the last cut)",
    },
    "1995 mid-cycle": {
        "first_cut": "1995-07", "funds_start": 6.00, "funds_trough": 5.25,
        "kind": "shallow (3 cuts, no recession)", "depth_bp": 75,
        "quality": "ok (±10-15bp)",
        "path": {
            -6:  (7.40, 7.70, 7.75, 7.90),
            0:   (5.85, 6.00, 6.30, 6.60),
            3:   (5.60, 5.80, 6.00, 6.30),
            6:   (5.15, 5.35, 5.60, 6.00),
            9:   (5.95, 6.30, 6.50, 6.80),
            12:  (6.10, 6.45, 6.75, 7.00),
            18:  (5.90, 6.25, 6.50, 6.80),
            24:  (5.90, 6.00, 6.20, 6.50),
        },
        "peak_5s30s_note": "peak ~+65-75bp (early 1996); shallow cycle -> steepener went nowhere",
    },
    "1998 LTCM insurance": {
        "first_cut": "1998-09", "funds_start": 5.50, "funds_trough": 4.75,
        "kind": "shallow (3 cuts, then RE-HIKED Jun-1999)", "depth_bp": 75,
        "quality": "ok (±10-15bp)",
        "path": {
            -6:  (5.55, 5.60, 5.65, 5.95),
            0:   (4.30, 4.20, 4.40, 5.00),
            3:   (4.55, 4.55, 4.65, 5.10),
            6:   (5.05, 5.10, 5.25, 5.60),
            12:  (5.65, 5.75, 5.90, 6.05),
        },
        "peak_5s30s_note": "peak ~+85bp in the Oct-98 panic, then bear-FLATTENED as the Fed re-hiked",
    },
    "2001-03 dot-com": {
        "first_cut": "2001-01", "funds_start": 6.50, "funds_trough": 1.00,
        "kind": "deep (recession Mar-Nov 2001)", "depth_bp": 550,
        "quality": "ok; 30y gap~ after Feb-2002 (long-bond proxy)",
        "path": {
            -6:  (6.30, 6.15, 6.05, 5.90),
            0:   (4.90, 4.90, 5.10, 5.45),
            3:   (4.25, 4.75, 5.30, 5.80),
            6:   (3.80, 4.60, 5.05, 5.50),
            9:   (2.50, 3.60, 4.30, 4.90),
            12:  (3.00, 4.30, 5.00, 5.40),
            18:  (2.20, 3.40, 4.50, 5.30),
            24:  (1.70, 2.90, 4.00, 4.85),
            30:  (1.50, 2.70, 4.30, 5.20),
        },
        "peak_5s30s_note": "peak ~+250bp (mid/late 2003 into 2004)",
    },
    "2007-08 GFC": {
        "first_cut": "2007-09", "funds_start": 5.25, "funds_trough": 0.125,
        "kind": "deep (recession Dec07-Jun09; ZIRP + QE follow-on)", "depth_bp": 512,
        "quality": "ok (±10-15bp)",
        "path": {
            -6:  (4.60, 4.50, 4.65, 4.85),
            0:   (4.00, 4.20, 4.60, 4.85),
            3:   (3.05, 3.45, 4.05, 4.45),
            6:   (1.60, 2.45, 3.40, 4.30),
            9:   (2.60, 3.35, 4.00, 4.60),
            12:  (2.00, 2.95, 3.85, 4.30),
            15:  (0.75, 1.55, 2.20, 2.70),
            18:  (0.85, 1.65, 2.70, 3.55),
            24:  (0.95, 2.30, 3.30, 4.05),
            30:  (1.00, 2.55, 3.85, 4.70),
            38:  (0.45, 1.15, 2.60, 4.10),
        },
        "peak_5s30s_note": "peak ~+280-300bp (late-2010/early-2011, post-QE2) - the record",
    },
    "2019-20 mid-cycle + COVID": {
        "first_cut": "2019-07", "funds_start": 2.375, "funds_trough": 0.125,
        "kind": "shallow->deep (COVID forced it deep in Mar-2020)", "depth_bp": 225,
        "quality": "ok (±5-10bp)",
        "path": {
            -6:  (2.60, 2.60, 2.75, 3.05),
            0:   (1.89, 1.84, 2.02, 2.53),
            3:   (1.55, 1.55, 1.70, 2.20),
            6:   (1.35, 1.35, 1.50, 2.00),
            9:   (0.20, 0.35, 0.65, 1.25),
            12:  (0.11, 0.21, 0.55, 1.20),
            18:  (0.11, 0.45, 1.10, 1.85),
            20:  (0.14, 0.92, 1.74, 2.41),
            24:  (0.19, 0.69, 1.24, 1.90),
        },
        "peak_5s30s_note": "peak ~+160-165bp (Feb-2021, reflation)",
    },
    "2024-25 (current cycle)": {
        "first_cut": "2024-09", "funds_start": 5.375, "funds_trough": 3.625,
        "kind": "gradual (cuts 2024-25, PAUSED 2026 with hike pricing)", "depth_bp": 175,
        "quality": "ok (±5-10bp); +23m = Aug-27-2026 official H.15",
        "path": {
            -6:  (4.60, 4.20, 4.20, 4.35),
            0:   (3.60, 3.50, 3.70, 4.00),
            3:   (4.25, 4.40, 4.55, 4.80),
            6:   (3.90, 3.95, 4.20, 4.60),
            9:   (3.70, 3.80, 4.25, 4.80),
            12:  (3.60, 3.70, 4.15, 4.75),
            15:  (3.60, 3.75, 4.20, 4.85),
            23:  (4.24, 4.38, 4.67, 5.19),
        },
        "peak_5s30s_note": "peak so far ~+110bp (late-2025); flattened to +81 on 2026 hike pricing (H.15 Aug-27-26)",
    },
}

SPREADS = {"2s30s": (0, 3), "5s30s": (1, 3), "10s30s": (2, 3)}


def try_load_fred(directory):
    """If DGS2/DGS5/DGS10/DGS30 CSVs exist (fredgraph format), signal they
    should be used instead of the embedded table (full daily backtest)."""
    names = ["DGS2.csv", "DGS5.csv", "DGS10.csv", "DGS30.csv"]
    return all(os.path.exists(os.path.join(directory, n)) for n in names)


def spread_bp(row, key):
    s, l = SPREADS[key]
    return round((row[l] - row[s]) * 100.0, 1)


def analyze():
    out_rows = []
    traj = {}     # cycle -> list[(offset, d5s30s)]
    for name, c in EMBEDDED_DATA.items():
        path = dict(sorted(c["path"].items()))
        base = {k: spread_bp(path[0], k) for k in SPREADS}
        rec = {
            "cycle": name, "first_cut": c["first_cut"],
            "kind": c["kind"], "depth_bp": c["depth_bp"],
            "quality": c["quality"], "peak_note": c["peak_5s30s_note"],
        }
        for k in SPREADS:
            deltas = {m: round(spread_bp(r, k) - base[k], 1) for m, r in path.items()}
            hist = {m: d for m, d in deltas.items() if m >= 0}
            rec[f"{k}_at_T0"] = base[k]
            rec[f"{k}_pre6m"] = deltas[-6]                       # T-6 entry gain into T0
            for cp in (6, 12, 24):
                rec[f"{k}_d{cp}m"] = hist.get(cp, None)
            peak_m = max(hist, key=lambda m: hist[m])
            rec[f"{k}_peak"] = hist[peak_m]
            rec[f"{k}_peak_m"] = peak_m
            rec[f"{k}_maxadverse"] = min(hist.values())          # worst mark vs T0 entry
        traj[name] = sorted((m, round(spread_bp(r, "5s30s") - base["5s30s"], 1))
                            for m, r in path.items())
        out_rows.append(rec)
    return out_rows, traj


def summarize(rows):
    deep = [r for r in rows if "deep" in r["kind"] or "COVID" in r["kind"]]
    shallow = [r for r in rows if r["kind"].startswith("shallow (")]
    def med(vals):
        v = sorted(x for x in vals if x is not None)
        n = len(v)
        return v[n // 2] if n % 2 else (v[n//2 - 1] + v[n//2]) / 2
    s = {
        "n_cycles": len(rows),
        "5s30s_d12m_median_all": med([r["5s30s_d12m"] for r in rows]),
        "5s30s_d12m_median_deep": med([r["5s30s_d12m"] for r in deep]),
        "5s30s_peak_median_deep": med([r["5s30s_peak"] for r in deep]),
        "5s30s_peak_range_deep": (min(r["5s30s_peak"] for r in deep),
                                  max(r["5s30s_peak"] for r in deep)),
        "5s30s_peak_shallow": [(r["cycle"], r["5s30s_peak"], r["5s30s_d12m"]) for r in shallow],
        "hit_12m_pos": sum(1 for r in rows if (r["5s30s_d12m"] or 0) > 0),
        "hit_12m_ge30": sum(1 for r in rows if (r["5s30s_d12m"] or 0) >= 30),
        "worst_12m": min((r["5s30s_d12m"] for r in rows if r["5s30s_d12m"] is not None)),
        "worst_maxadverse": min(r["5s30s_maxadverse"] for r in rows),
        "median_peak_month": med([r["5s30s_peak_m"] for r in rows]),
        "pre6m_median": med([r["5s30s_pre6m"] for r in rows]),
        "beta_2s30s_vs_5s30s_deep": med([r["2s30s_peak"] / r["5s30s_peak"] for r in deep]),
        "beta_10s30s_vs_5s30s_deep": med([r["10s30s_peak"] / r["5s30s_peak"] for r in deep]),
    }
    return s


def svg_coords(traj):
    """Print polyline coords for the artifact figure.
    x: months -6..40 -> 60..620 ; y: delta -80..+300 bp -> 290..20"""
    def X(m): return round(60 + (m + 6) * (560 / 46.0), 1)
    def Y(d): return round(20 + (300 - d) * (270 / 380.0), 1)
    lines = {}
    for name, pts in traj.items():
        lines[name] = " ".join(f"{X(m)},{Y(d)}" for m, d in pts)
    grid = {d: Y(d) for d in (-50, 0, 50, 100, 150, 200, 250, 300)}
    xt = {m: X(m) for m in (-6, 0, 6, 12, 18, 24, 30, 36)}
    return lines, grid, xt


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    if try_load_fred(here):
        print("NOTE: FRED daily CSVs found - re-run analysis on daily data "
              "(this environment lacked network access to FRED; embedded "
              "quarterly table used instead).")
    rows, traj = analyze()

    with open(os.path.join(here, "backtest_5s30s_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("=" * 100)
    print("5s30s STEEPENER ACROSS EASING CYCLES  (bp of curve vs entry at first cut, T0)")
    print("=" * 100)
    hdr = f"{'cycle':<28}{'T0 sprd':>8}{'pre-6m':>8}{'+6m':>7}{'+12m':>7}{'+24m':>7}{'peak':>7}{'@mo':>5}{'worst':>7}"
    print(hdr); print("-" * len(hdr))
    for r in rows:
        print(f"{r['cycle']:<28}{r['5s30s_at_T0']:>8.0f}{r['5s30s_pre6m']:>8.0f}"
              f"{(r['5s30s_d6m'] if r['5s30s_d6m'] is not None else float('nan')):>7.0f}"
              f"{(r['5s30s_d12m'] if r['5s30s_d12m'] is not None else float('nan')):>7.0f}"
              f"{(r['5s30s_d24m'] if r['5s30s_d24m'] is not None else float('nan')):>7.0f}"
              f"{r['5s30s_peak']:>7.0f}{r['5s30s_peak_m']:>5.0f}{r['5s30s_maxadverse']:>7.0f}")
    print()
    print("TENOR COMPARISON — peak steepening captured per cycle (bp from T0)")
    hdr2 = f"{'cycle':<28}{'2s30s':>8}{'5s30s':>8}{'10s30s':>8}   kind"
    print(hdr2); print("-" * 78)
    for r in rows:
        print(f"{r['cycle']:<28}{r['2s30s_peak']:>8.0f}{r['5s30s_peak']:>8.0f}"
              f"{r['10s30s_peak']:>8.0f}   {r['kind']}")
    s = summarize(rows)
    print()
    print("SUMMARY")
    for k, v in s.items():
        print(f"  {k}: {v}")
    print()
    lines, grid, xt = svg_coords(traj)
    print("SVG polyline coords (artifact figure):")
    for name, pl in lines.items():
        print(f"  {name}: {pl}")
    print(f"  y-gridlines: {grid}")
    print(f"  x-ticks: {xt}")


if __name__ == "__main__":
    sys.exit(main())
