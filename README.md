# Gold.de Price Tracker

Automated hourly extraction of 20g, 50g, and 100g gold bar prices from Gold.de with historical tracking in CSV format.

## Features

- **Hourly scraping** during trading hours (9 AM – 5 PM CEST, Mon–Fri)
- **Automatic GitHub Actions** — runs on schedule with zero setup after deployment
- **CSV history** — append-only log for trend analysis
- **Zero dependencies** during operation (Playwright auto-installed by GitHub Actions)
- **Atomic commits** — only pushes when prices change

## Scraper Versions

| Version | File | Usage | Dependencies |
|---------|------|-------|--------------|
| **Production** | `scraper.py` | GitHub Actions (auto-installed) | Playwright (headless browser) |
| **Simple** | `scraper_simple.py` | Local testing, may fail if Gold.de blocks | requests, BeautifulSoup4 |
| **Mock** | `scraper_mock.py` | Testing CSV structure only | None (stdlib only) |

**Recommended**: Deploy `scraper.py` to GitHub Actions. It uses Playwright (headless browser), which is more reliable against Gold.de blocking.

## Setup

### Option 1: GitHub (Recommended)

1. **Fork or create a new repo** and clone to your machine
   ```bash
   git clone https://github.com/YOUR_USERNAME/gold-price-tracker.git
   cd gold-price-tracker
   ```

2. **Copy these files into your repo root:**
   ```
   scraper.py
   requirements.txt
   .github/workflows/scraper.yml
   ```

3. **Commit and push:**
   ```bash
   git add scraper.py requirements.txt .github/workflows/
   git commit -m "Initial setup: gold price tracker"
   git push
   ```

4. **Enable Actions** (if needed):
   - Go to **Settings** → **Actions** → **General**
   - Ensure "Actions permissions" is set to allow workflows

5. **Verify** it runs:
   - Go to **Actions** tab
   - Click "Gold.de Price Scraper"
   - Wait for next scheduled run (top of the hour, 7–15 UTC = 9 AM – 5 PM CEST)
   - Or trigger manually: **Run workflow** → **Run workflow**

### Option 2: Local Testing

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

3. **Run scraper:**
   ```bash
   python scraper.py
   ```

4. **Check output:**
   ```bash
   cat gold_prices.csv
   ```

## CSV Format

```csv
timestamp,price_20g_eur,price_50g_eur,price_100g_eur
2026-08-10T09:00:00+00:00,2452.26,6084.16,12147.18
2026-08-10T10:00:00+00:00,2452.26,6084.16,12147.18
```

- **timestamp**: ISO 8601 UTC
- **price_***: Cheapest "ab" price in EUR from Gold.de homepage

## Data Analysis

### Pull data locally:
```bash
git pull
```

### Python example (pandas):
```python
import pandas as pd

df = pd.read_csv('gold_prices.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Plot 100g price over time
df['price_100g_eur'].plot(title='100g Gold Bar Price')

# Daily summary
df.resample('D').agg({'price_100g_eur': ['min', 'max', 'mean']})
```

## Troubleshooting

### "Workflow not running"
- Check **Actions** tab — if no runs, click **Run workflow** to test manually
- Verify `.github/workflows/scraper.yml` path is exact (note: lowercase)
- Cron runs in UTC; 7–15 UTC = 9 AM – 5 PM CEST

### "Error fetching Gold.de"
- Gold.de may block rapid requests; Playwright headless browser handles this
- If issue persists, check browser is actually running (GitHub Actions logs)

### CSV not updating
- Run manually: **Actions** → **Gold.de Price Scraper** → **Run workflow**
- Check **logs** for errors (click the failed run)

### "playwright not found"
- `requirements.txt` installs it; GitHub Actions runs `playwright install chromium`
- Locally: `pip install playwright && playwright install chromium`

## Customization

### Change schedule:
Edit `.github/workflows/scraper.yml`, line with `- cron`:
```yaml
- cron: "0 7-15 * * 1-5"  # Current: 7–15 UTC, Mon–Fri
- cron: "0 9-17 * * *"     # Example: 9–17 UTC, every day
```
See [crontab.guru](https://crontab.guru) for syntax.

### Add more weights:
1. Edit `scraper.py` line `targets = {...}`:
   ```python
   targets = {"20": "20-gramm", "50": "50-gramm", "100": "100-gramm", "250": "250-gramm"}
   ```
2. Update CSV header in `append_to_csv()` function

### Use a different parser:
Edit `scrape_gold_prices()` function — currently uses Playwright (reliable for JS sites). Could use BeautifulSoup if Gold.de serves static HTML.

## Legal / Ethical

- Gold.de ToS: Scraping is not explicitly forbidden, but check ToS before deployment
- Rate limiting: We scrape once per hour (9 times per trading day) — minimal load
- User-Agent: Playwright identifies as a real browser; no deception
- Consider reaching out to Gold.de if large-scale scraping is planned

## Cost

- **GitHub**: Free (unlimited Actions for public repos; 2,000 min/month for private)
- **Storage**: CSV stays under 1 MB for ~2 years of hourly data
- **Bandwidth**: Negligible

## Next Steps

1. Deploy to GitHub
2. Let it run for 1–2 weeks to build history
3. Export CSV and analyze in Python/Excel/Sheets
4. Set up alerts (e.g., email if 100g price drops below target)

---

**Created**: 2026-08-10  
**Last updated**: 2026-08-10
