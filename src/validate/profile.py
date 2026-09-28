#%%
import pandas as pd

#%%
from src.validate import rules

raw_path = "data/raw/prices.csv"


def inferred_schema(df):
    print("\nInferred schema")
    print("_______________________")
    print(df.dtypes)


def row_count(df):
    print("\nRow count")
    print("_______________________")
    print(len(df))


def missing_values(df):
    print("\nMissing values per column")
    print("_______________________")
    print(df.isna().sum())


def unique_value_counts(df):
    print("\nUnique value counts")
    print("_______________________")
    print(f"Unique ids:        {df['id'].nunique()}")
    print(f"Unique markets:    {df['market'].nunique()} -> {sorted(df['market'].dropna().unique())}")
    print(f"Unique commodities:{df['Commodity'].nunique()} -> {sorted(df['Commodity'].dropna().unique())}")


def price_summary(df):
    print("\nPrice summary statistics")
    print("_______________________")
    print(df["price"].describe())


def negative_values(df):
    negative_values = rules.rule_positive_price(df)
    print("\nNegative/zero price rows")
    print("_______________________")
    print(len(negative_values))


def duplicate_ids(df):
    dup_ids = rules.rule_duplicate_ids(df)
    print("\nDuplicate record IDs")
    print("_______________________")
    print(len(dup_ids))


def duplicate_rows(df):
    dup_rows = rules.rule_duplicate_rows(df)
    print("\nDuplicate rows")
    print("_______________________")
    print(len(dup_rows))


def invalid_dates(df):
    bad_dates = rules.rule_valid_date(df)
    print("\nInvalid dates")
    print("_______________________")
    print(len(bad_dates))


def missing_market(df):
    missing = rules.rule_missing_market(df)
    print("\nMissing market values")
    print("_______________________")
    print(len(missing))


def unknown_commodity(df):
    unknown = rules.rule_known_Commodity(df)
    print("\nUnknown commodities")
    print("_______________________")
    print(len(unknown))


def run_files(path=raw_path):
    df = pd.read_csv(path)

    print(" \n          DATA PROFILE")
    print("======================================")

    inferred_schema(df)
    row_count(df)
    missing_values(df)
    unique_value_counts(df)
    price_summary(df)

    print(" \n      QUICK QUALITY ISSUE COUNTS")
    print("======================================")

    negative_values(df)
    duplicate_ids(df)
    duplicate_rows(df)
    invalid_dates(df)
    missing_market(df)
    unknown_commodity(df)

    
    print("  \n       PROFILE COMPLETE")
    print("======================================")


if __name__ == "__main__":
    run_files()
# %%
