import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SITREP_SYSTEM_PROMPT = """You are a Public Health Intelligence Officer specializing in
wastewater-based epidemiology and pandemic early warning.

You will be given a wastewater alert from the CDC National Wastewater Surveillance System (NWSS).
The alert has already been validated by a statistical pipeline — your job is NOT to re-evaluate
whether the signal is real. The math has already confirmed it.

Your job is to produce a structured 3-paragraph Situational Report (SITREP) that helps a
public health official understand:
1. What type of catchment this is and why it matters epidemiologically
2. What external factors (travel, events, seasonal drivers, population movement)
   could explain or amplify this signal
3. What the recommended immediate actions are — specific, actionable, not generic

Rules:
- Be specific. Name real events, real travel patterns, real seasonal factors for that region and time period.
- Do NOT say "further monitoring is recommended" as a standalone conclusion. That is not actionable.
- Do NOT hallucinate specific numbers (case counts, hospitalization rates) unless you are certain.
  If uncertain, say "available data suggests" or "historical patterns indicate."
- Keep each paragraph to 3-5 sentences.
- Where relevant, note critical infrastructure or vulnerable populations within the catchment — hospitals, nursing homes, schools, international airports, convention centers.
- End with a Priority Level: URGENT / HIGH / ELEVATED and one sentence justification.

Format:
CATCHMENT PROFILE
[paragraph]

SIGNAL DRIVERS
[paragraph]

RECOMMENDED ACTIONS
[paragraph]

PRIORITY: [URGENT/HIGH/ELEVATED] — [one sentence justification]"""


def generate_sitrep(alert: dict) -> str:
    """
    Generate a public health SITREP for a single wastewater alert.

    alert: dict with keys:
        jurisdiction, county, population_served, date_start, date_end,
        percentile, ptc_15d, priority_score
    """
    ptc_direction = "increasing" if alert['ptc_15d'] > 0 else "declining"
    ptc_abs = abs(alert['ptc_15d'])

    user_message = f"""WASTEWATER ALERT — NWSS PRIORITY SIGNAL

Jurisdiction: {alert['jurisdiction']}
County/Counties: {alert['county']}
Population Served by Catchment: {alert['population_served']:,}
Alert Window: {alert['date_start']} to {alert['date_end']}
Percentile (site-normalized): {alert['percentile']:.1f}th
15-Day Trend: {ptc_direction} {ptc_abs:.0f}%
Priority Score: {alert['priority_score']:.1f}

Generate a SITREP for the public health official responsible for this jurisdiction."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=800,
        system=SITREP_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.content[0].text


def generate_sitreps_for_top_alerts(alerts_df, top_n: int = 3) -> list:
    """
    Run SITREP generation for top N alerts.
    Returns list of dicts with alert metadata + sitrep text.
    """
    results = []

    for i, row in alerts_df.head(top_n).iterrows():
        print(f"\n[contextualizer] Generating SITREP {i+1}/{top_n}: "
              f"{row['wwtp_jurisdiction']} — {row['county_names']}...")

        alert = {
            'jurisdiction': row['wwtp_jurisdiction'],
            'county': row['county_names'],
            'population_served': int(row['population_served']),
            'date_start': str(row['date_start'].date()),
            'date_end': str(row['date_end'].date()),
            'percentile': float(row['percentile']),
            'ptc_15d': float(row['ptc_15d']),
            'priority_score': float(row['priority_score'])
        }

        sitrep = generate_sitrep(alert)

        results.append({
            'alert': alert,
            'sitrep': sitrep
        })

        print(f"[contextualizer] Done.")

    return results
