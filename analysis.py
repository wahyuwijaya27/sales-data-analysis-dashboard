"""
PROJECT: Sales Data Analysis Dashboard
Author: Wahyu Wijayanto

Description:
End-to-end sales dashboard visualization for business insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ========================
# STYLE
# ========================
MAIN_COLOR = "#2F80ED"

plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# ========================
# LOAD & CLEAN
# ========================
df = pd.read_csv("superstore.csv", encoding='latin1')

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df['order_date'] = pd.to_datetime(df['order_date'])

# ✅ FIX PENTING (JANGAN STRING)
df['month'] = df['order_date'].dt.to_period('M')

# ========================
# KPI
# ========================
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_orders = df['order_id'].nunique()
avg_profit = df['profit'].mean()

# ========================
# AGGREGATION
# ========================
trend = df.groupby("month")["sales"].sum().sort_index()

# ✅ ubah ke datetime untuk plotting
trend.index = trend.index.to_timestamp()

kota = df.groupby("city")["sales"].sum().sort_values(ascending=False).head(5)

# ========================
# DASHBOARD
# ========================
fig, axes = plt.subplots(2, 2, figsize=(14,8))

# ===== KPI TEXT =====
fig.text(0.1, 0.95, f"Total Sales\n${total_sales:,.0f}", fontsize=11, weight='bold')
fig.text(0.35, 0.95, f"Total Profit\n${total_profit:,.0f}", fontsize=11, weight='bold')
fig.text(0.6, 0.95, f"Total Orders\n{total_orders}", fontsize=11, weight='bold')
fig.text(0.8, 0.95, f"Avg Profit\n${avg_profit:,.2f}", fontsize=11, weight='bold')

# ===== TREND =====
axes[0,0].plot(trend.index, trend.values, color=MAIN_COLOR, marker='o')

axes[0,0].set_title("Monthly Sales Trend")
axes[0,0].set_xlabel("Month")
axes[0,0].set_ylabel("Total Sales")

axes[0,0].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
axes[0,0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.setp(axes[0,0].get_xticklabels(), rotation=30, ha='right')

axes[0,0].grid(True, linestyle='--', alpha=0.4)

# ===== TOP CITY =====
axes[0,1].bar(kota.index, kota.values, color=MAIN_COLOR)

axes[0,1].set_title("Top 5 Cities by Sales")
axes[0,1].set_xlabel("City")
axes[0,1].set_ylabel("Total Sales")

axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].grid(axis='y', linestyle='--', alpha=0.4)

# ===== SALES VS PROFIT =====
axes[1,0].scatter(df['sales'], df['profit'], color=MAIN_COLOR, alpha=0.5)

axes[1,0].set_title("Sales vs Profit")
axes[1,0].set_xlabel("Sales")
axes[1,0].set_ylabel("Profit")

axes[1,0].grid(True, linestyle='--', alpha=0.4)

# ===== DISCOUNT VS PROFIT =====
axes[1,1].scatter(df['discount'], df['profit'], color=MAIN_COLOR, alpha=0.5)

axes[1,1].set_title("Discount Impact on Profit")
axes[1,1].set_xlabel("Discount")
axes[1,1].set_ylabel("Profit")

axes[1,1].grid(True, linestyle='--', alpha=0.4)

# ========================
# FINAL TOUCH
# ========================
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("dashboard.png")
plt.close()

print("=== DASHBOARD CREATED SUCCESSFULLY ===")