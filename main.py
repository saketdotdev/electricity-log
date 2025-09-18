#!/usr/bin/env python3
"""
Electricity Meter Logger (with 2 averages)
- Saves every entry in meter_log.csv
- Modes:
    * add  -> Add new reading (asks for date & kWh)
    * show -> Show last entry and averages
"""

import csv
import os
import sys
from datetime import datetime

LOG_FILE = "meter_log.csv"


def read_entries():
    """Read all log entries (excluding header)."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
            return rows[1:] if len(rows) > 1 else []
    return []


def add_entry(date_str, kwh):
    entries = read_entries()
    last_entry = entries[-1] if entries else None
    first_entry = entries[0] if entries else None
    entry_date = datetime.strptime(date_str, "%d-%m-%Y")

    if last_entry:
        # --- Interval calculation ---
        last_date = datetime.strptime(last_entry[0], "%d-%m-%Y")
        last_kwh = float(last_entry[1])
        days_interval = (entry_date - last_date).days
        units_interval = kwh - last_kwh
        avg_interval = units_interval / \
            days_interval if days_interval > 0 else units_interval

        # --- Overall calculation ---
        first_date = datetime.strptime(first_entry[0], "%d-%m-%Y")
        first_kwh = float(first_entry[1])
        days_total = (entry_date - first_date).days
        units_total = kwh - first_kwh
        avg_total = units_total / days_total if days_total > 0 else units_total

        # print results
        print("\n========== New Entry ==========")
        print(f"Previous Date : {last_entry[0]} ({last_kwh} kWh)")
        print(f"Current Date  : {date_str} ({kwh} kWh)")
        print(f"Days Passed   : {days_interval} days")
        print(f"Units Consumed: {units_interval} kWh")
        print(f"Interval Avg  : {avg_interval:.2f} kWh/day")
        print(
            f"Overall Avg   : {avg_total:.2f} kWh/day (since {first_entry[0]})")
        print("===============================")
    else:
        print("First entry saved. No previous data to compare.")

    # save new entry
    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["date", "kwh"])
        writer.writerow([date_str, kwh])


def show_last():
    entries = read_entries()
    if not entries:
        print("⚠ No entries found in log.")
        return

    last_entry = entries[-1]
    first_entry = entries[0]
    last_date = datetime.strptime(last_entry[0], "%d-%m-%Y")
    last_kwh = float(last_entry[1])
    first_date = datetime.strptime(first_entry[0], "%d-%m-%Y")
    first_kwh = float(first_entry[1])

    days_total = (last_date - first_date).days
    units_total = last_kwh - first_kwh
    avg_total = units_total / days_total if days_total > 0 else units_total

    print("\n========== Latest Reading ==========")
    print(f"Last Date     : {last_entry[0]} ({last_kwh} kWh)")
    print(f"Since Start   : {units_total} kWh over {days_total} days")
    print(f"Overall Avg   : {avg_total:.2f} kWh/day")
    print("===================================")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [add|show]")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "add":
        print("Electricity Meter Logger - Add Mode")
        date_str = input("Enter date (DD-MM-YYYY): ").strip()
        kwh = float(input("Enter kWh reading: ").strip())
        add_entry(date_str, kwh)
    elif mode == "show":
        print("Electricity Meter Logger - Show Mode")
        show_last()
    else:
        print("Unknown command. Use 'add' or 'show'.")
