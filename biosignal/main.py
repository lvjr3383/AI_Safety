import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pipeline import load_and_clean, score, get_alerts
from contextualizer import generate_sitreps_for_top_alerts

# ── Configuration ──────────────────────────────────────────────────────────
DATA_PATH = "data/NWSS_Public_SARS-CoV-2_Wastewater_Metric_Data.csv"

# Historical validation window — JN.1 surge
ALERT_DATE_FROM = "2023-11-15"
ALERT_DATE_TO   = "2023-12-31"
PERCENTILE_THRESHOLD = 80.0
TOP_N_ALERTS = 10
TOP_N_SITREPS = 3


def print_divider(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    print("\nBioSignal — Pandemic Early Warning Intelligence System")
    print("Wastewater Anomaly Contextualization Layer\n")

    # Step 1 — Load and clean
    print_divider("STEP 1: DATA PIPELINE")
    df = load_and_clean(DATA_PATH)
    df = score(df)

    # Step 2 — Get alerts
    print_divider("STEP 2: PRIORITY ALERT LIST")
    print(f"Window: {ALERT_DATE_FROM} → {ALERT_DATE_TO}")
    print(f"Threshold: percentile ≥ {PERCENTILE_THRESHOLD}")

    alerts = get_alerts(
        df,
        date_from=ALERT_DATE_FROM,
        date_to=ALERT_DATE_TO,
        percentile_threshold=PERCENTILE_THRESHOLD,
        top_n=TOP_N_ALERTS
    )

    print(f"\nTop {TOP_N_ALERTS} Priority Alerts:\n")
    print(alerts.to_string(index=False))

    # Step 3 — Contextualize top 3
    print_divider("STEP 3: SITREP GENERATION")
    print(f"Generating SITREPs for top {TOP_N_SITREPS} alerts...\n")

    sitreps = generate_sitreps_for_top_alerts(alerts, top_n=TOP_N_SITREPS)

    # Step 4 — Print SITREPs
    print_divider("STEP 4: SITUATIONAL REPORTS")

    for i, result in enumerate(sitreps):
        a = result['alert']
        print(f"\n{'─'*60}")
        print(f"ALERT #{i+1} | Priority Score: {a['priority_score']:.1f}")
        print(f"Location: {a['jurisdiction']} — {a['county']}")
        print(f"Population: {a['population_served']:,}")
        print(f"Period: {a['date_start']} to {a['date_end']}")
        print(f"Percentile: {a['percentile']:.1f}th | 15-day trend: {a['ptc_15d']:+.0f}%")
        print(f"{'─'*60}\n")
        print(result['sitrep'])

    # Step 5 — Save results
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"results/biosignal_{timestamp}.json"

    output = {
        "run_metadata": {
            "date_window": f"{ALERT_DATE_FROM} to {ALERT_DATE_TO}",
            "percentile_threshold": PERCENTILE_THRESHOLD,
            "timestamp": timestamp
        },
        "alert_list": alerts.to_dict(orient='records'),
        "sitreps": sitreps
    }

    # Convert timestamps to strings for JSON serialization
    for record in output['alert_list']:
        for key in ['date_start', 'date_end']:
            if hasattr(record[key], 'isoformat'):
                record[key] = str(record[key])

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n[biosignal] Results saved to {output_path}")
    print("[biosignal] Run complete.\n")


if __name__ == "__main__":
    main()
