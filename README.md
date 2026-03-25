# AU Gender Pay Stats

Analyse gender pay gaps at Australian companies using real data from the [Workplace Gender Equality Agency (WGEA)](https://www.wgea.gov.au).

## What it shows

- **Pay gap %** (median & average, total remuneration & base salary) for 2024-25 and 2023-24
- **Workforce quartiles** — what % of top earners are women
- **Senior management breakdown** — % of CEOs, executives, and senior managers who are men vs women
- **Employment type split** — full-time/part-time/casual by gender

Pay figures use WGEA's FTE-equivalent annualised salary, so part-time workers are fairly compared to full-time.

## Setup

```bash
pip3 install openpyxl
python3 fetch_wgea_data.py   # downloads ~200 MB of WGEA data (one-time)
```

## Usage

```bash
# Search by company name
python3 wgea_analyze.py "Commonwealth Bank"
python3 wgea_analyze.py "BHP"
python3 wgea_analyze.py "Woolworths"

# Interactive mode
python3 wgea_analyze.py

# National summary by industry
python3 wgea_analyze.py --industry
```

## Data sources

| File | Source | Licence |
|---|---|---|
| `wgea_employer_pay_gaps.xlsx` | [WGEA Employer Gender Pay Gaps Report](https://www.wgea.gov.au/publications/employer-gender-pay-gaps-report) | CC BY 3.0 AU |
| `wgea_workforce_composition_2024.csv` | [data.gov.au — WGEA Dataset](https://data.gov.au/data/dataset/wgea-dataset) | CC BY 3.0 AU |

The downloaded data files are excluded from this repo via `.gitignore` — run `fetch_wgea_data.py` to get them.

## Other scripts

- `generate_sample_data.py` — generates synthetic employee data (`sample_employees.csv`) for testing
- `analyze_pay.py` — analyses a CSV of your own employee data (see script for column format)
