# AU Gender Pay Stats

Built by Anna Syme and Claude (AI). Uses real data from the [Workplace Gender Equality Agency (WGEA)](https://www.wgea.gov.au).

### Pre-generated results

Click any file to read now — no setup needed.

| Category | Top 20 | Top 100 |
|---|---|---|
| Worst pay gap % | [top20_worst_pay_gap.md](results/top20_worst_pay_gap.md) | [top100_worst_pay_gap.md](results/top100_worst_pay_gap.md) |
| Worst hourly gap ($/hr) | [top20_worst_hourly_gap.md](results/top20_worst_hourly_gap.md) | [top100_worst_hourly_gap.md](results/top100_worst_hourly_gap.md) |
| Fewest women in leadership | [top20_fewest_women_in_leadership.md](results/top20_fewest_women_in_leadership.md) | [top100_fewest_women_in_leadership.md](results/top100_fewest_women_in_leadership.md) |

All tables cover companies with 500+ employees.

### What a company lookup shows

- **Pay gap %** — median and average gender pay gap for 2024-25
- **Approx. hourly gap** — estimated dollar difference per hour (men vs women)
- **Senior management** — breakdown across CEO, executive, and senior manager roles

Pay figures use full-time-equivalent annual salary, so part-time workers are fairly compared to full-time.

### Setup (one-time, ~5 minutes)

You need **Python 3**. To check: open Terminal and run `python3 --version`. If you get a version number, you're good. If not, download from [python.org](https://www.python.org/downloads/).

**1. Download this project**

Click the green **Code** button → **Download ZIP**. Unzip it, open Terminal, and navigate to the folder:
```
cd ~/Downloads/gender-stats-main
```

**2. Install the required library**
```
pip3 install openpyxl
```

**3. Download the WGEA data** (~200 MB, one-time only)
```
python3 fetch_wgea_data.py
```

### Look up a company

```
python3 wgea_analyze.py "Woolworths"
```

Replace `Woolworths` with any Australian company name. If there are multiple matches, you'll pick from a numbered list. Here's what the output looks like (Qantas example):

```
════════════════════════════════════════════════════════════
  Qantas Airways Limited
  Transport, Postal and Warehousing  |  5000+ employees
════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────
  PAY GAP 2024-25 (FTE-equivalent annualised salary)
────────────────────────────────────────────────────────────
  Positive % = men earn more.  Negative % = women earn more.

  Metric                                   2024-25
  Median total remuneration GPG (%)         +32.2%
  Median base salary GPG (%)                +37.0%
  Average total remuneration GPG (%)        +40.1%
  Average base salary GPG (%)               +40.8%
  Approx. hourly gap (men earn more)     ~$49.06/hr
    (based on avg remuneration, 38hr/52wk)

────────────────────────────────────────────────────────────
  SENIOR MANAGEMENT — gender breakdown
────────────────────────────────────────────────────────────
  Role                      Women     Men
  CEOs                          0%   100%
  Other Executives              22%    78%
  Senior Managers               28%    72%
  ─────────────────────────────────────
  All senior roles combined     25%    75%   ⚠ 75% men
```

Other commands:
```
python3 wgea_analyze.py "Commonwealth Bank"   # search by name
python3 wgea_analyze.py                       # browse interactively
python3 wgea_analyze.py --industry            # national industry summary
```

### Regenerate the result tables

The `results/` folder already has pre-built tables. To regenerate them after downloading the data:
```
python3 generate_results.py
```
```
Loading data...
  8,617 employers, 1,652 with senior management data

Generating tables...
  Written: results/top20_worst_pay_gap.md       ← Top 20 by median pay gap %
  Written: results/top100_worst_pay_gap.md      ← Top 100 by median pay gap %
  Written: results/top20_worst_hourly_gap.md    ← Top 20 by estimated $/hr gap
  Written: results/top100_worst_hourly_gap.md   ← Top 100 by estimated $/hr gap
  Written: results/top20_fewest_women_in_leadership.md   ← Top 20 fewest women in senior roles
  Written: results/top100_fewest_women_in_leadership.md  ← Top 100 fewest women in senior roles

Done. Results saved to results/
```
Open `.md` files in a text editor, or view on GitHub where they render as formatted tables.

### Limitations

- **Large employers only** — only companies with 100+ employees are required to report. Smaller companies not included.
- **Private sector focus** — covers private sector employers; some Commonwealth public sector employers included, but not state/territory government.
- **No individual salaries** — figures are aggregated per company, not per person.
- **Pay gap %, not raw hourly rate** — WGEA uses full-time-equivalent annual salary. The $/hr figure shown is an estimate derived from this.
- **Self-reported** — employers report their own data; not independently audited.
- **Australia only.**

### Data sources

All data is publicly available under Creative Commons Attribution 3.0 Australia.

| Data | Source |
|---|---|
| Employer pay gap percentages | [WGEA Employer Gender Pay Gaps Report](https://www.wgea.gov.au/publications/employer-gender-pay-gaps-report) |
| Workforce composition by gender & role | [data.gov.au — WGEA Dataset](https://data.gov.au/data/dataset/wgea-dataset) |

Data files are not stored in this repo — run `fetch_wgea_data.py` to download them.

### Other scripts

- `analyze_pay.py` — analyse a CSV of your own employee data
- `generate_sample_data.py` — generate fake employee data for testing
