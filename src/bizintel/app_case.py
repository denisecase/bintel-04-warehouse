"""app_case.py - example.

An example of loading and visualizing raw business data.

Author: Denise Case
Date: 2026-06

Process:
    - Load raw CSV data files.
    - Visualize sales by region and product category.
    - Log a summary of findings.

Data Source:
- data/raw/customers_data.csv
- data/raw/products_data.csv
- data/raw/sales_data.csv

Terminal command to run this file from the root project folder:

uv run python -m bizintel.app_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it with your alias, and modify your copy.
  If you do, include your command to run it in the docstring above and in README.md.
"""

# === Section 1. Import dependencies and set up constants ===

# === DECLARE IMPORTS (bring in free code from elsewhere) ===

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import matplotlib.pyplot as plt
import pandas as pd

from bizintel.utils_data import (
    load_data,
)
from bizintel.utils_logger import LOG, log_header
from bizintel.utils_viz import plot_bar

# === DECLARE GLOBAL CONSTANTS AND CONFIGURATION ===

# In Python, a constant is a variable that should not change after it is defined.
# We indicate this with all capital letters and the Final type hint from the typing module.

# Raw data folder path (relative to the root project folder).
DATA_RAW: Final[Path] = Path("data/raw")

# The three raw data files for the smart sales project.
CUSTOMERS_FILE: Final[Path] = DATA_RAW / "customers_data.csv"
PRODUCTS_FILE: Final[Path] = DATA_RAW / "products_data.csv"
SALES_FILE: Final[Path] = DATA_RAW / "sales_data.csv"


# === Section 2. Define Reusable Functions ===

# === Section 2.1 DEFINE A SALES BY REGION FUNCTION ===

# Define a reusable function that takes
# the customers and sales DataFrames as input
# and returns a DataFrame with total sales by region.
# A pandas DataFrame is like a sheet - two-dimensional data with rows and columns.


def sales_by_region(
    df_customers: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate total sales amount by customer region.

    Args:
        df_customers: Customers DataFrame with CustomerID and Region columns.
        df_sales: Sales DataFrame with CustomerID and SaleAmount columns.

    Returns:
        DataFrame with Region and SaleAmount columns, sorted by SaleAmount.
    """
    LOG.info("Aggregating sales by region")

    # Make a copy of the sales DataFrame to avoid modifying the original
    df_sales = df_sales.copy()

    # Convert the SaleAmount column to numeric, coercing errors to NaN ("not a number")
    df_sales["SaleAmount"] = pd.to_numeric(df_sales["SaleAmount"], errors="coerce")

    # Merge the sales DataFrame with the customers DataFrame on CustomerID
    # to get the Region for each sale (like a "left join" in SQL)
    # A left join means we keep all rows from df_sales and add matching Region values from df_customers.
    df_merged: pd.DataFrame = df_sales.merge(
        df_customers[["CustomerID", "Region"]],
        on="CustomerID",
        how="left",
    )

    # Clean up the Region column by stripping whitespace and capitalizing each word
    df_merged["Region"] = df_merged["Region"].str.strip().str.title()

    # Group the merged DataFrame by Region and sum the SaleAmount for each region.
    # This returns a Series (a single column of values, one per region).
    # We cast to Series because we are grouping a single column.
    grouped: pd.Series = pd.Series(df_merged.groupby("Region")["SaleAmount"].sum())

    # Reset the index to turn the Series back into a DataFrame with two columns:
    # Region and SaleAmount.
    # Then sort by SaleAmount descending so the highest-revenue region appears first.
    df_region: pd.DataFrame = grouped.reset_index().sort_values(
        "SaleAmount", ascending=False
    )

    # Use the built-in dataframe iloc (index location) method
    # to get the first row of the sorted DataFrame (the region with the highest sales)
    # as a string.
    # In Python, we start counting with 0
    # (no offset from the beginning of the list),
    # so the first row is at index 0.
    top_region: str = str(df_region.iloc[0]["Region"])

    # Use the built-in dataframe iloc (index location) method
    # to get the first row of the sorted DataFrame
    # (the region with the highest sales)
    # as a float.
    top_sales: float = float(df_region.iloc[0]["SaleAmount"])

    # Log the top region and its total sales amount for quick reference
    # Using handy dandy f-strings (formatted string literals).
    # Format the sales amount as currency with commas and two floating decimal places.
    LOG.info(f"  Top region: {top_region} (${top_sales:,.2f})")

    LOG.info("Returning DataFrame with total sales by region")
    return df_region


# === Section 2.2 DEFINE A SALES BY CATEGORY FUNCTION ===

# Define a reusable function that takes
# the products and sales DataFrames as input
# and returns a DataFrame with total sales by category.
# A pandas DataFrame is like a sheet - two-dimensional data with rows and columns.


def sales_by_category(
    df_products: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate total sales amount by product category.

    WHY: Product category is another key business dimension.
    Understanding which categories drive revenue helps prioritize
    inventory, marketing, and purchasing decisions.

    Args:
        df_products: Products DataFrame with ProductID and Category columns.
        df_sales: Sales DataFrame with ProductID and SaleAmount columns.

    Returns:
        DataFrame with Category and SaleAmount columns, sorted by SaleAmount.
    """
    LOG.info("Aggregating sales by product category")

    # Make a copy of the sales DataFrame to avoid modifying the original
    df_sales = df_sales.copy()

    # Convert the SaleAmount column to numeric, coercing errors to NaN ("not a number")
    df_sales["SaleAmount"] = pd.to_numeric(df_sales["SaleAmount"], errors="coerce")

    # Merge the sales DataFrame with the products DataFrame on ProductID
    # to get the Category for each sale (like a "left join" in SQL)
    # A left join means we keep all rows from df_sales and add matching Category values from df_products.
    df_merged: pd.DataFrame = df_sales.merge(
        df_products[["ProductID", "Category"]],
        on="ProductID",
        how="left",
    )

    # Group the merged DataFrame by Category and sum the SaleAmount for each category.
    # This returns a Series (a single column of values, one per category).
    # We cast to Series because we are grouping a single column.
    grouped: pd.Series = pd.Series(df_merged.groupby("Category")["SaleAmount"].sum())

    # Reset the index to turn the Series back into a DataFrame with two columns:
    # Category and SaleAmount.
    # Then sort by SaleAmount descending so the highest-revenue category appears first.
    df_category: pd.DataFrame = grouped.reset_index().sort_values(
        "SaleAmount", ascending=False
    )

    # Use the built-in dataframe iloc (index location) method
    # to get the first row of the sorted DataFrame (the category with the highest sales)
    # as a string.
    # In Python, we start counting with 0 (no offset from the beginning of the list),
    # so the first row is at index 0.
    top_category: str = str(df_category.iloc[0]["Category"])

    # Use the built-in dataframe iloc (index location) method
    # to get the first row of the sorted DataFrame
    # (the category with the highest sales)
    # as a float.
    top_sales: float = float(df_category.iloc[0]["SaleAmount"])

    # Log the top category and its total sales amount for quick reference
    # Using handy dandy f-strings (formatted string literals).
    # Format the sales amount as currency with commas and two floating decimal places.
    LOG.info(f"  Top category: {top_category} (${top_sales:,.2f})")

    return df_category


# === Section 2.3 DEFINE A SUMMARIZE FUNCTION ===

# Define a reusable function that takes
# all 3 dataframes as input and logs a summary of each dataset.
# A pandas DataFrame is like a sheet - two-dimensional data with rows and columns.


def summarize(
    df_customers: pd.DataFrame,
    df_products: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> None:
    """Log a brief summary of all three datasets.

    Args:
        df_customers: Customers DataFrame.
        df_products: Products DataFrame.
        df_sales: Sales DataFrame.

    Returns:
        None
    """
    LOG.info("========================")
    LOG.info("SUMMARY")
    LOG.info("========================")

    # Get the number of rows and columns in each using the shape attribute (0=rows, 1=columns)
    cust_rows: int = df_customers.shape[0]
    cust_cols: int = df_customers.shape[1]

    # Get the number of rows and columns in the products DataFrame using the shape attribute (0=rows, 1=columns)
    prod_rows: int = df_products.shape[0]
    prod_cols: int = df_products.shape[1]

    # Get the number of rows and columns in the sales DataFrame using the shape attribute (0=rows, 1=columns)
    sale_rows: int = df_sales.shape[0]
    sale_cols: int = df_sales.shape[1]

    # Log the summary of each dataset using f-strings (formatted string literals)
    # Start with an f outside the string, then use curly braces {} to insert variables into the string.
    LOG.info(f"Customers:  {cust_rows} rows, {cust_cols} columns")
    LOG.info(f"Products:   {prod_rows} rows, {prod_cols} columns")
    LOG.info(f"Sales:      {sale_rows} rows, {sale_cols} columns")

    LOG.info("========================")
    LOG.info("ANALYST NOTES:")
    LOG.info("Note any data quality issues.")
    LOG.info("We will clean data later.")
    LOG.info("========================")


# === DEFINE THE MAIN FUNCTION (WHERE THE MAGIC HAPPENS) ===


def main() -> None:
    """Main function to run the BI logic.
    This is where the main logic starts
    when this script is run.
    """

    # First, log the header for the BI module to indicate the start of the workflow.
    log_header(LOG, "BI")

    # Clearly indicate the start of the main function in the logs for easy tracking.
    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    # Use the imported log_path function to
    # log the paths of all critical paths and files for reference.
    log_path(LOG, "Raw data: ", DATA_RAW)
    log_path(LOG, "Customers:", CUSTOMERS_FILE)
    log_path(LOG, "Products: ", PRODUCTS_FILE)
    log_path(LOG, "Sales:    ", SALES_FILE)

    LOG.info("CALL a function to load each dataset.............")
    df_customers = load_data(CUSTOMERS_FILE, "customers")
    df_products = load_data(PRODUCTS_FILE, "products")
    df_sales = load_data(SALES_FILE, "sales")

    LOG.info("CALL a function to get sales by region........")
    df_region = sales_by_region(df_customers, df_sales)

    LOG.info("CALL a function to plot sales by region........")
    plot_bar(
        df=df_region,
        x="Region",
        y="SaleAmount",
        title="Total Sales by Region",
        xlabel="Region",
        ylabel="Total Sales Amount ($)",
        palette="Blues_d",
    )

    LOG.info("CALL a function to get sales by product category........")
    df_category = sales_by_category(df_products, df_sales)

    LOG.info("CALL a function to plot sales by product category........")
    plot_bar(
        df=df_category,
        x="Category",
        y="SaleAmount",
        title="Total Sales by Product Category",
        xlabel="Category",
        ylabel="Total Sales Amount ($)",
        palette="Greens_d",
    )

    LOG.info("CALL a function to summarize the datasets........")
    summarize(df_customers, df_products, df_sales)

    LOG.info("CALL a function to show charts........")
    plt.show()

    LOG.info("Workflow complete")
    LOG.info("CLOSE chart windows to continue.")
    LOG.info("Terminate this process with CTRL+c as needed.")
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    # This conditional ensures that the main() function is only executed
    # when this script is run directly, not when it is imported as a module.
    main()
