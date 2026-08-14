#!/usr/bin/env python3
"""
Analysis examples for gold_prices.csv

Run any of these after collecting real data:
    python analysis_examples.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def load_data(filepath='gold_prices.csv'):
    """Load and parse the CSV file."""
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df


# ============================================================================
# EXAMPLE 1: Basic Statistics
# ============================================================================

def example_basic_stats():
    """Print min, max, mean, std dev for each weight."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Statistics")
    print("=" * 70)
    
    df = load_data()
    
    for col in ['price_20g_eur', 'price_50g_eur', 'price_100g_eur']:
        weight = col.split('_')[1]
        print(f"\n{weight} Bar:")
        print(f"  Current:   €{df[col].iloc[-1]:.2f}")
        print(f"  Min:       €{df[col].min():.2f}")
        print(f"  Max:       €{df[col].max():.2f}")
        print(f"  Average:   €{df[col].mean():.2f}")
        print(f"  Std Dev:   €{df[col].std():.2f}")
        print(f"  Range:     €{df[col].max() - df[col].min():.2f}")


# ============================================================================
# EXAMPLE 2: Daily Summary
# ============================================================================

def example_daily_summary():
    """Group by day and show min/max/mean."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Daily Summary")
    print("=" * 70)
    
    df = load_data()
    
    daily = df.groupby(df.index.date).agg({
        'price_20g_eur': ['min', 'max', 'mean'],
        'price_50g_eur': ['min', 'max', 'mean'],
        'price_100g_eur': ['min', 'max', 'mean'],
    })
    
    print(daily.to_string())


# ============================================================================
# EXAMPLE 3: Price Changes
# ============================================================================

def example_price_changes():
    """Show how much price changed over time."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Price Changes")
    print("=" * 70)
    
    df = load_data()
    
    if len(df) < 2:
        print("Need at least 2 data points")
        return
    
    for col in ['price_20g_eur', 'price_50g_eur', 'price_100g_eur']:
        weight = col.split('_')[1]
        first = df[col].iloc[0]
        last = df[col].iloc[-1]
        change = last - first
        pct_change = (change / first) * 100
        
        print(f"\n{weight} Bar:")
        print(f"  First: €{first:.2f}")
        print(f"  Last:  €{last:.2f}")
        print(f"  Change: €{change:+.2f} ({pct_change:+.2f}%)")


# ============================================================================
# EXAMPLE 4: Find Best Buy Price (Lowest)
# ============================================================================

def example_best_buy_price():
    """Find when each weight was cheapest."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Best Buy Price (Lowest)")
    print("=" * 70)
    
    df = load_data()
    
    for col in ['price_20g_eur', 'price_50g_eur', 'price_100g_eur']:
        weight = col.split('_')[1]
        min_idx = df[col].idxmin()
        min_price = df[col].min()
        
        print(f"\n{weight} Bar:")
        print(f"  Lowest Price: €{min_price:.2f}")
        print(f"  Date/Time:    {min_idx.strftime('%Y-%m-%d %H:%M UTC')}")


# ============================================================================
# EXAMPLE 5: Plot Trends
# ============================================================================

def example_plot_trends():
    """Create a line chart of price trends."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Plot Trends (saves as price_chart.png)")
    print("=" * 70)
    
    df = load_data()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df.index, df['price_20g_eur'], marker='o', label='20g', linewidth=2)
    ax.plot(df.index, df['price_50g_eur'], marker='s', label='50g', linewidth=2)
    ax.plot(df.index, df['price_100g_eur'], marker='^', label='100g', linewidth=2)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Price (€)')
    ax.set_title('Gold Bar Prices Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.savefig('price_chart.png', dpi=150)
    print("✓ Saved to: price_chart.png")


# ============================================================================
# EXAMPLE 6: Hourly Comparison
# ============================================================================

def example_hourly_comparison():
    """Compare morning vs afternoon prices."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Morning vs Afternoon")
    print("=" * 70)
    
    df = load_data()
    
    # Split into morning (before noon) and afternoon (after noon)
    morning = df[df.index.hour < 12]
    afternoon = df[df.index.hour >= 12]
    
    if len(morning) == 0 or len(afternoon) == 0:
        print("Need data from multiple hours")
        return
    
    for col in ['price_20g_eur', 'price_50g_eur', 'price_100g_eur']:
        weight = col.split('_')[1]
        morning_avg = morning[col].mean()
        afternoon_avg = afternoon[col].mean()
        diff = afternoon_avg - morning_avg
        
        print(f"\n{weight} Bar:")
        print(f"  Morning Avg:    €{morning_avg:.2f}")
        print(f"  Afternoon Avg:  €{afternoon_avg:.2f}")
        print(f"  Difference:     €{diff:+.2f}")


# ============================================================================
# EXAMPLE 7: Volatility
# ============================================================================

def example_volatility():
    """Measure price volatility (std dev)."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Volatility (Standard Deviation)")
    print("=" * 70)
    
    df = load_data()
    
    for col in ['price_20g_eur', 'price_50g_eur', 'price_100g_eur']:
        weight = col.split('_')[1]
        std_dev = df[col].std()
        mean = df[col].mean()
        cv = (std_dev / mean) * 100  # Coefficient of variation
        
        print(f"\n{weight} Bar:")
        print(f"  Std Dev:        €{std_dev:.2f}")
        print(f"  Volatility %:   {cv:.2f}%")
        print(f"  Interpretation: {'High' if cv > 1 else 'Low'} volatility")


# ============================================================================
# EXAMPLE 8: Export to Excel
# ============================================================================

def example_export_excel():
    """Save data to Excel file (requires openpyxl)."""
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Export to Excel")
    print("=" * 70)
    
    df = load_data()
    
    try:
        df.to_excel('gold_prices.xlsx')
        print("✓ Saved to: gold_prices.xlsx")
    except ImportError:
        print("Install openpyxl: pip install openpyxl")


# ============================================================================
# Run Examples
# ============================================================================

if __name__ == "__main__":
    try:
        example_basic_stats()
        example_daily_summary()
        example_price_changes()
        example_best_buy_price()
        example_plot_trends()
        example_hourly_comparison()
        example_volatility()
        example_export_excel()
        
        print("\n" + "=" * 70)
        print("All examples completed!")
        print("=" * 70)
    
    except FileNotFoundError:
        print("Error: gold_prices.csv not found")
        print("Run the scraper first: python scraper_mock.py")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
