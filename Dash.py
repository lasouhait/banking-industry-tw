# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

st.title("臺灣金融業統計")
st.write("Dashboard")

df = pd.read_csv("大盤_2016.csv")
