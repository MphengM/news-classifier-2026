import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Coastal News Classification Dashboard")
st.write("Analysis of ocean and coast related news articles in South Africa (2105-2016)")

# Load data
df = pd.read_csv('coastal_news_clean.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df[df['date'] >= '2000-01-01']

# Group by date and category, count articles
timeline_data = df.groupby([df['date'].dt.to_period('M'), 'category']).size().reset_index(name='article_count')

# Convert period back to timestamp for plotting
timeline_data['date'] = timeline_data['date'].dt.to_timestamp()

# Group categories
category_data = df.groupby(['category']).size().reset_index(name="category_count")

# Set date range
date_range = f"{df['date'].min().strftime('%b %Y')} - {df['date'].max().strftime('%b %Y')}"

# Summary stats
col1, col2, col3 = st.columns([2,0.5,0.5])
col2.metric('Total Articles: ', len(df))
col1.metric('Date Range:', date_range)
col3.metric("Categories:", df['category'].nunique())

# Fig 1: Timeline
st.subheader("Articles over Time")

fig = px.bar(timeline_data,
              x='date',
              y='article_count',
             color='category',
              title='Articles over Time by Category',
              labels={'date': 'Date', 'article_count': 'Number of Articles', 'category': 'Category'})

st.plotly_chart(fig, width='stretch')

# Fig 2 Categories
st.subheader("Distribution of Article Categories")

fig2 = px.bar(category_data,
             x='category_count', 
             y='category',
             orientation='h',
             title='Most Common Occurences',
             labels={'category': '', 'category_count':'Number of occurances'})

fig2.update_layout(yaxis = {"categoryorder":"total ascending"})

st.plotly_chart(fig2, width='stretch')

# Table
st.subheader("Article Browser")

# Category filter
categories = ['All'] + sorted(df['category'].unique().tolist())
selected_category = st.selectbox("Filter by category:", categories)

if selected_category!= 'All':
    filtered_df = df[df['category'] == selected_category]

else:
    filtered_df = df


# Display table
st.dataframe(filtered_df[['date', 'headlines', 'url']], 
             width='stretch',
             hide_index=True,
             column_config={
                 "date": st.column_config.DateColumn(
                     "Date",
                     format="DD-MM-YYYY"),
                 "headlines": st.column_config.TextColumn(
                     "Headline",
                     width="large"),
                 "url": st.column_config.LinkColumn("Source"),
             })

