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

    # displays result as text
    st.text(total_profit)
