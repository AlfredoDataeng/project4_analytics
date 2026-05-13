# --- Importing libs ----------------------------------------------------------------------
import pandas as pd
import duckdb
import logging

# --- Logging Config ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Function to execute queries ---------------------------------------------------------

def generate_insights():
    try:
        # --- Data base connection --------------------------------------------------------
        logging.info("Starting database connection...")
        duck = duckdb.connect("data/processed/superstore.duckdb")
        
        # --- Generating insights --------------------------------------------------------
        
        df_insight_by_category = duck.execute(
            '''
                 SELECT
                    category,
                    sub_category,
                    COUNT(DISTINCT order_id)      AS total_orders,
                    ROUND(SUM(sales), 2)          AS total_sales,
                    ROUND(AVG(sales), 2)          AS avg_order_value
                FROM vendas_limpas
                GROUP BY category, sub_category
                ORDER BY total_sales DESC
            '''
        ).df()
        
        df_insight_trend = duck.execute(
                '''
                SELECT
                    order_year,
                    order_month,
                    COUNT(DISTINCT order_id)  AS total_orders,
                    ROUND(SUM(sales), 2)      AS total_sales,
                    ROUND(AVG(sales), 2)      AS avg_sales
                FROM vendas_limpas
                GROUP BY order_year, order_month
                ORDER BY order_year, order_month
                '''
        ).df()
        
        df_insight_geography = duck.execute(
            '''
            SELECT
                region,
                state,
                COUNT(DISTINCT order_id)  AS total_orders,
                ROUND(SUM(sales), 2)      AS total_sales,
                ROUND(AVG(sales), 2)      AS avg_sales
            FROM vendas_limpas
            GROUP BY region, state
            ORDER BY total_sales DESC
            '''
        ).df()
        
        df_insight_clients = duck.execute(
            '''
            SELECT
                customer_id,
                customer_name,
                segment,
                COUNT(DISTINCT order_id)  AS total_orders,
                ROUND(SUM(sales), 2)      AS total_sales,
                ROUND(AVG(sales), 2)      AS avg_order_value
            FROM vendas_limpas
            GROUP BY customer_id, customer_name, segment
            ORDER BY total_sales DESC
            LIMIT 20
            '''
        ).df()
        
        df_insight_operations = duck.execute(
            '''
            SELECT
                ship_mode,
                region,
                COUNT(DISTINCT order_id)                AS total_orders,
                ROUND(AVG(shipping_days), 1)            AS avg_shipping_days,
                ROUND(SUM(sales), 2)                    AS total_sales
            FROM vendas_limpas
            GROUP BY ship_mode, region
            ORDER BY avg_shipping_days
            '''
        ).df()
        logging.info("insights generated sucessfully!") 
        # --- Creating tables from insights --------------------------------------------------
        try:
            # Starting process
            logging.info("Transforming Insights to table...")
            
            # Turnig dataframes to tables on duckDB
            duck.execute("CREATE OR REPLACE TABLE insight_sales_by_category AS SELECT * FROM df_insight_by_category")
            duck.execute("CREATE OR REPLACE TABLE insight_trend AS SELECT * FROM df_insight_trend")
            duck.execute("CREATE OR REPLACE TABLE insight_geography AS SELECT * FROM df_insight_geography")
            duck.execute("CREATE OR REPLACE TABLE insight_clients AS SELECT * FROM df_insight_clients")
            duck.execute("CREATE OR REPLACE TABLE insight_operations AS SELECT * FROM df_insight_operations")
            
            # Closing connection
            logging.info("New tables saved on duckDB!")
            duck.close()
        except Exception as e:
            logging.error(f"Failed to convert df_insights to tables on duckDB: {e}")
            
    except Exception as e:
        logging.error(f"Failed to generate insights: {e}")    
    
    
    
    
if __name__ == "__main__":
    try:
        logging.info("Starting to generate insights...")
        generate_insights()
        
        logging.info("Insights available on the database for queries!")
        
    except Exception as e:
        logging.error(f"Failed to load insights to the database: {e}")
        

        