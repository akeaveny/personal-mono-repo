---
timestamp_local: "2026-03-30 ET"
timestamp_utc: "2026-03-30T00:00:00Z"
source_type: "13f"
source: "SEC EDGAR 13F — Fisher Asset Management Q4 2025 + Yahoo Finance institutional data"
url: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000850529&type=13F-HR"
tickers: [FCX, SCCO, TECK, RIO, BHP, VALE]
tags: [filing, materials]
summary: "Full research session on FCX position (currently losing). Ran scan, peer technicals, and institutional flow across copper names. Key finding: FCX and peers in broad sector selloff (-20-27% from highs), Fisher running a $6.9B copper basket with FCX as top conviction name, Franklin +31% add is bullish signal, but Wellington/Capital Research both trimming 14-16%. 200DMA at $48.24 is the key support level."
thesis_impact: "MIXED"
conviction_delta: -1
status: "logged"
---

# FCX Position Review — Copper Peer Analysis & Institutional Flow

Research session: 2026-03-30 | Position status: Losing

## Context

Existing FCX position in drawdown. Session objective: determine whether to hold, sell, or add.
Data pulled via `fetch.py scan FCX`, `fetch.py institutions` on peers, and Fisher Asset Management's
Q4 2025 13F (CIK: 0000850529, filed 2026-02-09, $293B AUM).

---

## FCX Snapshot

| Metric | Value |
|--------|-------|
| Price | $54.65 |
| 52w High | $68.82 |
| vs 52w High | **-20.6%** |
| 200DMA | $48.24 |
| vs 200DMA | +13.3% |
| 50DMA | $61.19 |
| vs 50DMA | **-10.7%** (broke below) |
| RSI(14) | 40.3 — weak, not yet oversold |
| Trailing PE | 35.95x |
| Forward PE | **14.46x** |
| Forward EPS | $3.78 vs trailing $1.52 |
| Earnings growth | +47.7% YoY |
| Revenue growth | -1.5% |
| Free cash flow | $1.56B |

---

## Copper Peer Technicals

| Ticker | Price | vs 50DMA | vs 200DMA | RSI | vs 52w High | Character |
|--------|-------|----------|-----------|-----|-------------|-----------|
| **FCX** | $54.65 | -10.7% | +13.3% | 40.3 | -20.6% | Pure play copper |
| **SCCO** | $159.28 | -15.6% | +18.2% | 38.1 | -27.2% | Pure play copper (Grupo Mexico 89%) |
| **TECK** | $48.32 | -10.8% | +10.3% | 40.9 | -21.2% | Diversified Canadian miner |
| **RIO** | $88.82 | -2.3% | +24.2% | 49.3 | -9.4% | Diversified (iron ore + copper) |
| **BHP** | $69.02 | -2.9% | +18.5% | 45.8 | -15.2% | Diversified (iron ore + copper) |

FCX, SCCO, TECK are in a deeper drawdown than RIO/BHP — pure copper plays carry more
price leverage. RIO and BHP are holding up better due to diversification and dividend support
(RIO ~6%, BHP ~5%).

---

## Institutional Flow (Q4 2025)

### Fisher Asset Management — Full Copper Basket ($6.9B, 2.35% of AUM)

| Ticker | Position | % AUM | Shares | Portfolio Rank |
|--------|----------|-------|--------|----------------|
| FCX | $3.24B | 1.11% | 63.9M | #25 of 1,017 |
| RIO | $1.57B | 0.54% | 19.6M | #49 |
| BHP | $1.41B | 0.48% | 23.4M | #59 |
| SCCO | $0.36B | 0.12% | 2.5M | #111 |
| VALE | $0.28B | 0.10% | 21.6M | #120 |

Fisher is the #1 institutional holder of both RIO and BHP ADRs. FCX is their highest-conviction
copper name but they diversify across the whole sector. They hold FCX at 2x the weight of any
other single copper name.

### Cross-Name Institutional Flow Summary

| Fund | FCX | RIO | BHP | Direction |
|------|-----|-----|-----|-----------|
| Fisher Asset Management | +1.0% | +2.7% | +1.1% | Adding broadly |
| **Franklin Resources** | **+31.2%** | — | — | Strong FCX conviction buy |
| Morgan Stanley | +10.1% | -5.5% | +22.8% | Rotating FCX/RIO → BHP |
| **Wellington Management** | **-14.2%** | — | -21.8% | Reducing copper broadly |
| **Capital Research Global** | **-16.3%** | — | — | Reducing FCX specifically |
| Goldman Sachs | — | +0.8% | -32.8% | Cutting diversified mining |

---

## Key Claims

1. **FCX is a commodity price bet, not a moated business.** Earnings are almost entirely a function of copper price. Forward PE of 14.46x is reasonable IF copper stays above midcycle — but trailing PE of 36x shows the current valuation on backward earnings.
2. **Franklin Resources' +31% add is the most meaningful signal.** Not a passive index rebalance — a deliberate active conviction increase at lower prices. Franklin Templeton is a value-oriented manager; this is a buy-the-dip call.
3. **Wellington and Capital Research trimming 14-16% is a meaningful counter-signal.** Both are large active managers reducing copper exposure broadly — not just FCX.
4. **Fisher's basket approach suggests RIO/BHP as lower-risk copper alternatives.** Same commodity exposure, better diversification, higher dividends, less price volatility. Morgan Stanley is actively rotating from RIO toward BHP.
5. **$48.24 is the critical 200DMA support.** FCX is 13.3% above it. A break below confirms the long-term uptrend is broken and changes the hold thesis entirely.
6. **SCCO is most technically oversold** (RSI 38.1, -27% from 52w high) but 89% controlled by Grupo Mexico — very limited institutional float, not a clean trade.
7. **The entire sector faces the same Morningstar risk.** Copper at ~$5.90/lb vs Morningstar's $3.80 midcycle estimate. If copper normalizes, forward earnings across FCX, SCCO, TECK, RIO, BHP all deteriorate.

---

## Thesis Impact

- **Impact:** MIXED
- **Tickers affected:** FCX, SCCO, TECK, RIO, BHP
- **Claims touched:**
  - *SUPPORTS* — Energy transition / deglobalization macro thesis still intact. Copper demand from EVs, grid expansion, and reshoring is a structural decade-long driver. Fisher and Franklin's active adds reflect this.
  - *CONTRADICTS* — Morningstar copper midcycle ($3.80 vs $5.90 current) is a serious challenge to the forward earnings thesis. FCX is only cheap at 14.46x forward PE if current copper prices are sustained.
  - *CONTRADICTS* — Wellington and Capital Research both reducing. Two large active shops independently reducing copper exposure is a meaningful institutional vote of caution.
  - *NEUTRAL* — Mark Meldrum's "overweight materials via FCX" thesis from logged research was bullish, but his broader caution on commodities (lower oil structural) suggests commodity price risk is real across the board.

---

## Decision Framework

| Scenario | Action |
|----------|--------|
| Copper thesis intact, can hold drawdown | Hold. Hard stop at 200DMA ($48.24). |
| Want to reduce risk, still believe thesis | Trim to half, hold remainder with $48 stop. |
| No longer convicted on copper above midcycle | Sell. Morningstar midcycle = significant further downside. |
| High conviction, want more copper exposure | Consider RIO or BHP instead — same thesis, better risk profile. |
| High conviction on FCX specifically | Add near $48–50 (200DMA zone), not at current $54. |

## What I'm Taking Away

- **Hold with a $48 stop** is the base case given: (1) Franklin's +31% conviction add, (2) Fisher's sustained copper basket, (3) RSI approaching but not at oversold, (4) forward PE reasonable if earnings materialize.
- **Do not add here at $54.** The 200DMA at $48 is the natural add point if the thesis holds. Adding now means accepting 12% further downside to support before any margin of safety.
- **RIO as partial hedge.** If reducing FCX feels right, RIO is the logical rotation — same copper exposure, Fisher's #2 copper name, better technical (only -9% from 52w high), ~6% dividend yield provides a floor.
- **Revisit after Q1 2026 earnings** (~April 2026). FCX will report Q1 results then — revenue/earnings vs consensus will either validate or break the forward PE thesis. Copper price at that point is the key input.

## TODO

- [ ] Re-evaluate FCX hold/sell/add after Q1 2026 earnings report (~April 2026)
- [ ] Monitor copper spot price vs $5.90 current and Morningstar $3.80 midcycle
- [ ] Set price alert at $48.24 (200DMA) — break below = exit trigger

## Source

Fisher Asset Management Q4 2025 13F: [SEC EDGAR](https://www.sec.gov/Archives/edgar/data/850529/000085052926000002/0000850529-26-000002-index.htm)
Institutional data via `fetch.py institutions` on FCX, SCCO, TECK, RIO, BHP.
Analysis run: 2026-03-30 via `fetch.py scan FCX`.
