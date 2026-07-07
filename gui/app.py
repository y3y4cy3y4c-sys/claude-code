"""
Synthetic IR — allocator intelligence (GUI v1, internal tool).

Run:  streamlit run gui/app.py

Two views over the same pipeline the CLI uses:
  * Universe — the allocator database: ranked names, tiers, drill-in,
    tier-1 briefing memos, cap intro package export.
  * Ingest — run a document through classify -> extract -> resolve ->
    score -> route and save it to the database.
Nothing here bypasses the discipline machinery; this is a renderer.
"""
import json
import os
import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tests"))

import extractor
from brief_gen import generate_brief
from classify import classify, is_prompt_ready
from package import build_package
from resolve_fields import resolve
from route import audit_record
from score import confidence_score, fit_score, load_weights
from store import load_all, save_profile

st.set_page_config(page_title="Institutional Capital Intelligence", layout="wide")

# House style: Goldman-inspired institutional luxury. Warm-white stone paper,
# near-black charcoal surfaces, and a single muted-gold accent; forest green and
# deep burgundy are reserved for status only. Hairline borders do the work that
# shadows would elsewhere; motion is restrained (120ms). Serif display headings
# for an editorial, timeless register; one clean sans for everything else. The
# gold accent is rationed — it marks the primary CTA, the active tab, timeline
# nodes and the profile hero rule, and nothing else. No emoji.
st.markdown("""<style>
:root {
  --paper:      #FAFAF8;   /* warm-white page (stone) */
  --paper-2:    #F2F3F1;   /* secondary surface / neutral chips */
  --card:       #FFFFFF;   /* card surface */
  --stone:      #F4F3EF;   /* profile hero band */
  --charcoal:   #1A1D21;   /* primary dark surface, default buttons */
  --sidebar:    #111315;   /* near-black sidebar (never true black) */
  --ink:        #111111;   /* primary text */
  --ink-2:      #50545A;   /* secondary text */
  --muted:      #7D8288;   /* muted text / labels */
  --hairline:   #E6E6E2;   /* borders — Goldman leans on lines, not shadow */
  --accent:     #A6864A;   /* muted gold — the one accent */
  --accent-2:   #8E7340;   /* gold hover */
  --accent-sel: #F5F1E8;   /* gold wash for selected states */
  --success:    #1D5C42;   /* institutional forest green */
  --negative:   #9A3A3A;   /* deep burgundy */
  --link:       #153A5B;   /* dark-navy links */
  --radius:     8px;       /* subtle rounding — never dramatic */
}
[data-testid="stAppViewContainer"] { background: var(--paper); }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* one sans stack for every piece of UI text (icon fonts untouched) */
p, label, li, td, th, dt, dd, input, textarea, select, option,
[data-baseweb="tab"], .stButton button, .stDownloadButton button,
[data-testid="stCaptionContainer"], [data-testid="stWidgetLabel"] p {
  font-family: "Segoe UI", -apple-system, Helvetica, Arial, sans-serif
  !important; }

h1, h2, h3 { font-family: Georgia, "Times New Roman", serif !important;
             font-weight: 400 !important; color: var(--ink) !important;
             letter-spacing: .01em; }
[data-testid="stAppViewContainer"] h1 {
  border-bottom: 1px solid var(--hairline); padding-bottom: .45rem; }

[data-testid="stCaptionContainer"], .stCaption, small { color: var(--muted); }

[data-testid="stSidebar"] { background: var(--sidebar);
  border-right: 1px solid var(--hairline); }
[data-testid="stSidebar"] * { color: #E9E7DF !important; }
[data-testid="stSidebar"] h1 { font-family: Georgia, serif !important;
  font-weight: 400 !important; color: #FFFFFF !important;
  font-size: 1.35rem; line-height: 1.35; letter-spacing: .04em;
  border-bottom: 1px solid rgba(233,231,223,.20); padding-bottom: .6rem; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *
  { color: #A8AFBD !important; font-size: .78rem; }
[data-testid="stSidebar"] hr { border-color: rgba(233,231,223,.18); }
/* selected view in the dark sidebar gets a quiet gold indicator */
[data-testid="stSidebar"] [role="radiogroup"] label:hover
  { background: rgba(166,134,74,.10); }

[data-testid="stMetric"] { border-top: 2px solid var(--accent);
  padding-top: .5rem; }
[data-testid="stMetricLabel"] p { text-transform: uppercase;
  letter-spacing: .09em; font-size: .68rem !important; color: var(--muted); }
[data-testid="stMetricValue"] { font-family: Georgia, serif;
  font-size: 1.55rem; color: var(--ink); }

/* default button: charcoal, subtle radius, restrained hover */
.stButton button, .stDownloadButton button {
  background: var(--charcoal) !important; color: #FFFFFF !important;
  border: 1px solid var(--charcoal) !important; border-radius: 6px !important;
  text-transform: uppercase; letter-spacing: .08em; font-size: .72rem;
  padding: .55rem 1.3rem;
  transition: background 120ms ease, border-color 120ms ease; }
.stButton button:hover, .stDownloadButton button:hover {
  background: #2A2E33 !important; border-color: #2A2E33 !important; }
/* primary CTA is the one place gold is spent (Discover / Run & save / Ingest) */
.stButton button[kind="primary"],
.stButton button[data-testid="baseButton-primary"] {
  background: var(--accent) !important; border-color: var(--accent) !important;
  color: #FFFFFF !important; }
.stButton button[kind="primary"]:hover,
.stButton button[data-testid="baseButton-primary"]:hover {
  background: var(--accent-2) !important;
  border-color: var(--accent-2) !important; }

[data-baseweb="tab-list"] { border-bottom: 1px solid var(--hairline); }
[data-baseweb="tab"] { text-transform: uppercase; letter-spacing: .08em;
  font-size: .72rem; }
[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }

[data-testid="stExpander"] { border: 1px solid var(--hairline);
  border-radius: var(--radius) !important; background: var(--card); }

.chip { display: inline-block; font-size: .64rem; letter-spacing: .09em;
  text-transform: uppercase; padding: 1px 8px 2px; border: 1px solid;
  border-radius: 3px; vertical-align: middle; }
.chip-stated   { color: #1D5C42; border-color: #B9C9BF; background: #EEF3EF; }
.chip-inferred { color: #7A6326; border-color: #D8C9A0; background: #F6F1E6; }
.chip-unknown  { color: #7D8288; border-color: #DCDAD3; background: #F3F2EE; }

blockquote { border-left: 2px solid var(--accent) !important;
  color: var(--ink-2) !important; font-family: Georgia, serif; }

/* profile header band — Goldman hero: light stone, gold left rule, dark ink
   (replaces the old solid-navy banner) */
.band { background: var(--stone); color: var(--ink);
  border-left: 3px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 1.3rem 1.6rem 1.1rem; margin: .2rem 0 1rem; }
.band-name { font-family: Georgia, serif; font-size: 1.7rem;
  color: var(--ink); letter-spacing: .01em; margin-bottom: .9rem; }
.band-facts { display: flex; gap: 2.2rem; flex-wrap: wrap;
  border-top: 1px solid var(--hairline); padding-top: .8rem; }
.fact-l { text-transform: uppercase; letter-spacing: .09em;
  font-size: .62rem; color: var(--muted); margin-bottom: .15rem; }
.fact-v { font-size: .95rem; color: var(--ink); }

/* signals timeline */
.tl-item { display: flex; gap: 0; margin-bottom: .9rem; }
.tl-date { width: 58px; flex: none; text-align: right; padding-right: .8rem;
  text-transform: uppercase; letter-spacing: .06em; font-size: .66rem;
  color: var(--muted); line-height: 1.5; padding-top: .35rem; }
.tl-rail { flex: none; width: 20px; position: relative; }
.tl-rail::before { content: ""; position: absolute; left: 9px; top: 0;
  bottom: -0.9rem; width: 1px; background: var(--hairline); }
.tl-dot { position: absolute; left: 4px; top: .45rem; width: 11px;
  height: 11px; border-radius: 50%; background: var(--card);
  border: 3px solid var(--accent); }
.tl-card { flex: 1; border: 1px solid var(--hairline); background: var(--card);
  border-radius: var(--radius);
  padding: .75rem 1rem .6rem; margin-left: .55rem; }
.tl-value { font-size: .95rem; color: #1F2937; margin: .35rem 0 .25rem; }
.tl-card blockquote { margin: .3rem 0 .2rem; padding-left: .7rem;
  font-size: .85rem; }
.tag { display: inline-block; font-size: .64rem; letter-spacing: .07em;
  text-transform: uppercase; padding: 1px 8px 2px; margin-right: .35rem;
  color: var(--ink); background: var(--paper-2);
  border: 1px solid var(--hairline); border-radius: 3px; }

/* top brand band — charcoal terminal bar */
.topband { background: var(--charcoal); color: #FFF; display: flex;
  justify-content: space-between; align-items: baseline;
  padding: .55rem 1.1rem; margin: -1rem 0 1.2rem; }
.topband-brand { font-family: Georgia, serif; font-size: .95rem;
  letter-spacing: .05em; }
.topband-meta { font-size: .68rem; text-transform: uppercase;
  letter-spacing: .09em; color: #A8AFBD; }

/* insights feed */
.ins-card { border: 1px solid var(--hairline); background: var(--card);
  border-radius: var(--radius);
  padding: 1rem 1.2rem .8rem; margin-bottom: 1rem; }
.ins-date { text-transform: uppercase; letter-spacing: .09em;
  font-size: .66rem; color: var(--muted); margin-bottom: .25rem; }
.ins-head { font-family: Georgia, serif; font-size: 1.18rem;
  color: var(--ink); margin-bottom: .4rem; }
.ins-bullets { margin: .2rem 0 .4rem 1.1rem; padding: 0; }
.ins-bullets li { font-size: .9rem; color: #1F2937; margin-bottom: .15rem; }
.rail-card { background: var(--charcoal); color: #FFF; padding: .7rem .9rem;
  border-radius: var(--radius); margin-bottom: .7rem; }
.rail-l { text-transform: uppercase; letter-spacing: .09em;
  font-size: .62rem; color: #A8AFBD; margin-bottom: .35rem; }
.rail-v { font-size: .85rem; background: rgba(255,255,255,.12);
  border-radius: 4px; padding: .35rem .55rem; }

/* record-type badges (WI's Mandate / I&P / RFP chips) */
.badge { display: inline-block; font-size: .62rem; letter-spacing: .08em;
  text-transform: uppercase; padding: 1px 10px 2px; margin-right: .4rem;
  border-radius: 9px; }
.badge-m { background: var(--charcoal); color: #FFF; }
.badge-i { background: var(--paper-2); color: var(--ink);
  border: 1px solid var(--hairline); }
.badge-r { background: var(--accent); color: #FFF; }
.badge-c { background: var(--negative); color: #FFF; }

/* in-app navigation links */
a.navlink { color: var(--ink) !important; text-decoration: none !important;
  border-bottom: 1px solid var(--accent); font-size: .85rem; }
a.navlink:hover { border-bottom-width: 2px; }
a.railwrap { text-decoration: none !important; display: block; }
a.railwrap:hover .rail-v { background: rgba(255,255,255,.25); }
a.tag { text-decoration: none !important; }
a.tag:hover { background: var(--charcoal); color: #FFF; }

/* preference cards */
.pref-card { border: 1px solid var(--hairline); background: var(--card);
  border-radius: var(--radius);
  padding: .7rem .95rem .6rem; min-height: 4.4rem; margin-bottom: .8rem; }
.pref-label { text-transform: uppercase; letter-spacing: .08em;
  font-size: .62rem; color: var(--muted); margin-bottom: .3rem; }
.pref-yes { color: var(--success); font-weight: 600; }
.pref-no  { color: var(--negative); font-weight: 600; }
.pref-val { color: var(--ink); font-weight: 600; }
.pref-na  { color: var(--muted); }
</style>""", unsafe_allow_html=True)

CONF_BADGE = {"stated": "stated", "inferred": "inferred", "unknown": "unknown"}
CONF_CHIP = {c: f'<span class="chip chip-{c}">{c}</span>' for c in CONF_BADGE}
TIER_BADGE = {1: "1 · Engage", 2: "2 · Research",
              3: "3 · Long-term", 4: "4 · Rescan quarterly"}

st.sidebar.title("Institutional Capital Intelligence")
st.sidebar.caption("Allocator intelligence · fit scoring · "
                   "capital-introduction targeting")
view = st.sidebar.radio("View", ["Insights", "Explore", "Performance",
                                 "Discover & add allocator",
                                 "Ingest a document"],
                        on_change=lambda: st.query_params.clear())

_recs = load_all()
_ndocs = len(list((REPO / "data" / "raw").glob("*.txt")))
st.markdown(
    f'<div class="topband"><span class="topband-brand">Institutional '
    f'Capital Intelligence</span><span class="topband-meta">'
    f"{len(_recs)} allocators · {_ndocs} documents · internal prototype"
    f"</span></div>", unsafe_allow_html=True)


def profile_rows(prof: dict) -> list[dict]:
    rows = []
    for field, v in prof.items():
        if not isinstance(v, dict) or "confidence" not in v:
            continue
        rows.append({
            "field": field,
            "value": "—" if v["value"] is None else str(v["value"]),
            "confidence": CONF_BADGE.get(v["confidence"], v["confidence"]),
            "source": v.get("winning_source") or "—",
            "conflict": v.get("conflict_note") or "",
        })
    return rows


def evidence_panels(ev: dict):
    for field, entries in ev.items():
        if not isinstance(entries, list) or not entries:
            continue
        if not all(isinstance(e, dict) and "confidence" in e for e in entries):
            continue
        with st.expander(f"{field} — {len(entries)} claim(s)"):
            for e in entries:
                st.markdown(f"**{e['value']}** &nbsp;"
                            f"{CONF_CHIP.get(e['confidence'], e['confidence'])}"
                            + (f" · as of {e['as_of']}" if e.get("as_of") else "")
                            + f" · {e.get('source', '')}",
                            unsafe_allow_html=True)
                if e.get("quote"):
                    st.markdown(f"> {e['quote']}")
    mgrs = (ev.get("macro_exposure") or {}).get("managers") or []
    with st.expander(f"macro_exposure — {len(mgrs)} manager claim(s)"):
        if mgrs:
            for e in mgrs:
                st.markdown(f"**{e['value']}** &nbsp;"
                            f"{CONF_CHIP.get(e['confidence'], '')}",
                            unsafe_allow_html=True)
                if e.get("quote"):
                    st.markdown(f"> {e['quote']}")
        else:
            st.markdown("*Empty — no investment or mandate relationship "
                        "evidenced. Absence is a finding, not a gap.*")


# ================================================================= helpers
import html as _html


def _pval(prof: dict, field: str):
    v = prof.get(field)
    return v.get("value") if isinstance(v, dict) else None


def _fmt_aum(v) -> str:
    try:
        return f"${float(v):,.0f}m"
    except (TypeError, ValueError):
        return "—"


def _latest_asof(rec: dict) -> str:
    dates = [e["as_of"] for v in rec["evidence"].values() if isinstance(v, list)
             for e in v if isinstance(e, dict) and e.get("as_of")]
    return max(dates) if dates else ""


def _timeline_items(rec: dict, limit: int = 12) -> list[tuple]:
    seen, items = set(), []
    for field, v in rec["evidence"].items():
        if not isinstance(v, list):
            continue
        for e in v:
            if not (isinstance(e, dict) and e.get("as_of")):
                continue
            if e.get("value") in (None, "None", ""):
                continue
            key = (field, str(e["value"]), e["as_of"])
            if key in seen:
                continue
            seen.add(key)
            items.append((e["as_of"], field, e))
    items.sort(key=lambda t: t[0], reverse=True)
    return items[:limit]


def _badge(field: str) -> str:
    """WI's record-type chips, mapped deterministically from the field."""
    if field == "active_search":
        return '<span class="badge badge-r">RFP</span>'
    if field == "policy_change":
        return '<span class="badge badge-m">Mandate</span>'
    return '<span class="badge badge-i">I&amp;P</span>'


def _profile_href(cid: str) -> str:
    return f"?page=profile&id={cid}"


def _consultant_href(name: str) -> str:
    from urllib.parse import quote
    return f"?page=consultant&name={quote(name)}"


@st.cache_data
def _registry_urls() -> dict[str, str]:
    """Per-fund public meetings-page URL from config/universe.yaml."""
    import yaml
    p = REPO / "config" / "universe.yaml"
    if not p.is_file():
        return {}
    reg = yaml.safe_load(p.read_text(encoding="utf-8"))["allocators"]
    out = {}
    for cid, meta in reg.items():
        d = meta.get("discovery") or {}
        url = d.get("page_url") or d.get("check_url")
        if url:
            out[cid] = url
    return out


def _tl_html(items: list[tuple], with_fund: bool = False) -> str:
    import datetime as _dt
    out = []
    for as_of, field, e in items:
        try:
            d = _dt.date.fromisoformat(str(as_of)[:10])
            date_lbl = d.strftime("%b<br>%Y")
        except ValueError:
            date_lbl = _html.escape(str(as_of))
        chip = CONF_CHIP.get(e.get("confidence", ""), "")
        fund = ""
        if with_fund and e.get("fund"):
            fname = _html.escape(e["fund"])
            if e.get("fund_cid"):
                fund = (f'<a class="tag" target="_self" '
                        f'href="{_profile_href(e["fund_cid"])}">{fname}</a>')
            else:
                fund = f'<span class="tag">{fname}</span>'
        quote = (f"<blockquote>{_html.escape(str(e['quote'])[:280])}</blockquote>"
                 if e.get("quote") else "")
        out.append(
            f'<div class="tl-item"><div class="tl-date">{date_lbl}</div>'
            f'<div class="tl-rail"><span class="tl-dot"></span></div>'
            f'<div class="tl-card">{_badge(field)}{fund}<span class="tag">'
            f'{_html.escape(field)}</span> {chip}'
            f'<div class="tl-value">{_html.escape(str(e["value"]))}</div>'
            f"{quote}</div></div>")
    return "".join(out) or "<p style='color:#7D8288'>No dated signals yet.</p>"


def _pref_card(label: str, value, suffix: str = "") -> str:
    if value is True:
        cls, text = "pref-yes", "Yes"
    elif value is False:
        cls, text = "pref-no", "No"
    elif value in (None, "", "None"):
        cls, text = "pref-na", "—"
    else:
        cls, text = "pref-val", _html.escape(f"{value}{suffix}")
    return (f'<div class="pref-card"><div class="pref-label">'
            f"{_html.escape(label)}</div><div class='{cls}'>{text}</div></div>")


INSIGHT_FIELDS = {
    "policy_change": "Policy change",
    "active_search": "Active search",
    "cio_change": "CIO / key person",
    "consultant_name": "Consultant",
    "hf_allocation_pct": "Hedge fund allocation",
    "ic_frequency": "IC cadence",
}


def _insights_for(rec: dict) -> list[dict]:
    prof, fund = rec["profile"], rec["legal_name"]
    tags = [t for t in (_pval(prof, "allocator_type"),
                        _pval(prof, "domicile")) if t]
    consultant = _pval(prof, "consultant_name")
    items = []
    for as_of, field, e in _timeline_items(rec, limit=20):
        if field not in INSIGHT_FIELDS:
            continue
        items.append({
            "date": str(as_of), "fund": fund, "cid": rec["canonical_id"],
            "headline": f"{fund} — {INSIGHT_FIELDS[field]}",
            "bullets": [str(e["value"])],
            "quote": e.get("quote") or "",
            "chip": CONF_CHIP.get(e.get("confidence", ""), ""),
            "badge": _badge(field),
            "tags": [INSIGHT_FIELDS[field]] + tags,
            "source": e.get("source") or "",
            "consultant": consultant,
        })
    for ch in rec.get("changes_last_ingest") or []:
        label = INSIGHT_FIELDS.get(ch["field"], ch["field"])
        items.append({
            "date": (rec.get("saved_at") or "")[:10], "fund": fund,
            "cid": rec["canonical_id"],
            "headline": f"{fund} — {label} changed",
            "bullets": [f"{ch['from'] or '—'}  →  {ch['to'] or '—'}",
                        "Detected by cross-document comparison at ingest"],
            "quote": "",
            "chip": "",
            "badge": '<span class="badge badge-c">Change</span>',
            "tags": ["Change detected"] + tags,
            "source": ", ".join(rec.get("source_documents", [])),
            "consultant": consultant,
        })
    return items


def _ins_card_html(item: dict) -> str:
    tags_html = "".join(f'<span class="tag">{_html.escape(t)}</span>'
                        for t in item["tags"])
    bullets = "".join(f"<li>{_html.escape(b)}</li>" for b in item["bullets"])
    quote = (f"<blockquote>{_html.escape(item['quote'][:320])}</blockquote>"
             if item["quote"] else "")
    src = (f'<div class="ins-date">source · {_html.escape(item["source"])}'
           f"</div>" if item["source"] else "")
    return (f'<div class="ins-card"><div class="ins-date">'
            f'{item.get("badge", "")} {_html.escape(item["date"])}</div>'
            f'<div class="ins-head">{_html.escape(item["headline"])}</div>'
            f'<ul class="ins-bullets">{bullets}</ul>{quote}'
            f'<div>{tags_html} {item["chip"]}</div>{src}</div>')


@st.cache_data
def _load_wi_funds() -> list[dict]:
    """Licensed WI trial export, if imported (src/import_wi.py). Read-only
    display data — never merged into evidence, never sent anywhere."""
    p = REPO / "data" / "licensed" / "wi_funds.json"
    if not p.is_file():
        return []
    return json.loads(p.read_text(encoding="utf-8"))["funds"]


SAVED_SEARCHES = REPO / "data" / "saved_searches.json"


def _load_saved_searches() -> dict:
    if SAVED_SEARCHES.is_file():
        return json.loads(SAVED_SEARCHES.read_text(encoding="utf-8"))
    return {}


def _doc_provenance() -> dict[str, dict]:
    """Parse data/raw/SOURCES.md into {doc_filename: provenance} — both the
    per-file `## name.txt` sections and the 2026-07-07 refresh table rows."""
    import re as _re
    out = {}
    src = REPO / "data" / "raw" / "SOURCES.md"
    if not src.is_file():
        return out
    text = src.read_text(encoding="utf-8")
    for sec in _re.split(r"^## ", text, flags=_re.M)[1:]:
        name = sec.splitlines()[0].strip().split(" ")[0]
        url = _re.search(r"\*\*URL:\*\* (\S+)", sec)
        if name in out and out[name]["url"] and not url:
            continue  # e.g. the "(history)" note must not clobber the entry
        sha = _re.search(r"sha256:\*\* ([0-9a-f]+)", sec)
        ret = _re.search(r"\*\*Retrieved:\*\* ([0-9-]{10})", sec)
        conf = _re.search(r"confidence ([0-9.]+)", sec)
        out[name] = {"url": url.group(1) if url else "",
                     "sha256": sha.group(1)[:16] if sha else "",
                     "retrieved": ret.group(1) if ret else "",
                     "retrieval_conf": conf.group(1) if conf else ""}
    # refresh-table rows: | file.txt | meeting | url | sha |
    for m in _re.finditer(r"^\| (\S+\.txt) \| [^|]+ \| (https?://\S+) \| "
                          r"([0-9a-f]+) \|", text, flags=_re.M):
        name, url, sha = m.group(1), m.group(2), m.group(3)
        if not out.get(name, {}).get("url"):
            out[name] = {"url": url, "sha256": sha[:16],
                         "retrieved": "2026-07-07", "retrieval_conf": ""}
    return out


def render_profile(rec: dict):
    r = rec["routing"]
    prof = rec["profile"]
    cid = rec["canonical_id"]

    nav = ['<a class="navlink" href="/" target="_self">‹ Back to Explore</a>']
    site = _registry_urls().get(cid)
    if site:
        nav.append(f'<a class="navlink" href="{site}" target="_blank">'
                   "See website ↗</a>")
    cons = _pval(prof, "consultant_name")
    if cons:
        nav.append(f'<a class="navlink" target="_self" '
                   f'href="{_consultant_href(str(cons))}">Consultant: '
                   f"{_html.escape(str(cons))}</a>")
    st.markdown(" &nbsp;·&nbsp; ".join(nav), unsafe_allow_html=True)

    facts = [
        ("Investor type", _pval(prof, "allocator_type") or "—"),
        ("Location", _pval(prof, "domicile") or "—"),
        ("AuM", _fmt_aum(_pval(prof, "total_aum_usd_mm"))),
        ("Tier", TIER_BADGE[r["tier"]]),
        ("As of", _latest_asof(rec) or "—"),
    ]
    hf_pct = _pval(prof, "hf_allocation_pct")
    if hf_pct not in (None, "", "None"):
        facts.insert(3, ("Hedge funds", f"{hf_pct}%"))
    macro_n = _pval(prof, "macro_manager_count")
    if isinstance(macro_n, int):
        facts.insert(4, ("Macro managers", str(macro_n)))
    facts_html = "".join(
        f'<div class="fact"><div class="fact-l">{_html.escape(l)}</div>'
        f'<div class="fact-v">{_html.escape(str(v))}</div></div>'
        for l, v in facts)
    st.markdown(f'<div class="band"><div class="band-name">'
                f'{_html.escape(rec["legal_name"])}</div>'
                f'<div class="band-facts">{facts_html}</div></div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tier", f"{r['tier']} · {r['label']}")
    c2.metric("Fit", f"{r['fit_score']} / 100")
    c3.metric("Confidence", f"{r['confidence_score']} / 1.00")
    c4.metric("Review status", r["review_status"])
    st.caption(f"Routing rationale: {r['rationale']} · weights "
               f"{r['weights_sha256']} ({r['weights_status']}) · assigned "
               f"{r['assigned_at']}")
    if r["tier"] == 1:
        st.download_button("Export brief (markdown)", generate_brief(rec),
                           file_name=f"brief_{cid}.md")

    tab1, tab2, tab6, tab3, tab7, tab8, tab4, tab5 = st.tabs(
        ["Summary", "Intentions & signals", "Insights", "Preferences",
         "People", "Documents", "Evidence", "Briefing memo"])
    with tab1:
        st.dataframe(profile_rows(prof), use_container_width=True,
                     hide_index=True)
    with tab2:
        iq = st.text_input("Search intentions and preferences",
                           placeholder="Search intentions and preferences",
                           label_visibility="collapsed", key=f"iq_{cid}")
        items = _timeline_items(rec)
        if iq:
            iql = iq.lower()
            items = [(a, f, e) for a, f, e in items
                     if iql in f"{f} {e.get('value')} {e.get('quote', '')}".lower()]
        hdr, exp = st.columns([4, 1])
        hdr.caption(f"{len(items)} intention(s) / signal(s)")
        csv_lines = ["date,field,value,confidence,source,quote"]
        for a, f, e in items:
            vals = [str(a), f, str(e.get("value", "")),
                    str(e.get("confidence", "")), str(e.get("source", "")),
                    str(e.get("quote", ""))]
            csv_lines.append(",".join('"' + v.replace('"', '""') + '"'
                                      for v in vals))
        exp.download_button("Export (CSV)", "\n".join(csv_lines),
                            file_name=f"{cid}_intentions.csv")
        st.markdown(_tl_html(items), unsafe_allow_html=True)
    with tab6:
        items = sorted(_insights_for(rec), key=lambda x: x["date"],
                       reverse=True)
        if items:
            for item in items[:10]:
                st.markdown(_ins_card_html(item), unsafe_allow_html=True)
        else:
            st.caption("No dated signals for this allocator yet.")
    with tab7:
        st.caption("A people/contacts layer is deliberately absent from "
                   "schema v0.1: key-contact data comes from the internal "
                   "fields below (firm records — a meeting decision), and "
                   "extracting names from public minutes is deferred until "
                   "the data-handling policy is settled.")
        cols = st.columns(3)
        for col, (label, field) in zip(cols, [
                ("Relationship owner", "relationship_owner"),
                ("Existing relationship", "existing_relationship"),
                ("MS cap intro coverage", "ms_coverage")]):
            col.markdown(_pref_card(label, _pval(prof, field)),
                         unsafe_allow_html=True)
    with tab8:
        prov = _doc_provenance()
        doc_rows = []
        for p in sorted((REPO / "data" / "raw").glob(f"{cid}_*.txt")):
            pr = prov.get(p.name, {})
            doc_rows.append({
                "document": p.name,
                "meeting date": p.stem.rsplit("_", 1)[-1],
                "retrieved": pr.get("retrieved", ""),
                "retrieval conf": pr.get("retrieval_conf", ""),
                "sha256 (16)": pr.get("sha256", ""),
                "URL": pr.get("url", ""),
            })
        if doc_rows:
            st.dataframe(doc_rows, use_container_width=True, hide_index=True)
        else:
            st.caption("No documents on file for this allocator.")
        st.caption("Full provenance in data/raw/SOURCES.md — every document "
                   "traceable to an official public source.")
    with tab3:
        macro_n = _pval(prof, "macro_manager_count")
        asia_n = _pval(prof, "asia_manager_count")
        cards = [
            ("Uses consultant", _pval(prof, "uses_consultant"), ""),
            ("Consultant", _pval(prof, "consultant_name"), ""),
            ("IC frequency", _pval(prof, "ic_frequency"), ""),
            ("Direct staff authority", _pval(prof, "direct_authority"), ""),
            ("Macro exposure", (macro_n > 0) if isinstance(macro_n, int)
             else macro_n, ""),
            ("Asia exposure", (asia_n > 0) if isinstance(asia_n, int)
             else asia_n, ""),
            ("HF allocation", _pval(prof, "hf_allocation_pct"), "%"),
            ("Typical ticket", _pval(prof, "ticket_typical_usd_mm"), "m"),
            ("MS cap intro coverage", _pval(prof, "ms_coverage"), ""),
            ("Existing relationship", _pval(prof, "existing_relationship"), ""),
        ]
        st.caption("Decision structure and access — resolved values only; "
                   "each claim's citation is under Evidence.")
        for i in range(0, len(cards), 4):
            cols = st.columns(4)
            for col, (label, val, suffix) in zip(cols, cards[i:i + 4]):
                col.markdown(_pref_card(label, val, suffix),
                             unsafe_allow_html=True)
    with tab4:
        evidence_panels(rec["evidence"])
    with tab5:
        if r["tier"] == 1:
            st.markdown(generate_brief(rec))
        else:
            st.info(f"Briefs are generated for tier 1 only (this name is "
                    f"tier {r['tier']} — {r['label']}). Preview below is "
                    "watermarked and not for issue.")
            if st.checkbox("Show watermarked preview anyway"):
                st.markdown(generate_brief(rec, allow_non_tier1=True))


def render_consultant(name: str, records: list[dict]):
    """Consultant profile page — WI's Consultants entity, from our evidence."""
    st.markdown('<a class="navlink" href="/" target="_self">'
                "‹ Back to Explore</a>", unsafe_allow_html=True)
    advised, mentions = [], []
    for rec in records:
        entries = [e for e in (rec["evidence"].get("consultant_name") or [])
                   if isinstance(e, dict) and str(e.get("value")) == name]
        resolved = _pval(rec["profile"], "consultant_name") == name
        if entries or resolved:
            advised.append((rec, resolved))
            for e in entries:
                mentions.append((e.get("as_of") or "", "consultant_name",
                                 dict(e, fund=rec["legal_name"],
                                      fund_cid=rec["canonical_id"])))
    facts_html = "".join(
        f'<div class="fact"><div class="fact-l">{l}</div>'
        f'<div class="fact-v">{v}</div></div>'
        for l, v in [("Entity", "Investment consultant"),
                     ("Advises (in universe)",
                      str(sum(1 for _, res in advised if res))),
                     ("Evidenced mentions", str(len(mentions)))])
    st.markdown(f'<div class="band"><div class="band-name">'
                f'{_html.escape(name)}</div>'
                f'<div class="band-facts">{facts_html}</div></div>',
                unsafe_allow_html=True)
    if advised:
        st.dataframe([{
            "allocator": rec["legal_name"],
            "relationship": ("current consultant" if res
                             else "mentioned in evidence"),
            "tier": TIER_BADGE[rec["routing"]["tier"]],
            "open": _profile_href(rec["canonical_id"]),
        } for rec, res in advised], use_container_width=True,
            hide_index=True,
            column_config={"open": st.column_config.LinkColumn(
                "open", display_text="Open profile")})
    st.markdown("#### Evidence trail")
    mentions.sort(key=lambda t: t[0], reverse=True)
    st.markdown(_tl_html(mentions, with_fund=True), unsafe_allow_html=True)


# ================================================================= routing
# WI-style click-through: table links and card links navigate by URL query
# params; the sidebar radio clears them (see on_change) to return to views.
_qp = st.query_params
if _qp.get("page") == "profile" and _qp.get("id"):
    _match = [r0 for r0 in _recs if r0["canonical_id"] == _qp["id"]]
    if _match:
        render_profile(_match[0])
        st.stop()
    st.error(f"No profile in the database: {_qp['id']}")
elif _qp.get("page") == "consultant" and _qp.get("name"):
    render_consultant(_qp["name"], _recs)
    st.stop()

# ================================================================= insights
if view == "Insights":
    records = load_all()
    st.title("Insights")
    st.caption("Dated signals from official public documents. Headlines are "
               "deterministic template fills — nothing here is generated "
               "prose; every item carries its verbatim source line.")
    if not records:
        st.info("Database is empty — ingest a document first.")
        st.stop()

    feed = [i for r in records for i in _insights_for(r)]
    feed.sort(key=lambda x: x["date"], reverse=True)

    for item in feed[:20]:
        left, right = st.columns([3, 1])
        with left:
            st.markdown(_ins_card_html(item), unsafe_allow_html=True)
        with right:
            st.markdown(
                f'<a class="railwrap" target="_self" '
                f'href="{_profile_href(item["cid"])}">'
                f'<div class="rail-card"><div class="rail-l">Investor '
                f'profile</div><div class="rail-v">'
                f'{_html.escape(item["fund"])}</div></div></a>',
                unsafe_allow_html=True)
            if item["consultant"]:
                st.markdown(
                    f'<a class="railwrap" target="_self" '
                    f'href="{_consultant_href(str(item["consultant"]))}">'
                    f'<div class="rail-card"><div class="rail-l">Consultant '
                    f'profile</div><div class="rail-v">'
                    f'{_html.escape(str(item["consultant"]))}</div></div></a>',
                    unsafe_allow_html=True)

# ================================================================= explore
elif view == "Explore":
    records = load_all()
    st.title("Explore")
    if not records:
        st.info("Database is empty — ingest a document first.")
        st.stop()

    ranked = sorted(records, key=lambda r: (r["routing"]["tier"],
                                            -r["routing"]["fit_score"],
                                            -r["routing"]["confidence_score"]))
    st.caption(f"{len(ranked)} allocators · every profile built from an "
               "official public document (see data/raw/SOURCES.md)")

    # a saved search applies its values BEFORE widgets instantiate
    if "_apply_search" in st.session_state:
        for k, v in st.session_state.pop("_apply_search").items():
            st.session_state[k] = v

    wi_funds = _load_wi_funds()
    cons_map: dict[str, list] = {}
    for r in ranked:
        for e in (r["evidence"].get("consultant_name") or []):
            if isinstance(e, dict) and e.get("value"):
                lst = cons_map.setdefault(str(e["value"]), [])
                if r["canonical_id"] not in [x["canonical_id"] for x in lst]:
                    lst.append(r)
    labels = [f"Allocators · {len(ranked)}",
              f"Mandates & intentions · {sum(len(_timeline_items(r, limit=4)) for r in ranked)}",
              f"Consultants · {len(cons_map)}",
              f"Documents · {len(list((REPO / 'data' / 'raw').glob('*.txt')))}"]
    if wi_funds:
        labels.append(f"Funds · {len(wi_funds):,}")
    tabs = st.tabs(labels)
    tab_a, tab_s, tab_c, tab_d = tabs[0], tabs[1], tabs[2], tabs[3]

    with tab_a:
        q = st.text_input("Search records", placeholder="Search records",
                          label_visibility="collapsed", key="f_q")

        ALL_COLS = ["allocator", "type", "location", "AuM (USD/m)",
                    "consultant", "tier", "fit", "confidence", "as of"]
        with st.expander("Filters and columns"):
            fc1, fc2, fc3 = st.columns(3)
            types = sorted({_pval(r["profile"], "allocator_type") or "—"
                            for r in ranked})
            cons = sorted({_pval(r["profile"], "consultant_name") or "—"
                           for r in ranked})
            sel_type = fc1.multiselect("Investor type", types, key="f_type")
            sel_tier = fc2.multiselect("Tier", [1, 2, 3, 4],
                                       format_func=lambda t: TIER_BADGE[t],
                                       key="f_tier")
            sel_cons = fc3.multiselect("Consultant", cons, key="f_cons")
            sel_cols = st.multiselect("Columns", ALL_COLS, default=ALL_COLS,
                                      key="f_cols")
            st.markdown("---")
            sv1, sv2, sv3, sv4 = st.columns([2, 1, 2, 1])
            sname = sv1.text_input("Save current as", key="f_savename")
            if sv2.button("Save search") and sname.strip():
                saved = _load_saved_searches()
                saved[sname.strip()] = {
                    "f_q": st.session_state.get("f_q", ""),
                    "f_type": sel_type, "f_tier": sel_tier,
                    "f_cons": sel_cons, "f_cols": sel_cols}
                SAVED_SEARCHES.write_text(json.dumps(saved, indent=1),
                                          encoding="utf-8")
                st.success(f"Saved: {sname.strip()}")
            saved = _load_saved_searches()
            pick_s = sv3.selectbox("My saved searches",
                                   ["—"] + sorted(saved), key="f_pick")
            if sv4.button("Apply") and pick_s != "—":
                st.session_state["_apply_search"] = saved[pick_s]
                st.rerun()

        rows = ranked
        if q:
            rows = [r for r in rows if q.lower() in r["legal_name"].lower()]
        if sel_type:
            rows = [r for r in rows if (_pval(r["profile"], "allocator_type")
                                        or "—") in sel_type]
        if sel_tier:
            rows = [r for r in rows if r["routing"]["tier"] in sel_tier]
        if sel_cons:
            rows = [r for r in rows if (_pval(r["profile"], "consultant_name")
                                        or "—") in sel_cons]
        table = [{
            "allocator": r["legal_name"],
            "open": _profile_href(r["canonical_id"]),
            "type": _pval(r["profile"], "allocator_type") or "—",
            "location": _pval(r["profile"], "domicile") or "—",
            "AuM (USD/m)": _fmt_aum(_pval(r["profile"], "total_aum_usd_mm")),
            "consultant": _pval(r["profile"], "consultant_name") or "—",
            "tier": TIER_BADGE[r["routing"]["tier"]],
            "fit": r["routing"]["fit_score"],
            "confidence": r["routing"]["confidence_score"],
            "as of": _latest_asof(r),
        } for r in rows]
        cols = ["open"] + (sel_cols or ALL_COLS)
        st.caption(f"{len(table)} of {len(ranked)} records — click "
                   "'Open' to go to the profile page")
        st.dataframe([{k: t[k] for k in cols} for t in table],
                     use_container_width=True, hide_index=True,
                     column_config={"open": st.column_config.LinkColumn(
                         "open", display_text="Open")})
        if st.button("Export cap intro package (markdown + CSV)"):
            md, csvp = build_package(records)
            st.success(f"Written: out/{md.name} and out/{csvp.name}")
            st.download_button("Download markdown",
                               md.read_text(encoding="utf-8"),
                               file_name=md.name)

    with tab_s:
        all_items = []
        for r in ranked:
            for as_of, field, e in _timeline_items(r, limit=4):
                e = dict(e, fund=r["legal_name"],
                         fund_cid=r["canonical_id"])
                all_items.append((as_of, field, e))
        all_items.sort(key=lambda t: t[0], reverse=True)
        st.markdown(_tl_html(all_items[:15], with_fund=True),
                    unsafe_allow_html=True)

    with tab_c:
        st.caption("Every consultant evidenced in the universe — click "
                   "through for the allocators they advise and the verbatim "
                   "evidence trail.")
        st.dataframe([{
            "consultant": name,
            "open": _consultant_href(name),
            "allocators": len(lst),
            "advises": ", ".join(x["legal_name"] for x in lst[:3])
                       + (" …" if len(lst) > 3 else ""),
        } for name, lst in sorted(cons_map.items(),
                                  key=lambda kv: -len(kv[1]))],
            use_container_width=True, hide_index=True,
            column_config={"open": st.column_config.LinkColumn(
                "open", display_text="Open")})

    with tab_d:
        docs = [{
            "document": p.name,
            "allocator": p.stem.rsplit("_", 1)[0],
            "meeting date": p.stem.rsplit("_", 1)[-1],
            "chars": f"{len(p.read_text(encoding='utf-8')):,}",
        } for p in sorted((REPO / "data" / "raw").glob("*.txt"))]
        st.dataframe(docs, use_container_width=True, hide_index=True)
        st.caption("Full provenance (URL, sha256, retrieval confidence) in "
                   "data/raw/SOURCES.md")

    if wi_funds:
        with tabs[3]:
            st.caption("Licensed With Intelligence trial export — internal "
                       "use only; never merged into the evidence store, "
                       "never sent to any API (data/licensed/LICENSE_NOTE.md)")
            fq = st.text_input("Search funds",
                               placeholder="Search funds or managers",
                               label_visibility="collapsed")
            fx1, fx2, fx3 = st.columns(3)
            strats = sorted({f["Primary Strategy"] for f in wi_funds
                             if f.get("Primary Strategy")})
            regions = sorted({r.strip() for f in wi_funds
                              for r in (f.get("Investment Region") or "").split(",")
                              if r.strip()})
            sel_strat = fx1.multiselect("Primary strategy", strats)
            sel_region = fx2.multiselect("Investment region", regions)
            open_only = fx3.checkbox("Open to investment only")
            sub = wi_funds
            if fq:
                fql = fq.lower()
                sub = [f for f in sub
                       if fql in (f.get("Fund Name") or "").lower()
                       or fql in (f.get("Manager Name") or "").lower()]
            if sel_strat:
                sub = [f for f in sub if f.get("Primary Strategy") in sel_strat]
            if sel_region:
                sub = [f for f in sub
                       if any(r.strip() in sel_region for r in
                              (f.get("Investment Region") or "").split(","))]
            if open_only:
                sub = [f for f in sub if f.get("Open to Investment") == "Yes"]
            cap, expbtn = st.columns([4, 1])
            cap.caption(f"{len(sub):,} of {len(wi_funds):,} funds"
                        + (" · showing first 500" if len(sub) > 500 else ""))
            import io as _io
            import csv as _csv
            _buf = _io.StringIO()
            if sub:
                w = _csv.DictWriter(_buf, fieldnames=list(sub[0].keys()))
                w.writeheader()
                w.writerows(sub)
            expbtn.download_button("Export (CSV)", _buf.getvalue(),
                                   file_name="wi_funds_filtered.csv")
            st.dataframe([{
                "fund": f.get("Fund Name"),
                "manager": f.get("Manager Name"),
                "asset class": f.get("Asset Class") or "—",
                "primary strategy": f.get("Primary Strategy") or "—",
                "region": f.get("Investment Region") or "—",
                "AuM (m)": f.get("Fund AuM (m)") or "—",
                "AuM date": f.get("Fund AuM Date") or "—",
                "mgmt fee": f.get("Management Fee") or "—",
                "perf fee": f.get("Performance Fee") or "—",
                "open": f.get("Open to Investment") or "—",
            } for f in sub[:500]], use_container_width=True, hide_index=True)

    st.divider()
    names = {r["legal_name"]: r for r in ranked}
    pick = st.selectbox("Open profile", list(names))
    render_profile(names[pick])

# ============================================================= performance
elif view == "Performance":
    st.title("Performance")
    wi_funds = _load_wi_funds()
    if not wi_funds:
        st.info("Import a licensed WI funds export first "
                "(python -m src.import_wi <xlsx>).")
        st.stop()
    st.caption("Fee and AuM analytics over the licensed fund universe — "
               "10,000 funds, With Intelligence trial export, internal use "
               "only. Fund return data is not licensed; this page becomes "
               "true performance benchmarking if that module is trialled.")
    import pandas as pd
    df = pd.DataFrame(wi_funds)
    df["mgmt_fee_%"] = pd.to_numeric(df["Management Fee"],
                                     errors="coerce") * 100
    df["perf_fee_%"] = pd.to_numeric(df["Performance Fee"],
                                     errors="coerce") * 100
    df["aum_m"] = pd.to_numeric(df["Fund AuM (m)"], errors="coerce")

    strats = df["Primary Strategy"].value_counts().head(12)
    sel = st.multiselect("Filter strategies", list(strats.index),
                         default=list(strats.index[:6]))
    sub = df[df["Primary Strategy"].isin(sel)] if sel else df

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Funds", f"{len(sub):,}")
    m2.metric("Median mgmt fee", f"{sub['mgmt_fee_%'].median():.2f}%")
    m3.metric("Median perf fee", f"{sub['perf_fee_%'].median():.0f}%")
    m4.metric("Reported AuM", f"${sub['aum_m'].sum():,.0f}m")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("###### Funds by primary strategy")
        st.bar_chart(sub["Primary Strategy"].value_counts().head(10),
                     color="#1A1D21", horizontal=True)
    with c2:
        st.markdown("###### Median management fee by strategy (%)")
        st.bar_chart(sub.groupby("Primary Strategy")["mgmt_fee_%"]
                     .median().dropna().sort_values(ascending=False).head(10),
                     color="#A6864A", horizontal=True)
    st.markdown("###### Fee structure — management vs performance fee")
    scat = sub.dropna(subset=["mgmt_fee_%", "perf_fee_%"])
    scat = scat[(scat["mgmt_fee_%"] < 5) & (scat["perf_fee_%"] < 50)]
    if len(scat) > 1500:
        scat = scat.sample(1500, random_state=7)
    st.scatter_chart(scat, x="mgmt_fee_%", y="perf_fee_%",
                     color="Primary Strategy", size=28)

# ======================================================== discover & add
elif view == "Discover & add allocator":
    st.title("Discover & add allocator")
    st.caption("Give a fund's homepage. The generic ladder finds its newest "
               "minutes, downloads, verifies the document type, records "
               "provenance, and ingests — all from here. Failures are loud.")
    c1, c2 = st.columns(2)
    legal = c1.text_input("Legal name", placeholder="Ohio Public Employees Retirement System")
    cid = c2.text_input("Canonical id", placeholder="opers")
    homepage = st.text_input("Homepage URL (optional — leave blank and the "
                             "system searches the web by name)",
                             placeholder="https://www.opers.org")
    key_default = os.environ.get("GROQ_API_KEY", "")
    groq_key = st.text_input("Groq API key", value=key_default, type="password")

    if st.button("Discover, verify and ingest", type="primary"):
        if not (legal and cid):
            st.error("Legal name and canonical id are required.")
            st.stop()
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
        os.environ.setdefault("SIR_ENSEMBLE_MODELS",
                              "meta-llama/llama-4-scout-17b-16e-instruct")
        if not homepage.strip():
            from websearch import resolve_homepage
            with st.spinner(f"searching the web for {legal}…"):
                homepage = resolve_homepage(legal.strip()) or ""
            if not homepage:
                st.error("Could not resolve a homepage by search — paste one.")
                st.stop()
            st.info(f"Resolved homepage: {homepage}")
        from acquire import acquire
        with st.spinner("ladder (crawl → web search → rendered) → download "
                        "→ classify → provenance → ingest"):
            res = acquire(homepage, cid.strip().lower(), legal.strip())
        st.session_state["acq_result"] = res
        st.session_state["acq_inputs"] = (legal.strip(), cid.strip().lower())

    res = st.session_state.get("acq_result")
    if res:
        for s in res["steps"]:
            st.markdown(f"- {s}")
        if res["ok"]:
            st.success(f"tier {res['tier']} ({res['label']}) · "
                       f"fit {res['fit']} · confidence {res['confidence']}")
            st.caption("Open the Universe view to see it ranked. Consider "
                       "adding it to config/universe.yaml for staleness "
                       "monitoring.")
        else:
            st.error(res["error"])
            if res.get("needs_manual"):
                st.markdown("**Manual assist** — find the minutes PDF in "
                            "your browser (the fund's board/meetings page) "
                            "and paste its direct URL:")
                pdf_url = st.text_input("Minutes PDF URL",
                                        placeholder="https://.../board-minutes-2026-06.pdf")
                if st.button("Download, verify and ingest this PDF"):
                    legal2, cid2 = st.session_state.get("acq_inputs", (legal, cid))
                    from acquire import acquire_direct
                    with st.spinner("download → classify → provenance → ingest"):
                        res2 = acquire_direct(pdf_url.strip(), cid2, legal2)
                    for s in res2["steps"]:
                        st.markdown(f"- {s}")
                    if res2["ok"]:
                        st.success(f"tier {res2['tier']} ({res2['label']}) · "
                                   f"fit {res2['fit']} · confidence "
                                   f"{res2['confidence']} — retrieval marked "
                                   "manual (0.40) in provenance")
                        st.session_state.pop("acq_result", None)
                    else:
                        st.error(res2["error"])

# ================================================================== ingest
else:
    st.title("Ingest a document")
    raw_dir = REPO / "data" / "raw"
    docs = sorted(p.name for p in raw_dir.glob("*.txt"))
    doc_name = st.selectbox("Document", docs)
    cid = st.text_input("Canonical id", value=Path(doc_name).stem.split("_")[0])
    legal = st.text_input("Legal name", value=cid)
    key_default = os.environ.get("GROQ_API_KEY", "")
    groq_key = st.text_input("Groq API key", value=key_default, type="password")
    model = st.selectbox("Model", [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-20b",
    ])
    if (raw_dir / "SOURCES.md").is_file():
        with st.expander("Data provenance (data/raw/SOURCES.md)"):
            st.markdown((raw_dir / "SOURCES.md").read_text(encoding="utf-8"))

    if st.button("Run and save to database", type="primary"):
        document = (raw_dir / doc_name).read_text(encoding="utf-8")
        doc_type = classify(document)
        if doc_type == "unknown" or not is_prompt_ready(doc_type):
            st.error(f"No designed extraction prompt for '{doc_type}' — "
                     "refusing to extract with a stub.")
            st.stop()
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            extractor.GROQ_MODEL = model
        else:
            os.environ.pop("GROQ_API_KEY", None)
            from mock_extractions import disciplined_mock
            extractor.register_mock(disciplined_mock)
            st.warning("No key — using the hand-labelled CalSTRS mock. Only "
                       "meaningful for the CalSTRS document.")
        with st.spinner("classify → extract → resolve → score → route → store"):
            evidence = extractor.extract(document, f"{doc_type}:{Path(doc_name).stem}",
                                         canonical_id=cid, legal_name=legal,
                                         doc_type=doc_type)
            profile = resolve(evidence)
            w = load_weights()
            fit, conf = fit_score(profile, w), confidence_score(profile, w)
            routing = audit_record(fit, conf, w)
            path = save_profile(evidence, profile,
                                scores={"fit": round(fit, 2),
                                        "confidence": round(conf, 3)},
                                routing=routing, source_doc=doc_name)
        st.success(f"{legal}: tier {routing['tier']} ({routing['label']}) · "
                   f"fit {fit:.1f} · confidence {conf:.2f} → {path.name}")
        st.caption("Open the Universe view to see the updated ranking.")
