#!/usr/bin/env python3
"""
Gold.de price scraper using requests + BeautifulSoup
Fallback version (more reliable than Playwright for this site)
"""

import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def scrape_gold_prices():
    """Scrape Gold.de using requests + BeautifulSoup."""
    
    url = "https://www.gold.de"
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9",
        "Referer": "https://www.gold.de/",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    prices = {}
    
    # Get all text from page
    text = soup.get_text()
    
    # Look for patterns: "20 g ... ab 2.452,26 EUR"
    patterns = [
        (r"20\s*g.*?ab\s+([\d.]+,\d{2})\s*EUR", "20"),
        (r"50\s*g.*?ab\s+([\d.]+,\d{2})\s*EUR", "50"),
        (r"100\s*g.*?ab\s+([\d.]+,\d{2})\s*EUR", "100"),
    ]
    
    for pattern, weight in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            price_str = match.group(1).replace(".", "").replace(",", ".")
            try:
                prices[weight] = float(price_str)
                print(f"✓ Found {weight}g: €{prices[weight]:.2f}")
            except ValueError:
                pass
    
    if len(prices) > 0:
        return prices
    
    print(f"Warning: Only found {len(prices)} prices")
    return None


def append_to_csv(prices):
    """Append prices to CSV file."""
    
    csv_path = Path("gold_prices.csv")
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Initialize CSV if doesn't exist or is empty
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "price_20g_eur",
                "price_50g_eur",
                "price_100g_eur"
            ])
    
    # Append new row
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            prices.get("20"),
            prices.get("50"),
            prices.get("100"),
        ])
    
    print(
        f"[{timestamp}] Recorded: "
        f"20g={prices.get('20', 'N/A')}€ "
        f"50g={prices.get('50', 'N/A')}€ "
        f"100g={prices.get('100', 'N/A')}€"
    )


def main():
    prices = scrape_gold_prices()
    if prices and len(prices) > 0:
        append_to_csv(prices)
        print(f"✓ Success: Recorded {len(prices)} prices")
        return 0
    else:
        print("✗ Failed to extract prices")
        return 1


if __name__ == "__main__":
    exit(main())
