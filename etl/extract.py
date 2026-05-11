# --- importing libs ----------------------------------------------------------------------------
import pandas as pd
import logging


# --- logging config ----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Extract Module ----------------------------------------------------------------------------

def extract_sales_data():
    try:
        logging.info("Starting data extraction...")
        df = pd.read_csv("data/raw/superstore_sales_dataset.csv")
        
        logging.info(f"Data exctracted sucessfully: {len(df)} lines!")
        return df
    except Exception as e:
        logging.error(f"Data extraction failed: {e}")
        

if __name__ == "__main__":
    logging.info("Testing data extraction")
    data = extract_sales_data()
    
    print(data.head())
    print(data.info())