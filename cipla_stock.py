import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load and display the dataset
st.set_page_config(layout="wide")  # Use wide layout for better visualization
df = pd.read_csv("cipla.csv")
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime format

# Custom color schemes for charts
color_palette = plt.cm.tab10.colors  # Use a vibrant color palette

# Add introductory section
st.markdown(
    """
    <div style="background-color:#1abc9c;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Cipla Stock Analysis</h1>
    </div>
    <p style="font-size:18px;">
        Welcome to the Cipla Stock Analysis dashboard! This app provides comprehensive insights into the historical performance of Cipla's stock. 
        Here’s what you can explore:
    </p>
    <ul style="font-size:16px;">
        <li>Stock Visualization: Analyze trading volumes and adjusted closing prices over custom date ranges.</li>
        <li>Investment Analysis: Evaluate annual returns and identify periods of growth and profitability.</li>
        <li>COVID-19 Impact: Understand how external factors influenced Cipla's stock performance.</li>
    </ul>
    <p style="font-size:18px;">
        Dive into the data and uncover key trends that showcase Cipla's consistent growth and market reliability.
    </p>
    """, 
    unsafe_allow_html=True
)

# Sidebar for analysis selection
st.sidebar.header("Make Your Analysis On")
analysis_section = st.sidebar.radio(
    "Select Analysis Section",
    ["Stock Visualization", "Investment Analysis", "COVID-19 Analysis"]
)

# Limit analysis between 1996 and 2024
min_year, max_year = 1996, 2024

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

    # Display the last 100 values first
    st.subheader("Last 100 Values from the Dataset")
    st.dataframe(df.tail(100), height=400)  # Scrollable table for better visibility

    # Chart selection
    chart_type = st.sidebar.radio("Select Chart Type", ["Bar Chart", "Line Chart"])

    # Display selected chart
    if chart_type == "Bar Chart":
        st.subheader(f"Bar Chart of Stock Volume ({start_year}-{end_year})")
        bar_data = filtered_df[['Date', 'Volume']].set_index('Date').resample('Y').sum()
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
        ax.bar(bar_data.index.year, bar_data['Volume'], color=color_palette[2])
        ax.set_xlabel("Year")
        ax.set_ylabel("Volume")
        ax.set_title("Stock Volume Over Years")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.1f}K'))
        ax.tick_params(axis='x', rotation=45)  # Rotate year labels to avoid collision
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader(f"Line Chart of Adjusted Close Prices ({start_year}-{end_year})")
        line_data = filtered_df[['Date', 'Adj_Close']].set_index('Date')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(line_data.index, line_data['Adj_Close'], color=color_palette[4], linewidth=2)
        ax.set_title("Adjusted Close Prices Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Adjusted Close Price")
        st.pyplot(fig)



# -------------------- INVESTMENT ANALYSIS --------------------
elif analysis_section == "Investment Analysis":
    st.title("Investment Analysis Over the Years")

    # Calculate annual returns
    df['Year'] = df['Date'].dt.year
    investment_data = df.groupby('Year')['Adj_Close'].agg(['first', 'last'])
    investment_data['Return (%)'] = ((investment_data['last'] - investment_data['first']) / investment_data['first']) * 100

    # Calculate total and average returns for the entire dataset
    total_return = ((df['Adj_Close'].iloc[-1] - df['Adj_Close'].iloc[0]) / df['Adj_Close'].iloc[0]) * 100
    avg_annual_return = investment_data['Return (%)'].mean()

    st.markdown(
        f"""
        <div style="background-color:#1abc9c;padding:10px;border-radius:10px;">
            <h3 style="color:white;text-align:center;">Investor Insights</h3>
            <p style="color:white;font-size:18px;text-align:center;">
                If an investor had invested in Cipla stock from the start of the dataset to the most recent date:
            </p>
            <ul style="color:white;font-size:16px;">
                <li><b>Total Return:</b> {total_return:.2f}%</li>
                <li><b>Average Annual Return:</b> {avg_annual_return:.2f}%</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Last decade filter
    last_decade_data = investment_data.loc[2014:2024]

    # Chart type selection
    chart_type = st.sidebar.radio("Select Chart Type for Investment Analysis", ["Pie Chart", "Line Chart"])

    if chart_type == "Pie Chart":
        st.subheader("Pie Chart of Positive Annual Returns (Last Decade)")
        positive_returns = last_decade_data[last_decade_data['Return (%)'] > 0]
        pie_data = positive_returns['Return (%)']
        fig, ax = plt.subplots(figsize=(6, 6))  # Fixed smaller figure size
        wedges, texts, autotexts = ax.pie(
            pie_data,
            labels=positive_returns.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=color_palette
        )
        for text in texts:
            text.set_fontsize(10)  # Adjust label font size
        for autotext in autotexts:
            autotext.set_fontsize(10)
        ax.axis('equal')
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader("Line Chart of Annual Returns (Last Decade)")
        fig, ax = plt.subplots(figsize=(8, 5))  # Balanced figure size
        ax.plot(last_decade_data.index, last_decade_data['Return (%)'], color=color_palette[2], marker='o')
        ax.set_title("Annual Returns Over the Last Decade")
        ax.set_xlabel("Year")
        ax.set_ylabel("Return (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)








# -------------------- PIE CHART LABEL FIX --------------------
elif analysis_section == "Investment Analysis":
    st.title("Investment Analysis Over the Years")

    # Calculate annual returns
    df['Year'] = df['Date'].dt.year
    investment_data = df.groupby('Year')['Adj_Close'].agg(['first', 'last'])
    investment_data['Return (%)'] = ((investment_data['last'] - investment_data['first']) / investment_data['first']) * 100

    # Last decade filter
    last_decade_data = investment_data.loc[2014:2024]

    # Chart type selection
    chart_type = st.sidebar.radio("Select Chart Type for Investment Analysis", ["Pie Chart", "Line Chart"])

    if chart_type == "Pie Chart":
        st.subheader("Pie Chart of Positive Annual Returns (Last Decade)")
        positive_returns = last_decade_data[last_decade_data['Return (%)'] > 0]
        pie_data = positive_returns['Return (%)']
        fig, ax = plt.subplots(figsize=(6, 6))  # Fixed smaller figure size
        wedges, texts, autotexts = ax.pie(
            pie_data,
            labels=positive_returns.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=color_palette
        )
        for text in texts:
            text.set_fontsize(10)  # Adjust label font size
        for autotext in autotexts:
            autotext.set_fontsize(10)
        ax.axis('equal')
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader("Line Chart of Annual Returns (Last Decade)")
        fig, ax = plt.subplots(figsize=(8, 5))  # Balanced figure size
        ax.plot(last_decade_data.index, last_decade_data['Return (%)'], color=color_palette[2], marker='o')
        ax.set_title("Annual Returns Over the Last Decade")
        ax.set_xlabel("Year")
        ax.set_ylabel("Return (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)


#---------------------------- Covid analysis -----------------------#

elif analysis_section == "COVID-19 Analysis":
    st.title("Impact of COVID-19 on Cipla Stock Performance")

    # Define the COVID-19 period
    covid_start = pd.to_datetime("2020-03-01")
    covid_end = pd.to_datetime("2021-12-31")

    # Filter data for the COVID-19 period
    covid_data = df[(df['Date'] >= covid_start) & (df['Date'] <= covid_end)]
    pre_covid_data = df[(df['Date'] < covid_start)]
    post_covid_data = df[(df['Date'] > covid_end)]

    # Chart type selection
    chart_type = st.sidebar.radio("Select Chart Type for COVID-19 Analysis", ["Bar Chart", "Line Chart"])

    if chart_type == "Bar Chart":
        st.subheader("Stock Performance During COVID-19")
        covid_avg = covid_data['Adj_Close'].mean()
        pre_covid_avg = pre_covid_data['Adj_Close'].mean()
        post_covid_avg = post_covid_data['Adj_Close'].mean()

        # Bar chart for average prices
        comparison_data = {
            "Period": ["Pre-COVID-19", "COVID-19", "Post-COVID-19"],
            "Avg Price": [pre_covid_avg, covid_avg, post_covid_avg]
        }
        comparison_df = pd.DataFrame(comparison_data)
        fig, ax = plt.subplots(figsize=(8, 5))  # Balanced figure size
        ax.bar(comparison_df["Period"], comparison_df["Avg Price"], color=color_palette[:3])
        ax.set_title("Average Adjusted Close Prices During COVID-19")
        ax.set_ylabel("Average Adjusted Close Price")
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.subheader("Adjusted Close Prices During COVID-19")
        fig, ax = plt.subplots(figsize=(10, 5))  # Balanced figure size
        ax.plot(covid_data['Date'], covid_data['Adj_Close'], color=color_palette[1], marker='o', label="COVID-19 Period")
        ax.axvspan(covid_start, covid_end, color='lightgrey', alpha=0.3, label="COVID-19 Period Highlight")
        ax.set_title("Adjusted Close Prices During COVID-19")
        ax.set_xlabel("Date")
        ax.set_ylabel("Adjusted Close Price")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)

    # Insights
    st.markdown(
        """
        **Key Insights:**
        - Cipla's stock showed resilience and growth during the COVID-19 period, reflecting its pivotal role in addressing healthcare needs.
        - Post-COVID-19, the stock stabilized, maintaining a higher average price than the pre-COVID period.
        - The increase in adjusted close prices during COVID-19 indicates strong investor confidence in Cipla's ability to capitalize on the healthcare demand surge.
        """
    )





# -------------------- CONCLUDING ANALYSIS --------------------
st.markdown(
    """
    <div style="background-color:#f4d03f;padding:10px;border-radius:10px">
        <h2 style="color:black;">Concluding Analysis for Cipla Stock</h2>
        <ul style="font-size:16px; color:black ">
            <li><b>Steady Growth Over the Years:</b> Cipla has demonstrated consistent growth in its stock value, with notable peaks during periods of increased demand for healthcare and pharmaceutical products.</li>
            <li><b>Impact of External Factors:</b> The COVID-19 pandemic significantly boosted Cipla's stock performance, reflecting its critical role in addressing healthcare challenges during the crisis.</li>
            <li><b>Last Decade Performance:</b> Over the last decade (2014–2024), Cipla's stock has provided an average annual return of 28.98%, showcasing its reliability as an investment choice.</li>
            <li><b>Investor Returns:</b> Positive returns for investors indicate that Cipla has remained a stable and profitable investment, particularly during high-demand periods for the pharmaceutical industry.</li>
            <li><b>Market Trends:</b> The analysis of trading volumes shows high investor confidence during critical periods, indicating strong market sentiment towards Cipla's business strategies and growth potential.</li>
        </ul>
    </div>
    """, 
    unsafe_allow_html=True
)
