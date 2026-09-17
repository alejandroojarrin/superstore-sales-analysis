# ==========================================
# SALES ANALYSIS - EXPLORATORY DATA ANALYSIS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
VISUALIZATIONS_DIR = Path("visualizations")
VISUALIZATIONS_DIR.mkdir(exist_ok=True)
# ==========================================
# 1. DATA LOADING AND INITIAL EXPLORATION
# ==========================================
# Load the Superstore dataset into a Pandas DataFrame.

df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin-1")
# Inspect the structure, data types and non-null values.

df.info()
print(df.head())
# ==========================================
# 2. OVERALL SALES AND PROFITABILITY
# ==========================================
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Total Sales:", round(df["Sales"].sum(), 2))
# Calculate the overall profit margin.
profit_margin = df["Profit"].sum() / df["Sales"].sum() * 100

print("Overall Profit Margin:", round(profit_margin, 2), "%")

print(df.groupby("Category")[["Sales", "Profit"]].sum())
# ==========================================
# 3. CATEGORY AND SUB-CATEGORY ANALYSIS
# ==========================================

# --- 3.1 Profitability by Category ---

# Compare sales and profit across product categories.
category_analysis = df.groupby("Category")[["Sales", "Profit"]].sum()
# Calculate the profit margin for each category.

category_analysis["Profit_Margin"] = category_analysis["Profit"] / category_analysis ["Sales"] * 100
print(category_analysis)

# --- 3.2 Profitability by Sub-Category ---

# Analyze profitability at a more detailed product level.
subcategory_analysis = df.groupby("Sub-Category")[["Sales", "Profit"]].sum()
# Calculate the profit margin for each sub-category.
subcategory_analysis["Profit_Margin"] = subcategory_analysis["Profit"] / subcategory_analysis["Sales"] * 100
# Sort sub-categories from the lowest to highest profit margin.
print(subcategory_analysis.sort_values("Profit_Margin"))

# ==========================================
# 4. TEMPORAL ANALYSIS
# ==========================================

# Convert Order Date from string to datetime format.
df["Order Date"] = pd.to_datetime(df["Order Date"])
# Extract the year from the order date.
df["Year"] = df["Order Date"].dt.year
print(df[["Order Date", "Year"]].head())

# --- 4.1 Yearly Performance ---

year_analysis = df.groupby("Year")[["Sales", "Profit"]].sum()
# Calculate yearly profit margin.
year_analysis["Profit Margin"] = year_analysis["Profit"] / year_analysis["Sales"] * 100
print(year_analysis)

# --- 4.2 Performance by Category and Year ---

temporal_category_analysis = df.groupby(["Year", "Category"])[["Sales", "Profit"]].sum()
temporal_category_analysis["Profit_Margin"] = (
    temporal_category_analysis["Profit"] /
    temporal_category_analysis["Sales"] * 100
)
# Analyze sub-category profitability over time.

# --- 4.3 Performance by Sub-Category and Year ---

temporal_subcategory_analysis = df.groupby(["Year", "Sub-Category"])[["Sales", "Profit"]].sum()
print(temporal_subcategory_analysis)
temporal_subcategory_analysis["Profit_Margin"] = (
    temporal_subcategory_analysis["Profit"] /
    temporal_subcategory_analysis["Sales"] * 100
)
print(temporal_subcategory_analysis) 

# --- 4.4 Category Performance in 2017 ---

category_2017 = temporal_category_analysis.loc[2017]

print(category_2017)

# --- 4.5 Sales and Profit Evolution ---

# Visualize the evolution of sales and profit over time.

plt.plot(year_analysis.index, year_analysis["Sales"], marker="o", label="Sales")
plt.plot(year_analysis.index, year_analysis["Profit"], marker="o", label="Profit")

plt.title("Sales and Profit Evolution")
plt.xlabel("Year")
plt.ylabel("Amount")
plt.legend()
plt.grid(True)
plt.savefig(
VISUALIZATIONS_DIR / "sales_profit_evolution.png",

    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --- 4.6 Profit Margin Evolution ---

# Visualize the evolution of profit margin over time.

plt.plot(
    year_analysis.index,
    year_analysis["Profit Margin"],
    marker="o"
)

plt.title("Profit Margin Evolution")
plt.xlabel("Year")
plt.ylabel("Profit Margin (%)")
plt.grid(True)
plt.savefig(
    VISUALIZATIONS_DIR / "profit_margin_evolution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ==========================================
# 5. TABLES DEEP-DIVE
# ==========================================

# --- 5.1 Overall Tables Performance ---

# Filter the dataset to investigate the Tables sub-category.
tables = df[df["Sub-Category"] == "Tables"]
# Analyze the relationship between discount levels and average profit.
print(tables.groupby("Discount")["Profit"].mean())
print("Average Discount for Tables: ", round(tables["Discount"].mean(), 2))
print("Average Profit for Tables: ", round(tables["Profit"].mean(), 2))

# --- 5.2 Tables Performance in 2017 ---

# Investigate whether the profitability problem of Tables
# became more severe in 2017.

tables_2017 = df[(df["Sub-Category"] == "Tables") & (df["Year"] == 2017)]
print(tables_2017.groupby("Discount")["Profit"].mean())
print("Average Discount:", tables_2017["Discount"].mean())
print("Average Profit:", tables_2017["Profit"].mean())

# --- 5.3 Furniture Sub-Categories in 2017 ---

furniture_2017 = df[
    (df["Year"] == 2017) &
    (df["Category"] == "Furniture")
]

furniture_2017_analysis = furniture_2017.groupby(
    "Sub-Category"
)[["Sales", "Profit"]].sum()

furniture_2017_analysis["Profit_Margin"] = (
    furniture_2017_analysis["Profit"] /
    furniture_2017_analysis["Sales"] * 100
)

print(furniture_2017_analysis.sort_values("Profit_Margin"))

# Visualize profit by Furniture sub-category in 2017.
furniture_2017_analysis["Profit"].sort_values().plot(kind="bar")

plt.title("Profit by Furniture Sub-Category - 2017")
plt.xlabel("Sub-Category")
plt.ylabel("Profit ($)")
plt.axhline(0)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# --- 5.4 Tables Profit by Discount Level ---

# Calculate the average profit for each discount level in Tables.
tables_discount_analysis = tables.groupby("Discount")["Profit"].mean()

print(tables_discount_analysis)
# Visualize the relationship between discount levels
# and average profit for Tables.

tables_discount_analysis.plot(
    kind="bar"
)

plt.title("Average Profit by Discount Level - Tables")
plt.xlabel("Discount")
plt.ylabel("Average Profit ($)")
plt.axhline(0)
plt.xticks(
    range(len(tables_discount_analysis.index)),
    [f"{discount * 100:.0f}%" for discount in tables_discount_analysis.index],
    rotation=0
)
plt.tight_layout()
plt.savefig(
    VISUALIZATIONS_DIR / "tables_profit_by_discount.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Check the number of orders at each discount level
# to assess the reliability of the comparison.
discount_counts = tables["Discount"].value_counts().sort_index()

print(discount_counts)

# --- 5.5 Tables by State ---

# HYPOTHESIS:
# The poor profitability of Tables may be concentrated
# in specific geographical areas.
tables_state = df[df["Sub-Category"]=="Tables"]
tables_state_analysis = tables_state.groupby("State")[["Sales", "Profit"]].sum()
print(tables_state_analysis.sort_values("Profit"))
# Analyze the evolution of Tables profitability by state and year.
tables_state_analysis = tables_state.groupby(["State", "Year"])[["Sales", "Profit"]].sum()
print(tables_state_analysis.sort_values("Profit").head(15))
tables_state_analysis["Profit_Margin"] = (
    tables_state_analysis["Profit"] /
    tables_state_analysis["Sales"] * 100
)
print(tables_state_analysis.sort_values("Profit_Margin").head(15))

# --- 5.6 Illinois and Chicago Drill-Down ---

# HYPOTHESIS:
# Illinois may contain specific cities responsible
# for a significant proportion of Tables' losses.

illinois_tables = df[(df["Sub-Category"]=="Tables") & (df["State"]=="Illinois")]
illinois_city = illinois_tables.groupby("City")[["Sales", "Profit"]].sum()

print(illinois_city.sort_values("Profit"))

# Focus on Chicago to investigate whether high discounts
# are associated with the observed losses.
# HYPOTHESIS:
# The losses observed in Chicago may be associated with
# unusually high discount levels.
tables_chicago = df[
    (df["Sub-Category"] == "Tables") &
    (df["City"] == "Chicago")
]

print(tables_chicago.groupby("Discount")["Profit"].mean())
# Investigate whether the losses are concentrated among
# a specific customer.
print(tables_chicago[["Order Date", "Product Name", "Sales", "Discount", "Profit"]])

print(tables_chicago[["Customer Name", "Product Name", "Sales", "Discount", "Profit"]])
print(tables_chicago["Customer Name"].value_counts())
# FINDING:
# The losses are not concentrated in a single customer.
# The analyzed orders belong to different customers.

# --- 5.7 Chicago Product Analysis ---

# Investigate whether specific products are responsible
# for the losses observed in Chicago.
product_analysis = tables_chicago.groupby("Product Name")[["Sales", "Profit"]].sum()

product_analysis["Profit_Margin"] = (
    product_analysis["Profit"] /
    product_analysis["Sales"] * 100
)

print(product_analysis.sort_values("Profit"))
# FINDING:
# All analyzed Table products generated negative profit.
# BoxOffice By Design concentrated the largest absolute loss.


# ==========================================
# 6. GEOGRAPHICAL ANALYSIS
# ==========================================

# --- 6.1 State Profitability ---

# Compare sales and profitability across states.
state_analysis = df.groupby("State")[["Sales", "Profit"]].sum()
print(state_analysis)
state_analysis["Profit_Margin"] = state_analysis["Profit"] / state_analysis["Sales"] * 100
print(state_analysis.sort_values("Profit"))

# --- 6.2 States with Largest Absolute Losses ---

# Identify the states generating the largest total losses.

worst_states = state_analysis.sort_values("Profit").head(10)
print(worst_states)

worst_states["Profit"].plot(
    kind="barh"
)

plt.title("Profit by State")
plt.xlabel("Profit ($)")
plt.ylabel("State")
plt.axvline(0)
plt.tight_layout()
plt.savefig(
    VISUALIZATIONS_DIR / "top_states_by_loss.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# --- 6.3 States with Lowest Profit Margins ---

# Identify the states with the lowest profitability relative to sales.
worst_margin_states = state_analysis.sort_values("Profit_Margin").head(10)
print(worst_margin_states)

worst_margin_states["Profit_Margin"].plot(
    kind="barh"
)

plt.title("Profit Margin by State")
plt.xlabel("Profit Margin (%)")
plt.ylabel("State")
plt.axvline(0)
plt.tight_layout()
plt.savefig(
    VISUALIZATIONS_DIR / "top_states_by_profit_margin.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ==========================================
# 7. OHIO DEEP-DIVE
# ==========================================

# --- 7.1 Category Analysis ---

# Filter Ohio transactions to investigate the drivers behind its losses.
ohio = df[df["State"] == "Ohio"]

ohio_category_analysis = ohio.groupby("Category")[["Sales", "Profit"]].sum()
ohio_category_analysis["Profit_Margin"] = (
    ohio_category_analysis["Profit"] / ohio_category_analysis["Sales"] * 100
)
print(ohio_category_analysis)

# --- 7.2 Sub-Category Analysis ---

ohio_subcategory_analysis = ohio.groupby("Sub-Category")[["Sales", "Profit"]].sum()
ohio_subcategory_analysis["Profit_Margin"] = (
    ohio_subcategory_analysis["Profit"] / ohio_subcategory_analysis["Sales"] * 100
)
print(ohio_subcategory_analysis)

ohio_subcategory_analysis["Profit"].plot(kind="bar")

plt.title("Profit by Sub-category - Ohio")
plt.xlabel("Sub-category")
plt.ylabel("Profit ($)")
plt.axhline(0)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(
    VISUALIZATIONS_DIR / "ohio_profit_by_subcategory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --- 7.3 Machines in Ohio ---

ohio_machines = ohio[ohio["Sub-Category"] == "Machines"]
ohio_machine_discount_analysis =  ohio_machines.groupby("Discount")[["Sales", "Profit"]].sum()
print(ohio_machine_discount_analysis)
print("Machine records in Ohio:", len(ohio_machines))

print(
    "Unique orders:",
    ohio_machines["Order ID"].nunique()
)

# --- 7.4 Machines Product Analysis ---

# Analyze profitability by product within the Machines sub-category in Ohio.

ohio_machine_products = ohio_machines.groupby(
    "Product Name"
)[["Sales", "Profit"]].sum()

ohio_machine_products["Profit_Margin"] = (
    ohio_machine_products["Profit"] /
    ohio_machine_products["Sales"] * 100
)

print(ohio_machine_products.sort_values("Profit"))

# ==========================================
# 8. MACHINES AND DISCOUNT ANALYSIS
# ==========================================

# --- 8.1 Profitability by Discount Level ---

# Analyze whether the high discounts observed in Ohio
# are also present in Machine sales across other states.

machines = df[df["Sub-Category"] == "Machines"]

machines_discount_analysis = machines.groupby("Discount").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Average_Profit=("Profit", "mean"),
    Records=("Profit", "size")
)

machines_discount_analysis["Profit_Margin"] = (
    machines_discount_analysis["Profit"] /
    machines_discount_analysis["Sales"] * 100
)

print(machines_discount_analysis)

# --- 8.2 Profit Margin Visualization ---

machines_discount_analysis["Profit_Margin"].plot(kind="line", marker="o")
plt.title("Profit Margin by Discount Level - Machines")
plt.xlabel("Discount Level")
plt.ylabel("Profit Margin (%)")
plt.axhline(0)
plt.grid(True)
plt.xticks(
    machines_discount_analysis.index,
    [f"{discount * 100:.0f}%" for discount in machines_discount_analysis.index],
    rotation=0
)
plt.tight_layout()
plt.savefig(
    VISUALIZATIONS_DIR / "machines_profit_margin_by_discount.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()