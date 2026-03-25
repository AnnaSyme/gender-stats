"""
Download WGEA data files from data.gov.au and wgea.gov.au.

Run this once before using wgea_analyze.py.

Data sources (Creative Commons Attribution 3.0 Australia):
  - WGEA Employer Gender Pay Gaps Spreadsheet (wgea.gov.au)
  - WGEA 2024 Public Dataset — Workforce Composition (data.gov.au)
"""

import os
import sys
import urllib.request
import zipfile

FILES = [
    {
        "name": "wgea_employer_pay_gaps.xlsx",
        "url":  "https://www.wgea.gov.au/sites/default/files/documents/Employer-Gender-Pay-Gaps-Spreadsheet.xlsx",
        "desc": "WGEA Employer Gender Pay Gaps (2024-25 & 2023-24)",
    },
    {
        "name": "wgea_2024.zip",
        "url":  "https://data.gov.au/data/dataset/4d35cd80-2538-4705-82f3-d0d18e823d98/resource/f12cc138-44a8-45fc-9ba7-97ee5dadd683/download/wgea_public_dataset_2024.zip",
        "desc": "WGEA 2024 Public Dataset (workforce composition)",
    },
]

WORKFORCE_CSV_IN_ZIP  = "wgea_public_dataset_2024/wgea_workforce_composition_2024.csv"
WORKFORCE_CSV_OUT     = "wgea_workforce_composition_2024.csv"


def download(url, dest, desc):
    if os.path.exists(dest):
        print(f"  ✓ {dest} already exists, skipping download.")
        return
    print(f"  Downloading {desc}...")
    print(f"    {url}")

    def progress(block_count, block_size, total_size):
        if total_size > 0:
            pct = min(block_count * block_size / total_size * 100, 100)
            print(f"\r    {pct:.0f}%", end="", flush=True)

    urllib.request.urlretrieve(url, dest, reporthook=progress)
    print(f"\r    Done. ({os.path.getsize(dest) / 1_048_576:.1f} MB)")


def extract_workforce_csv(zip_path):
    if os.path.exists(WORKFORCE_CSV_OUT):
        print(f"  ✓ {WORKFORCE_CSV_OUT} already exists, skipping extraction.")
        return
    print(f"  Extracting {WORKFORCE_CSV_IN_ZIP} from zip...")
    with zipfile.ZipFile(zip_path) as z:
        with z.open(WORKFORCE_CSV_IN_ZIP) as src, open(WORKFORCE_CSV_OUT, "wb") as dst:
            dst.write(src.read())
    print(f"  Done. ({os.path.getsize(WORKFORCE_CSV_OUT) / 1_048_576:.1f} MB)")


def main():
    print("Fetching WGEA data files...\n")
    for f in FILES:
        download(f["url"], f["name"], f["desc"])

    extract_workforce_csv("wgea_2024.zip")

    print("\nAll files ready:")
    for path in [FILES[0]["name"], WORKFORCE_CSV_OUT]:
        size = os.path.getsize(path) / 1_048_576
        print(f"  {path}  ({size:.1f} MB)")

    print("\nYou can now run:  python3 wgea_analyze.py")


if __name__ == "__main__":
    main()
