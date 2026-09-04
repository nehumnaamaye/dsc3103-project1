import pandas as pd


def rule_positive_price(df):
    failed = df[df["price"] <= 0].copy()
    failed["Reason"] = "Price must be greater than 0"
    return failed


def rule_duplicate_ids(df):
    failed = df[df["id"].duplicated(keep=False)].copy()
    failed["Reason"] = "Duplicate record_id"
    return failed


def rule_duplicate_rows(df):
    failed = df[df.duplicated(keep=False)].copy()
    failed["Reason"] = "Duplicate row"
    return failed


def rule_valid_date(df):
    dates = pd.to_datetime(df["date"], errors="coerce")
    failed = df[dates.isna()].copy()
    failed["Reason"] = "Invalid date"
    return failed


def rule_missing_market(df):
    failed = df[df["market"].isna()].copy()
    failed["Reason"] = "Missing market value"
    return failed


def rule_known_Commodity(df):
    known = ["Maize", "Beans","Sorghum", "Wheat", "Rice"]

    normalized = (
        df["Commodity"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    failed = df[~normalized.isin(known)].copy()
    failed["Reason"] = "Unknown commodity"

    return failed