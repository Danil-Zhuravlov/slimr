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

        df = pd.DataFrame(data['sample_data'])

        st.write("df processed successfully!")
        st.write("Received df structure:", df)
        
        #basic table structure on streamlit
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

        # calculate profit from all products
        total_profits_sum = total_profit['profit'].sum()


        # calculate profit distribution in % = (product_profit / total profit from all products) * 100%
        total_profit_percents = (total_profit['profit'] / total_profits_sum) * 100
        rounded_percents = total_profit_percents.round(1)

        # Create visualization
        fig = px.bar(
            x=rounded_percents.index, # product_id
            y=rounded_percents.values,
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
            customdata=total_profit['profit'] # total profit per product_id
        )

        # Update the chart layout
        fig.update_layout(
            # Clean, professional look
            plot_bgcolor='white',
            yaxis=dict(
                gridcolor='#E1E1E1',
                zeroline=True,
                zerolinecolor='#E1E1E1'
            ),
            xaxis=dict(
                gridcolor='#E1E1E1'
            ),
            # Spacing and style
            bargap=0.4,
            height=500,
            margin=dict(t=50, b=50)
        )

        # Update bars
        fig.update_traces(
            marker_color='#2980B9',
            texttemplate='%{y:.1f}%',  # Show percentage on bars
            textposition='outside'      # Place text above bars
        )

        st.plotly_chart(fig)


        # create two columns with metrics of most/least profitable products
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
