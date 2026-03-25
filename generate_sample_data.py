"""
Generate sample employee data for gender pay analysis.
Produces sample_employees.csv with realistic variation.
"""

import csv
import random

random.seed(42)

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "Finance", "HR", "Operations"]

# Base annual salaries by role (intentionally include a small pay gap for realism)
ROLES = {
    "Junior Analyst":    (45_000, 55_000),
    "Analyst":           (55_000, 70_000),
    "Senior Analyst":    (70_000, 90_000),
    "Manager":           (85_000, 110_000),
    "Senior Manager":    (110_000, 140_000),
    "Director":          (140_000, 180_000),
}

WEEKLY_HOURS_OPTIONS = [40, 40, 40, 40, 32, 24, 20]  # weighted toward full-time


def make_employee(emp_id):
    gender = random.choice(["Male", "Female", "Female", "Male"])  # slight imbalance
    role, (low, high) = random.choice(list(ROLES.items()))
    department = random.choice(DEPARTMENTS)

    base_salary = random.randint(low, high)
    # Introduce a small structural pay gap (women earn ~5-10% less on average)
    if gender == "Female":
        base_salary = int(base_salary * random.uniform(0.90, 0.98))

    weekly_hours = random.choice(WEEKLY_HOURS_OPTIONS)
    # Part-time employees have proportionally lower salaries
    if weekly_hours < 40:
        base_salary = int(base_salary * (weekly_hours / 40))

    return {
        "employee_id": f"EMP{emp_id:04d}",
        "gender": gender,
        "department": department,
        "role": role,
        "annual_salary": base_salary,
        "weekly_hours": weekly_hours,
    }


def main():
    employees = [make_employee(i) for i in range(1, 201)]
    fieldnames = ["employee_id", "gender", "department", "role", "annual_salary", "weekly_hours"]

    with open("sample_employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)

    print(f"Generated {len(employees)} employees → sample_employees.csv")


if __name__ == "__main__":
    main()
