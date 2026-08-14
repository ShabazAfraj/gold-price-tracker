# Gold.de Price Tracker

Automated hourly extraction of 20g, 50g, and 100g gold bar prices from Gold.de with historical tracking in CSV format.

## Features

- **Hourly scraping** — Every hour, 24/7 (configurable)
- **Automatic GitHub Actions** — Runs on schedule with zero manual intervention
- **CSV history** — Append-only log of all prices with timestamps
- **Reliable scraper** — Uses requests + BeautifulSoup (fast, stable)
- **Zero cost** — GitHub Actions free for public repos
- **Easy customization** — Change schedule in one line

## How It Works

```
GitHub Actions (every hour)
    ↓
Python scraper (requests + BeautifulSoup)
    ↓
Extract: 20g, 50g, 100g prices from Gold.de
    ↓
Append to gold_prices.csv
    ↓
Auto-commit if prices changed
```

## Data Format

```csv
timestamp,price_20g_eur,price_50g_eur,price_100g_eur
2026-08-10T09:00:00+00:00,2452.26,6084.16,12147.18
2026-08-10T10:00:00+00:00,2451.95,6082.50,12145.00
2026-08-10T11:00:00+00:00,2453.10,6088.75,12151.25
```

**Columns:**
- `timestamp` — ISO 8601 UTC time
- `price_20g_eur` — Cheapest 20g bar price in EUR (ab price from Gold.de)
- `price_50g_eur` — Cheapest 50g bar price in EUR
- `price_100g_eur` — Cheapest 100g bar price in EUR

## Setup (Already Done)

This repo is already configured and deployed to GitHub. The workflow runs automatically.

**What's deployed:**
- ✓ Scraper (requests + BeautifulSoup)
- ✓ GitHub Actions workflow
- ✓ CSV data collection
- ✓ Automatic hourly runs

## Current Schedule

**Runs every hour, 24/7**

To view the schedule, check `.github/workflows/scraper.yml`:
```yaml
- cron: "0 * * * *"  # Every hour
```

### Change the Schedule

Edit `.github/workflows/scraper.yml` and modify the cron line:

| Schedule | Cron |
|----------|------|
| Every hour (current) | `0 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Daily (midnight UTC) | `0 0 * * *` |
| Trading hours only (9 AM–5 PM CEST, Mon–Fri) | `0 7-15 * * 1-5` |

See [crontab.guru](https://crontab.guru) for other schedules.

## Data Analysis

### Python Example (Pandas)

```python
import pandas as pd

df = pd.read_csv('gold_prices.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Basic statistics
print(df['price_100g_eur'].describe())

# Daily summary
print(df.groupby(df['timestamp'].dt.date)['price_100g_eur'].agg(['min', 'max', 'mean']))

# Plot trend
df.set_index('timestamp')['price_100g_eur'].plot(figsize=(12, 5), title='100g Gold Bar Price')
```

### Excel

1. Download `gold_prices.csv` from the repo
2. Open in Excel
3. Create pivot tables or charts

## Workflow Details

### What Happens Each Hour

1. GitHub Actions triggers
2. Python environment loads
3. Dependencies install (requests, BeautifulSoup4)
4. `scraper.py` runs:
   - Fetches Gold.de homepage
   - Parses HTML to extract prices
   - Appends to `gold_prices.csv`
5. If prices changed:
   - Git commit
   - Git push
6. Done

### Automatic Retries

If the workflow fails, it doesn't retry automatically. It will run again at the next scheduled hour.

## Troubleshooting

### Workflow Failed

Go to **Actions** tab → click the failed run → click **"Run scraper"** step to see error.

**Common issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Gold.de not reachable | Retry next hour (temporary) |
| `prices: {}` | HTML structure changed | Update scraper.py selectors |
| `FileNotFoundError` | gold_prices.csv missing | Repo setup error (shouldn't happen) |

### CSV Not Updating

1. Check Actions tab for failed runs
2. Manually trigger: Actions → "Gold.de Price Scraper" → "Run workflow"
3. Check logs for error messages

### Add More Bar Sizes

Edit `scraper.py` to add more weights (250g, 500g, etc.):

1. Find the `patterns` section
2. Add new line like:
   ```python
   (r"250\s*g.*?ab\s+([\d.]+,\d{2})\s*EUR", "250"),
   ```
3. Update `gold_prices.csv` header to add `price_250g_eur` column

## File Structure

```
gold-price-tracker/
├── .github/workflows/
│   └── scraper.yml              GitHub Actions configuration
├── scraper.py                   Main scraper code
├── requirements.txt             Python dependencies
├── gold_prices.csv              Historical price data (auto-populated)
├── README.md                    This file
└── DEPLOYMENT.md                Setup reference (already deployed)
```

## Requirements

**Python packages** (automatically installed by GitHub Actions):
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing

No installation needed locally unless you want to run scraper manually.

### Run Locally (Optional)

```bash
pip install requests beautifulsoup4
python scraper.py
```

## API & Data Access

**No API key needed.** All data is public:
- Gold prices are from Gold.de homepage
- Data stored in git history
- CSV is plain text (human-readable)

## Storage & Cost

| Resource | Size | Cost |
|----------|------|------|
| CSV file | ~1 KB/month | $0 |
| Git history | Minimal | $0 |
| GitHub Actions | 1 run/hour = ~730 runs/month | FREE (unlimited for public repos) |
| **Total** | | **$0/year** |

Private repos: FREE (2,000 min/month); $21/year for unlimited.

## Analysis Tools

Included file `analysis_examples.py` has 8 examples:

1. Basic statistics (min, max, mean, std dev)
2. Daily summaries
3. Price change tracking
4. Best buy price finder
5. Volatility measurements
6. Trend charts (PNG export)
7. Hourly comparison (morning vs afternoon)
8. Excel export

## Next Steps

1. **Monitor:** Check Actions tab occasionally for workflow status
2. **Collect:** Let data accumulate for 1–2 weeks
3. **Analyze:** Download `gold_prices.csv`, run analysis locally
4. **Plan:** Use trends to inform gold purchase decisions
5. **Customize:** Adjust schedule or add more bar sizes as needed

## Git History

Every price change is tracked in git:

```bash
git log --oneline gold_prices.csv
```

Shows every time prices were recorded:
```
abc1234 chore: record gold prices at 2026-08-10 15:00 UTC
def5678 chore: record gold prices at 2026-08-10 14:00 UTC
ghi9012 chore: record gold prices at 2026-08-10 13:00 UTC
```

Click any commit to see what prices were recorded.

## Support

- **Full documentation:** See README.md and DEPLOYMENT.md
- **Workflow logs:** Actions tab → click run → check error messages
- **Code issues:** Check scraper.py or workflow configuration

## License

This tracker is provided as-is for personal use. No warranty or support guarantees.

## Legal Notice

- Gold.de scraping not prohibited by ToS (friendly bots welcome)
- Rate limit: 1 request per hour (very minimal load on server)
- User-Agent: Standard Python requests (identifies as a bot)

---

**Deployed:** 2026-08-10  
**Status:** Active & collecting data ✓  
**Schedule:** Every hour, 24/7  
**Last updated:** 2026-08-10
