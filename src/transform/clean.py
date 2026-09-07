import os

import pandas as pd

from src.validate import rules

raw_path = "data/raw/prices.csv"
data_path = "data/processed/prices_clean.parquet"


def clean_data(path=raw_path):
    df = pd.read_csv(path)
    log = []

    # 1. Drop exact duplicate rows
    repeated_rows = rules.rule_duplicate_rows(df)
    if len(repeated_rows) > 0:
        before = len(df)
        df = df.drop_duplicates(keep="first")
        log.append(f"Dropped {before - len(df)} duplicate row occurrence(s), keeping the first of each.")

    # 2. Drop rows with duplicate ids, keeping the first occurrence
    duplicate_ids = rules.rule_duplicate_ids(df)
    if len(duplicate_ids) > 0:
        before = len(df)
        df = df.drop_duplicates(subset="id", keep="first")
        log.append(f"Removed {before - len(df)} row(s) with duplicate ids (kept first occurrence).")

    # 3. Normalize Commodity casing (MAIZE / Maize / maize -> Maize)
    df["Commodity"] = df["Commodity"].astype(str).str.strip().str.title()
    log.append("Normalized Commodity values to title case (e.g. MAIZE -> Maize).")

    unknown_commodity = rules.rule_known_Commodity(df)
    if len(unknown_commodity) > 0:
        before = len(df)
        df = df.drop(index=unknown_commodity.index)
        log.append(f"Dropped {before - len(df)} row(s) with unknown commodities.")

    # 4. Drop rows with invalid/unparseable dates
    invalid_dates = rules.rule_valid_date(df)
    if len(invalid_dates) > 0:
        before = len(df)
        df = df.drop(index=invalid_dates.index)
        log.append(f"Dropped {before - len(df)} row(s) with invalid dates.")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 5. Fill missing market values instead of dropping, so we don't lose price data
    missing_market = rules.rule_missing_market(df)
    if len(missing_market) > 0:
        df["markets"] = df["markets"].fillna("Unknown")
        log.append(f"Filled {len(missing_market)} missing market value(s) with 'Unknown'.")

    # 6. Drop rows with non-positive prices (bad/unusable data)
    bad_price = rules.rule_positive_price(df)
    if len(bad_price) > 0:
        before = len(df)
        df = df.drop(index=bad_price.index)
        log.append(f"Dropped {before - len(df)} row(s) with non-positive prices.")

    df = df.reset_index(drop=True)
    return df, log


def save_clean_data(df, path=data_path):
    path = path.strip()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)


def run():
    df, log = clean_data()

    print("======================================")
    print("           DATA CLEANING")
    print("======================================")
    for entry in log:
        print(f"- {entry}")

    print(f"\nFinal cleaned row count: {len(df)}")

    save_clean_data(df)
    print(f"Saved cleaned data to: {data_path.strip()}")

    print("\n======================================")
    print("        CLEANING COMPLETE")
    print("======================================")

    return df


if __name__ == "__main__":
    run()