import pandas as pd
import os

from src.validate import rules

raw_path= "data/raw/prive.csv"
data_path=" data/processed/prices_clean.parquet"

def clean_data(path=raw_path):
    df = pd.read_csv("path")
    log = []
    
    repeated_rows = rules.rule_duplicate_rows(df)
    if len(repeated_rows) > 0:
        pass
        

