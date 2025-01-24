import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Slimr Analytics",
    page_icon="📊",
    layout='wide'
)

st.title("📊 Slimr Analytics Dashboard")

# widget to upload a file (csv will be the only file that can be attached)
uploaded_file = st.file_uploader(label="Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# basic table structure on streamlit
    col1, col2, col3 =st.columns(3)
    with col1:
        st.metric("Total Sales", f"€{df['price'].sum():.2f}")
    with col2:
        st.metric("Total Products Sold", f"{df['quantity'].sum()}")
    with col3:
        st.metric("Average Order Value", f"€{(df['price'] * df['quantity']).mean():.2f}")

    # Create profit column
    df['profit'] = (df['price'] - df['cost']) * df['quantity']

    # Calculate sum of the profit for each individual product
    total_profit = df.groupby('product_id').agg({
        'profit': 'sum',
    }).sort_values(by='profit' ,ascending=False)

   
    # For most profitable
    most_profitable_id = total_profit.index[0]  # get the first product ID
    most_profitable_value = total_profit['profit'].iloc[0]  # get its profit value

    # For least profitable
    least_profitable_id = total_profit.index[-1] # get the last product ID
    least_profitable_value = total_profit['profit'].iloc[-1] # get its profit value

    col1, col2 = st.columns(2)
    with col1:
    # display results
        st.metric(
        f"Most Profitable Product (#{most_profitable_id})", 
        f"€{most_profitable_value:.2f}"
        )


    with col2:
        st.metric(
            f"Least Profitable Product (#{least_profitable_id})",
            f"€{least_profitable_value:.2f}"
        )
