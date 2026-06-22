import logging
import sys
from src.extract import extract_crypto_data
from src.transform import transform_crypto_data
from src.load import load_to_postgres


# ── Logging Setup ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),      # Print to terminal
        logging.FileHandler("pipeline.log"),    # Save to file
    ],
    encoding='utf-8'
)


def run_etl_pipeline():
    """
    Orchestrates the full ETL pipeline:
        1. Extract — fetch top 20 crypto prices from CoinGecko
        2. Transform — clean, enrich, and categorize the data
        3. Load — insert into PostgreSQL
    """
    logging.info("=" * 55)
    logging.info("       CRYPTO PRICE ETL PIPELINE — STARTED")
    logging.info("=" * 55)

    try:
        # ── EXTRACT ──────────────────────────────────────────────
        logging.info("[1/3] EXTRACT — Fetching from CoinGecko API...")
        raw_data = extract_crypto_data(limit=20)
        logging.info(f"      ✅ Extracted {len(raw_data)} coins")

        # ── TRANSFORM ────────────────────────────────────────────
        logging.info("[2/3] TRANSFORM — Cleaning and enriching data...")
        transformed_df = transform_crypto_data(raw_data)
        logging.info(f"      ✅ Transformed {len(transformed_df)} rows")

        # ── LOAD ─────────────────────────────────────────────────
        logging.info("[3/3] LOAD — Inserting into PostgreSQL...")
        rows_loaded = load_to_postgres(transformed_df)
        logging.info(f"      ✅ Loaded {rows_loaded} rows")

        logging.info("=" * 55)
        logging.info("       PIPELINE COMPLETED SUCCESSFULLY ✅")
        logging.info("=" * 55)

    except Exception as e:
        logging.error("=" * 55)
        logging.error(f"  PIPELINE FAILED ❌ — {e}")
        logging.error("=" * 55)
        sys.exit(1)


if __name__ == "__main__":
    run_etl_pipeline()
