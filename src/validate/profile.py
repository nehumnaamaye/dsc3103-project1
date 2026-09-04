#%%
import pandas as pd
#%%
from src.validate import rules 

raw_path ="data/raw/prices.csv"

def inferred_schema(df):
    print("\n Inferred schema")
    print("\n _______________________")
    print(df.dtypes)
    
def row_count(df):
    print("\n row count")
    print("\n _______________________")
    print (len(df))    
    
def negative_values(df):
    negative_values= rules.rule_positive_price(df)
    print("\n Negative price")
    print("\n__________________")    
    print(len(negative_values))
    
def run_files(path= raw_path):
    df = pd.read_csv(path)
    inferred_schema(df)
    row_count(df)   
    negative_values(df)
    
    
    
    
    
    
if __name__ == "__main__":
    run_files()    