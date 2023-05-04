import pandas as pd
import streamlit as st
from os.path import dirname, abspath, join
import sys
import datetime
from PIL import Image

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

# Title
st.title('Monthly Spending Tracker')

# Load data
df = pd.read_sql_table('transactions', 'sqlite:///../instance/test.db')

today = datetime.date.today()
current_month = today.month
current_year = today.year
st.caption(today.strftime('%B %d, %Y'))

this_month_tab, all_tab, trends_tab = st.tabs(
    ['This month', 'All Transactions', 'Trends'])


with this_month_tab:
    image_column, data_column = st.columns(2)

    with image_column:
        image = Image.open('money_robot.png')
        st.image(image)
    with data_column:
        # Filter df to only include transactions from this month
        spending_this_month = df[df['date'].str.startswith(
            today.strftime('%Y-%m'))]['amount'].sum()
        st.header("Total Spending This Month")
        st.header(f"${spending_this_month}")

with all_tab:
    st.header('All Transactions')
    all_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', "December"]
    selected_month = st.selectbox(label='Month',
                                  options=range(0, 12),
                                  format_func=lambda number: all_months[number],
                                  index=current_month-1)
    st.dataframe(
        df[df['date'].str.startswith(
            f'{current_year}-{selected_month+1:02}')][['amount', 'date', 'description']],
        use_container_width=True)

with trends_tab:
    st.header('Transactions by Month')
    grouped_by_monthyear = df.groupby(
        df['date'].str.slice(0, 7))['amount'].sum()
    st.bar_chart(grouped_by_monthyear)
