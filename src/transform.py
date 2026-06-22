import pandas as pd
from datetime import datetime
import logging


def categorize_coin(pct_change: float) -> str:
    """
    Classify a coin based on its 24-hour price change percentage.

    Args:
        pct_change: Price change percentage over 24 hours

    Returns:
        'gainer' if > +2%, 'loser' if < -2%, else 'stable'
    """
    if pct_change > 2:
        return "gainer"
    elif pct_change < -2:
        return "loser"
    else:
        return "stable"


def transform_crypto_data(raw_data: list) -> pd.DataFrame:
    """
    Transform raw CoinGecko API response into a clean, enriched DataFrame.

    Steps:
        1. Select only the columns we need
        2. Fill missing values
        3. Add a 'category' column (gainer / loser / stable)
        4. Add an 'extracted_at' timestamp
        5. Cast columns to correct data types

    Args:
        raw_data: List of raw cryptocurrency dictionaries from the API

    Returns:
        Cleaned and enriched pandas DataFrame ready for loading
    """
    df = pd.DataFrame(raw_data)

    # --- Step 1: Select relevant columns ---
    columns_needed = [
        "id",
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
    ]
    df = df[columns_needed]

    # Rename 'id' to avoid conflict with PostgreSQL primary key
    df = df.rename(columns={"id": "coin_id"})

    # --- Step 2: Fill missing values ---
    df["price_change_24h"] = df["price_change_24h"].fillna(0)
    df["price_change_percentage_24h"] = df["price_change_percentage_24h"].fillna(0)
    df["market_cap"] = df["market_cap"].fillna(0)
    df["total_volume"] = df["total_volume"].fillna(0)
    df["high_24h"] = df["high_24h"].fillna(0)
    df["low_24h"] = df["low_24h"].fillna(0)

    # --- Step 3: Add 'category' column ---
    df["category"] = df["price_change_percentage_24h"].apply(categorize_coin)

    # --- Step 4: Add extraction timestamp ---
    df["extracted_at"] = datetime.utcnow()

    # --- Step 5: Cast to correct types ---
    df["market_cap"] = df["market_cap"].astype("int64")
    df["total_volume"] = df["total_volume"].astype("int64")
    df["market_cap_rank"] = df["market_cap_rank"].fillna(0).astype("int32")

    # Log a preview of the result
    gainers = (df["category"] == "gainer").sum()
    losers = (df["category"] == "loser").sum()
    stable = (df["category"] == "stable").sum()
    logging.info(
        f"Transform complete — {len(df)} rows | "
        f"Gainers: {gainers} | Losers: {losers} | Stable: {stable}"
    )

    return df
