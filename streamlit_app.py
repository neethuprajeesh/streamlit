import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

category_names = df["Category"].unique()
category = st.selectbox( "**Choose the category**", options=category_names, index = None ,key="categories")
st.write("**Selected Category**:", category)


st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
sub_categories = df[df["Category"] == category]["Sub_Category"].unique()
sub_category = st.multiselect("**Choose the Sub-Category**", options=sub_categories, key="sub_categories")
st.write("**Selected Sub-Categories**:", ", ".join(sub_category))


st.write("### (3) show a line chart of sales for the selected items in (2)")
if sub_category:
    filtered_df = df[(df["Sub_Category"].isin(sub_category))]
    sales_by_month_selected = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_selected, y="Sales")



st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")


def format_metric(value):
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    elif abs_value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif abs_value >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value}"

if sub_category:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    formatted_total_sales = format_metric(total_sales)
    formatted_total_profit = format_metric(total_profit)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="**Total Sales**", value=formatted_total_sales)
    col2.metric(label="**Total Profit**", value=formatted_total_profit)
    col3.metric(label="**Profit Margin (%)**", value=f"{profit_margin:.2f}%")

    


st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
# ...existing code...

if sub_category:
    
    # Calculate overall average profit margin for all products
    overall_total_sales = df["Sales"].sum()
    overall_total_profit = df["Profit"].sum()
    overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales > 0 else 0

    formatted_overall_total_sales = format_metric(overall_total_sales)
    formatted_overall_total_profit = format_metric(overall_total_profit)
    delta_margin = profit_margin - overall_profit_margin

    col4, col5, col6 = st.columns(3)
    col4.metric(label="**Overall Total Sales**", value=formatted_overall_total_sales)
    col5.metric(label="**Overall Total Profit**", value=formatted_overall_total_profit)
    col6.metric(
        label="**Overall Profit Margin (%)**",
        value=f"{overall_profit_margin:.2f}%",
        delta=f"{delta_margin:+.2f}%"
    )
#
