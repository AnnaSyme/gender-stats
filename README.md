# AU Gender Pay Stats

Built by Anna Syme and Claude (AI).

This tool looks up real gender pay gap data for Australian companies, using data published by the [Workplace Gender Equality Agency (WGEA)](https://www.wgea.gov.au). 

## Pre-generated results

Click any file name below to see pre-generated results. 

**Worst pay gap for women** (ranked by median total remuneration gap, companies with 500+ employees):

| File | What it shows |
|---|---|
| [top20_worst_pay_gap.md](results/top20_worst_pay_gap.md) | Top 20 companies |
| [top100_worst_pay_gap.md](results/top100_worst_pay_gap.md) | Top 100 companies |

**Worst hourly pay gap for women** (ranked by estimated $/hr men earn more than women, companies with 500+ employees):

| File | What it shows |
|---|---|
| [top20_worst_hourly_gap.md](results/top20_worst_hourly_gap.md) | Top 20 companies |
| [top100_worst_hourly_gap.md](results/top100_worst_hourly_gap.md) | Top 100 companies |

**Fewest women in senior leadership** (CEOs, executives, senior managers — companies with 500+ employees, at least 5 people in senior roles):

| File | What it shows |
|---|---|
| [top20_fewest_women_in_leadership.md](results/top20_fewest_women_in_leadership.md) | Top 20 companies |
| [top100_fewest_women_in_leadership.md](results/top100_fewest_women_in_leadership.md) | Top 100 companies |

---

## What it shows

For any Australian company you search for:

- **Pay gap %** — how much more (or less) men earn compared to women, for 2024-25 and 2023-24
- **Workforce quartiles** — what % of the top earners are women vs the bottom earners
- **Senior management** — % of CEOs, executives, and senior managers who are men vs women
- **Employment types** — how many men and women work full-time, part-time, or casually

Pay figures use full-time-equivalent annual salary, so part-time workers are fairly compared to full-time.

---

## Before you start — what you need

You need **Python 3** installed on your computer. To check, open Terminal and type:

```
python3 --version
```

If you see a version number (e.g. `Python 3.11.2`), you're good. If not, download Python from [python.org](https://www.python.org/downloads/).

---

## Step 1 — Download this project

Click the green **Code** button on this page, then **Download ZIP**. Unzip it, and open Terminal.

Navigate to the folder you just unzipped. For example:

```
cd ~/Downloads/gender-stats-main
```

---

## Step 2 — Install the one required library

Copy and paste this into Terminal, then press Enter:

```
pip3 install openpyxl
```

You only need to do this once.

---

## Step 3 — Download the WGEA data

This downloads the real pay gap data from the Australian government (~200 MB, one-time only):

```
python3 fetch_wgea_data.py
```

Wait for it to finish. You only need to do this once.

---

## Step 4 — Look up a company

```
python3 wgea_analyze.py "Woolworths"
```

Replace `Woolworths` with any Australian company name. If there are multiple matches, you'll be shown a numbered list to choose from.

The results print directly to your Terminal — no file is created. Here's what you'll see (using Qantas as an example):

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
  WORKFORCE QUARTILES — % women in each pay quartile
────────────────────────────────────────────────────────────
  Upper quartile (top earners)               19%   $178,804
  Upper-middle quartile                      26%   $107,827
  Lower-middle quartile                      37%    $74,773
  Lower quartile (bottom earners)            40%    $53,088
  Total workforce                            33%   $103,588

────────────────────────────────────────────────────────────
  SENIOR MANAGEMENT — gender breakdown
────────────────────────────────────────────────────────────
  Role                      Women     Men
  CEOs                          0%   100%
  Other Executives              22%    78%
  Senior Managers               28%    72%
  ─────────────────────────────────────
  All senior roles combined     25%    75%   ⚠ 75% men

────────────────────────────────────────────────────────────
  EMPLOYMENT TYPES
────────────────────────────────────────────────────────────
  Type         Women     Men
  Full-time      52%      48%
  Part-time      73%      27%
  Casual         56%      44%
```

Other examples:

```
python3 wgea_analyze.py "Commonwealth Bank"
python3 wgea_analyze.py "BHP"
python3 wgea_analyze.py "Qantas"
```

**Just want to browse?** Run without a name and you'll be prompted:

```
python3 wgea_analyze.py
```

**See a summary across all industries:**

```
python3 wgea_analyze.py --industry
```

---

## Optional — Regenerate the pre-built result tables

The `results/` folder already contains pre-built tables (see top of this page). If you want to regenerate them yourself after downloading the data:

```
python3 generate_results.py
```

You'll see this in your Terminal:

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

Open any of those `.md` files in a text editor, or view them on GitHub where they render as formatted tables. All tables are filtered to companies with 500 or more employees.

---

## Limitations of this data

- **Large employers only** — reporting is only required from employers with **100 or more employees**. Smaller companies are not included.
- **Private sector focus** — the pay gap spreadsheet covers private sector employers. Some Commonwealth public sector employers are included, but state/territory government employers are not.
- **No individual salaries** — the data shows aggregated figures per company, not individual employee pay. You can see the gap between men and women, but not exact salaries.
- **Pay gap %, not hourly rate** — WGEA reports a gender pay gap percentage using full-time-equivalent annual salary. It accounts for part-time work by converting everyone to a full-time equivalent, rather than reporting an actual hourly rate.
- **Self-reported** — employers report their own data to WGEA. While WGEA does some validation, figures are not independently audited.
- **Australia only** — this tool currently uses Australian data only.

---

## Data sources

All data is publicly available under Creative Commons Attribution 3.0 Australia.

| Data | Source |
|---|---|
| Employer pay gap percentages | [WGEA Employer Gender Pay Gaps Report](https://www.wgea.gov.au/publications/employer-gender-pay-gaps-report) |
| Workforce composition by gender & role | [data.gov.au — WGEA Dataset](https://data.gov.au/data/dataset/wgea-dataset) |

The data files themselves are not stored in this repo — run `fetch_wgea_data.py` to download them to your computer.

---

## Other scripts

- `analyze_pay.py` — analyse a CSV file of your own employee data (see the script for the required column format)
- `generate_sample_data.py` — generate fake employee data for testing
