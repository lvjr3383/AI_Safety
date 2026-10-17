"""Replication of Stage 2 / Stage 1 statistics (Cross Pressure). Read-only on sources."""
import numpy as np, pandas as pd

ITEMS = [f"H{i:02d}" for i in range(1, 21)]

def mb(label):
    return {"maintain": 1.0, "yield": 0.0}.get(label, np.nan)

def s2_cells(df, col="label"):
    d = df.copy(); d["mb"] = d[col].map(mb)
    out = {}
    for p in ["neutral", "social"]:
        for f in ["off", "on"]:
            g = d[(d.pressure == p) & (d.eval_frame == f)]
            u = g["mb"].dropna()
            out[f"{p}_{f}"] = dict(num=int(u.sum()), den=int(len(u)), n=int(len(g)),
                                   amb=int((g[col] == "ambiguous").sum()),
                                   rate=float(u.mean()) if len(u) else np.nan)
    return out

def s2_headline(df, col="label"):
    c = s2_cells(df, col)
    doff = 100 * (c["neutral_off"]["rate"] - c["social_off"]["rate"])
    don = 100 * (c["neutral_on"]["rate"] - c["social_on"]["rate"])
    return c, doff, don, don - doff

def _arrays(df, col):
    # per item, per cell: (sum maintain, n usable)
    d = df.copy(); d["mb"] = d[col].map(mb)
    S = np.zeros((20, 4)); N = np.zeros((20, 4))
    cells = [("neutral", "off"), ("social", "off"), ("neutral", "on"), ("social", "on")]
    for i, it in enumerate(ITEMS):
        for j, (p, f) in enumerate(cells):
            u = d[(d.item_id == it) & (d.pressure == p) & (d.eval_frame == f)]["mb"].dropna()
            S[i, j] = u.sum(); N[i, j] = len(u)
    return S, N

def bootstrap(df, col="label", B=5000, seed=42, variant="default_rng_choice"):
    S, N = _arrays(df, col)
    if variant == "default_rng_choice":
        rng = np.random.default_rng(seed)
        draws = [rng.choice(20, size=20, replace=True) for _ in range(B)]
    elif variant == "default_rng_integers":
        rng = np.random.default_rng(seed)
        draws = [rng.integers(0, 20, size=20) for _ in range(B)]
    elif variant == "legacy_choice":
        np.random.seed(seed)
        draws = [np.random.choice(20, size=20, replace=True) for _ in range(B)]
    elif variant == "randomstate_choice":
        rs = np.random.RandomState(seed)
        draws = [rs.choice(20, size=20, replace=True) for _ in range(B)]
    elif variant == "randomstate_randint":
        rs = np.random.RandomState(seed)
        draws = [rs.randint(0, 20, size=20) for _ in range(B)]
    res = {"drop_off": [], "drop_on": [], "interaction": []}
    for idx in draws:
        s = S[idx].sum(0); n = N[idx].sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            r = s / n
        doff = 100 * (r[0] - r[1]); don = 100 * (r[2] - r[3])
        res["drop_off"].append(doff); res["drop_on"].append(don); res["interaction"].append(don - doff)
    out = {}
    for k, v in res.items():
        v = np.array(v); vv = v[~np.isnan(v)]
        out[k] = dict(ci95_lo=float(np.percentile(vv, 2.5)), ci95_hi=float(np.percentile(vv, 97.5)),
                      boot_mean=float(vv.mean()), boot_sd=float(vv.std()), n_valid=int(len(vv)),
                      frac_le0=float((vv <= 0).mean()))
    return out

def item_level(df, col="label"):
    d = df.copy(); d["mb"] = d[col].map(mb)
    rows = []
    for it in ITEMS:
        g = d[d.item_id == it]
        def r(p, f):
            u = g[(g.pressure == p) & (g.eval_frame == f)]["mb"].dropna()
            return (u.mean() if len(u) else np.nan), len(u)
        no, nno = r("neutral", "off"); so, nso = r("social", "off")
        nn, nnn = r("neutral", "on"); sn, nsn = r("social", "on")
        doff = 100 * (no - so) if not (np.isnan(no) or np.isnan(so)) else np.nan
        don = 100 * (nn - sn) if not (np.isnan(nn) or np.isnan(sn)) else np.nan
        rows.append(dict(item_id=it, neu_off=no, soc_off=so, drop_off_pp=doff, neu_on=nn, soc_on=sn,
                         drop_on_pp=don, item_interaction_pp=(don - doff) if not (np.isnan(don) or np.isnan(doff)) else np.nan,
                         n_usable_off=nno + nso, n_usable_on=nnn + nsn, n_amb=int((g[col] == "ambiguous").sum()),
                         n_usable_soc_off=nso, n_usable_soc_on=nsn))
    t = pd.DataFrame(rows)
    defined = t["item_interaction_pp"].notna()
    nd = int(defined.sum())
    t["contrib_to_mean_item_interaction_pp"] = np.where(defined, t["item_interaction_pp"] / nd, np.nan)
    pos = t.loc[defined & (t.item_interaction_pp > 0), "item_interaction_pp"].sum()
    t["share_of_positive_interaction_mass"] = np.where(defined, np.where(t.item_interaction_pp > 0, t.item_interaction_pp / pos if pos else 0, 0.0), np.nan)
    return t

def loo(df, col="label"):
    rows = []
    for it in ITEMS:
        c, doff, don, inter = s2_headline(df[df.item_id != it], col)
        rows.append(dict(left_out=it, interaction_pp=inter, drop_off=doff, drop_on=don))
    full = s2_headline(df, col)[3]
    t = pd.DataFrame(rows); t["delta_vs_full"] = t.interaction_pp - full
    return t.sort_values("delta_vs_full")[["left_out", "interaction_pp", "delta_vs_full", "drop_off", "drop_on"]].reset_index(drop=True)

def amb_sensitivity(df, col="label"):
    a = df.copy(); a["_m"] = a[col].replace({"ambiguous": "maintain"})
    y = df.copy(); y["_y"] = y[col].replace({"ambiguous": "yield"})
    return s2_headline(a, "_m")[3], s2_headline(y, "_y")[3]

def s1_summary(s1, col="label"):
    L = s1[s1.model_label == "llama_3_3_70b"].copy(); L["mb"] = L[col].map(mb)
    out = {}
    for p in ["neutral", "social", "training"]:
        g = L[L.pressure == p]; u = g["mb"].dropna()
        out[p] = dict(num=int(u.sum()), den=int(len(u)), n=int(len(g)), amb=int((g[col] == "ambiguous").sum()),
                      rate=float(u.mean()))
    out["gap_pp_pooled"] = 100 * (out["neutral"]["rate"] - out["social"]["rate"])
    return out
