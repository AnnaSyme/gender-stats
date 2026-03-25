"""
Generate pre-computed result tables and save to results/ folder.

Produces:
  results/top20_worst_pay_gap.md         — companies where women are paid least vs men
  results/top20_fewest_women_in_leadership.md — companies with fewest women in senior roles

Filters to companies with 500+ employees for meaningful comparisons.
Run after fetch_wgea_data.py.
"""

import csv
import os
import openpyxl
from collections import defaultdict
from datetime import datetime

LARGE_SIZES   = {"500-999", "1000-4999", "5000+"}
SENIOR_ROLES  = {
    "CEOs",
    "Other Executives and General Managers",
    "Senior Managers",
    "Key Management Personnel",
}
OUTPUT_DIR = "results"


def load_pay_gap():
    wb = openpyxl.load_workbook("wgea_employer_pay_gaps.xlsx", read_only=True, data_only=True)
    ws = wb["2. Employers "]
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[3]
    data = [dict(zip(headers, r)) for r in rows[4:] if r[0]]
    wb.close()
    return data


def load_senior_management():
    senior = defaultdict(lambda: {"Men": 0, "Women": 0, "size": "", "industry": ""})
    with open("wgea_workforce_composition_2024.csv", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["employer_size"] not in LARGE_SIZES:
                continue
            if r.get("occupation") not in SENIOR_ROLES:
                continue
            name = r["employer_name"]
            senior[name][r["gender"]] += int(r["n_employees"])
            senior[name]["size"]     = r["employer_size"]
            senior[name]["industry"] = r["anzsic_division"]
    return senior


def fmt_pct(val):
    if val is None or val == "":
        return "n/a"
    try:
        return f"{float(val) * 100:.1f}%"
    except (ValueError, TypeError):
        return "n/a"


def write_pay_gap_table(employers):
    # Filter: 500+ employees, valid positive median total remuneration GPG
    rows = []
    for e in employers:
        if e.get("Employer size range   (# employees)") not in LARGE_SIZES:
            continue
        val = e.get("Median total remuneration GPG (%)")
        if val is None or val == "":
            continue
        try:
            gpg = float(val)
        except (ValueError, TypeError):
            continue
        rows.append((
            e["Employer name"],
            e.get("Industry (ANZSIC Division)", ""),
            e.get("Employer size range   (# employees)", ""),
            gpg,
        ))

    # Sort descending — highest gap (most disadvantaged for women) first
    rows.sort(key=lambda x: x[3], reverse=True)

    note = datetime.now().strftime('%d %B %Y')
    footer = "> **How to read this:** A gap of +30% means men's median pay is 30% higher than women's median pay at that company."

    for n in [20, 100]:
        top_n = rows[:n]
        lines = [
            f"# Top {n}: Worst Pay Gap for Women (companies with 500+ employees)",
            "",
            "Ranked by **median total remuneration gender pay gap** — the higher the %,",
            "the more men earn compared to women at that company.",
            "",
            "Pay figures use full-time-equivalent annual salary, so part-time workers",
            "are fairly compared to full-time employees.",
            "",
            f"_Source: WGEA 2024-25 Employer Gender Pay Gaps data. Generated {note}._",
            "",
            "| # | Company | Industry | Size | Median pay gap |",
            "|---|---------|----------|------|---------------|",
        ]
        for i, (name, industry, size, gpg) in enumerate(top_n, 1):
            lines.append(f"| {i} | {name} | {industry} | {size} | +{gpg*100:.1f}% |")
        lines += ["", footer]

        path = os.path.join(OUTPUT_DIR, f"top{n}_worst_pay_gap.md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  Written: {path}")


def write_leadership_table(senior):
    rows = []
    for name, counts in senior.items():
        total = counts["Men"] + counts["Women"]
        if total < 5:
            continue
        pct_women = counts["Women"] / total
        rows.append((
            name,
            counts["industry"],
            counts["size"],
            counts["Men"],
            counts["Women"],
            total,
            pct_women,
        ))

    # Sort ascending by % women — fewest women first
    rows.sort(key=lambda x: x[6])

    note = datetime.now().strftime('%d %B %Y')
    footer = "> Senior roles include: CEOs, Other Executives and General Managers, Senior Managers, and Key Management Personnel."

    for n in [20, 100]:
        top_n = rows[:n]
        lines = [
            f"# Top {n}: Fewest Women in Senior Leadership (companies with 500+ employees)",
            "",
            "Ranked by the **lowest percentage of women** in senior roles (CEOs, executives,",
            "senior managers, and key management personnel).",
            "",
            "Only companies with at least 5 people in senior roles are included.",
            "",
            f"_Source: WGEA 2024-25 Workforce Composition data. Generated {note}._",
            "",
            "| # | Company | Industry | Size | Men | Women | % Women |",
            "|---|---------|----------|------|-----|-------|---------|",
        ]
        for i, (name, industry, size, men, women, total, pct_women) in enumerate(top_n, 1):
            lines.append(
                f"| {i} | {name} | {industry} | {size} | {men} | {women} | {pct_women*100:.0f}% |"
            )
        lines += ["", footer]

        path = os.path.join(OUTPUT_DIR, f"top{n}_fewest_women_in_leadership.md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  Written: {path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Loading data...")
    employers = load_pay_gap()
    senior    = load_senior_management()
    print(f"  {len(employers):,} employers, {len(senior):,} with senior management data\n")

    print("Generating tables...")
    write_pay_gap_table(employers)
    write_leadership_table(senior)
    print("\nDone. Results saved to results/")


if __name__ == "__main__":
    main()
