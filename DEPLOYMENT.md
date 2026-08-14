# Gold.de Price Tracker — Deployment Checklist

## What We Built

✅ **Automated hourly gold price scraper** for Gold.de (20g, 50g, 100g bars)  
✅ **GitHub Actions workflow** (runs Mon–Fri, 9 AM – 5 PM CEST)  
✅ **CSV historical log** (append-only, git-tracked)  
✅ **Three scraper versions** (production, simple, mock)  
✅ **Comprehensive documentation**

---

## Files to Copy to Your Repo

```
your-repo/
├── scraper.py                          [Production: Playwright version]
├── scraper_simple.py                   [Fallback: requests + BeautifulSoup]
├── scraper_mock.py                     [Testing: mock data only]
├── requirements.txt                    [Python dependencies]
├── gold_prices.csv                     [Data file - starts empty]
├── README.md                           [Full documentation]
├── .github/workflows/scraper.yml       [GitHub Actions configuration]
└── DEPLOYMENT.md                       [This file]
```

### Critical: .github/workflows/ Directory

The workflow file **must** go in `.github/workflows/` (note: dot-github, all lowercase).

```bash
mkdir -p .github/workflows
# Copy scraper.yml into this directory
```

---

## Quick Start (5 minutes)

### 1. Create GitHub Repo
```bash
mkdir gold-price-tracker
cd gold-price-tracker
git init
git config user.name "your-name"
git config user.email "your-email"
```

### 2. Copy Files
```bash
# Copy all files from /home/claude/ to your repo
# Make sure .github/workflows/ directory structure is correct
```

### 3. Commit & Push
```bash
git add .
git commit -m "Initial: gold price tracker"
git remote add origin https://github.com/YOUR_USERNAME/gold-price-tracker.git
git branch -M main
git push -u origin main
```

### 4. Enable Actions (if needed)
- Go to repo → **Settings** → **Actions** → **General**
- Ensure "Actions permissions" allows workflows

### 5. Test Manually
- Go to **Actions** tab
- Click "Gold.de Price Scraper"
- Click "Run workflow" → "Run workflow"
- Wait 30 seconds, refresh
- Check for green ✓ and data in `gold_prices.csv`

### 6. Verify Scheduled Runs
- Workflow runs hourly: **top of each hour (UTC time)**
- Schedule: **Mon–Fri, 7 AM – 3 PM UTC** (= 9 AM – 5 PM CEST)
- View in **Actions** tab

---

## File Purpose Reference

| File | Purpose | Edit? |
|------|---------|-------|
| `scraper.py` | Production scraper (Playwright) | Only if changing targets |
| `scraper_simple.py` | Local testing fallback | No — for reference |
| `scraper_mock.py` | Mock data for testing | No — for reference |
| `requirements.txt` | Python dependencies | Add if you need more packages |
| `gold_prices.csv` | Data log | No — auto-generated |
| `README.md` | Full docs + troubleshooting | Update as needed |
| `.github/workflows/scraper.yml` | GitHub Actions schedule | See "Customization" below |

---

## Customization

### Change Schedule (Cron)
Edit `.github/workflows/scraper.yml`, line ~7:
```yaml
- cron: "0 7-15 * * 1-5"  # Current: 7–15 UTC (9 AM–5 PM CEST), Mon–Fri
```

Examples:
- Every day: `"0 0 * * *"` (runs at midnight UTC daily)
- Every 6 hours: `"0 */6 * * *"`
- See [crontab.guru](https://crontab.guru) for syntax

### Add More Bar Sizes
Edit `scraper.py`, line ~30:
```python
targets = {
    "20": "20-gramm",
    "50": "50-gramm", 
    "100": "100-gramm",
    "250": "250-gramm",  # Add new
}
```

Then update CSV header in `append_to_csv()`:
```python
writer.writerow(["timestamp", "price_20g_eur", "price_50g_eur", "price_100g_eur", "price_250g_eur"])
```

---

## Troubleshooting

### Workflow Not Running
1. Check `.github/workflows/scraper.yml` **exact path** (case-sensitive)
2. Click **Actions** → **Run workflow** manually to test
3. View logs if failed (click the red ✗)

### CSV Not Updating
- Run manually first (see above)
- Check for errors in **Actions** logs
- Verify commit permissions in repo settings

### "playwright not found" Error
- GitHub Actions auto-installs via `playwright install chromium` in workflow
- Locally: `pip install playwright && playwright install chromium`

### Gold.de Page Changed
- Check `gold_prices.csv` for recent bad data (NaN, None)
- Update `scraper.py` line ~30 to match new page structure
- Test locally with `scraper_simple.py` first
- Post issue in repo if you can't fix

---

## Data Usage Examples

### Python (Pandas)
```python
import pandas as pd

df = pd.read_csv('gold_prices.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Daily max/min
print(df.groupby(df['timestamp'].dt.date)['price_100g_eur'].agg(['min', 'max']))

# Plot trend
df.set_index('timestamp')['price_100g_eur'].plot(figsize=(12, 4))
```

### Excel
1. Download `gold_prices.csv`
2. Open in Excel → "From Text"
3. Create pivot table or charts

### Google Sheets
1. Upload CSV to Google Drive
2. Import into Sheets
3. Create charts + sharing dashboard

---

## Cost

| Component | Cost |
|-----------|------|
| GitHub (public repo) | **Free** (unlimited Actions) |
| GitHub (private repo) | **Free** (2,000 min/month; $21/yr for more) |
| Compute | None (GitHub-hosted) |
| Storage | Minimal (CSV < 10 MB for 2 years) |

**Total: $0 (or $21/year for unlimited private repo)**

---

## Next Steps

1. ✅ Deploy to GitHub
2. ⏸ Let run for 1–2 weeks (build history)
3. 📊 Export and analyze in Python/Excel/Sheets
4. 🔔 (Optional) Add alerts if price drops below target
5. 📈 Share analysis with investment decisions

---

## Support & Issues

- **Documentation**: See `README.md`
- **Errors in logs**: Check `.github/workflows/scraper.yml` → "Run scraper" step
- **Page structure changed**: Update `scraper.py` or file GitHub Issue
- **Want more features**: Edit `scraper.py` + test locally first

---

**Deployed**: August 10, 2026  
**Status**: Ready for GitHub  
**Maintenance**: Minimal (update if Gold.de page structure changes)
