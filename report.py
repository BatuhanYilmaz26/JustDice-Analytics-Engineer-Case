import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit_lottie as st_lottie
import requests

st.set_page_config(page_title="JustDice Financial Analysis", page_icon="📈", layout="wide")

# Define a function that we can use to load lottie files from a link.
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_49rdyysj.json")

col_lottie, col_title = st.columns([1, 3])

with col_lottie:
    st_lottie.st_lottie(lottie, width=200, height=200)

with col_title:
    st.title("JustDice Financial Analysis")
    st.markdown("""
    - The report uses data collected over the course of the year 2022 to analyze various aspects of the company's operations, including daily ad spend, daily installs, total installs by country, total installs by app, daily payouts, and daily revenue.
    - By analyzing this data, we aim to identify trends, patterns, and potential areas for improvement that can inform strategic decision-making and guide future investments and promotions.
    - The report includes several interactive charts and graphs to illustrate key findings and provide a visual representation of the data.
    - Overall, this report provides insights into JustDice's financial performance and can be used to inform future business decisions.
    """)

# INVESTIGATE ADS SPEND DATA
ads = pd.read_csv("adspend.csv")
ads['event_date'] = pd.to_datetime(ads['event_date'], format='%Y-%m-%d')
# Round value_usd to 2 decimal places
ads['value_usd'] = ads['value_usd'].round(2)

# Calculate sum of ads value_usd by date
ads_by_date = ads.groupby('event_date')['value_usd'].sum()
# Name  columns as event_date and daily ads spend
ads_by_date = ads_by_date.reset_index()
ads_by_date.columns = ['event_date', 'daily_ads_spend']
# Round daily_ads_spend to 2 decimal places
ads_by_date['daily_ads_spend'] = ads_by_date['daily_ads_spend'].round(2)

# Calculate total daily_ads_spend
total_ads_spend = ads_by_date['daily_ads_spend'].sum()

# min and max daily ads spend
min_ads_spend = ads_by_date['daily_ads_spend'].min()
max_ads_spend = ads_by_date['daily_ads_spend'].max()

col1, col2 = st.columns(2)
with col1:
    fig_ads = px.line(ads_by_date, x='event_date', y='daily_ads_spend', title='Daily Ads Spend', labels={'event_date':'Date', 'daily_ads_spend':'Daily Ads Spend ($)'})
    fig_ads.add_annotation(x=ads_by_date['event_date'].max(), y=ads_by_date['daily_ads_spend'].max(), text=f"Total Ads Spend: ${total_ads_spend:,.2f}", showarrow=False)
    fig_ads.update_layout(annotations=[dict(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', showarrow=False, font=dict(size=14, color='black', family='Arial'))])
    st.plotly_chart(fig_ads)

    st.markdown("""
    - The chart shows daily ads spend data for the year 2022.
    - There are clear fluctuations in ads spend throughout the year, with some months having higher ads spend compared to others.
    - The highest ads spend occurs in November, followed by August, January.
    - The lowest ads spend occurs in March, followed by April, June and October.
    - The dip in ads spend in mid-March and mid-April could be related to a seasonal slowdown or a change in marketing strategy.
    - The downward trend in ads spend after the peak in mid-November, along with the fluctuations observed during this time, suggest that there may have been changes in marketing goals or campaigns that impacted ads spend and resulted in a decrease in spending over time.
    - Identifying external factors that may influence ads spend and app usage, such as events, seasonality, or industry trends, can help explain fluctuations in the data and inform future marketing efforts.
    """)

    
# INVESTIGATE INSTALLS DATA
installs = pd.read_csv("installs.csv")
installs['event_date'] = pd.to_datetime(installs['event_date'], format='%Y-%m-%d')

# Calculate sum of installs by date
installs_by_date = installs.groupby('event_date').size().reset_index(name='daily_installs')

# Make sure the event_date column is a date
installs_by_date['event_date'] = pd.to_datetime(installs_by_date['event_date'])

total_installs = installs_by_date['daily_installs'].sum()

# Min and max installs
min_installs = installs_by_date['daily_installs'].min()
max_installs = installs_by_date['daily_installs'].max()

with col2:
    fig_installs = px.line(installs_by_date, x='event_date', y='daily_installs', title='Daily Installs', labels={'event_date':'Date', 'daily_installs':'Daily Installs'})
    fig_installs.add_annotation(x=installs_by_date['event_date'].max(), y=installs_by_date['daily_installs'].max(), text=f"Total Installs: {total_installs:,.0f}", showarrow=False)
    fig_installs.update_layout(annotations=[dict(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', showarrow=False, font=dict(size=14, color='black', family='Arial'))])
    st.plotly_chart(fig_installs)

    st.markdown("""
    - The line chart shows the daily installs of our apps or our partner companies apps over the course of the year 2022, with fluctuations from month to month.
    - There were dips in daily installs in January, March and April, followed by an increase in late May and then a more consistent upward trend from June to August, reaching a peak of around 1400 daily installs in mid-November.
    - After August, there was a fluctuation and downward trend in daily installs for the remaining months of the year, reaching around 500 daily installs by December.
    - These fluctuations in daily installs suggest that there may have been external factors at play, such as changes in consumer behavior or shifts in the competitive landscape.
    - Further investigation into the factors driving the increase in daily installs from June to August could provide valuable insights into effective marketing campaigns or other factors that could be replicated in the future.
    - Exploring the reasons for the subsequent decline in daily installs could help identify potential areas for improvement.
    - The chart highlights the importance of monitoring daily installs over time and identifying trends and patterns that can inform strategic decision-making.
    - It may be valuable to analyze the daily installs in comparison to competitors, to gain a better understanding of the product's position in the market.
    """)


# Calculate sum of installs by date and country_id
installs_by_date_country = installs.groupby(['event_date', 'country_id']).size().reset_index(name='daily_installs')

# Make sure the event_date column is a date
installs_by_date_country['event_date'] = pd.to_datetime(installs_by_date_country['event_date'])

# Calculate sum of daily_install for each country_id and sort by descending order
installs_by_country = installs_by_date_country.groupby('country_id')['daily_installs'].sum().reset_index()
# Change daily_installs column name to total_installs
installs_by_country.columns = ['country_id', 'total_installs']

# Calculate sum of installs by date and app_id
installs_by_app = installs.groupby(['event_date', 'app_id']).size().reset_index(name='daily_installs')

# Make sure the event_date column is a date
installs_by_app['event_date'] = pd.to_datetime(installs_by_app['event_date'], format='%Y-%m-%d')

# Calculate sum of daily_install for each country_id and sort by descending order
total_installs_by_app = installs_by_app.groupby('app_id')['daily_installs'].sum().reset_index().sort_values('daily_installs', ascending=False)
# Change daily_installs column name to total_installs
total_installs_by_app.columns = ['app_id', 'total_installs']


col3, col4 = st.columns(2)
with col3:
    # Visualize total installs by country in a pie chart
    fig_installs_by_country = px.pie(installs_by_country, values='total_installs', names='country_id', title='Total Installs by Country')
    st.plotly_chart(fig_installs_by_country)

    st.markdown("""
    - The chart displays the percentage of total installs by country_id, with four different country_ids represented.
    - The chart shows that country_id=1 has a significantly higher percentage of total installs compared to the other countries, with over 60% of all installs coming from this country.
    - The second most popular country for installs is country_id=109, with just over 28% of all installs.
    - Country_id=17 and country_id=213 have much smaller percentages of total installs, at 4.92% and 4.12%, respectively.
    - Based on this data, it appears that country_id=1 is the most popular country for installs and could be a target for future marketing and growth efforts.
    - Additionally, there could be potential for growth in countries with smaller percentages of total installs, such as country_id=17 and country_id=213.
    - It could be useful to investigate why country_id=1 is the most popular country for installs and whether there are specific factors contributing to this trend.
    - Further analysis could involve comparing these results to data from previous time periods or from similar products or services to determine if there are any significant changes or trends over time or across different products or services.
    """)

with col4:
    # Visualize total installs by app in a pie chart
    fig_installs_by_app = px.pie(total_installs_by_app, values='total_installs', names='app_id', title='Total Installs by App')
    st.plotly_chart(fig_installs_by_app)

    st.markdown("""
    - The pie chart displays the percentage of app installs for different apps
    - The top 5 app installs by app ID are app ID 174 with 21.9%, app ID 121 with 18.4%, app ID 94 with 14.9%, app ID 189 with 4.65%, and app ID 71 with 3.83%.
    - The data suggests that there are a few apps that are particularly popular among users. These apps may be worth investing in further or promoting more heavily.
    - It's important to note that there are many other app IDs with smaller percentages of installs, indicating that there may be opportunities for growth and improvement among these apps as well.
    - We should consider factors such as the type of app and the target audience when analyzing the data. For example, certain apps may be more popular among younger or older users, or may be more popular in certain geographic regions.
    - Overall, the data from the chart can help inform our decision-making processes and guide our investments and promotions in different apps.
    """)

# INVESTIGATE PAYOUTS DATA
payouts = pd.read_csv('payouts.csv')
payouts['event_date'] = pd.to_datetime(payouts['event_date'], format='%Y-%m-%d')

# Calculate sum of payouts value_usd by date
payouts_by_date = payouts.groupby('event_date')['value_usd'].sum().reset_index()
# Name  columns as event_date and daily ads spend
payouts_by_date.columns = ['event_date', 'daily_payouts']
# Round daily_payouts to 2 decimal places
payouts_by_date['daily_payouts'] = payouts_by_date['daily_payouts'].round(2)

# Calculate total payouts
total_payouts = payouts_by_date['daily_payouts'].sum()

# Calculate min, max, and average daily payouts
min_daily_payouts = payouts_by_date['daily_payouts'].min()
max_daily_payouts = payouts_by_date['daily_payouts'].max()
avg_daily_payouts = payouts_by_date['daily_payouts'].mean()

col5, col6 = st.columns(2)
with col5:
    # Visualize daily payouts by date in a line chart
    fig_payouts = px.line(payouts_by_date, x='event_date', y='daily_payouts', title='Daily Payouts', labels={'event_date':'Date', 'daily_payouts':'Daily Payouts ($)'})
    # Add annotations to the chart to show total payouts and average daily payouts 
    fig_payouts.add_annotation(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', showarrow=False, text=f"Total Payouts: ${total_payouts:,.2f}", font=dict(size=14, color='black', family='Arial'))
    fig_payouts.add_annotation(x=0.9, y=1, xref='paper', yref='paper', xanchor='right', yanchor='bottom', showarrow=False, text=f"Average Daily Payouts: ${avg_daily_payouts:,.2f}", font=dict(size=14, color='black', family='Arial'))
    st.plotly_chart(fig_payouts)

    st.markdown("""
    - The chart displays the daily payouts of the company for the year 2022.
    - There is a general upward trend in the daily payout amounts over time, indicating that the number of users installing our apps or our partner companies apps is increasing.
    - However, the fluctuations in the payout amounts over time do not appear to follow a consistent pattern. Rather, they may be due to various factors such as changes in the market, fluctuations in customer behavior or changes in the company's payout policies.
    - There does not appear to be a clear seasonal pattern in the payout amounts over time.
    - The company's payout strategy appears to be successful in attracting new customers and retaining existing ones.
    - It may be useful to conduct further analysis to identify factors driving fluctuations in the payout amounts and to assess the long-term sustainability of the company's payout strategy.
    """)



# INVESTIGATE REVENUE DATA
revenue = pd.read_csv('revenue.csv')
revenue['event_date'] = pd.to_datetime(revenue['event_date'], format='%Y-%m-%d')

#  Calculate sum of revenue value_usd by date
revenue_by_date = revenue.groupby('event_date')['value_usd'].sum().reset_index()
# Name  columns as event_date and daily revenue
revenue_by_date.columns = ['event_date', 'daily_revenue']
# Round daily_revenue to 2 decimal places
revenue_by_date['daily_revenue'] = revenue_by_date['daily_revenue'].round(2)

# Calculate total revenue
total_revenue = revenue_by_date['daily_revenue'].sum()
# Calculate average daily revenue
avg_daily_revenue = revenue_by_date['daily_revenue'].mean()



with col6:
    # Visualize daily revenue by date in a line chart
    fig_revenue = px.line(revenue_by_date, x='event_date', y='daily_revenue', title='Daily Revenue', labels={'event_date':'Date', 'daily_revenue':'Daily Revenue ($)'})
    # Add average daily revenue annotation to top right of chart
    fig_revenue.add_annotation(x=1, y=1, xref='paper', yref='paper', xanchor='right', yanchor='bottom', text=f"Average Daily Revenue: ${avg_daily_revenue:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    # Add total revenue annotation to top left of chart
    fig_revenue.add_annotation(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', text=f"Total Revenue: ${total_revenue:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    st.plotly_chart(fig_revenue)

    st.markdown("""
    - The chart displays the daily revenue of the company for the year 2022.
    - The daily revenue ranges between \\$387.22 and \\$2,973.45, with an average of $1,147.52 per day.
    - The chart shows that the company's daily revenue is fairly consistent throughout the year, but there are notable exceptions.
    - The daily revenue dips significantly below the average in mid-April, early June, mid-October and late December.
    - The daily revenue spikes above the average in late February, late May, late July, mid-November.
    - Towards the end of the year, there appears to be a general trend of decreasing daily revenue, with the lowest revenue occurring in late December.
    - The wide range of daily revenue suggests that there may be a high degree of variability in the factors that influence revenue from day to day.
    - We may want to investigate the factors that are driving the days with the highest and lowest revenue in order to better understand what is contributing to the variability.
    - It may be useful to compare this year's revenue to previous years in order to see if there are any significant changes or trends over time.
    - We may also want to investigate any external factors that may have influenced the revenue, such as changes in the industry or economy, major events or announcements, etc.
    """)

# Create a dataframe with total ads spend, total payouts, and total revenue
total = pd.DataFrame({'total_ads_spend': [total_ads_spend], 'total_payouts': [total_payouts], 'total_revenue': [total_revenue]})


col7, col8 = st.columns(2)

with col7:
    # Visualize total ads spend, total payouts, and total revenue in a bar chart.
    fig_total = go.Figure(data=[
        go.Bar(name='Total Revenue', x=['Revenue'], y=[total_revenue], marker_color='#4d79ff'),
        go.Bar(name='Total Payouts', x=['Payouts'], y=[total_payouts],  marker_color='#ff4d4d'),
        go.Bar(name='Total Ads Spend', x=['Ads Spend'], y=[total_ads_spend], marker_color='#ffbb33')
    ])
    # Add text in the middle of each bar to show the value of each metric in USD, font size 14, and font family Arial
    fig_total.add_annotation(x='Revenue', y=total_revenue, text=f"${total_revenue:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    fig_total.add_annotation(x='Payouts', y=total_payouts, text=f"${total_payouts:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    fig_total.add_annotation(x='Ads Spend', y=total_ads_spend, text=f"${total_ads_spend:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    fig_total.update_layout(yaxis_title='USD ($)')
    fig_total.update_layout(title_text='Total Revenue, Payouts and Ads Spend')
    st.plotly_chart(fig_total)

    st.markdown("""
    - The chart displays a bar graph with three bars representing the total revenue, total ads spend, and total payouts for our company.
    - The total revenue for our company is \\$418,845.29, which is the highest value among the three bars. This indicates that our company generates more revenue than it spends on advertising or payouts.
    - The total ads spend for our company is \\$254,075.99, which is significantly higher than the total payouts of $62,320.97. This suggests that we are investing heavily in advertising in order to generate revenue.
    - The profit margin for our company can be calculated by subtracting the total ads spend and payouts from the total revenue. In this case, our profit margin is $102,448.33, representing approximately 24.46% of our total revenue.
    - Based on this information, it may be beneficial to analyze our advertising strategies and campaigns to identify areas for optimization or cost reduction, without significantly impacting revenue.
    - Additionally, comparing the profit margin of the company to industry standards or competitors may provide insights into areas for improvement.
    """)

with col8:
    # Calculate total profit
    total_profit = total_revenue - total_payouts - total_ads_spend
    # Calculate average profit for each install.
    avg_profit = total_profit / total_installs
    # Add total profit to the total dataframe
    total['total_profit'] = total_profit
    # Visualize total revenue, total payouts, total ads spend, and total profit in a pie chart with a hole in the middle.
    # Gather all values of total dataframe in a new dataframe in 1 column.
    total_values = total.melt(value_vars=['total_ads_spend', 'total_payouts', 'total_revenue', 'total_profit'], value_name='value')
    
    # Calculate profit margin.
    profit_margin = (total_profit / total_revenue) * 100
    # Visualize total values in a pie chart with a hole in the middle.
    fig_total_values = px.pie(total_values, values='value', names='variable', hole=.3, title='Total Revenue, Payouts, Ads Spend and Profit')
    fig_total_values.update_traces(textposition='inside', textinfo='percent+label')
    # Change colors of each metric in the pie chart.
    fig_total_values.update_traces(marker=dict(colors=['#ffbb33', '#ff4d4d', '#4d79ff', '#00cc96']))
    # Add annotation to show total profit on top left corner.
    fig_total_values.add_annotation(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', text=f"Total Profit: ${total_profit:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    # Add annotation to show average profit on top right corner.
    fig_total_values.add_annotation(x=1, y=1, xref='paper', yref='paper', xanchor='right', yanchor='bottom', text=f"Average Profit Per Install: ${avg_profit:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    # Add annotation to show profit margin on bottom left corner.
    fig_total_values.add_annotation(x=0, y=0, xref='paper', yref='paper', xanchor='left', yanchor='top', text=f"Profit Margin: {profit_margin:.2f}%", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    st.plotly_chart(fig_total_values)



    st.markdown("""
    - The pie chart displays the financial performance of our company for a given time period.
    - Our company had a total revenue of \\$418,845.29 during this period, and a total profit of $102,448.33.
    - The chart shows that our company spent $254,075.99 on ads during this period, which represents a significant portion of our expenses.
    - The chart indicates that our company's total payouts were $62,320.97, which suggests that we have a relatively low level of expenses compared to revenue.
    - Based on these figures, it appears that our company has a healthy financial position, with a decent amount of profit despite significant ads spend.
    - To further improve our financial performance, we may want to consider reducing our ads spend or exploring more cost-effective advertising strategies.
    - Additionally, we could consider investing in areas that have shown potential for revenue growth, such as expanding our product offerings or increasing our customer base.
    """)


col9, col10 = st.columns(2)
with col9:
    # Visualize daily revenue, daily payouts, and daily ads_spend as a line chart using plotly express
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=revenue_by_date['event_date'], y=revenue_by_date['daily_revenue'], mode='lines', name='Daily Revenue', marker_color='#4d79ff'))
    fig_daily.add_trace(go.Scatter(x=payouts_by_date['event_date'], y=payouts_by_date['daily_payouts'], mode='lines', name='Daily Payouts',  marker_color='#ff4d4d'))
    fig_daily.add_trace(go.Scatter(x=ads_by_date['event_date'], y=ads_by_date['daily_ads_spend'], mode='lines', name='Daily Ads Spend', marker_color='#ffbb33'))
    fig_daily.update_layout(title='Daily Revenue, Payouts and Ads Spend', yaxis_title='USD ($)',  xaxis_title='Date', showlegend=True)
    st.plotly_chart(fig_daily)

    st.markdown("""
    - Based on the trends in the chart, we can see that our daily revenue and daily ads spend follow a similar trend, which indicates that advertising is likely a significant driver of revenue for our company. We can focus on optimizing our advertising strategy to maximize the return on our ads spend by analyzing the performance of different ad channels, testing different ad creatives, or targeting different audience segments.
    - The decrease in revenue and ads spend after day 40 may indicate a shift in market conditions or a change in consumer behavior. We can conduct market research to better understand our target audience and identify any changes in their preferences or needs.
    - The consistent daily payouts suggest that we have regular expenses or payouts that need to be made. We can review our expenses and identify areas where we can reduce costs to improve profitability.
    - By regularly analyzing and monitoring these variables, we can make data-driven decisions about our business strategy and marketing efforts, ultimately leading to increased profitability and growth.
    """)

with col10:
    # Calculate daily profit by date and add it to the revenue_by_date dataframe as a new column called daily_profit.
    revenue_by_date['daily_profit'] = revenue_by_date['daily_revenue'] - payouts_by_date['daily_payouts'] - ads_by_date['daily_ads_spend']
    # Calculate total profit.
    total_profit = revenue_by_date['daily_profit'].sum()
    # Calculate average daily profit.
    avg_profit = revenue_by_date['daily_profit'].mean()
    # Visualize daily profit as a line chart using plotly express
    fig_daily_profit = px.line(revenue_by_date, x='event_date', y='daily_profit', title='Daily Profit', color_discrete_sequence=['#00cc96'], labels={'event_date': 'Date', 'daily_profit': 'USD ($)'})
    # Add annotation to show total profit on top left corner.
    fig_daily_profit.add_annotation(x=0, y=1, xref='paper', yref='paper', xanchor='left', yanchor='bottom', text=f"Total Profit: ${total_profit:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    # Add annotation to show average daily profit on top right corner.
    fig_daily_profit.add_annotation(x=1, y=1, xref='paper', yref='paper', xanchor='right', yanchor='bottom', text=f"Average Daily Profit: ${avg_profit:,.2f}", showarrow=False, font=dict(size=14, color='black', family='Arial'))
    fig_daily_profit.add_hline(y=0)
    st.plotly_chart(fig_daily_profit)

    st.markdown("""
    - The chart shows an initial upward trend in profit, followed by a sharp decline and continued fluctuations at a lower level.
    - The reasons behind the initial upward trend may include successful marketing campaigns, new product launches, or other factors that contributed to increased sales.
    - The reasons for the decline in profit and continued fluctuations may include changes in the market or economic conditions, increased competition, or internal issues such as operational inefficiencies or supply chain problems.
    - It's important to investigate the causes of these fluctuations and identify strategies to improve profitability.
    - We may want to analyze any changes we made in response to the decline in profit and determine their impact on profitability.
    - By identifying patterns or trends in the fluctuations, we can make more informed business decisions in the future.
    """)

st.markdown("""
### 📊 SWOT Analysis
#### Strengths:
- The company has a successful payout strategy that appears to be attracting and retaining customers.
- There are a few popular apps that are particularly popular among users, providing a strong foundation for investment and promotion.
- The company is generating consistent daily revenue, indicating a stable and profitable business model.
#### Weaknesses:
- There are fluctuations in daily ad spend and daily installs, suggesting potential issues with marketing strategy or external factors impacting user behavior.
- The data on total installs by country shows a heavy reliance on one country, which could be a vulnerability if that market were to experience significant changes or competition.
- There are smaller percentages of installs for certain apps, indicating potential areas for improvement in terms of product or marketing strategy.
#### Opportunities:
- The fluctuations in daily installs and ad spend could provide opportunities to identify new marketing strategies or approaches that better align with user behavior and external factors.
- There is potential for growth in countries with smaller percentages of total installs, providing opportunities for expansion and diversification.
- The popularity of certain apps could be leveraged to introduce new features or products that appeal to the same user base.
#### Threats:
- Changes in the competitive landscape could impact the company's position in the market.
- External factors such as changes in consumer behavior or industry trends could impact daily installs and ad spend.
- Heavy reliance on one country for a majority of installs could leave the company vulnerable to political or economic changes in that country.
""")

col11, col12 = st.columns(2)

with col11:
    st.markdown("""
    ### 🏆 Conclusions
    - The financial analysis of JustDice provides valuable insights into the company's performance and potential areas for improvement.
    - The fluctuation in ad spend, daily installs, and payouts highlight the importance of monitoring these metrics over time and identifying trends and patterns that can inform strategic decision-making.
    - The company's payout strategy appears to be successful in attracting new customers and retaining existing ones, and the consistency in daily revenue suggests a healthy financial position.
    - By exploring the reasons behind fluctuations in these metrics, the company can identify areas for improvement and make strategic investments in marketing efforts and product development to drive growth and maximize revenue.
    """)

with col12:
    st.markdown("""
    ### ➡️ Next Steps
    - Conduct a deeper analysis of external factors that may be influencing ad spend and daily installs, such as seasonality, industry trends, and changes in consumer behavior.
    - Explore the reasons for the decline in daily installs after the peak in mid-November and identify potential areas for improvement.
    - Investigate why country_id=1 is the most popular country for installs and whether there are specific factors contributing to this trend.
    - Identify opportunities for growth and improvement among apps with smaller percentages of installs.
    - Conduct further analysis to identify factors driving fluctuations in the payout amounts and to assess the long-term sustainability of the company's payout strategy.
    - Continuously monitor daily installs, ad spend, payouts, and revenue to identify trends and patterns that can inform strategic decision-making.
    """)
