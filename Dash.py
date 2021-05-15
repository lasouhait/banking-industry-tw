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

df_Bank_2016 = pd.read_csv("金融股_2016.csv")
df_Bank_2017 = pd.read_csv("金融股_2017.csv")
df_Bank_2018 = pd.read_csv("金融股_2018.csv")
df_Bank_2019 = pd.read_csv("金融股_2019.csv")
df_Bank_2020 = pd.read_csv("金融股_2020.csv")
df_Bank_2021 = pd.read_csv("金融股_2021.csv")

Company_List = df_Bank_2016[["證券代號","證券名稱"]].append(df_Bank_2017[["證券代號","證券名稱"]]).append(df_Bank_2018[["證券代號","證券名稱"]]).append(df_Bank_2019[["證券代號","證券名稱"]]).append(df_Bank_2020[["證券代號","證券名稱"]]).append(df_Bank_2021[["證券代號","證券名稱"]]).unique()
Company_List = Company_List.sort_values("證券代號")
Company_List["清單"] = Company_List["證券代號"]+Company_List["證券名稱"]
List = list(Company_List["清單"])

Company = st.selectbox("選擇證券名稱",List)
