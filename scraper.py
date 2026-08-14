#!/usr/bin/env python3
"""
Gold.de price scraper for 20g, 50g, 100g bars
Extracts prices from the homepage table and appends to CSV
Uses Playwright for JS rendering support
"""

import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed. Install with: pip install playwright")
    sys.exit(1)


def scrape_gold_prices():
    """Scrape Gold.de homepage for bar prices using Playwright."""
    
    url = "https://www.gold.de"
    prices = {}
    
    try:
        with sync_playwright() as p:
            # Use chromium browser
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.set_default_timeout(30000)
            
            # Navigate to page
            try:
                page.goto(url, wait_until="load")
            except Exception as e:
                print(f"Error navigating to {url}: {e}")
                browser.close()
                return None
            
            # Look for the BARREN section and extract prices
            # Target: links containing "goldbarren/20-gramm", etc.
            targets = {"20": "20-gramm", "50": "50-gramm", "100": "100-gramm"}
            
            for weight, path in targets.items():
                try:
                    # Find the link for this weight
                    selector = f"a[href*='{path}']"
                    link = page.query_selector(selector)
                    
                    if link:
                        # Get the parent row
                        row = link.evaluate("el => el.closest('tr')")
                        if row:
                            # Extract all text from the row
                            row_text = page.evaluate(
                                "el => el.innerText",
                                row
                            )
                            
                            # Look for price pattern "ab X.XXX,XX EUR"
                            price_match = re.search(
                                r"ab\s+([\d.]+,\d{2})\s*EUR",
                                row_text
                            )
                            if price_match:
                                price_str = price_match.group(1).replace(".", "").replace(",", ".")
                                prices[weight] = float(price_str)
                except Exception as e:
                    print(f"Error extracting price for {weight}g: {e}")
            
            browser.close()
    
    except Exception as e:
        print(f"Playwright error: {e}")
        return None
    
    if len(prices) >= 2:
        return prices
    else:
        print(f"Warning: Only found {len(prices)} prices, expected 3")
        print(f"Found prices: {prices}")
        return prices if len(prices) > 0 else None


def append_to_csv(prices):
    """Append prices to CSV file."""
    
    csv_path = Path("gold_prices.csv")
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Initialize CSV if it doesn't exist
    if not csv_path.exists():
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
        f"[{timestamp}] Prices recorded: "
        f"20g={prices.get('20')}€ "
        f"50g={prices.get('50')}€ "
        f"100g={prices.get('100')}€"
    )


def main():
    prices = scrape_gold_prices()
    if prices:
        append_to_csv(prices)
        return 0
    else:
        print("Failed to extract prices")
        return 1


if __name__ == "__main__":
    exit(main())
