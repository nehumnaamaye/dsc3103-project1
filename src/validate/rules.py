import pandas as pd
import os

from src.validate.rules import (
    rule_positive_price,
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_valid_date,
    rule_missing_market,
    rule_known_commodity
)


df = pd.read_csv("data/raw/prices.csv")


log = []


# 1. Positive price
failed = rule_positive_price(df)

log.append(
    f"Positive price rule: rejected {len(failed)} rows because price <= 0."
)

df = df[df["price"] > 0]


# 2. Duplicate rows
failed = rule_duplicate_rows(df)

log.append(
    f"Duplicate row rule: rejected {len(failed)} duplicate rows."
)

df = df.drop_duplicates()


# 3. Duplicate IDs
failed = rule_duplicate_ids(df)

log.append(
    f"Duplicate ID rule: rejected {len(failed)} rows with duplicate record IDs."
)

df = df.drop_duplicates(subset="record_id", keep="first")


# 4. Valid dates
failed = rule_valid_date(df)

log.append(
    f"Valid date rule: rejected {len(failed)} rows with invalid dates."
)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])


# 5. Missing market
failed = rule_missing_market(df)

log.append(
    f"Missing market rule: found {len(failed)} rows with missing market values."
)

# Here we reject rows with missing market
df = df.dropna(subset=["market"])


# 6. Normalize commodity
failed = rule_known_commodity(df)

df["commodity"] = (
    df["commodity"]
    .str.strip()
    .str.title()
)

log.append(
    "Commodity values were normalized by removing whitespace "
    "and standardizing capitalization."
)


# Create output directory
os.makedirs("data/processed", exist_ok=True)


# Save cleaned data
df.to_parquet(
    "data/processed/prices_clean.parquet",
    index=False
)


# Save log
with open("cleaning_log.txt", "w") as file:
    for entry in log:
        file.write(entry + "\n")


print("Cleaning completed.")
print(df)