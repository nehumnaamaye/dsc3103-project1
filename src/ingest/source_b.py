import requests
import pandas as pd
import time
import os


from src.common.config import (
    SOURCE_B_RAW_PATH,
    MARKET_COORDS,
    RAINFALL_START_DATE,
    RAINFALL_END_DATE,
    RAINFALL_URL
    )


def get_mkt_rainfall(mkt_name, latitude, longitude, start_date=RAINFALL_START_DATE, end_date=RAINFALL_END_DATE):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "daily": "precipitation_sum",
    }

    response = requests.get(RAINFALL_URL, params=params, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch rainfall data for {mkt_name}. Status code: {response.status_code}"
        )

    daily = response.json()["daily"]
    return pd.DataFrame(
        {
            "market": mkt_name,
            "date": daily["time"],
            "rainfall_mm": daily["precipitation_sum"],
        }
    )


def get_all_mkt_rain():
    all_mkts_rain =[]
    for mkt_name, (latitude, longitude) in MARKET_COORDS.items():
        rainfall= get_mkt_rainfall(mkt_name, latitude, longitude)
        all_mkts_rain.append(rainfall)
        time.sleep(5)
    return pd.concat(all_mkts_rain, ignore_index=True)

def ingest_source_b(path= SOURCE_B_RAW_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)
    
    df_b = get_all_mkt_rain()
    df_b.to_csv(path, index=False)  
    return df_b
