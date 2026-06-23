# 🪙 Crypto Price ETL Pipeline

## Built by Ibrahim — Data Engineering Portfolio

An automated data pipeline that extracts real-time cryptocurrency prices from the **CoinGecko API**, transforms and enriches the data using **Python & Pandas**, and loads it into a **PostgreSQL** database.

> Built as Project 1 of a Data Engineering Portfolio — demonstrating core ETL skills.

---

## 🏗️ Architecture

graph LR
    A[CoinGecko API<br>Free, No Key] -->|requests| B(Extract<br>Top 20 Coins)
    B -->|DataFrame| C(Transform<br>Pandas Clean & Enrich)
    C -->|psycopg2| D[(PostgreSQL<br>Structured DB)]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#fdd,stroke:#333,stroke-width:2px

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core programming language |
| CoinGecko API | Free data source — no API key needed |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database for storage |
| psycopg2 | PostgreSQL connector for Python |
| python-dotenv | Secure environment variable management |

---

## 📊 What Data Is Collected

Each pipeline run fetches the **top 20 cryptocurrencies by market cap** and stores:

| Column | Description |
|--------|-------------|
| `coin_id` | CoinGecko identifier (e.g. `bitcoin`) |
| `symbol` | Ticker symbol (e.g. `BTC`) |
| `current_price` | Price in USD |
| `market_cap` | Total market capitalization |
| `price_change_percentage_24h` | % price change in last 24 hours |
| `high_24h / low_24h` | Daily high and low price |
| `total_volume` | 24-hour trading volume |
| `category` | Enriched label: `gainer`, `loser`, or `stable` |
| `extracted_at` | Timestamp of when the data was fetched |

---

## 📁 Project Structure

```
crypto-etl-pipeline/
│
├── src/
│   ├── __init__.py
│   ├── extract.py        ← Fetches data from CoinGecko API
│   ├── transform.py      ← Cleans and enriches data with Pandas
│   └── load.py           ← Inserts into PostgreSQL
│
├── sql/
│   └── create_tables.sql ← Database schema & useful queries
│
├── .env.example          ← Template for environment variables
├── .gitignore
├── requirements.txt
├── README.md
└── main.py               ← Entry point — run the full pipeline
```

---



```
2024-01-15 10:30:00 | INFO     | =======================================================
2024-01-15 10:30:00 | INFO     |        CRYPTO PRICE ETL PIPELINE — STARTED
2024-01-15 10:30:00 | INFO     | =======================================================
2024-01-15 10:30:00 | INFO     | [1/3] EXTRACT — Fetching from CoinGecko API...
2024-01-15 10:30:01 | INFO     |       ✅ Extracted 20 coins
2024-01-15 10:30:01 | INFO     | [2/3] TRANSFORM — Cleaning and enriching data...
2024-01-15 10:30:01 | INFO     |       ✅ Transformed 20 rows
2024-01-15 10:30:01 | INFO     | [3/3] LOAD — Inserting into PostgreSQL...
2024-01-15 10:30:01 | INFO     |       ✅ Loaded 20 rows
2024-01-15 10:30:01 | INFO     | =======================================================
2024-01-15 10:30:01 | INFO     |        PIPELINE COMPLETED SUCCESSFULLY ✅
2024-01-15 10:30:01 | INFO     | =======================================================
```

---

## 🔍 Useful SQL Queries

```sql
-- Latest prices snapshot
SELECT name, current_price, price_change_percentage_24h, category
FROM crypto_prices
ORDER BY extracted_at DESC, market_cap_rank ASC
LIMIT 20;

-- Top gainers
SELECT name, current_price, price_change_percentage_24h
FROM crypto_prices
WHERE category = 'gainer'
ORDER BY price_change_percentage_24h DESC;

-- Bitcoin price over time
SELECT current_price, extracted_at
FROM crypto_prices
WHERE coin_id = 'bitcoin'
ORDER BY extracted_at DESC;

-- How many times has the pipeline run?
SELECT DATE(extracted_at) AS run_date, COUNT(DISTINCT extracted_at) AS runs
FROM crypto_prices
GROUP BY DATE(extracted_at)
ORDER BY run_date DESC;
```

---

## 💡 Skills Demonstrated

- **ETL Pipeline Design** — clean separation of Extract → Transform → Load
- **REST API Integration** — consuming public APIs with proper error handling
- **Data Transformation** — cleaning, type casting, and enriching data with Pandas
- **PostgreSQL** — schema design, indexing strategy, and efficient bulk inserts
- **Python Best Practices** — logging, environment variables, modular code structure

---


