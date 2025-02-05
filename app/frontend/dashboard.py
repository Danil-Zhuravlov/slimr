import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import APIClient

api_client = APIClient()

st.set_page_config(
    page_title="Slimr Analytics",
    page_icon="📊",
    layout='wide'
)

st.title("📊 Slimr Analytics Dashboard")

# widget to upload a file (csv will be the only file that can be attached)
uploaded_file = st.file_uploader(label="Upload your CSV file", type="csv")

if uploaded_file is not None:
    data = api_client.upload_and_process_csv(uploaded_file)
    if data:
        # Convert to DataFrame
        df = pd.DataFrame(data['sample_data'])

        st.write("df processed successfully!")
        st.write("Received df structure:", df)
        
        # Basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sales", f"€{df['revenue'].sum():.2f}")  # Using revenue instead of price
        with col2:
            st.metric("Total Products Sold", f"{df['quantity'].sum()}")
        with col3:
            st.metric("Average Order Value", f"€{df['revenue'].mean():.2f}")  # Using revenue

        # Calculate profit distribution (using total_profit that's already calculated)
        total_profit = df.groupby('product_id').agg({
            'total_profit': 'sum',
        }).sort_values(by='total_profit', ascending=False)
    
        # For most/least profitable
        most_profitable_id = total_profit.index[0]
        most_profitable_value = total_profit['total_profit'].iloc[0]
        least_profitable_id = total_profit.index[-1]
        least_profitable_value = total_profit['total_profit'].iloc[-1]

        # Calculate percentages
        total_profits_sum = total_profit['total_profit'].sum()
        profit_percents = (total_profit['total_profit'] / total_profits_sum * 100).round(1)

        # Create visualization
        fig = px.bar(
            x=profit_percents.index,
            y=profit_percents.values,
            labels={
                'x': 'Product ID',
                'y': 'Profit Contribution (%)'
            },
            title="Product Profit Distribution"
        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "Product: %{x}",
                "Contribution: %{y}%",
                "Actual Profit: €%{customdata:.2f}",
                "<br><i>Consider both % and actual profit</i>"
            ]),
            customdata=total_profit['total_profit'],
            marker_color='#2980B9',
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            plot_bgcolor='white',
            yaxis=dict(
                gridcolor='#E1E1E1',
                zeroline=True,
                zerolinecolor='#E1E1E1'
            ),
            xaxis=dict(
                gridcolor='#E1E1E1'
            ),
            bargap=0.4,
            height=500,
            margin=dict(t=50, b=50)
        )

        st.plotly_chart(fig)

        # Most/least profitable products metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                f"Most Profitable Product (#{most_profitable_id})", 
                f"€{most_profitable_value:.2f}"
            )
        with col2:
            st.metric(
                f"Least Profitable Product (#{least_profitable_id})",
                f"€{least_profitable_value:.2f}"
            )
