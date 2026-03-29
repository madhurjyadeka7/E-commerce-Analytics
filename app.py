import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("ecommerce/Nassau Candy Distributor.csv")

# Create metrics
df['Gross Margin %'] = (df['Gross Profit'] / df['Sales']) * 100
df['Profit per Unit'] = df['Gross Profit'] / df['Units']

# TITLE
st.title("📊 E-Commerce Profitability Dashboard")

# FILTERS (User Capabilities)
st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division", df['Division'].unique(), default=df['Division'].unique()
)

margin = st.sidebar.slider("Minimum Margin %", 0, 100, 0)

product = st.sidebar.text_input("Search Product")

# Apply filters
filtered = df[df['Division'].isin(division)]
filtered = filtered[filtered['Gross Margin %'] >= margin]

if product:
    filtered = filtered[filtered['Product Name'].str.contains(product, case=False)]

# PRODUCT PROFITABILITY
st.header("📦 Product Profitability Overview")

product_profit = filtered.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False)

st.subheader("Top Products (Leaderboard)")
st.bar_chart(product_profit.head(10))

# Profit contribution
st.subheader("Profit Contribution")
st.bar_chart(product_profit.head(10) / product_profit.sum())

# DIVISION PERFORMANCE
st.header("🏢 Division Performance")

division_data = filtered.groupby('Division').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum',
    'Gross Margin %': 'mean'
})

st.subheader("Revenue vs Profit")
st.bar_chart(division_data[['Sales', 'Gross Profit']])

st.subheader("Margin Distribution")
st.bar_chart(division_data['Gross Margin %'])

# COST vs MARGIN
st.header("💰 Cost vs Margin Diagnostics")

fig, ax = plt.subplots()
sns.scatterplot(data=filtered, x='Cost', y='Gross Margin %', hue='Division', ax=ax)
st.pyplot(fig)

# Risk products
st.subheader("⚠️ Low Margin Products")
risk = filtered[filtered['Gross Margin %'] < 10]
st.dataframe(risk.head())

# PARETO ANALYSIS
st.header("📈 Profit Concentration (Pareto)")

df_sorted = filtered.sort_values(by='Gross Profit', ascending=False)
df_sorted['Cumulative Profit'] = df_sorted['Gross Profit'].cumsum()
total_profit = filtered['Gross Profit'].sum()

df_sorted['Profit %'] = df_sorted['Cumulative Profit'] / total_profit * 100

st.line_chart(df_sorted['Profit %'])

# KPI SUMMARY
st.header("📊 Key Metrics")

st.metric("Total Sales", int(filtered['Sales'].sum()))
st.metric("Total Profit", int(filtered['Gross Profit'].sum()))
st.metric("Avg Margin %", round(filtered['Gross Margin %'].mean(), 2))
