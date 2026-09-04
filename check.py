import pandas as pd

from src.validate.rules import (
    rule_positive_price,
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_valid_date,
    rule_missing_market,
    rule_known_Commodity
)


# Load the raw dataset
df = pd.read_csv("data/raw/prices.csv")

print("======================================")
print("       DATA VALIDATION CHECK")
print("======================================")

print("\nRaw dataset:")
print(df)


# 1. Positive Price Rule
print("\n--------------------------------------")
print("1. POSITIVE PRICE RULE")
print("--------------------------------------")

failed = rule_positive_price(df)

if failed.empty:
    print("PASS: No invalid prices found.")
else:
    print(f"FAIL: {len(failed)} row(s) have invalid prices.")
    print(failed)


# 2. Duplicate ID Rule
print("\n--------------------------------------")
print("2. DUPLICATE ID RULE")
print("--------------------------------------")

failed = rule_duplicate_ids(df)

if failed.empty:
    print("PASS: No duplicate record IDs found.")
else:
    print(f"FAIL: {len(failed)} row(s) have duplicate record IDs.")
    print(failed)


# 3. Duplicate Row Rule
print("\n--------------------------------------")
print("3. DUPLICATE ROW RULE")
print("--------------------------------------")

failed = rule_duplicate_rows(df)

if failed.empty:
    print("PASS: No duplicate rows found.")
else:
    print(f"FAIL: {len(failed)} duplicate row(s) found.")
    print(failed)


# 4. Valid Date Rule
print("\n--------------------------------------")
print("4. VALID DATE RULE")
print("--------------------------------------")

failed = rule_valid_date(df)

if failed.empty:
    print("PASS: All dates are valid.")
else:
    print(f"FAIL: {len(failed)} row(s) have invalid dates.")
    print(failed)


# 5. Missing Market Rule
print("\n--------------------------------------")
print("5. MISSING MARKET RULE")
print("--------------------------------------")

failed = rule_missing_market(df)

if failed.empty:
    print("PASS: No missing market values found.")
else:
    print(f"FAIL: {len(failed)} row(s) have missing market values.")
    print(failed)


# 6. Known Commodity Rule
print("\n--------------------------------------")
print("6. KNOWN COMMODITY RULE")
print("--------------------------------------")

failed = rule_known_Commodity(df)

if failed.empty:
    print("PASS: All commodities are known.")
else:
    print(f"FAIL: {len(failed)} row(s) have unknown commodities.")
    print(failed)


print("\n======================================")
print("       VALIDATION CHECK COMPLETE")
print("======================================")