#!/usr/bin/env python3
"""
run_experiments.py
==================
Orchestrates the full FLnCCN evaluation matrix.

Usage (from FLnCCN/ project root):
    python3 run_experiments.py            # run all 6 configs + parse results
    python3 run_experiments.py --parse-only  # skip simulations, just parse reports

Scenarios:
    A  Epidemic FL        (baseline flooding)
    B  CCN-NoCache        (CCN routing, no relay caching)
    C  CCN-Cache          (proposed UFCR + adaptive aggregation)

Each scenario runs under two mobility models:
    RWP   – Random Waypoint (open field)
    SPMBM – Shortest Path Map-Based Movement (Helsinki street map)
"""

import subprocess
import os
import sys
import time
import re
from multiprocessing import Pool

# ─────────────────────────────────────────────────────────────
# Experiment matrix: 6 configurations
# Each dict describes one simulation run.
# ─────────────────────────────────────────────────────────────
EXPERIMENTS = [
    {
        "name":       "FL_A_Epidemic_50_RWP",
        "label":      "Scenario A | Epidemic | RWP",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_A_epidemic_50_rwp.txt",
        "app_report": "reports/fl/FL_A_Epidemic_50_RWP_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_A_Epidemic_50_RWP_MessageStatsReport.txt",
    },
    {
        "name":       "FL_A_Epidemic_50_SPMBM",
        "label":      "Scenario A | Epidemic | SPMBM",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_A_epidemic_50_spmbm.txt",
        "app_report": "reports/fl/FL_A_Epidemic_50_SPMBM_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_A_Epidemic_50_SPMBM_MessageStatsReport.txt",
    },
    {
        "name":       "FL_B_CCN_NoCache_50_RWP",
        "label":      "Scenario B | CCN-NoCache | RWP",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_B_ccn_nocache_50_rwp.txt",
        "app_report": "reports/fl/FL_B_CCN_NoCache_50_RWP_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_B_CCN_NoCache_50_RWP_MessageStatsReport.txt",
    },
    {
        "name":       "FL_B_CCN_NoCache_50_SPMBM",
        "label":      "Scenario B | CCN-NoCache | SPMBM",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_B_ccn_nocache_50_spmbm.txt",
        "app_report": "reports/fl/FL_B_CCN_NoCache_50_SPMBM_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_B_CCN_NoCache_50_SPMBM_MessageStatsReport.txt",
    },
    {
        "name":       "FL_D_CCN_LRU_50_RWP",
        "label":      "Scenario D | CCN-LRU    | RWP",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_D_ccn_lru_50_rwp.txt",
        "app_report": "reports/fl/FL_D_CCN_LRU_50_RWP_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_D_CCN_LRU_50_RWP_MessageStatsReport.txt",
    },
    {
        "name":       "FL_D_CCN_LRU_50_SPMBM",
        "label":      "Scenario D | CCN-LRU    | SPMBM",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_D_ccn_lru_50_spmbm.txt",
        "app_report": "reports/fl/FL_D_CCN_LRU_50_SPMBM_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_D_CCN_LRU_50_SPMBM_MessageStatsReport.txt",
    },
    {
        "name":       "FL_C_CCN_Cache_50_RWP",
        "label":      "Scenario C | CCN-Cache  | RWP",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_C_ccn_cache_50_rwp.txt",
        "app_report": "reports/fl/FL_C_CCN_Cache_50_RWP_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_C_CCN_Cache_50_RWP_MessageStatsReport.txt",
    },
    {
        "name":       "FL_C_CCN_Cache_50_SPMBM",
        "label":      "Scenario C | CCN-Cache  | SPMBM",
        "cmd":        "./one.sh -b 1 fl_settings/fl_base_50.txt fl_settings/scenario_C_ccn_cache_50_spmbm.txt",
        "app_report": "reports/fl/FL_C_CCN_Cache_50_SPMBM_CCNApplicationReport.txt",
        "msg_report": "reports/fl/FL_C_CCN_Cache_50_SPMBM_MessageStatsReport.txt",
    },
]

# ─────────────────────────────────────────────────────────────
# Simulation runner
# ─────────────────────────────────────────────────────────────
def run_experiment(exp):
    """
    Launch one simulation via ./one.sh.
    Skips automatically if both report files already exist and are non-empty
    (safe to re-run after a partial failure).
    """
    name       = exp["name"]
    cmd        = exp["cmd"]
    app_report = exp["app_report"]
    msg_report = exp["msg_report"]

    # Smart skip: both report files exist and contain data → already done
    if (os.path.exists(app_report) and os.path.getsize(app_report) > 0 and
            os.path.exists(msg_report) and os.path.getsize(msg_report) > 0):
        print(f"[SKIP]  {name}  (reports already exist)")
        return name, 0

    print(f"[START] {name}")
    start_time = time.time()

    # Redirect all simulator stdout + stderr to a per-run log file
    log_file = f"{name}.log"
    with open(log_file, "w") as f:
        result = subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)

    elapsed = time.time() - start_time
    status  = "OK" if result.returncode == 0 else f"ERROR (exit {result.returncode})"
    print(f"[DONE]  {name}  {elapsed:.0f}s  {status}  → {log_file}")
    return name, result.returncode


# ─────────────────────────────────────────────────────────────
# Report parsers
# ─────────────────────────────────────────────────────────────
def parse_application_report(filepath):
    """
    Parse CCNApplicationReport.txt generated by CCNApplicationReport.java.

    Returns a dict with:
        rounds_completed         – number of rows in the per-round CSV table
        total_updates_collected  – sum of updates_collected across all rounds
        avg_round_latency        – mean of completion_lat_s (ignores -1.0 rows)
        useful_fl_cache_hits     – global useful FL cache hit counter
        useful_fl_cache_hit_ratio – ratio of useful hits to total FL cache hits
    """
    if not os.path.exists(filepath):
        return {}

    metrics = {
        "rounds_completed":        0,
        "total_updates_collected": 0,
        "avg_round_latency":       0.0,
        "useful_fl_cache_hits":    0,
        "useful_fl_cache_hit_ratio": 0.0,
    }

    with open(filepath, "r") as f:
        content = f.read()

    lines       = content.splitlines()
    parsing_csv = False
    csv_rows    = []

    for line in lines:
        # Global summary stats
        if "useful_fl_cache_hits:" in line and "ratio" not in line:
            try:
                metrics["useful_fl_cache_hits"] = int(line.split(":")[1].strip())
            except ValueError:
                pass
        elif "useful_fl_cache_hit_ratio:" in line:
            try:
                metrics["useful_fl_cache_hit_ratio"] = float(line.split(":")[1].strip())
            except ValueError:
                pass
        elif "=== FL Per-Round Metrics ===" in line:
            parsing_csv = True
            continue

        # CSV rows (skip header line)
        if parsing_csv and line.strip() and not line.startswith("round,"):
            csv_rows.append(line.strip().split(","))

    if csv_rows:
        metrics["rounds_completed"] = len(csv_rows)
        latencies = []
        updates   = 0
        for row in csv_rows:
            try:
                updates += int(row[1])
                lat = float(row[2])
                if lat >= 0:   # skip sentinel -1.0 (round timed out)
                    latencies.append(lat)
            except (ValueError, IndexError):
                pass
        metrics["total_updates_collected"] = updates
        metrics["avg_round_latency"] = (
            sum(latencies) / len(latencies) if latencies else 0.0
        )

    return metrics


def parse_message_report(filepath):
    """
    Parse MessageStatsReport.txt generated by the ONE simulator.

    Returns a dict with:
        delivery_prob   – fraction of messages delivered (delivery_prob field)
        overhead_ratio  – transmissions per delivered message
    """
    if not os.path.exists(filepath):
        return {}

    metrics = {
        "delivery_prob":  0.0,
        "overhead_ratio": 0.0,
    }

    with open(filepath, "r") as f:
        content = f.read()

    # Note: the ONE simulator uses "delivery_prob", not "delivery_ratio"
    m_deliv = re.search(r"delivery_prob:\s*([\d.]+)", content)
    m_over  = re.search(r"overhead_ratio:\s*([\d.]+)", content)

    if m_deliv:
        metrics["delivery_prob"]  = float(m_deliv.group(1))
    if m_over:
        metrics["overhead_ratio"] = float(m_over.group(1))

    return metrics


# ─────────────────────────────────────────────────────────────
# Results table builder
# ─────────────────────────────────────────────────────────────
def build_results_table():
    """Parse all reports and return a Markdown table string."""
    header = (
        "| Scenario | Protocol | Mobility | Rounds | Total Updates | "
        "Avg Round Latency (s) | Useful Cache Hits | Useful Cache Hit Ratio | "
        "Delivery Prob | Overhead Ratio |\n"
        "|---|---|---|---|---|---|---|---|---|---|"
    )
    rows = [header]

    for exp in EXPERIMENTS:
        # Parse label into columns: "Scenario X | Protocol | Mobility"
        parts    = exp["label"].split("|")
        scenario = parts[0].strip()
        protocol = parts[1].strip()
        mobility = parts[2].strip()

        app = parse_application_report(exp["app_report"])
        msg = parse_message_report(exp["msg_report"])

        rounds      = app.get("rounds_completed",        "N/A")
        updates     = app.get("total_updates_collected", "N/A")
        lat         = app.get("avg_round_latency",       0.0)
        u_hits      = app.get("useful_fl_cache_hits",    "N/A")
        u_ratio     = app.get("useful_fl_cache_hit_ratio", 0.0)
        deliv       = msg.get("delivery_prob",            0.0)
        overhead    = msg.get("overhead_ratio",           0.0)

        lat_str     = f"{lat:.1f}"     if isinstance(lat,     float) else lat
        u_ratio_str = f"{u_ratio:.4f}" if isinstance(u_ratio, float) else u_ratio
        deliv_str   = f"{deliv:.4f}"   if isinstance(deliv,   float) else deliv
        over_str    = f"{overhead:.4f}" if isinstance(overhead, float) else overhead

        rows.append(
            f"| {scenario} | {protocol} | {mobility} | {rounds} | {updates} | "
            f"{lat_str} | {u_hits} | {u_ratio_str} | {deliv_str} | {over_str} |"
        )

    return "\n".join(rows)


# ─────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────
def main():
    parse_only = "--parse-only" in sys.argv

    if not parse_only:
        print("=" * 60)
        print("  FLnCCN Parallel Experiment Suite")
        print("  Running 6 configurations (3 parallel workers)")
        print("=" * 60)

        with Pool(processes=3) as pool:
            pool.map(run_experiment, EXPERIMENTS)

        print("\nAll simulations finished. Parsing reports...\n")
    else:
        print("--parse-only: Skipping simulations, parsing existing reports.\n")

    table = build_results_table()

    print("=" * 60)
    print("  Results Summary")
    print("=" * 60)
    print(table)

    # Save to reports/fl/results_summary.md next to the report files
    output_path = "reports/fl/results_summary.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("# Comparative Simulation Results\n\n")
        f.write(
            "Evaluation of Utility-Based Federated Cache Replacement (UFCR) "
            "and Adaptive Aggregation Threshold against Epidemic and CCN-NoCache baselines.\n\n"
        )
        f.write(table + "\n")

    print(f"\nResults table saved to: {output_path}")


if __name__ == "__main__":
    main()
