# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

st.title("臺灣金融業統計")
st.write("Dashboard")

df_2016 = pd.read_csv("大盤_2016.csv")
df_2017 = pd.read_csv("大盤_2017.csv")
df_2018 = pd.read_csv("大盤_2018.csv")
df_2019 = pd.read_csv("大盤_2019.csv")
df_2020 = pd.read_csv("大盤_2020.csv")
df_2021 = pd.read_csv("大盤_2021.csv")


st.write(df.iloc[0:1])
