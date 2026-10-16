import pandas as pd


#def merge_data(clean_df, rainfall_df):
#   merged= clean_df.merge(rainfall_df,
#                          on=["market","date"],
#                          how="left"
#                          )
   
#   return merged

def merge_data(clean_df, rainfall_df):
    clean_df = clean_df.copy()
    rainfall_df = rainfall_df.copy()

    clean_df["date"] = pd.to_datetime(clean_df["date"], errors="coerce")
    rainfall_df["date"] = pd.to_datetime(rainfall_df["date"], errors="coerce")

    merged = clean_df.merge(
        rainfall_df,
        on=["market", "date"],
        how="left"
    )
    return merged