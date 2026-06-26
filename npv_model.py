"""
Professional NPV Model — HPC Data Center Infrastructure
Supports two project types:
  1. Colocation / HPC Lease  (CIFR, WULF style)
  2. AI Cloud / GPU-as-a-Service (IREN style)

Usage:
  Define projects in PROJECTS list at the bottom, then run:
    python npv_model.py
"""

from dataclasses import dataclass, field
from typing import Optional
import math

# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ColoProject:
    """
    Colocation / HPC Lease project (CIFR / WULF style).
    Revenue = rent from hyperscaler tenant under NNN lease.
    """
    name: str
    company: str

    # Revenue inputs
    annual_revenue_mm: float          # $mm/yr contracted rent
    lease_term_years: int             # base lease term
    cod_year: int                     # commercial operation date (year)

    # Cost & margin inputs
    noi_margin: float                 # NOI as % of revenue (e.g. 0.85 for triple-net)
    remaining_capex_mm: float         # remaining construction capex ($mm)

    # Financing inputs
    project_debt_mm: float            # project-level debt ($mm)
    ltc_ratio: float                  # loan-to-cost ratio (e.g. 0.85)

    # Discount rate
    discount_rate: float              # WACC or required return (e.g. 0.10)

    # Risk adjustments (for unsigned / pipeline deals)
    prob_signing: float = 1.0         # probability lease gets signed (0–1)
    prob_cod: float = 1.0             # probability project reaches COD (0–1)

    # Extension / renewal
    extension_years: int = 0          # optional renewal period (years)
    extension_revenue_haircut: float  = 0.80  # renewal rent as % of base rent
    prob_extension: float = 0.50      # probability tenant renews

    # Base year for discounting (today)
    base_year: int = 2026

    # Optional label
    status: str = ""


@dataclass
class CloudProject:
    """
    AI Cloud / GPU-as-a-Service project (IREN style).
    Revenue = cloud compute contract ($/GPU-hr or contracted ARR).
    """
    name: str
    company: str

    # Revenue inputs
    contracted_arr_mm: float          # contracted annual recurring revenue ($mm)
    contract_term_years: int          # contract term (years)
    cod_year: int                     # when revenue begins

    # GPU capex inputs
    gpu_capex_mm: float               # initial GPU purchase cost ($mm)
    gpu_useful_life_years: int        # depreciation / replacement cycle (years)
    replacement_capex_pct: float      # replacement capex as % of initial each cycle

    # Operating cost inputs
    power_cost_mm_yr: float           # annual power cost ($mm)
    dc_opex_mm_yr: float              # annual data center operating cost ($mm)
    software_support_mm_yr: float     # software / support cost ($mm/yr)

    # Utilization
    utilization_rate: float           # % of ARR actually realized (0–1)

    # Discount rate
    discount_rate: float              # WACC or required return

    # Financing
    debt_mm: float = 0.0              # debt against GPU / infrastructure
    interest_rate: float = 0.06       # interest rate on debt

    # Risk adjustments
    prob_signing: float = 1.0
    prob_cod: float = 1.0

    # Renewal
    renewal_years: int = 0
    renewal_arr_haircut: float = 0.80
    prob_renewal: float = 0.50

    # Base year
    base_year: int = 2026

    status: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def annuity_factor(rate: float, periods: int) -> float:
    """Present value annuity factor."""
    if rate == 0:
        return periods
    return (1 - (1 + rate) ** -periods) / rate


def discount_factor(rate: float, years_from_now: float) -> float:
    """Single period discount factor."""
    return 1 / (1 + rate) ** years_from_now


def calc_colo_npv(p: ColoProject) -> dict:
    """Calculate NPV for a colocation / HPC lease project."""
    results = {}
    years_to_cod = p.cod_year - p.base_year

    # ── Annual cash flows ──────────────────────────────────────────────────
    annual_noi = p.annual_revenue_mm * p.noi_margin

    # ── Base lease PV ─────────────────────────────────────────────────────
    # Annuity factor for lease term, then discounted back to today
    pv_noi_at_cod = annual_noi * annuity_factor(p.discount_rate, p.lease_term_years)
    pv_noi_today  = pv_noi_at_cod * discount_factor(p.discount_rate, years_to_cod)

    # ── Extension / renewal PV ────────────────────────────────────────────
    renewal_noi = annual_noi * p.extension_revenue_haircut
    pv_renewal_at_cod = (
        renewal_noi
        * annuity_factor(p.discount_rate, p.extension_years)
        * discount_factor(p.discount_rate, p.lease_term_years)  # starts after base term
    )
    pv_renewal_today = pv_renewal_at_cod * discount_factor(p.discount_rate, years_to_cod)
    risked_pv_renewal = pv_renewal_today * p.prob_extension

    # ── Total project value ───────────────────────────────────────────────
    gross_project_value = pv_noi_today + risked_pv_renewal

    # ── Unlevered project NPV ─────────────────────────────────────────────
    unlevered_npv = gross_project_value - p.remaining_capex_mm

    # ── Equity NPV (levered) ──────────────────────────────────────────────
    equity_invested = p.remaining_capex_mm * (1 - p.ltc_ratio)
    levered_npv = gross_project_value - p.project_debt_mm - equity_invested

    # ── Risk-adjust for pipeline deals ────────────────────────────────────
    risk_factor = p.prob_signing * p.prob_cod
    risked_unlevered_npv = unlevered_npv * risk_factor
    risked_levered_npv   = levered_npv   * risk_factor

    # ── Build year-by-year cash flows for reference ───────────────────────
    cashflows = []
    for yr in range(1, p.lease_term_years + p.extension_years + 1):
        if yr <= p.lease_term_years:
            cf = annual_noi
        else:
            cf = renewal_noi * p.prob_extension
        abs_year = p.cod_year + yr - 1
        disc_yr  = abs_year - p.base_year
        pv_cf    = cf * discount_factor(p.discount_rate, disc_yr)
        cashflows.append({
            "year": abs_year,
            "cash_flow_mm": cf,
            "pv_cash_flow_mm": pv_cf,
            "type": "base" if yr <= p.lease_term_years else "renewal"
        })

    results = {
        "project": p.name,
        "company": p.company,
        "type": "Colocation / HPC Lease",
        "status": p.status,
        "cod_year": p.cod_year,
        "lease_term": p.lease_term_years,
        "annual_revenue_mm": p.annual_revenue_mm,
        "annual_noi_mm": annual_noi,
        "noi_margin_pct": p.noi_margin * 100,
        "remaining_capex_mm": p.remaining_capex_mm,
        "project_debt_mm": p.project_debt_mm,
        "equity_invested_mm": equity_invested,
        "discount_rate_pct": p.discount_rate * 100,
        "years_to_cod": years_to_cod,
        "pv_base_lease_mm": pv_noi_today,
        "pv_renewal_mm": risked_pv_renewal,
        "gross_project_value_mm": gross_project_value,
        "unlevered_npv_mm": unlevered_npv,
        "levered_npv_mm": levered_npv,
        "risk_factor": risk_factor,
        "risked_unlevered_npv_mm": risked_unlevered_npv,
        "risked_levered_npv_mm": risked_levered_npv,
        "cashflows": cashflows,
    }
    return results


def calc_cloud_npv(p: CloudProject) -> dict:
    """Calculate NPV for an AI cloud / GPU-as-a-service project."""
    years_to_cod = p.cod_year - p.base_year

    # ── Annual economics ───────────────────────────────────────────────────
    annual_revenue    = p.contracted_arr_mm * p.utilization_rate
    annual_power      = p.power_cost_mm_yr
    annual_dc_opex    = p.dc_opex_mm_yr
    annual_sw_support = p.software_support_mm_yr
    annual_interest   = p.debt_mm * p.interest_rate
    annual_ebitda     = annual_revenue - annual_power - annual_dc_opex - annual_sw_support
    annual_fcf        = annual_ebitda - annual_interest  # pre-replacement capex

    # ── GPU replacement capex ─────────────────────────────────────────────
    # Occurs every gpu_useful_life_years cycles within the contract
    replacement_cost  = p.gpu_capex_mm * p.replacement_capex_pct
    replacement_years = [
        p.cod_year + (i * p.gpu_useful_life_years)
        for i in range(1, math.ceil(p.contract_term_years / p.gpu_useful_life_years) + 1)
        if i * p.gpu_useful_life_years < p.contract_term_years
    ]

    # ── Base contract PV ───────────────────────────────────────────────────
    pv_fcf_at_cod = annual_fcf * annuity_factor(p.discount_rate, p.contract_term_years)
    pv_fcf_today  = pv_fcf_at_cod * discount_factor(p.discount_rate, years_to_cod)

    # PV of replacement capex events
    pv_replacement = sum(
        replacement_cost * discount_factor(p.discount_rate, yr - p.base_year)
        for yr in replacement_years
    )

    # ── Renewal PV ─────────────────────────────────────────────────────────
    renewal_rev      = annual_revenue * p.renewal_arr_haircut
    renewal_ebitda   = renewal_rev - annual_power - annual_dc_opex - annual_sw_support
    renewal_fcf      = renewal_ebitda - annual_interest
    pv_renewal_at_end = (
        renewal_fcf
        * annuity_factor(p.discount_rate, p.renewal_years)
        * discount_factor(p.discount_rate, p.contract_term_years)
    )
    pv_renewal_today  = pv_renewal_at_end * discount_factor(p.discount_rate, years_to_cod)
    risked_pv_renewal = pv_renewal_today * p.prob_renewal

    # ── Total project value ───────────────────────────────────────────────
    gross_project_value = pv_fcf_today - pv_replacement + risked_pv_renewal

    # ── NPV ───────────────────────────────────────────────────────────────
    total_initial_invest = p.gpu_capex_mm  # initial GPU investment
    equity_invested      = total_initial_invest - p.debt_mm
    unlevered_npv        = gross_project_value - total_initial_invest
    levered_npv          = gross_project_value - p.debt_mm - equity_invested

    # ── Risk-adjust ───────────────────────────────────────────────────────
    risk_factor          = p.prob_signing * p.prob_cod
    risked_unlevered_npv = unlevered_npv * risk_factor
    risked_levered_npv   = levered_npv   * risk_factor

    # ── Build year-by-year cash flows ─────────────────────────────────────
    cashflows = []
    # Year 0: GPU capex
    cashflows.append({
        "year": p.cod_year,
        "cash_flow_mm": -total_initial_invest,
        "pv_cash_flow_mm": -total_initial_invest * discount_factor(p.discount_rate, years_to_cod),
        "type": "initial_capex"
    })
    for yr_offset in range(1, p.contract_term_years + p.renewal_years + 1):
        abs_year = p.cod_year + yr_offset
        disc_yr  = abs_year - p.base_year
        if yr_offset <= p.contract_term_years:
            cf = annual_fcf
            label = "base"
        else:
            cf = renewal_fcf * p.prob_renewal
            label = "renewal"
        # Add replacement capex if it falls in this year
        if abs_year in replacement_years:
            cf -= replacement_cost
            label += "+replacement_capex"
        pv_cf = cf * discount_factor(p.discount_rate, disc_yr)
        cashflows.append({
            "year": abs_year,
            "cash_flow_mm": cf,
            "pv_cash_flow_mm": pv_cf,
            "type": label
        })

    ebitda_margin = (annual_ebitda / annual_revenue * 100) if annual_revenue > 0 else 0

    return {
        "project": p.name,
        "company": p.company,
        "type": "AI Cloud / GPU-as-a-Service",
        "status": p.status,
        "cod_year": p.cod_year,
        "contract_term": p.contract_term_years,
        "contracted_arr_mm": p.contracted_arr_mm,
        "utilization_rate_pct": p.utilization_rate * 100,
        "realized_revenue_mm": annual_revenue,
        "annual_power_mm": annual_power,
        "annual_dc_opex_mm": annual_dc_opex,
        "annual_ebitda_mm": annual_ebitda,
        "ebitda_margin_pct": ebitda_margin,
        "annual_fcf_mm": annual_fcf,
        "gpu_capex_mm": p.gpu_capex_mm,
        "debt_mm": p.debt_mm,
        "equity_invested_mm": equity_invested,
        "replacement_years": replacement_years,
        "pv_replacement_mm": pv_replacement,
        "discount_rate_pct": p.discount_rate * 100,
        "years_to_cod": years_to_cod,
        "pv_base_contract_mm": pv_fcf_today,
        "pv_renewal_mm": risked_pv_renewal,
        "gross_project_value_mm": gross_project_value,
        "unlevered_npv_mm": unlevered_npv,
        "levered_npv_mm": levered_npv,
        "risk_factor": risk_factor,
        "risked_unlevered_npv_mm": risked_unlevered_npv,
        "risked_levered_npv_mm": risked_levered_npv,
        "cashflows": cashflows,
    }


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT / DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def fmt(v: float, prefix: str = "$", suffix: str = "mm") -> str:
    """Format a number with sign, prefix, and suffix."""
    sign = "-" if v < 0 else ""
    return f"{sign}{prefix}{abs(v):,.1f}{suffix}"


def print_colo_result(r: dict):
    w = 62
    print("=" * w)
    print(f"  {r['company']} | {r['project']}")
    print(f"  {r['type']}")
    if r['status']:
        print(f"  Status: {r['status']}")
    print("-" * w)
    print(f"  COD Year:                  {r['cod_year']}  ({r['years_to_cod']}yr from today)")
    print(f"  Lease Term:                {r['lease_term']} years")
    print(f"  Annual Revenue:            {fmt(r['annual_revenue_mm'])}")
    print(f"  NOI Margin:                {r['noi_margin_pct']:.0f}%")
    print(f"  Annual NOI:                {fmt(r['annual_noi_mm'])}")
    print(f"  Discount Rate:             {r['discount_rate_pct']:.1f}%")
    print("-" * w)
    print(f"  PV of Base Lease:          {fmt(r['pv_base_lease_mm'])}")
    print(f"  PV of Renewal (risked):    {fmt(r['pv_renewal_mm'])}")
    print(f"  Gross Project Value:       {fmt(r['gross_project_value_mm'])}")
    print("-" * w)
    print(f"  Remaining Capex:           {fmt(r['remaining_capex_mm'])}")
    print(f"  Project Debt:              {fmt(r['project_debt_mm'])}")
    print(f"  Equity Invested:           {fmt(r['equity_invested_mm'])}")
    print("-" * w)
    print(f"  Unlevered Project NPV:     {fmt(r['unlevered_npv_mm'])}")
    print(f"  Levered Equity NPV:        {fmt(r['levered_npv_mm'])}")
    print(f"  Risk Factor:               {r['risk_factor']*100:.0f}%  (sign × COD)")
    print(f"  Risked Unlevered NPV:      {fmt(r['risked_unlevered_npv_mm'])}")
    print(f"  Risked Levered NPV:        {fmt(r['risked_levered_npv_mm'])}")
    print("=" * w)
    print()


def print_cloud_result(r: dict):
    w = 62
    print("=" * w)
    print(f"  {r['company']} | {r['project']}")
    print(f"  {r['type']}")
    if r['status']:
        print(f"  Status: {r['status']}")
    print("-" * w)
    print(f"  COD Year:                  {r['cod_year']}  ({r['years_to_cod']}yr from today)")
    print(f"  Contract Term:             {r['contract_term']} years")
    print(f"  Contracted ARR:            {fmt(r['contracted_arr_mm'])}")
    print(f"  Utilization:               {r['utilization_rate_pct']:.0f}%")
    print(f"  Realized Revenue/yr:       {fmt(r['realized_revenue_mm'])}")
    print(f"  Power Cost/yr:             {fmt(r['annual_power_mm'])}")
    print(f"  DC Opex/yr:                {fmt(r['annual_dc_opex_mm'])}")
    print(f"  Annual EBITDA:             {fmt(r['annual_ebitda_mm'])}  ({r['ebitda_margin_pct']:.0f}% margin)")
    print(f"  Annual FCF (post-int):     {fmt(r['annual_fcf_mm'])}")
    print(f"  Discount Rate:             {r['discount_rate_pct']:.1f}%")
    print("-" * w)
    print(f"  GPU Capex (initial):       {fmt(r['gpu_capex_mm'])}")
    repl_yrs = ", ".join(str(y) for y in r['replacement_years']) or "None"
    print(f"  Replacement Capex Years:   {repl_yrs}")
    print(f"  PV of Replacement Capex:   {fmt(r['pv_replacement_mm'])}")
    print(f"  Debt:                      {fmt(r['debt_mm'])}")
    print(f"  Equity Invested:           {fmt(r['equity_invested_mm'])}")
    print("-" * w)
    print(f"  PV of Base Contract:       {fmt(r['pv_base_contract_mm'])}")
    print(f"  PV of Renewal (risked):    {fmt(r['pv_renewal_mm'])}")
    print(f"  Gross Project Value:       {fmt(r['gross_project_value_mm'])}")
    print("-" * w)
    print(f"  Unlevered Project NPV:     {fmt(r['unlevered_npv_mm'])}")
    print(f"  Levered Equity NPV:        {fmt(r['levered_npv_mm'])}")
    print(f"  Risk Factor:               {r['risk_factor']*100:.0f}%  (sign × COD)")
    print(f"  Risked Unlevered NPV:      {fmt(r['risked_unlevered_npv_mm'])}")
    print(f"  Risked Levered NPV:        {fmt(r['risked_levered_npv_mm'])}")
    print("=" * w)
    print()


def print_portfolio_summary(results: list):
    w = 62
    print()
    print("=" * w)
    print("  PORTFOLIO SUMMARY")
    print("=" * w)
    header = f"  {'Company':<8} {'Project':<20} {'Risked Unlev NPV':>16} {'Risked Lev NPV':>14}"
    print(header)
    print("-" * w)
    total_unl = 0.0
    total_lev = 0.0
    for r in results:
        un  = r['risked_unlevered_npv_mm']
        lev = r['risked_levered_npv_mm']
        total_unl += un
        total_lev += lev
        name = r['project'][:20]
        print(f"  {r['company']:<8} {name:<20} {fmt(un):>16} {fmt(lev):>14}")
    print("-" * w)
    print(f"  {'TOTAL':<29} {fmt(total_unl):>16} {fmt(total_lev):>14}")
    print("=" * w)


def run_model(projects: list):
    results = []
    for p in projects:
        if isinstance(p, ColoProject):
            r = calc_colo_npv(p)
            print_colo_result(r)
        elif isinstance(p, CloudProject):
            r = calc_cloud_npv(p)
            print_cloud_result(r)
        else:
            raise TypeError(f"Unknown project type: {type(p)}")
        results.append(r)
    print_portfolio_summary(results)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# *** PLUG YOUR PROJECTS IN HERE ***
# ─────────────────────────────────────────────────────────────────────────────

PROJECTS = [

    # ── CIFR: Barber Lake ─────────────────────────────────────────────────
    ColoProject(
        name                    = "Barber Lake",
        company                 = "CIFR",
        annual_revenue_mm       = 300 * 1.65,    # 300 MW critical IT × $1.65/W/yr = $495mm
        lease_term_years        = 15,
        cod_year                = 2027,           # Phase I Sept 2026, ramp 2027
        noi_margin              = 0.85,           # triple-net
        remaining_capex_mm      = 450.0,          # ~$1.5/W × 300 MW
        project_debt_mm         = 382.5,          # 85% LTC
        ltc_ratio               = 0.85,
        discount_rate           = 0.10,
        prob_signing            = 1.0,            # lease signed
        prob_cod                = 0.85,           # under construction
        extension_years         = 5,
        extension_revenue_haircut = 0.90,
        prob_extension          = 0.60,
        status                  = "Under construction; Phase I Sept 2026",
    ),

    # ── CIFR: Black Pearl ─────────────────────────────────────────────────
    ColoProject(
        name                    = "Black Pearl",
        company                 = "CIFR",
        annual_revenue_mm       = 300 * 1.65,    # 300 MW × $1.65/W/yr = $495mm
        lease_term_years        = 15,
        cod_year                = 2027,           # Phase I Q4 2026, full ramp Q1 2027
        noi_margin              = 0.85,
        remaining_capex_mm      = 450.0,
        project_debt_mm         = 382.5,
        ltc_ratio               = 0.85,
        discount_rate           = 0.10,
        prob_signing            = 1.0,
        prob_cod                = 0.85,
        extension_years         = 5,
        extension_revenue_haircut = 0.90,
        prob_extension          = 0.60,
        status                  = "Under construction; Phase I Q4 2026 (AWS 15-yr)",
    ),

    # ── WULF: Lake Mariner (Core42, 60 MW live) ───────────────────────────
    ColoProject(
        name                    = "Lake Mariner (Core42)",
        company                 = "WULF",
        annual_revenue_mm       = 60 * 1.65,     # 60 MW critical IT × $1.65/W/yr = $99mm
        lease_term_years        = 15,
        cod_year                = 2026,           # already generating revenue
        noi_margin              = 0.85,
        remaining_capex_mm      = 0.0,            # CB-3/4/5 capex tracked separately
        project_debt_mm         = 0.0,
        ltc_ratio               = 0.85,
        discount_rate           = 0.10,
        prob_signing            = 1.0,
        prob_cod                = 1.0,            # live
        extension_years         = 5,
        extension_revenue_haircut = 0.90,
        prob_extension          = 0.60,
        status                  = "Operational — 60 MW live, CB-3/4/5 pending",
    ),

    # ── WULF: Abernathy JV ────────────────────────────────────────────────
    ColoProject(
        name                    = "Abernathy JV",
        company                 = "WULF",
        annual_revenue_mm       = 168 * 1.65,    # 168 MW critical IT × $1.65/W/yr = $277mm
        lease_term_years        = 25,            # 25-yr lease with annual escalators
        cod_year                = 2027,
        noi_margin              = 0.85,
        remaining_capex_mm      = 252.0,          # ~$1.5/W × 168 MW
        project_debt_mm         = 214.2,
        ltc_ratio               = 0.85,
        discount_rate           = 0.10,
        prob_signing            = 1.0,
        prob_cod                = 0.80,
        extension_years         = 0,
        prob_extension          = 0.0,
        status                  = "JV under construction; Fluidstack/Google; Q4 2026 target",
    ),

    # ── IREN: NVIDIA Contract ─────────────────────────────────────────────
    CloudProject(
        name                    = "NVIDIA Blackwell Contract",
        company                 = "IREN",
        contracted_arr_mm       = 1_900.0,        # $1.9B ARR anchor
        contract_term_years     = 5,
        cod_year                = 2027,           # ramp from early 2027
        gpu_capex_mm            = 2_000.0,        # est. GPU purchase cost for Blackwell fleet
        gpu_useful_life_years   = 4,
        replacement_capex_pct   = 0.80,           # 80% replacement cost per cycle
        power_cost_mm_yr        = 180.0,          # est. based on ~60 MW @ $0.05/kWh
        dc_opex_mm_yr           = 80.0,
        software_support_mm_yr  = 40.0,
        utilization_rate        = 0.90,
        discount_rate           = 0.12,           # higher rate for cloud execution risk
        debt_mm                 = 1_200.0,        # est. GPU financing
        interest_rate           = 0.07,
        prob_signing            = 1.0,            # contract signed
        prob_cod                = 0.85,
        renewal_years           = 3,
        renewal_arr_haircut     = 0.75,
        prob_renewal            = 0.50,
        status                  = "Signed; 20% prepayment received; ramp 2027",
    ),

    # ── IREN: Microsoft Contract ──────────────────────────────────────────
    CloudProject(
        name                    = "Microsoft AI Cloud Contract",
        company                 = "IREN",
        contracted_arr_mm       = 1_940.0,        # $9.7B / 5yr ≈ $1.94B/yr ARR
        contract_term_years     = 5,
        cod_year                = 2026,
        gpu_capex_mm            = 2_500.0,
        gpu_useful_life_years   = 4,
        replacement_capex_pct   = 0.80,
        power_cost_mm_yr        = 220.0,
        dc_opex_mm_yr           = 100.0,
        software_support_mm_yr  = 50.0,
        utilization_rate        = 0.90,
        discount_rate           = 0.12,
        debt_mm                 = 1_500.0,
        interest_rate           = 0.07,
        prob_signing            = 1.0,
        prob_cod                = 0.90,
        renewal_years           = 3,
        renewal_arr_haircut     = 0.75,
        prob_renewal            = 0.50,
        status                  = "Signed; $9.7B total contract value; 5yr",
    ),

]


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("  HPC DATA CENTER NPV MODEL")
    print(f"  Base Year: 2026  |  All figures in $mm USD")
    print()
    run_model(PROJECTS)
