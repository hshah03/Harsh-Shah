"""
Production Schedule Generator
Reads the master schedule Excel and outputs a filtered Schedule_YYYY-MM-DD.xlsx
containing Summary, Daily KPI, and per-process sheets for a given date.
"""

import pandas as pd
import os
import sys
import logging
from datetime import datetime

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule_generator.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
FOLDER = os.path.dirname(os.path.abspath(__file__))

# Date format used in the source Excel: "DD.MM.YY HH:MM:SS"
SCH_DATE_FMT = "%d.%m.%y %H:%M:%S"

DATE_COLS   = ["Start", "End", "Latest end"]
OUTPUT_COLS = ["part number", "Task", "process_name", "Station",
               "Start", "End", "order_type", "Latest end", "ExFactoryDate",
               "lot area"]

PROCESS_COL = "process_name"


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_target_date() -> str:
    raw = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        log.error("Invalid date '%s'. Use YYYY-MM-DD format.", raw)
        sys.exit(1)


def find_excel_file(folder: str) -> str:
    files = [f for f in os.listdir(folder)
             if f.endswith(".xlsx") and not f.startswith("Schedule_")]
    if not files:
        log.error("No source .xlsx file found in %s", folder)
        sys.exit(1)
    if len(files) > 1:
        log.warning("Multiple .xlsx files found – using '%s'", files[0])
    return os.path.join(folder, files[0])


def load_data(path: str) -> pd.DataFrame:
    log.info("Loading '%s'", os.path.basename(path))
    df = pd.read_excel(path)
    df.columns = [c.strip() for c in df.columns]

    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=SCH_DATE_FMT, errors="coerce")

    if "ExFactoryDate" in df.columns:
        df["ExFactoryDate"] = pd.to_datetime(df["ExFactoryDate"], errors="coerce")

    return df


def build_summary(df_day: pd.DataFrame) -> pd.DataFrame:
    """One row per (part number, ExFactoryDate) = one row per production order."""
    return (
        df_day
        .groupby(["part number", "ExFactoryDate"], sort=False, dropna=False)
        .agg(
            task_count  =("Task",          "count"),
            order_type  =("order_type",    "first"),
            latest_end  =("Latest end",    "max"),
            first_start =("Start",         "min"),
            last_end    =("End",           "max"),
            processes   =(PROCESS_COL,     lambda x: ", ".join(x.dropna().unique())),
            total_area  =("lot area",      "sum"),
        )
        .reset_index()
    )


def build_kpi(df_day: pd.DataFrame) -> pd.DataFrame:
    """Scheduled tasks and overdue count per process step."""
    scheduled = (
        df_day.groupby(PROCESS_COL)
        .agg(
            scheduled=("Task",     "count"),
            total_area=("lot area","sum"),
        )
        .reset_index()
    )
    # Overdue = task starts after its deadline
    overdue = (
        df_day[df_day["Start"] > df_day["Latest end"]]
        .groupby(PROCESS_COL)
        .size()
        .rename("overdue")
        .reset_index()
    )
    kpi = pd.merge(scheduled, overdue, on=PROCESS_COL, how="left").fillna(0)
    kpi["overdue"] = kpi["overdue"].astype(int)
    return kpi


def save_excel(out_path: str, summary: pd.DataFrame, kpi: pd.DataFrame,
               df_day: pd.DataFrame) -> None:
    processes = df_day[PROCESS_COL].dropna().unique()
    avail_cols = [c for c in OUTPUT_COLS if c in df_day.columns]

    log.info("Writing %d process sheet(s) + Summary + KPI → '%s'",
             len(processes), os.path.basename(out_path))

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary",  index=False)
        kpi.to_excel(    writer, sheet_name="Daily KPI", index=False)
        for proc in processes:
            (
                df_day.loc[df_day[PROCESS_COL] == proc, avail_cols]
                .to_excel(writer, sheet_name=str(proc)[:31], index=False)
            )


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    print("Production Schedule Generator")
    print("─" * 40)

    target   = get_target_date()
    src_path = find_excel_file(FOLDER)
    out_path = os.path.join(FOLDER, f"Schedule_{target}.xlsx")

    df     = load_data(src_path)
    df_day = df[df["Start"].dt.normalize() == target].copy()

    if df_day.empty:
        log.warning("No rows found for %s. Output will contain empty sheets.", target)

    summary = build_summary(df_day)
    kpi     = build_kpi(df_day)

    save_excel(out_path, summary, kpi, df_day)
    log.info("✅ Done  →  %s", out_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
    except Exception as e:
        log.exception("Unexpected error: %s", e)
        sys.exit(1)
    finally:
        if os.name == "nt":
            os.system("pause")
