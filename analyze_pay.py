"""
Gender Pay Analysis — Hourly Rate Comparison

Usage:
    python analyze_pay.py                          # uses sample_employees.csv
    python analyze_pay.py path/to/your_data.csv

Expected CSV columns:
    employee_id, gender, department, role, annual_salary, weekly_hours

Hourly rate is derived as:  annual_salary / (weekly_hours * 52)
"""

import csv
import sys
import statistics
from collections import defaultdict


def load_employees(filepath):
    employees = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                annual_salary = float(row["annual_salary"])
                weekly_hours = float(row["weekly_hours"])
                if weekly_hours <= 0:
                    continue
                hourly_rate = annual_salary / (weekly_hours * 52)
                employees.append({
                    "id":           row["employee_id"],
                    "gender":       row["gender"].strip(),
                    "department":   row.get("department", "Unknown").strip(),
                    "role":         row.get("role", "Unknown").strip(),
                    "hourly_rate":  hourly_rate,
                    "weekly_hours": weekly_hours,
                })
            except (ValueError, KeyError) as e:
                print(f"  Skipping row (bad data): {row} — {e}")
    return employees


def pay_gap_pct(a, b):
    """How much less does group b earn relative to group a? (positive = b earns less)"""
    if a == 0:
        return None
    return (a - b) / a * 100


def group_stats(employees, key="gender"):
    groups = defaultdict(list)
    for emp in employees:
        groups[emp[key]].append(emp["hourly_rate"])
    return {
        group: {
            "count":  len(rates),
            "mean":   statistics.mean(rates),
            "median": statistics.median(rates),
        }
        for group, rates in groups.items()
    }


def print_section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def print_group_table(stats_dict, label="Group"):
    col = max(len(k) for k in stats_dict) + 2
    print(f"\n  {'Gender':<{col}}  {'Count':>6}  {'Mean $/hr':>10}  {'Median $/hr':>12}")
    print(f"  {'-'*col}  {'------':>6}  {'----------':>10}  {'------------':>12}")
    for group, s in sorted(stats_dict.items()):
        print(f"  {group:<{col}}  {s['count']:>6}  {s['mean']:>10.2f}  {s['median']:>12.2f}")


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "sample_employees.csv"
    print(f"\nLoading data from: {filepath}")
    employees = load_employees(filepath)
    print(f"Loaded {len(employees)} employees.")

    if not employees:
        print("No valid employee records found. Exiting.")
        return

    # ── Overall gender breakdown ──────────────────────────────────────
    print_section("OVERALL HOURLY PAY BY GENDER")
    overall = group_stats(employees, key="gender")
    print_group_table(overall)

    genders = sorted(overall.keys())
    if "Male" in overall and "Female" in overall:
        gap_mean   = pay_gap_pct(overall["Male"]["mean"],   overall["Female"]["mean"])
        gap_median = pay_gap_pct(overall["Male"]["median"], overall["Female"]["median"])
        print(f"\n  Pay gap (women vs men):")
        print(f"    Mean gap:    {gap_mean:+.1f}%  (women earn {abs(gap_mean):.1f}% {'less' if gap_mean > 0 else 'more'} on average)")
        print(f"    Median gap:  {gap_median:+.1f}%  (women earn {abs(gap_median):.1f}% {'less' if gap_median > 0 else 'more'} at the median)")

    # ── By department ─────────────────────────────────────────────────
    departments = sorted({e["department"] for e in employees})
    if len(departments) > 1:
        print_section("HOURLY PAY BY GENDER × DEPARTMENT")
        for dept in departments:
            dept_emps = [e for e in employees if e["department"] == dept]
            dept_stats = group_stats(dept_emps, key="gender")
            if len(dept_stats) < 2:
                continue
            print(f"\n  [{dept}]")
            print_group_table(dept_stats)
            if "Male" in dept_stats and "Female" in dept_stats:
                g = pay_gap_pct(dept_stats["Male"]["mean"], dept_stats["Female"]["mean"])
                direction = "less" if g > 0 else "more"
                print(f"    → Mean gap: women earn {abs(g):.1f}% {direction} than men")

    # ── By role ───────────────────────────────────────────────────────
    roles = sorted({e["role"] for e in employees})
    if len(roles) > 1:
        print_section("HOURLY PAY BY GENDER × ROLE")
        for role in roles:
            role_emps = [e for e in employees if e["role"] == role]
            role_stats = group_stats(role_emps, key="gender")
            if len(role_stats) < 2:
                continue
            print(f"\n  [{role}]")
            print_group_table(role_stats)
            if "Male" in role_stats and "Female" in role_stats:
                g = pay_gap_pct(role_stats["Male"]["mean"], role_stats["Female"]["mean"])
                direction = "less" if g > 0 else "more"
                print(f"    → Mean gap: women earn {abs(g):.1f}% {direction} than men")

    print(f"\n{'='*55}\n")


if __name__ == "__main__":
    main()
