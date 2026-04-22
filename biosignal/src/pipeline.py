import pandas as pd
import numpy as np


def load_and_clean(filepath: str) -> pd.DataFrame:
    """
    Load NWSS CSV and apply all sentinel/data quality filters.
    Returns a clean DataFrame ready for scoring.
    """
    df = pd.read_csv(filepath)

    raw_count = len(df)

    # Drop rows with nulls in key fields
    df = df.dropna(subset=['percentile', 'ptc_15d', 'population_served'])

    # Filter sentinel values
    # percentile > 100 are error codes (e.g. 999)
    df = df[df['percentile'] <= 100]

    # ptc_15d: max int32 overflow, -99/-98 etc are null sentinels
    # Cap at realistic biological range: -100% to +500%
    df = df[df['ptc_15d'] >= -100]
    df = df[df['ptc_15d'] < 500]

    # Parse dates
    df['date_start'] = pd.to_datetime(df['date_start'])
    df['date_end'] = pd.to_datetime(df['date_end'])

    clean_count = len(df)
    print(f"[pipeline] Loaded {raw_count:,} rows → {clean_count:,} after cleaning "
          f"({raw_count - clean_count:,} removed)")

    return df


def score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply population-weighted priority score.
    Score = (percentile * 0.5) + (log10(population_served) * 10)

    Rationale:
    - percentile is the primary signal (CDC-normalized, site-relative)
    - log10(population) is the tiebreaker — large catchments get priority
      because transmission potential scales with population density
    - Log scale prevents NYC (2.6M) from completely drowning out mid-size cities
    """
    df = df.copy()
    df['log_pop'] = np.log10(df['population_served'])
    df['priority_score'] = (df['percentile'] * 0.5) + (df['log_pop'] * 10)
    return df


def get_alerts(df: pd.DataFrame,
               date_from: str,
               date_to: str,
               percentile_threshold: float = 80.0,
               top_n: int = 10) -> pd.DataFrame:
    """
    Filter to a date window, apply high-alert threshold,
    deduplicate to one row per site, return top N by priority score.
    """
    window = df[
        (df['date_start'] >= date_from) &
        (df['date_start'] <= date_to) &
        (df['percentile'] >= percentile_threshold)
    ].copy()

    top = (
        window
        .sort_values('priority_score', ascending=False)
        .drop_duplicates(subset=['wwtp_id'])
        .head(top_n)
    )

    return top[[
        'wwtp_jurisdiction', 'county_names', 'population_served',
        'date_start', 'date_end', 'percentile', 'ptc_15d', 'priority_score'
    ]].reset_index(drop=True)
