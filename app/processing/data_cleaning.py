import pandas as pd
from datetime import datetime

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess sales data
    Args:
        df: Raw sales DataFrame
    Returns:
        Cleaned DataFrame
    """

    # CLEANING STEPS
    df = df.copy()  # Create a copy to avoid modifying original data
    df = df.dropna()  # We won't use missing data for now
    df = df.drop_duplicates()
    df = df.loc[df['price'] > df['cost']] # price shouldn't be less than cost
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['quantity'] > 0]  # you can't sell zero, and negative quantity

    # FEATURE ENGINEERING

    # basic features
    df['profit'] = df['price'] - df['cost']
    df['revenue'] = df['price'] * df['quantity']
    df['total_profit'] = df['profit'] * df['quantity']

    # time-based fields to better understand sales nature
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']) # boolean

    return df
