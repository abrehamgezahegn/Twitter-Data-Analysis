import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch

st.set_page_config(page_title="Day 5", layout="wide")

def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df

def selectHashTag():
    df = loadData()
    hashTags = st.multiselect("choose combination of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


st.title("Data Display")
selectHashTag()
