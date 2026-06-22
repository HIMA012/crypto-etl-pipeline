-- ============================================================
--  Crypto ETL Pipeline — Database Schema
--  Run this ONCE to set up your PostgreSQL table
-- ============================================================

-- Step 1: Create the database (run separately in psql)
-- CREATE DATABASE crypto_db;

-- Step 2: Create the main table
CREATE TABLE IF NOT EXISTS crypto_prices (
    id                          SERIAL          PRIMARY KEY,
    coin_id                     VARCHAR(50)     NOT NULL,
    symbol                      VARCHAR(20)     NOT NULL,
    name                        VARCHAR(100)    NOT NULL,
    current_price               DECIMAL(20, 8),
    market_cap                  BIGINT,
    market_cap_rank             INTEGER,
    price_change_24h            DECIMAL(20, 8),
    price_change_percentage_24h DECIMAL(10, 4),
    total_volume                BIGINT,
    high_24h                    DECIMAL(20, 8),
    low_24h                     DECIMAL(20, 8),
    category                    VARCHAR(20)     CHECK (category IN ('gainer', 'loser', 'stable')),
    extracted_at                TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_crypto_coin_id     ON crypto_prices(coin_id);
CREATE INDEX IF NOT EXISTS idx_crypto_extracted_at ON crypto_prices(extracted_at);
CREATE INDEX IF NOT EXISTS idx_crypto_category     ON crypto_prices(category);


-- ============================================================
--  Useful Queries (for reference — run after loading data)
-- ============================================================

-- View the latest snapshot
-- SELECT name, current_price, price_change_percentage_24h, category
-- FROM crypto_prices
-- ORDER BY extracted_at DESC, market_cap_rank ASC
-- LIMIT 20;

-- Top gainers in the latest run
-- SELECT name, current_price, price_change_percentage_24h
-- FROM crypto_prices
-- WHERE category = 'gainer'
-- ORDER BY price_change_percentage_24h DESC
-- LIMIT 5;

-- Bitcoin price history over time
-- SELECT current_price, extracted_at
-- FROM crypto_prices
-- WHERE coin_id = 'bitcoin'
-- ORDER BY extracted_at DESC;

-- Count how many times the pipeline has run
-- SELECT DATE(extracted_at) AS run_date, COUNT(DISTINCT extracted_at) AS runs
-- FROM crypto_prices
-- GROUP BY DATE(extracted_at)
-- ORDER BY run_date DESC;
