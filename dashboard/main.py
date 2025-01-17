import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
# import matplotlib.pyplot as plt
from st_aggrid import AgGrid

import plotly.express as px
# from add_data import db_execute_fetch

import pandas as pd
import numpy as np
import altair as alt



st.set_page_config(page_title="Dashboard", layout="wide")

def loadData():
    query = "select * from TweetInformation"
    # df = db_execute_fetch(query, dbName="tweets", rdf=True)
    df = pd.read_csv("cleaned_tweet_data_2.csv")
    return df

def selectHashTag():
    df = loadData()
    hashTags = st.multiselect("choose combination of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)

def original_and_cleaned_text():
    df = loadData()
    st.write(df[['original_text', 'clean_text']])

# def selectLocAndAuth():
#     df = loadData()
#     location = st.multiselect("choose Location of tweets", list(df['place_coordinate'].unique()))
#     lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

#     if location and not lang:
#         df = df[np.isin(df, location).any(axis=1)]
#         st.write(df)
#     elif lang and not location:
#         df = df[np.isin(df, lang).any(axis=1)]
#         st.write(df)
#     elif lang and location:
#         location.extend(lang)
#         df = df[np.isin(df, location).any(axis=1)]
#         st.write(df)
#     else:
#         st.write(df)

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)




def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())

def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['clean_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")


st.title("Data Display")
selectHashTag()

st.title('Original vs Clean tweet')
original_and_cleaned_text()

st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)
# selectLocAndAuth()

st.title("Data Visualizations")
wordCloud()
with st.expander("Show More Graphs"):
    stBarChart()



df = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)
