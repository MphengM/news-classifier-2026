import streamlit as st
import pandas as pd
import plotly.express as px

# st.set_page_config(layout='wide')


st.title("Coastal News Classification Dashboard")
st.write("Analysis of ocean and coast related news articles in South Africa (2014-2016)")

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

with st.container():
    # Category filter
    categories = ['All'] + sorted(df['category'].unique().tolist())
    selected_category = st.selectbox("Filter by category:", categories)



# Adding the map (!!!)
# Load the geocoded data
df_geo = pd.read_csv('coastal_news_geocoded.csv')

# Add date_display column to get rid of the 00:00:00 currently in the date column
df_geo['date_display'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')

    
if selected_category!= 'All':
    filtered_df_geo = df_geo[df_geo['category'] == selected_category]

else:
    filtered_df_geo = df_geo

    # The map
fig_map = px.scatter_map(filtered_df_geo,
                        lat="latitude",
                        lon="longitude",
                        color="category",
                        color_discrete_map={
                            'development': 'rgb(15, 133, 84)',
                            'illegal fishing': 'rgb(56, 166, 165)',
                            'waste':'rgb(102, 102, 102)',
                            'red tide': 'rgb(204, 80, 62)',
                            'sea life':'rgb(57, 105, 172)',
                            'natural event':'rgb(115, 175, 72)',
                            'public concern': 'rgb(237, 173, 8)',
                        },
                        hover_name='headlines',
                        hover_data={
                            'headlines': False,
                            'date': False,
                            'date_display': True,
                            'location': True,
                            'latitude': False,
                            'longitude': False
                        })

fig_map.update_traces(
    marker=dict(
        size=12
        )
    )

fig_map.update_layout(
    autosize=True,
    map=dict(
        center=dict(lat=-32, lon=24),
        zoom=5,
        style='satellite-streets',       
        ),
    legend=dict(
        font=dict(
            family='Arial',
            size=14,
            color='black',
            textcase='word caps'),
        bgcolor='rgba(255, 255, 255, 0.65)',
        bordercolor='white',
        borderwidth=2,
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.33), 
        height=600
    )

st.plotly_chart(fig_map)
    

# Table
st.subheader("Article Browser")

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
        



# Set colour scheme
color_discrete_map={
    'development': 'rgb(15, 133, 84)',
    'illegal fishing': 'rgb(56, 166, 165)',
    'waste':'rgb(102, 102, 102)',
    'red tide': 'rgb(204, 80, 62)',
    'sea life':'rgb(29, 105, 150)',
    'natural event':'rgb(115, 175, 72)'
}

# Fig 1: Timeline
st.subheader("Articles over Time")

fig = px.bar(timeline_data,
              x='date',
              y='article_count',
              color='category',
              color_discrete_map=color_discrete_map,
              title='Articles over Time by Category',
              labels={'date': 'Date', 'article_count': 'Number of Articles', 'category': 'Category'})

st.plotly_chart(fig, width='stretch')

# Fig 2 Categories
st.subheader("Distribution of Article Categories")

fig2 = px.bar(category_data,
             x='category_count', 
             y='category',
             orientation='h',
             color='category',
             color_discrete_map=color_discrete_map,
             title='Most Common Occurences',
             labels={'category': '', 'category_count':'Number of occurances'})

fig2.update_layout(yaxis = {"categoryorder":"total ascending"})

st.plotly_chart(fig2, width='stretch')



