import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load and display the dataset
st.set_page_config(layout="wide")  # Use wide layout for better visualization
df = pd.read_csv("cipla.csv")
print(df.tail(200))
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime format

# Sidebar for analysis selection
st.sidebar.header("Make Your Analysis On")
analysis_section = st.sidebar.radio(
    "Select Analysis Section",
    ["Stock Visualization", "Investment Analysis", "COVID-19 Analysis"]
)

# Limit analysis between 1996 and 2024
min_year, max_year = 1996, 2024

# Sidebar GitHub Link
st.sidebar.markdown("""
### Connect on GitHub
[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-blue?logo=github)](https://github.com/Crow-6-9/Cipla-Stock-Analysis)
""")

# -------------------- STOCK VISUALIZATION --------------------
if analysis_section == "Stock Visualization":
    st.title("Cipla Stock Data Visualization")

    # User input for year range
    start_year = st.sidebar.number_input("Start Year (1996-2024)", min_value=min_year, max_value=max_year - 1, value=min_year)
    end_year = st.sidebar.number_input("End Year (1996-2024)", min_value=start_year + 1, max_value=max_year, value=max_year)

    # Filter data based on the selected range
    start_date = pd.to_datetime(f"{start_year}-01-01")
    end_date = pd.to_datetime(f"{end_year}-12-31")
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Chart selection
    chart_type = st.sidebar.radio("Select Chart Type", ["Bar Chart", "Line Chart"])

    # Display selected chart
    if chart_type == "Bar Chart":
        st.subheader(f"Bar Chart of Stock Volume ({start_year}-{end_year})")
        bar_data = filtered_df[['Date', 'Volume']].set_index('Date').resample('Y').sum()
        fig, ax = plt.subplots()
        ax.bar(bar_data.index.year, bar_data['Volume'], color='skyblue')
        ax.set_xlabel("Year")
        ax.set_ylabel("Volume")
        ax.set_title("Stock Volume Over Years")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.1f}K'))
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader(f"Line Chart of Adjusted Close Prices ({start_year}-{end_year})")
        line_data = filtered_df[['Date', 'Adj_Close']].set_index('Date')
        st.line_chart(line_data)
        st.write("**X-axis:** Date | **Y-axis:** Adjusted Close Price")

# -------------------- INVESTMENT ANALYSIS --------------------
elif analysis_section == "Investment Analysis":
    st.title("Investment Analysis Over the Years")

    # Calculate annual returns
    df['Year'] = df['Date'].dt.year
    investment_data = df.groupby('Year')['Adj_Close'].agg(['first', 'last'])
    investment_data['Return (%)'] = ((investment_data['last'] - investment_data['first']) / investment_data['first']) * 100

    # Last decade filter
    last_decade_data = investment_data.loc[2014:2024]
    avg_return_last_decade = last_decade_data['Return (%)'].mean()

    # Display analysis
    st.subheader("Investment Analysis: Last Decade (2014-2024)")
    st.write(f"""
    **Average Annual Return for Last Decade:** {avg_return_last_decade:.2f}%  
    """)

    # Chart selection
    chart_type = st.sidebar.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"], key="investment_chart")

    if chart_type == "Bar Chart":
        st.subheader("Bar Chart of Annual Returns (%)")
        fig, ax = plt.subplots()
        ax.bar(last_decade_data.index, last_decade_data['Return (%)'], color='skyblue')
        ax.set_xlabel("Year")
        ax.set_ylabel("Return (%)")
        ax.set_title("Annual Returns (%) for Last Decade")
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader("Line Chart of Annual Returns (%)")
        fig, ax = plt.subplots()
        ax.plot(last_decade_data.index, last_decade_data['Return (%)'], marker='o', color='green')
        ax.set_xlabel("Year")
        ax.set_ylabel("Return (%)")
        ax.set_title("Annual Returns (%) for Last Decade")
        st.pyplot(fig)

    elif chart_type == "Pie Chart":
        st.subheader("Pie Chart of Positive Annual Returns (Last Decade)")
        positive_returns = last_decade_data[last_decade_data['Return (%)'] > 0]
        pie_data = positive_returns['Return (%)']
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=positive_returns.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# -------------------- COVID-19 ANALYSIS --------------------
elif analysis_section == "COVID-19 Analysis":
    st.title("COVID-19 Impact on Cipla Stock Prices")
    
    covid_start = pd.to_datetime("2020-03-01")
    covid_end = pd.to_datetime("2021-12-31")

    # Filter data for the relevant period
    covid_data = df[(df['Date'] >= covid_start - pd.DateOffset(months=6)) &
                    (df['Date'] <= covid_end + pd.DateOffset(months=6))]
    pre_covid = covid_data[covid_data['Date'] < covid_start]
    during_covid = covid_data[(covid_data['Date'] >= covid_start) & (covid_data['Date'] <= covid_end)]
    post_covid = covid_data[covid_data['Date'] > covid_end]

    # Chart selection
    chart_type = st.sidebar.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"], key="covid_chart")

    if chart_type == "Bar Chart":
        st.subheader("Bar Chart: COVID-19 Impact")
        fig, ax = plt.subplots()
        ax.bar(['Pre-COVID', 'During COVID', 'Post-COVID'], 
               [pre_covid['Adj_Close'].mean(), during_covid['Adj_Close'].mean(), post_covid['Adj_Close'].mean()], 
               color=['blue', 'red', 'green'])
        ax.set_ylabel("Average Adjusted Close Price")
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader("Line Chart: COVID-19 Impact")
        fig, ax = plt.subplots()
        ax.plot(pre_covid['Date'], pre_covid['Adj_Close'], label="Pre-COVID", color="blue", linestyle='--')
        ax.plot(during_covid['Date'], during_covid['Adj_Close'], label="During COVID", color="red")
        ax.plot(post_covid['Date'], post_covid['Adj_Close'], label="Post-COVID", color="green")
        ax.set_xlabel("Date")
        ax.set_ylabel("Adjusted Close Price")
        ax.legend()
        st.pyplot(fig)

    elif chart_type == "Pie Chart":
        st.subheader("Pie Chart: COVID-19 Period Distribution")
        periods = ['Pre-COVID', 'During COVID', 'Post-COVID']
        avg_prices = [
            pre_covid['Adj_Close'].mean(), 
            during_covid['Adj_Close'].mean(), 
            post_covid['Adj_Close'].mean()
        ]
        fig, ax = plt.subplots()
        ax.pie(avg_prices, labels=periods, autopct='%1.1f%%', startangle=90, colors=['blue', 'red', 'green'])
        ax.axis('equal')
        st.pyplot(fig)

    # Analysis statement
    st.write("""
    **Analysis:**
    - **Pre-COVID:** Moderate growth or stability.
    - **During COVID:** Significant stock price increase due to demand for healthcare products.
    - **Post-COVID:** Continued growth or stabilization at a higher level.
    """)
#AMit Khunmbahr
