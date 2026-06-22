import requests
import logging
from typing import List


def extract_crypto_data(limit: int = 20) -> List[dict]:
    """
    Extract top cryptocurrencies data from CoinGecko API.
    No API key required.

    Args:
        limit: Number of top coins to fetch (default: 20)

    Returns:
        List of raw cryptocurrency data dictionaries
    """
    
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
    }

    # ── التعديل الأول: إضافة الـ Headers لتخطي حماية الموقع ──────────────────
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        logging.info(f"Calling CoinGecko API for top {limit} coins...")
        
        # ── التعديل الثاني: تمرير الـ headers وزيادة الـ timeout إلى 15 ثانية ──
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        logging.info(f"API call successful — received {len(data)} coins")
        return data

    except requests.exceptions.ConnectionError:
        logging.error("Connection error — check your internet connection")
        raise
    except requests.exceptions.Timeout:
        logging.error("Request timed out — CoinGecko API did not respond")
        raise
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error from API: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during extraction: {e}")
        raise