# --- importing libs ----------------------------------------------------------------------------
import pandas as pd
import logging

# --- logging config ----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- importing modules --------------------------------------------------------------------------
from extract import extract_sales_data

# --- Transform module ---------------------------------------------------------------------------

def transform_sales_data(df):
    try:
        logging.info("Starting data transformation...")
        # --- Null values --------------------------------------------------------------------
        df = df.dropna()
        # --- Normalizing columns ------------------------------------------------------------
        df["Order ID"] = df["Order ID"].str.upper()
        df["Customer ID"] = df["Customer ID"].str.upper()
        df["Product ID"] = df["Product ID"].str.upper()
        
        df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
        
        # --- Data Enrichment -----------------------------------------------------------------
        df["order_year"] = df["Order Date"].dt.year
        df["order_month"] = df["Order Date"].dt.month
        df["shipping_days"] = df["Ship Date"] - df["Order Date"]
        # --- impossible to calculate profit margin there is no cost price --------------------
        
        # ---  ------------------------------------------------------------
        
        return df
    except Exception as e:
        logging.error(f"Data transformation failed: {e}")
        
        
if __name__ == "__main__":
    logging.info("Testing data transformation...")
    df = extract_sales_data()
    df_transformed = transform_sales_data(df)
    
    print(df_transformed.head())
    print(df_transformed.info())
    