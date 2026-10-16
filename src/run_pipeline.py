from src.common.logging_setup import get_logger
from src.ingest.source_a1 import ingest_source_a1
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
logger = get_logger()

def run_pipe():
    logger.info("===Pipeline run started===")
    
    logger.info("Stage 1: Ingesting source a1")
    source_a1 = ingest_source_a1()
    logger.info(f"Source 11:Source a1 ingested rows out:{len(source_a1)}")
    
    
    logger.info("Stage 2: Ingesting source b")
    source_b = ingest_source_b()
    logger.info(f"Source 22:Source a1 ingested rows out:{len(source_b)}")
        
    logger.info("Stage 3: Cleaning source a1 ") 
    clean_prices, decisions = clean_data()
    logger.info(f"Stage 33: Source A cleaned rows in:{len(source_a1)}"
                f" rows out:{len(clean_prices)}"
                f" decisions made:{len(decisions)}")
    
    logger.info("Stage 4: Merging price and rainfall ")
    merged = merge_data(clean_prices, source_b)  
    logger.info(f"Stage 44: Merged complete: rows in:{len(clean_prices)}"
                f" rows out:{len(merged)}")
    
    return 


if __name__ == "__main__":
    run_pipe()