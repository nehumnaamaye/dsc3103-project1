import os
import time
import pandas as pd
import duckdb as db

RAW_JOINED_PATH = "data/processed/prices_with_rainfall.parquet" 
    
def maize_query():
    t0 = time.perf_counter()
    result = db.sql(f"""
       SELECT market, AVG(price) AS mean_price
       FROM '{RAW_JOINED_PATH}'
       GROUP BY market
       ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== Step 1: Maize query (flat Parquet) ===")
    print(result)
    print(f"Time: {elapsed:.4f}s | File size: {os.path.getsize(RAW_JOINED_PATH)} bytes")
    return elapsed


    
def beans_query():
    t0 = time.perf_counter()
    result = db.sql(f"""
       SELECT market, AVG(price) AS mean_price
       FROM '{RAW_JOINED_PATH}'
       WHERE commodity = 'Beans'
       GROUP BY market
       ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== Step 2: Beans query (flat Parquet) ===")
    print(result)
    print(f"Time: {elapsed:.4f}s | File size: {os.path.getsize(RAW_JOINED_PATH)} bytes")
    return elapsed





DB_PATH= "data/processed/analytics.duckdb"

def build_star_schema():
    df = pd.read_parquet(RAW_JOINED_PATH)
    con = db.connect(DB_PATH)


    dim_market = (
        df[["market"]].drop_duplicates().reset_index(drop=True)
    )
    
    dim_market["market_id"] = dim_market.index
    
    con.execute("CREATE OR REPLACE TABLE dim_market AS SELECT * FROM dim_market")

    dim_commodity =(
        df[["commodity"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    
    dim_commodity["commodity_id"] = dim_commodity.index
    
    con.execute("CREATE OR REPLACE TABLE dim_commodity AS SELECT * FROM dim_commodity")


#fact table
    fact= df.merge(dim_market,
                   on= "market",
                   how="left")
    
    fact = fact.merge(dim_commodity,
                      on="commodity",
                      how="left")
    fact_price_observation = fact[
        ["id",
         "date",
         "market_id",
         "commodity_id",
         "price",
         "rainfall_mm"]
    ]
    con.execute(
        "CREATE OR REPLACE TABLE fact_price_observation AS SELECT * FROM fact_price_observation"
    )

    print("=== Step 3: Star schema built ===")
    print(
        "Fact table row count:",
        con.sql("SELECT COUNT(*) FROM fact_price_observation").fetchone()[0],
    )
    con.close()


def run_analytical_queries():
    con = db.connect(DB_PATH)

    print("=== Query 1: Average price by market ===")
    print(con.sql("""
        SELECT dm.market, AVG(f.price) AS mean_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_price DESC
    """).df())

    print("=== Query 2: Observation count by commodity ===")
    print(con.sql("""
        SELECT dc.commodity, COUNT(*) AS n_observations
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY n_observations DESC
    """).df())

    print("=== Query 3: Highest-priced market for each commodity ===")
    print(con.sql("""
        WITH commodity_market_avg AS (
            SELECT dc.commodity, dm.market, AVG(f.price) AS mean_price,
                   RANK() OVER (PARTITION BY dc.commodity ORDER BY AVG(f.price) DESC) AS rnk
            FROM fact_price_observation f
            JOIN dim_market dm ON f.market_id = dm.market_id
            JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
            GROUP BY dc.commodity, dm.market
        )
        SELECT commodity, market, mean_price
        FROM commodity_market_avg
        WHERE rnk = 1
        ORDER BY commodity
    """).df())

    print("=== Query 4: Average rainfall by market (excluding missing readings) ===")
    print(con.sql("""
        SELECT dm.market, AVG(f.rainfall_mm) AS mean_rainfall_mm,
               COUNT(f.rainfall_mm) AS n_with_rainfall,
               COUNT(*) AS n_total
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_rainfall_mm DESC
    """).df())

    print("=== Query 5: Monthly average price per commodity ===")
    print(con.sql("""
        SELECT dc.commodity,
        date_trunc('month', CAST (f.date AS DATE)) AS month,
               AVG(f.price) AS mean_price,
               COUNT(*) AS n_observations
        FROM fact_price_observation f
        
        JOIN dim_commodity dc 
            ON f.commodity_id = dc.commodity_id
            
        GROUP BY
            dc.commodity, date_trunc('month', CAST (f.date AS DATE))
        ORDER BY dc.commodity, month
    """).df())

    con.close()


def compare_performance():
    t0 = time.perf_counter()
    db.sql(f"""
        SELECT market, AVG(price) 
        FROM '{RAW_JOINED_PATH}'
        GROUP BY market
    """).df()
    flat_time = time.perf_counter() - t0

    con = db.connect(DB_PATH)
    t0 = time.perf_counter()
    con.sql("""
        SELECT dm.market, AVG(f.price)
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
    """).df()
    star_time = time.perf_counter() - t0
    con.close()

    print("=== Step 5: Performance comparison ===")
    print(f"Flat Parquet query time:  {flat_time:.4f}s")
    print(f"Star schema query time:   {star_time:.4f}s")


if __name__ == "__main__":
    maize_query()
    beans_query()
    build_star_schema()
    run_analytical_queries()
    compare_performance()
