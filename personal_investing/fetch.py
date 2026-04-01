"""
fetch.py — data fetching utilities for personal investing research.

Install:
    pip install requests yfinance yt-dlp beautifulsoup4 cloudscraper

Usage:
    python fetch.py fundamentals CVX
    python fetch.py sec CVX [--form 10-K] [--count 5]
    python fetch.py facts CVX [--concept us-gaap/EarningsPerShareBasic]
    python fetch.py insider CVX [--days 180]
    python fetch.py transcript "https://www.youtube.com/watch?v=VIDEO_ID"
    python fetch.py holdings BRK-B
    python fetch.py technicals CVX
    python fetch.py institutions CVX
    python fetch.py politicians CVX [--days 365]
    python fetch.py scan CVX [--insider-days 180] [--politician-days 365]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yfinance as yf
import yt_dlp
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# SEC requires a descriptive User-Agent with a contact email.
SEC_HEADERS = {
    "User-Agent": "personal-investing-tools contact@example.com",
    "Accept-Encoding": "gzip, deflate",
}
SEC_DELAY = 0.15  # SEC allows ~10 req/s

REFERENCES_DIR = Path(__file__).parent / "references"


# ---------------------------------------------------------------------------
# Yahoo Finance
# ---------------------------------------------------------------------------

_FUNDAMENTALS_FIELDS = [
    "longName", "sector", "industry", "marketCap",
    "trailingPE", "forwardPE", "priceToBook",
    "trailingEps", "forwardEps",
    "revenueGrowth", "earningsGrowth",
    "bookValue", "freeCashflow",
    "dividendYield", "payoutRatio",
    "totalRevenue", "netIncomeToCommon",
    "returnOnEquity", "returnOnAssets",
    "debtToEquity",
    "currentPrice", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
]


def get_fundamentals(ticker: str) -> dict:
    """Return key fundamentals for a ticker via Yahoo Finance."""
    info = yf.Ticker(ticker).info
    return {k: info.get(k) for k in _FUNDAMENTALS_FIELDS}


# ---------------------------------------------------------------------------
# SEC EDGAR
# ---------------------------------------------------------------------------

_cik_cache: dict[str, str] = {}


def get_cik(ticker: str) -> str | None:
    """
    Return the zero-padded 10-digit CIK for a ticker via SEC EDGAR.

    Strips exchange suffixes (e.g. ".TO") before searching, so cross-listed
    Canadian companies (CNQ.TO → CNQ) are found correctly.
    """
    clean = re.sub(r"\.[A-Z]+$", "", ticker.upper())
    if clean in _cik_cache:
        return _cik_cache[clean]

    resp = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=SEC_HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    time.sleep(SEC_DELAY)

    for entry in resp.json().values():
        if entry["ticker"].upper() == clean:
            cik = str(entry["cik_str"]).zfill(10)
            _cik_cache[clean] = cik
            return cik
    return None


def get_filings(cik: str, form_type: str = "10-K", count: int = 5) -> list[dict]:
    """Return the most recent filings of a given form type for a CIK."""
    resp = requests.get(
        f"https://data.sec.gov/submissions/CIK{cik}.json",
        headers=SEC_HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    time.sleep(SEC_DELAY)

    recent = resp.json().get("filings", {}).get("recent", {})
    forms       = recent.get("form", [])
    dates       = recent.get("filingDate", [])
    accessions  = recent.get("accessionNumber", [])
    primary_doc = recent.get("primaryDocument", [])

    results = []
    for form, date, acc, doc in zip(forms, dates, accessions, primary_doc):
        if form != form_type:
            continue
        acc_flat = acc.replace("-", "")
        results.append({
            "form": form,
            "date": date,
            "accession": acc,
            "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_flat}/{doc}",
        })
        if len(results) >= count:
            break
    return results


def get_company_facts(cik: str, concept: str | None = None) -> dict:
    """
    Fetch XBRL company facts from SEC EDGAR.

    concept: optional "namespace/tag" filter, e.g. "us-gaap/EarningsPerShareBasic".
    Without it the full facts blob is returned (can be several MB).
    """
    resp = requests.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        headers=SEC_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    time.sleep(SEC_DELAY)

    facts = resp.json()
    if concept is None:
        return facts

    namespace, tag = concept.split("/", 1)
    return facts.get("facts", {}).get(namespace, {}).get(tag, {})


# ---------------------------------------------------------------------------
# 13F Holdings
# ---------------------------------------------------------------------------

def _elem_text(parent: ET.Element, ns: str, tag: str) -> str:
    el = parent.find(f"{ns}{tag}")
    return el.text.strip() if el is not None and el.text else ""


def get_holdings(ticker: str) -> list[dict]:
    """
    Fetch the most recent 13F-HR equity holdings for an institutional filer.

    Example: get_holdings("BRK-B") → Berkshire Hathaway's latest disclosed positions.

    Returns holdings sorted by market value (descending). Each entry:
      issuer, cusip, title, value_thousands (USD), shares.
    """
    cik = get_cik(ticker)
    if not cik:
        raise ValueError(f"CIK not found for '{ticker}'")

    filings = get_filings(cik, form_type="13F-HR", count=1)
    if not filings:
        raise ValueError(f"No 13F-HR filings found for '{ticker}'")

    filing = filings[0]
    acc_flat = filing["accession"].replace("-", "")
    cik_int = int(cik)

    # Fetch the filing index page to locate the infotable XML
    index_url = (
        f"https://www.sec.gov/Archives/edgar/data/{cik_int}"
        f"/{acc_flat}/{filing['accession']}-index.htm"
    )
    resp = requests.get(index_url, headers=SEC_HEADERS, timeout=15)
    resp.raise_for_status()
    time.sleep(SEC_DELAY)

    soup = BeautifulSoup(resp.text, "html.parser")
    infotable_name = None
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 4:
            doc_type = cells[3].get_text(strip=True).upper()
            if doc_type == "INFORMATION TABLE":
                doc_link = cells[2].find("a", href=True)
                if doc_link and doc_link["href"].lower().endswith(".xml"):
                    infotable_name = doc_link["href"].split("/")[-1]
                    break

    if not infotable_name:
        raise FileNotFoundError(
            f"No INFORMATION TABLE XML found in filing {filing['accession']}.\n"
            f"Check manually: {index_url}"
        )

    # Fetch and parse the infotable XML
    xml_url = (
        f"https://www.sec.gov/Archives/edgar/data/{cik_int}"
        f"/{acc_flat}/{infotable_name}"
    )
    resp = requests.get(xml_url, headers=SEC_HEADERS, timeout=30)
    resp.raise_for_status()
    time.sleep(SEC_DELAY)

    root = ET.fromstring(resp.content)
    ns = "{" + root.tag[1:].split("}")[0] + "}" if root.tag.startswith("{") else ""

    holdings = []
    for info in root.findall(f"{ns}infoTable"):
        shrs_el = info.find(f"{ns}shrsOrPrnAmt")
        shares = ""
        if shrs_el is not None:
            s = shrs_el.find(f"{ns}sshPrnamt")
            shares = s.text.strip() if s is not None and s.text else ""

        holdings.append({
            "issuer": _elem_text(info, ns, "nameOfIssuer"),
            "title": _elem_text(info, ns, "titleOfClass"),
            "cusip": _elem_text(info, ns, "cusip"),
            "value_usd": _elem_text(info, ns, "value"),
            "shares": shares,
            "filing_date": filing["date"],
        })

    return sorted(
        holdings,
        key=lambda h: int(h["value_usd"].replace(",", "") or 0),
        reverse=True,
    )


# ---------------------------------------------------------------------------
# Insider Trading — OpenInsider
# ---------------------------------------------------------------------------

def get_insider_trades(ticker: str, days: int = 180) -> list[dict]:
    """
    Scrape OpenInsider for recent insider transactions.

    Returns only open-market purchases (trade type "P - Purchase") — the most
    meaningful signal. Awards, options exercises, and gifts are excluded.
    """
    url = (
        "https://openinsider.com/screener"
        f"?s={ticker.upper()}&fd={days}&cnt=100&sortcol=1&page=1"
    )
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", class_="tinytable")
    if not table:
        return []

    header_row = table.find("tr")
    raw_headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    # Normalise column names
    headers = [
        h.lower().replace(" ", "_").replace("%", "pct").replace("δ", "delta")
        for h in raw_headers
    ]

    trades = []
    for row in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells:
            continue
        trade = dict(zip(headers, cells))
        if "P - Purchase" in trade.get("trade_type", ""):
            trades.append(trade)

    return trades


# ---------------------------------------------------------------------------
# YouTube — yt-dlp transcript
# ---------------------------------------------------------------------------

def _extract_video_id(url: str) -> str | None:
    for pat in [
        r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def _vtt_to_text(vtt_path: Path) -> str:
    """
    Convert a VTT subtitle file to clean plain text.

    Auto-generated YouTube captions overlap heavily — consecutive duplicate
    lines are deduplicated so the transcript reads as continuous prose.
    """
    raw = vtt_path.read_text(encoding="utf-8")
    raw = re.sub(r"WEBVTT.*?\n\n", "", raw, flags=re.DOTALL)           # strip header
    raw = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> .*\n", "", raw)        # timestamps
    raw = re.sub(r"^\s*\d+\s*$", "", raw, flags=re.MULTILINE)           # cue numbers
    raw = re.sub(r"<[^>]+>", "", raw)                                    # VTT/HTML tags

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    deduped: list[str] = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    return " ".join(deduped)


def download_transcript(url: str, out_dir: Path | None = None) -> Path:
    """
    Download the English transcript for a YouTube video and save as markdown.

    Saves to: {out_dir}/{video_id}/transcript.md
    Default out_dir: references/youtube/ (relative to this file).
    """
    video_id = _extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not parse video ID from: {url}")

    base = (out_dir or REFERENCES_DIR / "youtube") / video_id
    base.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": str(base / "%(id)s"),
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    title    = info.get("title", "Unknown Title")
    channel  = info.get("uploader", "Unknown Channel")
    duration = info.get("duration_string", "")

    vtt_file = base / f"{video_id}.en.vtt"
    if not vtt_file.exists():
        raise FileNotFoundError(
            f"No English subtitles found for video {video_id}. "
            "The video may not have auto-generated captions enabled."
        )

    body = _vtt_to_text(vtt_file)
    vtt_file.unlink()

    md = (
        f"# {title}\n\n"
        f"**Channel:** {channel}  \n"
        f"**Duration:** {duration}  \n"
        f"**URL:** {url}\n\n"
        f"---\n\n"
        f"{body}\n"
    )
    out_path = base / "transcript.md"
    out_path.write_text(md, encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Technicals
# ---------------------------------------------------------------------------

def get_technicals(ticker: str, period: str = "2y") -> dict:
    """
    Return key price action and technical indicators for a ticker.

    Covers: current price, 50/200-day MAs, % distance from each, RSI(14),
    52-week high/low, and a flag if price is within 5% of the 200DMA.
    """
    hist = yf.Ticker(ticker).history(period=period)
    if hist.empty:
        raise ValueError(f"No price history found for '{ticker}'")

    close = hist["Close"]
    current = float(close.iloc[-1])

    ma50 = float(close.rolling(50).mean().iloc[-1])
    ma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else None

    # RSI(14) — Wilder's smoothing via EWM
    delta = close.diff()
    avg_gain = delta.clip(lower=0).ewm(com=13, min_periods=14).mean()
    avg_loss = (-delta.clip(upper=0)).ewm(com=13, min_periods=14).mean()
    rsi = float((100 - (100 / (1 + avg_gain / avg_loss))).iloc[-1])

    week52 = close.tail(252)
    high52 = float(week52.max())
    low52 = float(week52.min())

    return {
        "ticker": ticker.upper(),
        "price": round(current, 2),
        "ma50": round(ma50, 2),
        "pct_from_ma50": round((current - ma50) / ma50 * 100, 2),
        "ma200": round(ma200, 2) if ma200 else None,
        "pct_from_ma200": round((current - ma200) / ma200 * 100, 2) if ma200 else None,
        "approaching_200dma": (abs((current - ma200) / ma200 * 100) <= 5) if ma200 else False,
        "rsi_14": round(rsi, 1),
        "52w_high": round(high52, 2),
        "52w_low": round(low52, 2),
        "pct_from_52w_high": round((current - high52) / high52 * 100, 2),
    }


# ---------------------------------------------------------------------------
# Institutional Ownership
# ---------------------------------------------------------------------------

def get_institutions(ticker: str) -> dict:
    """
    Return top institutional holders and ownership breakdown via Yahoo Finance.
    """
    t = yf.Ticker(ticker)
    result: dict = {"ticker": ticker.upper()}

    major = t.major_holders
    if major is not None and not major.empty:
        result["major_holders"] = major["Value"].to_dict()

    inst = t.institutional_holders
    if inst is not None and not inst.empty:
        result["top_institutions"] = [
            {k: str(v) for k, v in row.items()}
            for _, row in inst.head(15).iterrows()
        ]

    return result


# ---------------------------------------------------------------------------
# Politician / Congressional Trades
# ---------------------------------------------------------------------------

def get_politician_trades(ticker: str, days: int = 365) -> list[dict]:
    """
    Fetch recent congressional trades (House + Senate) for a ticker.

    Source: QuiverQuant (quiverquant.com/congresstrading/) — scrapes the
    per-ticker page which embeds all historical trades in an HTML table.
    Returns trades sorted by transaction_date descending.

    Install: pip install cloudscraper  (handles Cloudflare)
    """
    import cloudscraper
    from datetime import datetime, timedelta, timezone

    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)

    scraper = cloudscraper.create_scraper()
    resp = scraper.get(
        f"https://www.quiverquant.com/congresstrading/stock/{ticker.upper()}",
        timeout=30,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []

    trades: list[dict] = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < 5:
            continue

        # Cell 0: Stock — spans contain [ticker, company name, share class]
        # Cell 1: Transaction — spans contain [type (Purchase/Sale), amount range]
        # Cell 2: Politician — spans contain [name, "House / R" or "Senate / D"]
        # Cell 3: Filed date
        # Cell 4: Traded date
        # Cell 5: Description

        spans_1 = cells[1].find_all("span")
        tx_type = spans_1[0].get_text(strip=True) if spans_1 else ""
        tx_amount = spans_1[1].get_text(strip=True) if len(spans_1) > 1 else ""

        spans_2 = cells[2].find_all("span")
        politician_name = spans_2[0].get_text(strip=True) if spans_2 else ""
        chamber_party = spans_2[1].get_text(strip=True) if len(spans_2) > 1 else ""

        # Parse "House / R" or "Senate / D"
        source = ""
        party = ""
        if " / " in chamber_party:
            parts = chamber_party.split(" / ", 1)
            source = parts[0].strip().lower()
            party = parts[1].strip()

        filed_date = cells[3].get_text(strip=True)
        traded_date = cells[4].get_text(strip=True)

        # Parse dates and apply cutoff (use filed date as fallback)
        traded_iso = traded_date
        filed_iso = filed_date
        try:
            filed_dt = datetime.strptime(filed_date, "%b %d, %Y").replace(
                tzinfo=timezone.utc
            )
            filed_iso = filed_dt.strftime("%Y-%m-%d")
        except ValueError:
            filed_dt = None

        try:
            trade_dt = datetime.strptime(traded_date, "%b %d, %Y").replace(
                tzinfo=timezone.utc
            )
            traded_iso = trade_dt.strftime("%Y-%m-%d")
            if trade_dt < cutoff:
                continue
        except ValueError:
            # No valid trade date — use filing date for cutoff
            if filed_dt and filed_dt < cutoff:
                continue

        trades.append({
            "source": source,
            "politician": politician_name,
            "party": party,
            "type": tx_type,
            "amount": tx_amount,
            "transaction_date": traded_iso,
            "disclosure_date": filed_iso,
        })

    return sorted(
        trades,
        key=lambda x: x.get("transaction_date", ""),
        reverse=True,
    )


# ---------------------------------------------------------------------------
# Research Scan
# ---------------------------------------------------------------------------

def scan(ticker: str, insider_days: int = 180, politician_days: int = 365) -> dict:
    """
    Full research snapshot for a ticker.

    Aggregates: fundamentals, technicals, recent 10-K/10-Q filings, top
    institutional holders, insider open-market purchases, and congressional trades.
    """
    def _safe(label: str, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            return {"error": f"{label}: {exc}"}

    result: dict = {"ticker": ticker.upper()}
    result["fundamentals"] = _safe("fundamentals", get_fundamentals, ticker)
    result["technicals"] = _safe("technicals", get_technicals, ticker)

    cik = get_cik(ticker)
    if cik:
        result["recent_filings"] = (
            _safe("10-K filings", get_filings, cik, form_type="10-K", count=3) or []
        ) + (
            _safe("10-Q filings", get_filings, cik, form_type="10-Q", count=2) or []
        )
    else:
        result["recent_filings"] = []

    result["institutions"] = _safe("institutions", get_institutions, ticker)
    result["insider_trades"] = _safe("insider_trades", get_insider_trades, ticker, days=insider_days)
    result["politician_trades"] = _safe("politician_trades", get_politician_trades, ticker, days=politician_days)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, default=str))


def _require_cik(ticker: str) -> str:
    cik = get_cik(ticker)
    if not cik:
        print(f"error: CIK not found for '{ticker}' — may not be SEC-registered", file=sys.stderr)
        sys.exit(1)
    return cik


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch investing research data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fundamentals", help="Yahoo Finance fundamentals")
    p.add_argument("ticker")

    p = sub.add_parser("sec", help="SEC EDGAR recent filings list")
    p.add_argument("ticker")
    p.add_argument("--form",  default="10-K", help="Form type  (default: 10-K)")
    p.add_argument("--count", type=int, default=5)

    p = sub.add_parser("facts", help="SEC EDGAR XBRL company facts")
    p.add_argument("ticker")
    p.add_argument("--concept", default=None,
                   help="e.g. us-gaap/EarningsPerShareBasic  (omit for full blob)")

    p = sub.add_parser("insider", help="Insider open-market purchases (OpenInsider)")
    p.add_argument("ticker")
    p.add_argument("--days", type=int, default=180)

    p = sub.add_parser("holdings", help="Most recent 13F-HR holdings (e.g. BRK-B for Berkshire)")
    p.add_argument("ticker")

    p = sub.add_parser("technicals", help="Price action + 50/200DMA + RSI(14)")
    p.add_argument("ticker")

    p = sub.add_parser("institutions", help="Top institutional holders (Yahoo Finance)")
    p.add_argument("ticker")

    p = sub.add_parser("politicians", help="Congressional trades (House + Senate)")
    p.add_argument("ticker")
    p.add_argument("--days", type=int, default=365)

    p = sub.add_parser("scan", help="Full research snapshot (fundamentals + technicals + filings + institutions + insiders + politicians)")
    p.add_argument("ticker")
    p.add_argument("--insider-days", type=int, default=180)
    p.add_argument("--politician-days", type=int, default=365)

    p = sub.add_parser("transcript", help="Download YouTube transcript as markdown")
    p.add_argument("url")
    p.add_argument("--out", default=None, help="Output directory  (default: references/youtube/)")

    args = parser.parse_args()

    if args.cmd == "fundamentals":
        _print_json(get_fundamentals(args.ticker))

    elif args.cmd == "sec":
        cik = _require_cik(args.ticker)
        print(f"CIK: {cik}\n")
        _print_json(get_filings(cik, form_type=args.form, count=args.count))

    elif args.cmd == "facts":
        cik = _require_cik(args.ticker)
        _print_json(get_company_facts(cik, concept=args.concept))

    elif args.cmd == "insider":
        _print_json(get_insider_trades(args.ticker, days=args.days))

    elif args.cmd == "holdings":
        _print_json(get_holdings(args.ticker))

    elif args.cmd == "technicals":
        _print_json(get_technicals(args.ticker))

    elif args.cmd == "institutions":
        _print_json(get_institutions(args.ticker))

    elif args.cmd == "politicians":
        _print_json(get_politician_trades(args.ticker, days=args.days))

    elif args.cmd == "scan":
        _print_json(scan(args.ticker, insider_days=args.insider_days, politician_days=args.politician_days))

    elif args.cmd == "transcript":
        out_dir = Path(args.out) if args.out else None
        path = download_transcript(args.url, out_dir=out_dir)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
