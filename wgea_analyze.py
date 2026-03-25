"""
WGEA Gender Pay Gap Analyzer — Australia

Uses real data from the Workplace Gender Equality Agency (WGEA):
  - wgea_employer_pay_gaps.xlsx      : pay gap % per employer (2024-25 & 2023-24)
  - wgea_workforce_composition_2024.csv : headcounts by gender, seniority, employment type

Data source: https://www.wgea.gov.au  (CC BY 3.0 AU)

Usage:
    python3 wgea_analyze.py                          # interactive company search
    python3 wgea_analyze.py "Commonwealth Bank"      # search by company name
    python3 wgea_analyze.py --industry               # show national industry summary
"""

import sys
import csv
import difflib
import argparse
from collections import defaultdict

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl is required.  Run: pip3 install openpyxl")
    sys.exit(1)

PAY_GAP_FILE        = "wgea_employer_pay_gaps.xlsx"
WORKFORCE_FILE      = "wgea_workforce_composition_2024.csv"

SENIOR_MANAGER_ROLES = {
    "CEOs",
    "Other Executives and General Managers",
    "Senior Managers",
    "Key Management Personnel",
}

# ─────────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────────

def load_pay_gap_data():
    """Return list of dicts with employer pay gap info from the XLSX."""
    wb = openpyxl.load_workbook(PAY_GAP_FILE, read_only=True, data_only=True)
    ws = wb["2. Employers "]
    rows = list(ws.iter_rows(values_only=True))

    # Row 4 (index 3) is the header row
    headers = rows[3]
    employers = []
    for row in rows[4:]:
        if row[0] is None:
            continue
        record = dict(zip(headers, row))
        employers.append(record)
    wb.close()
    return employers


def load_workforce_data():
    """Return list of dicts from the workforce composition CSV."""
    data = []
    with open(WORKFORCE_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["n_employees"] = int(row["n_employees"]) if row["n_employees"].isdigit() else 0
            data.append(row)
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Search helpers
# ─────────────────────────────────────────────────────────────────────────────

def find_employer(query, employers):
    """Return close matches to query in the pay-gap employer list."""
    names = [e["Employer name"] for e in employers if e.get("Employer name")]
    matches = difflib.get_close_matches(query, names, n=5, cutoff=0.3)
    # Also do a substring match
    query_lower = query.lower()
    substring = [n for n in names if query_lower in n.lower()]
    combined = list(dict.fromkeys(substring + matches))  # preserve order, deduplicate
    return combined[:8]


def get_employer_record(name, employers):
    return next((e for e in employers if e.get("Employer name") == name), None)


def find_workforce_rows(name, workforce):
    """Return all workforce composition rows for an employer (exact name match)."""
    name_lower = name.lower()
    return [r for r in workforce if r["employer_name"].lower() == name_lower]


# ─────────────────────────────────────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────────────────────────────────────

def fmt_pct(val):
    """Format a decimal GPG value (e.g. 0.216 → '+21.6%')."""
    if val is None or val == "" or (isinstance(val, str) and val.strip() == ""):
        return "  n/a  "
    try:
        v = float(val) * 100  # stored as decimal fraction
        sign = "+" if v > 0 else ""
        return f"{sign}{v:.1f}%"
    except (ValueError, TypeError):
        return str(val)


def fmt_dollar(val):
    if val is None or val == "":
        return "n/a"
    try:
        return f"${float(val):,.0f}"
    except (ValueError, TypeError):
        return str(val)


def print_section(title):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")


def print_pay_gap(record):
    print_section("PAY GAP 2024-25 (FTE-equivalent annualised salary)")
    print("  Positive % = men earn more.  Negative % = women earn more.\n")

    print(f"  {'Metric':<38} {'2024-25':>9}")
    print(f"  {'─'*38}  {'─'*9}")

    metrics = [
        "Median total remuneration GPG (%)",
        "Median base salary GPG (%)",
        "Average total remuneration GPG (%)",
        "Average base salary GPG (%)",
    ]
    for label in metrics:
        v = record.get(label)
        print(f"  {label:<38} {fmt_pct(v):>9}")

    # Quartile breakdown
    print_section("WORKFORCE QUARTILES — % women in each pay quartile")
    quartile_cols = [
        ("Upper quartile (top earners)",        "Upper quartile % women"),
        ("Upper-middle quartile",               "Upper-middle quartile % women"),
        ("Lower-middle quartile",               "Lower-middle quartile % women"),
        ("Lower quartile (bottom earners)",     "Lower quartile % women"),
        ("Total workforce",                     "Total workforce % women"),
    ]
    print(f"\n  {'Quartile':<36} {'% Women':>9}  {'Avg total remun.':>17}")
    print(f"  {'─'*36}  {'─'*9}  {'─'*17}")

    remun_cols = {
        "Upper quartile (top earners)":    "Upper quartile - average total remuneration ($)",
        "Upper-middle quartile":           "Upper-middle quartile - average total remuneration ($)",
        "Lower-middle quartile":           "Lower-middle quartile  - average total remuneration ($)",
        "Lower quartile (bottom earners)": "Lower quartile - average total remuneration ($)",
        "Total workforce":                 "Total workforce - average total remuneration ($)*",
    }
    for label, col in quartile_cols:
        pct_val = record.get(col)
        remun_col = remun_cols.get(label, "")
        remun_val = record.get(remun_col)

        pct_str = f"{float(pct_val)*100:.0f}%" if pct_val not in (None, "") else "n/a"
        try:
            pct_str = f"{float(pct_val)*100:.0f}%"
        except (TypeError, ValueError):
            pct_str = "n/a"

        print(f"  {label:<36} {pct_str:>9}  {fmt_dollar(remun_val):>17}")


def print_senior_management(wf_rows):
    print_section("SENIOR MANAGEMENT — gender breakdown")

    if not wf_rows:
        print("  No workforce composition data found for this employer.")
        return

    # Filter to senior roles
    senior_rows = [r for r in wf_rows if r.get("occupation") in SENIOR_MANAGER_ROLES]
    if not senior_rows:
        # Fallback: use manager_category = Manager
        senior_rows = [r for r in wf_rows if r.get("manager_category") == "Manager"]

    if not senior_rows:
        print("  No senior management data available.")
        return

    # Count by gender × role
    role_gender = defaultdict(lambda: defaultdict(int))
    for r in senior_rows:
        role_gender[r["occupation"]][r["gender"]] += r["n_employees"]

    all_genders = sorted({r["gender"] for r in senior_rows})
    col_w = max(len(k) for k in role_gender) + 2

    # Header
    gender_cols = "  ".join(f"{g:>8}" for g in all_genders)
    print(f"\n  {'Role':<{col_w}}  {gender_cols}  {'% Men':>7}  {'% Women':>9}")
    print(f"  {'─'*col_w}  {'  '.join('─'*8 for _ in all_genders)}  {'─'*7}  {'─'*9}")

    total_men = total_women = 0
    for role in sorted(role_gender):
        counts = role_gender[role]
        men   = counts.get("Men", 0)
        women = counts.get("Women", 0)
        total = men + women
        total_men   += men
        total_women += women
        pct_men   = f"{men/total*100:.0f}%" if total else "n/a"
        pct_women = f"{women/total*100:.0f}%" if total else "n/a"
        count_cols = "  ".join(f"{counts.get(g, 0):>8}" for g in all_genders)
        print(f"  {role:<{col_w}}  {count_cols}  {pct_men:>7}  {pct_women:>9}")

    # Total row
    grand_total = total_men + total_women
    pct_men_total   = f"{total_men/grand_total*100:.0f}%" if grand_total else "n/a"
    pct_women_total = f"{total_women/grand_total*100:.0f}%" if grand_total else "n/a"
    total_counts = "  ".join(
        f"{sum(role_gender[r].get(g, 0) for r in role_gender):>8}" for g in all_genders
    )
    print(f"  {'─'*col_w}  {'  '.join('─'*8 for _ in all_genders)}  {'─'*7}  {'─'*9}")
    print(f"  {'TOTAL (senior mgmt)':<{col_w}}  {total_counts}  {pct_men_total:>7}  {pct_women_total:>9}")


def print_employment_type_breakdown(wf_rows):
    print_section("WORKFORCE — employment type by gender")
    if not wf_rows:
        return

    type_gender = defaultdict(lambda: defaultdict(int))
    for r in wf_rows:
        key = f"{r['employment_status']} {r['employment_type']}"
        type_gender[key][r["gender"]] += r["n_employees"]

    all_genders = sorted({r["gender"] for r in wf_rows})
    col_w = max(len(k) for k in type_gender) + 2
    gender_cols = "  ".join(f"{g:>8}" for g in all_genders)
    print(f"\n  {'Employment type':<{col_w}}  {gender_cols}")
    print(f"  {'─'*col_w}  {'  '.join('─'*8 for _ in all_genders)}")

    for etype in sorted(type_gender):
        counts = type_gender[etype]
        count_cols = "  ".join(f"{counts.get(g, 0):>8}" for g in all_genders)
        print(f"  {etype:<{col_w}}  {count_cols}")


# ─────────────────────────────────────────────────────────────────────────────
# Industry summary
# ─────────────────────────────────────────────────────────────────────────────

def print_industry_summary(employers):
    print_section("NATIONAL SUMMARY — median base salary GPG by industry (2024-25)")
    from collections import defaultdict

    industry_gaps = defaultdict(list)
    for e in employers:
        ind = e.get("Industry (ANZSIC Division)")
        val = e.get("Median base salary GPG (%)")
        if ind and val not in (None, ""):
            try:
                industry_gaps[ind].append(float(val))
            except (ValueError, TypeError):
                pass

    rows = []
    for ind, vals in industry_gaps.items():
        rows.append((ind, len(vals), sum(vals)/len(vals)))
    rows.sort(key=lambda x: x[2], reverse=True)

    print(f"\n  {'Industry':<52} {'#cos':>5}  {'Avg median GPG':>14}")
    print(f"  {'─'*52}  {'─'*5}  {'─'*14}")
    for ind, n, avg in rows:
        print(f"  {ind:<52} {n:>5}  {fmt_pct(avg):>14}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="WGEA Gender Pay Gap Analyzer")
    parser.add_argument("company", nargs="?", help="Company name to search for")
    parser.add_argument("--industry", action="store_true", help="Show industry-level summary")
    args = parser.parse_args()

    print("Loading data...", end=" ", flush=True)
    try:
        employers  = load_pay_gap_data()
        workforce  = load_workforce_data()
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("Run fetch_wgea_data.py first to download the data files.")
        sys.exit(1)
    print(f"done. ({len(employers):,} employers, {len(workforce):,} workforce rows)")

    if args.industry:
        print_industry_summary(employers)
        print()
        return

    # Get company name
    query = args.company
    if not query:
        query = input("\nEnter company name (or part of it): ").strip()
    if not query:
        print("No company name entered.")
        return

    matches = find_employer(query, employers)
    if not matches:
        print(f"\nNo matches found for '{query}'.")
        return

    if len(matches) == 1:
        chosen = matches[0]
    else:
        print(f"\nFound {len(matches)} match(es) for '{query}':")
        for i, name in enumerate(matches, 1):
            print(f"  {i}. {name}")
        choice = input("Select number (or press Enter for #1): ").strip()
        idx = int(choice) - 1 if choice.isdigit() else 0
        chosen = matches[max(0, min(idx, len(matches)-1))]

    record = get_employer_record(chosen, employers)
    wf_rows = find_workforce_rows(chosen, workforce)

    print(f"\n{'═'*60}")
    print(f"  {chosen}")
    if record:
        print(f"  {record.get('Industry (ANZSIC Division)', '')}  |  "
              f"{record.get('Employer size range   (# employees)', '')} employees  |  "
              f"{record.get('Sector', '')}")
    print(f"{'═'*60}")

    if record:
        print_pay_gap(record)
    else:
        print("\n  (No pay gap data found in 2024-25 WGEA Employer spreadsheet)")

    print_senior_management(wf_rows)
    print_employment_type_breakdown(wf_rows)
    print()


if __name__ == "__main__":
    main()
