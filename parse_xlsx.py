'''
use this to parse the .xlsx file first to create an easier to work with file
this is AI assisted for some of the formatting stuff bc its super funky (o~o)

parse_xlsx.py  —  Run this ONCE to convert Laser_Goggles.xlsx into
                  goggle_library.json, a plain list that laser_goggles.py
                  uses for all lookups (no Excel or pandas required after).

Usage:
    python parse_xlsx.py       # uses Laser_Goggles.xlsx in same folder
    python parse_xlsx.py --file /path/to/file.xlsx
    python parse_xlsx.py --out  my_library.json   # custom output name
'''

import argparse
import json
import os
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas + openpyxl are needed only for this parser step.\n"
             "Run:  pip install pandas openpyxl")

#change back to Laser_Goggles.xlsx if this new file is buggin out
DEFAULT_XLSX   = "Laser_Goggles1.xlsx" 
DEFAULT_JSON   = "goggle_library.json"
SHEET_NAME     = "Catalog"
MAX_BANDS      = 9   # spreadsheet supports up to λ9 / OD9


def parse_xlsx(filepath: str = DEFAULT_XLSX) -> list[dict]:
    """
    Read the Excel catalog and return a plain Python list of goggle dicts.

    Each goggle dict looks like:
        {
            "product":      "KMZ-C500C",
            "manufacturer": "KENTEK",
            "notes":        "",           # empty string if no notes
            "bands": [
                {"start_nm": 532.0, "stop_nm": 532.0, "od": 7.0},
                {"start_nm": 755.0, "stop_nm": 810.0, "od": 7.0},
                ...
            ]
        }

    One entry per physical goggle row in the spreadsheet.
    Bands with missing/non-numeric values or entirely empty are skipped
    """
    if not os.path.exists(filepath):
        sys.exit(f"File not found: {filepath}")

    raw = pd.read_excel(filepath, sheet_name=SHEET_NAME)

    goggles = []

    for _, row in raw.iterrows():
        name         = str(row.get("Product Name", "")).strip()
        manufacturer = str(row.get("Manufacturer",  "")).strip()
        notes        = str(row.get("Notes", "")).strip()

        # Clean up pandas NaN strings
        if name         in ("nan", ""):  name         = ""
        if manufacturer in ("nan", ""):  manufacturer = ""
        if notes        in ("nan", ""):  notes        = ""

        # Skip completely blank rows
        if name == "" and manufacturer == "":
            continue

        # Collect protection bands
        bands = []
        for i in range(1, MAX_BANDS + 1):
            try:
                raw_start = row[f"λ{i}, start (nm)"]
                raw_stop  = row[f"λ{i}, stop (nm)"]
                raw_od    = row[f"OD{i}"]

                # Reject NaN / None / empty before converting
                if pd.isna(raw_start) or pd.isna(raw_stop) or pd.isna(raw_od):
                    continue

                start = float(raw_start)
                stop  = float(raw_stop)
                od    = float(raw_od)
                bands.append({"start_nm": start, "stop_nm": stop, "od": od})
            except (KeyError, TypeError, ValueError):
                continue   # band slot is empty or non-numeric — skip it

        # Skip rows that have no usable band data
        if not bands:
            continue

        goggles.append({
            "product":      name or "(no name)",
            "manufacturer": manufacturer or "(no manufacturer)",
            "notes":        notes,
            "bands":        bands,
        })

    return goggles


def save_library(goggles: list[dict], outpath: str = DEFAULT_JSON) -> None:
    """Write the goggle list to a JSON file."""
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(goggles, f, indent=2)
    print(f"Saved {len(goggles)} goggle entries → {outpath}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert Laser_Goggles.xlsx to goggle_library.json"
    )
    parser.add_argument("--file", "-f", default=DEFAULT_XLSX,
                        help=f"Input Excel file (default: {DEFAULT_XLSX})")
    parser.add_argument("--out",  "-o", default=DEFAULT_JSON,
                        help=f"Output JSON file (default: {DEFAULT_JSON})")
    args = parser.parse_args()

    print(f"Reading {args.file} ...")
    goggles = parse_xlsx(args.file)
    save_library(goggles, args.out)

    # Quick preview
    print(f"\nPreview — first 3 entries:")
    for g in goggles[:3]:
        print(f"  {g['product']} [{g['manufacturer']}]  —  {len(g['bands'])} band(s)")
        for b in g["bands"]:
            print(f"      {b['start_nm']:.0f}–{b['stop_nm']:.0f} nm  OD {b['od']}")


if __name__ == "__main__":
    main()