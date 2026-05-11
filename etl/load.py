# --- importing lib ------------------------------------------------------
import pandas as pd
import duckdb
import logging

# --- importing modules --------------------------------------------------
from extract import extract_sales_data
from transform import transform_sales_data

# --- Logging Config -----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Connecting with duckdb ---------------------------------------------

def get_connection():
    conn = duckdb.connect("data/processed/superstore.duckdb")
    return conn

def load_data(df):
    try:
        logging.info("Starting data loading...")
        # --- gettting connection -------------------------------------------
        conn = get_connection()
        
        # --- Creating table ------------------------------------------------
        with conn as con:
            con.execute(
                "CREATE TABLE IF NOT EXISTS vendas_limpas AS SELECT * FROM df"
            )
        logging.info("Data loaded sucessffuly!")
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        

if __name__ == "__main__":
    logging.info("PIPELINE ETL == LOADING DATA")
    df = extract_sales_data()
    df_transformed = transform_sales_data(df)
    
    load_data(df_transformed)