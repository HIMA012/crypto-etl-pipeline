import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import os
import logging
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """
    Create and return a PostgreSQL database connection
    using credentials from the .env file.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "crypto_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_to_postgres(df: pd.DataFrame) -> int:
    """
    Load a transformed DataFrame into the crypto_prices table in PostgreSQL.

    Uses psycopg2's execute_values for efficient bulk insertion.

    Args:
        df: Cleaned and enriched DataFrame from the transform step

    Returns:
        Number of rows successfully inserted
    """
    conn = None
    cur = None

    # Columns must match the PostgreSQL table exactly
    columns = [
        "coin_id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "price_change_24h",
        "price_change_percentage_24h",
        "total_volume",
        "high_24h",
        "low_24h",
        "category",
        "extracted_at",
    ]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Build list of tuples for bulk insert
        values = [tuple(row[col] for col in columns) for _, row in df.iterrows()]

        insert_query = f"""
            INSERT INTO crypto_prices ({', '.join(columns)})
            VALUES %s
        """

        execute_values(cur, insert_query, values)
        conn.commit()

        rows_inserted = len(values)
        logging.info(f"Successfully inserted {rows_inserted} rows into crypto_prices")
        return rows_inserted

    except psycopg2.OperationalError as e:
        logging.error(f"Could not connect to PostgreSQL: {e}")
        logging.error("Check your .env credentials and that PostgreSQL is running")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error loading data to PostgreSQL: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
