# AU Gender Pay Stats

Built by Anna Syme and Claude (AI).

This tool looks up real gender pay gap data for Australian companies, using data published by the [Workplace Gender Equality Agency (WGEA)](https://www.wgea.gov.au). It covers over 8,600 employers.

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

Replace `Woolworths` with any Australian company name. If there are multiple matches, you'll be shown a list to choose from.

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
