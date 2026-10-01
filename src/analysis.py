
"""
تحلیل داده‌های فروش تلفن همراه
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# تنظیم ظاهر نمودارها
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# ==================== ۱. بارگذاری داده ====================
print("=" * 50)
print("📊 تحلیل داده‌های فروش تلفن همراه")
print("=" * 50)

df = pd.read_csv('data/sales_data.csv', parse_dates=['date'])

print(f"\n✅ داده‌ها بارگذاری شد: {len(df):,} رکورد")
print(f"📅 بازه: {df['date'].min().date()} تا {df['date'].max().date()}")

# ==================== ۲. پاک‌سازی داده ====================
print("\n" + "=" * 50)
print("🧹 پاک‌سازی داده‌ها")
print("=" * 50)

# حذف مقادیر تکراری
initial_count = len(df)
df = df.drop_duplicates()
print(f"🗑️ رکوردهای تکراری حذف شد: {initial_count - len(df)}")

# حذف مقادیر منفی
df = df[df['total'] > 0]
print(f"✅ داده‌های نامعتبر حذف شد")

# افزودن ستون‌های زمانی
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['year_month'] = df['date'].dt.to_period('M')

# ==================== ۳. آمار کلی ====================
print("\n" + "=" * 50)
print("📈 آمار کلی")
print("=" * 50)

total_revenue = df['total'].sum()
total_units = df['quantity'].sum()
avg_price = df['price'].mean()

print(f"💰 مجموع درآمد: {total_revenue:,.0f} تومان")
print(f"📱 تعداد فروش: {total_units:,} دستگاه")
print(f"💵 میانگین قیمت: {avg_price:,.0f} تومان")

# ==================== ۴. پرفروش‌ترین برندها ====================
print("\n" + "=" * 50)
print("🏆 پرفروش‌ترین برندها")
print("=" * 50)

brand_sales = df.groupby('brand').agg({
    'quantity': 'sum',
    'total': 'sum'
}).sort_values('total', ascending=False)

brand_sales['percentage'] = (brand_sales['total'] / total_revenue * 100).round(2)

print(brand_sales)

# نمودار پرفروش‌ترین برندها
fig, ax = plt.subplots(figsize=(10, 6))
brand_sales['total'].plot(kind='bar', color='steelblue', ax=ax)
ax.set_title('پرفروش‌ترین برندها بر اساس درآمد', fontsize=14, fontweight='bold')
ax.set_xlabel('برند')
ax.set_ylabel('درآمد (تومان)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/brand_sales.png', dpi=300)
print("\n✅ نمودار برندها ذخیره شد: data/brand_sales.png")

# ==================== ۵. پرفروش‌ترین محصولات ====================
print("\n" + "=" * 50)
print("🏆 ۵ محصول پرفروش")
print("=" * 50)

top_products = df.groupby('model').agg({
    'quantity': 'sum',
    'total': 'sum'
}).sort_values('total', ascending=False).head(5)

print(top_products)

# محاسبه سهم ۵ محصول برتر
top5_share = (top_products['total'].sum() / total_revenue * 100).round(2)
print(f"\n📊 سهم ۵ محصول برتر از کل درآمد: {top5_share}%")

# ==================== ۶. روند فروش ماهانه ====================
print("\n" + "=" * 50)
print("📅 روند فروش ماهانه")
print("=" * 50)

monthly_sales = df.groupby('year_month')['total'].sum()

fig, ax = plt.subplots(figsize=(14, 6))
monthly_sales.plot(kind='line', color='darkgreen', linewidth=2, ax=ax)
ax.set_title('روند فروش ماهانه (۵ سال)', fontsize=14, fontweight='bold')
ax.set_xlabel('ماه')
ax.set_ylabel('درآمد (تومان)')
plt.tight_layout()
plt.savefig('data/monthly_trend.png', dpi=300)
print("✅ نمودار روند ماهانه ذخیره شد: data/monthly_trend.png")

# ==================== ۷. تحلیل فصلی ====================
print("\n" + "=" * 50)
print("🍂 تحلیل فصلی فروش")
print("=" * 50)

monthly_avg = df.groupby('month')['total'].sum() / df['year'].nunique()

fig, ax = plt.subplots(figsize=(12, 6))
monthly_avg.plot(kind='bar', color='coral', ax=ax)
ax.set_title('میانگین فروش ماهانه (تحلیل فصلی)', fontsize=14, fontweight='bold')
ax.set_xlabel('ماه')
ax.set_ylabel('میانگین درآمد (تومان)')
plt.xticks(range(12), ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'], rotation=45)
plt.tight_layout()
plt.savefig('data/seasonal_analysis.png', dpi=300)
print("✅ نمودار تحلیل فصلی ذخیره شد: data/seasonal_analysis.png")

# ==================== ۸. رشد سالانه ====================
print("\n" + "=" * 50)
print("📈 رشد سالانه فروش")
print("=" * 50)

yearly_sales = df.groupby('year')['total'].sum()
yearly_growth = yearly_sales.pct_change() * 100

for year, growth in yearly_growth.items():
    if pd.notna(growth):
        print(f"سال {year}: {growth:.1f}% رشد")

# ==================== ۹. نتیجه‌گیری ====================
print("\n" + "=" * 50)
print("🎯 نتایج کلیدی")
print("=" * 50)

print(f"""
1. مجموع درآمد ۵ سال: {total_revenue:,.0f} تومان
2. پرفروش‌ترین برند: {brand_sales.index[0]} با {brand_sales['percentage'].iloc[0]}% سهم
3. سهم ۵ محصول برتر: {top5_share}% از کل درآمد
4. اوج فروش: ماه‌های اسفند و مرداد
5. رشد سالانه: میانگین {yearly_growth.mean():.1f}%
""")

print("\n✅ تحلیل کامل شد!")
