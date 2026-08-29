#!/usr/bin/env python3
"""
2s30s vs 5s30s vs 10s30s on the actual Aug-27/28-2026 curve:
DV01-neutral sizing, and carry+rolldown done properly — each leg is priced as
a par bond today, then REPRICED as an aged bond on today's (unchanged) curve
at the horizon, with financing at repo. No coupon-minus-repo shortcut.

Curve: official H.15 Aug-27-2026 CMTs where known (2y 4.24, 5y 4.38,
10y 4.67, 20y 5.18, 30y 5.19); 1y/3y/7y interpolated estimates (flagged).
Funding: SOFR/GC repo assumed 3.65% (funds 3.50-3.75). All semiannual comp.

Caveats stated up front: ignores repo specialness, financing bid/offer,
futures CTD/calendar-roll costs, and the fact that "unchanged curve" is
itself a scenario — at the 2y point the rolldown IS the hike premium, so
static carry there is only realized if the Fed does not hike.
"""

CURVE = {0.0: 3.65, 1.0: 4.08, 2.0: 4.24, 3.0: 4.29, 5.0: 4.38,
         7.0: 4.51, 10.0: 4.67, 20.0: 5.18, 30.0: 5.19}
EST = {1.0, 3.0, 7.0}          # interpolated, not official H.15
REPO = 3.65
DV01_TARGET = 20_000.0         # $/bp per leg


def yld(t):
    ks = sorted(CURVE)
    if t <= ks[0]:
        return CURVE[ks[0]]
    for a, b in zip(ks, ks[1:]):
        if a <= t <= b:
            w = (t - a) / (b - a)
            return CURVE[a] * (1 - w) + CURVE[b] * w
    return CURVE[ks[-1]]


def price(coupon, y, years):
    """Clean price per 100 face, semiannual coupon/comp; fractional first period ok."""
    n = int(round(years * 2))
    assert abs(years * 2 - n) < 1e-9, "keep maturities on the semiannual grid"
    per = y / 200.0
    c = coupon / 2.0
    pv = sum(c / (1 + per) ** i for i in range(1, n + 1))
    pv += 100.0 / (1 + per) ** n
    return pv


def dv01_bp(coupon, y, years):
    up = price(coupon, y + 0.01, years)
    dn = price(coupon, y - 0.01, years)
    return (dn - up) / 2.0          # per 100 face, per 1bp


def leg_stats(tenor, horizon):
    y0 = yld(tenor)
    c = y0                          # par bond
    p0 = 100.0
    d0 = dv01_bp(c, y0, tenor)      # $ per bp per $100 face -> per $1mm: *10,000
    dv01_per_mm = d0 * 10_000
    face_mm = DV01_TARGET / dv01_per_mm
    # age the bond: horizon years pass, curve unchanged
    t1 = tenor - horizon
    y1 = yld(t1)
    p1 = price(c, y1, t1)
    coupon_income = c * horizon
    financing = REPO * horizon
    tr_pct = (p1 - p0) + coupon_income - financing      # % of face, financed TR
    tr_usd = tr_pct / 100.0 * face_mm * 1e6
    return dict(tenor=tenor, y=y0, dv01_per_mm=dv01_per_mm, face_mm=face_mm,
                y_aged=y1, px_aged=p1, tr_pct=tr_pct, tr_usd=tr_usd)


def pair(short_tenor, horizon=1.0):
    lg = leg_stats(short_tenor, horizon)          # long the shorter tenor
    sh = leg_stats(30.0, horizon)                 # short 30y
    net_usd = lg["tr_usd"] - sh["tr_usd"]
    net_curve_bp = net_usd / DV01_TARGET
    return lg, sh, net_usd, net_curve_bp


BETA = {2.0: 1.62, 5.0: 1.00, 10.0: 0.33}         # deep-cycle peak beta vs 5s30s (backtest)

print("Curve used (H.15 Aug-27-26; * = interpolated estimate):")
print("  " + "  ".join(f"{int(k) if k==int(k) else k}y {v:.2f}{'*' if k in EST else ''}"
                       for k, v in sorted(CURVE.items()) if k > 0))
print(f"  funding (repo) {REPO:.2f}%   DV01 per leg ${DV01_TARGET:,.0f}/bp\n")

hdr = (f"{'pair':<8}{'front yld':>10}{'face $mm':>10}{'x30y face':>10}"
       f"{'gross $mm':>10}{'carry+roll 12m':>16}{'6m':>8}{'hist beta':>10}")
print(hdr)
print("-" * len(hdr))
rows = []
for t in (2.0, 5.0, 10.0):
    lg, sh, usd, bp = pair(t, 1.0)
    _, _, usd3, bp3 = pair(t, 0.5)
    gross = lg["face_mm"] + sh["face_mm"]
    rows.append((t, lg, sh, usd, bp, bp3, gross))
    print(f"{int(t)}s30s{'':<3}{lg['y']:>9.2f}%{lg['face_mm']:>10.1f}{sh['face_mm']:>10.1f}"
          f"{gross:>10.1f}{bp:>+10.1f}bp ${usd/1000:>+6.0f}k{bp3:>+7.1f}bp{BETA[t]:>10.2f}x")

print("""
Reading:
 - carry+roll = financed 12m total return of both legs, curve unchanged, in
   curve-bp (divide $ by the $20k/bp DV01). At the 2y, most of that "carry"
   is the priced hike premium — it is only realized if the Fed doesn't hike:
   static carry at the front IS the trade, not a bonus.
 - hist beta = median deep-cycle peak steepening vs 5s30s (backtest table).
 - gross $mm = balance-sheet usage for the same curve DV01.""")
