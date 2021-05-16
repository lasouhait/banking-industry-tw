# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

st.set_page_config(page_title="臺灣金融業資訊分析")
st.title("臺灣金融業資訊分析")
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

Company_List = df_Bank_2016[["證券代號","證券名稱"]].append(df_Bank_2017[["證券代號","證券名稱"]]).append(df_Bank_2018[["證券代號","證券名稱"]]).append(df_Bank_2019[["證券代號","證券名稱"]]).append(df_Bank_2020[["證券代號","證券名稱"]]).append(df_Bank_2021[["證券代號","證券名稱"]])
Company_List = Company_List.sort_values("證券代號")
Company_List["清單"] = Company_List["證券代號"]+" "+Company_List["證券名稱"]
Selection_List = Company_List["清單"].unique()
Selection_Name_Dict = dict(zip(Company_List["清單"],Company_List["證券名稱"]))

Company = Selection_Name_Dict[st.selectbox("選擇證券名稱",list(Selection_List))]


st.write(Company+" 歷年年間最高、最低股價")
Stock_Annual_Summary = pd.DataFrame(columns=['證券代號','證券名稱','最低價','最低價日期','最高價','最高價日期','年初開盤價','年末收盤價'])

S2016 = df_Bank_2016[df_Bank_2016["證券名稱"]==Company]
Company_Num = S2016['證券代號'].unique()
min_record = S2016[S2016["最低價"]==S2016["最低價"].min()]
min_price = min_record['最低價']
min_day = min_record['日期']
max_record = S2016[S2016["最低價"]==S2016["最低價"].max()]
max_price = max_record['最低價']
max_day = max_record['日期']
first_open = S2016[S2016["日期"]==S2016["日期"].min()]["開盤價"]
last_close = S2016[S2016["日期"]==S2016["日期"].max()]["收盤價"]

Stock_Annual_Summary.append({'證券代號': Company_Num, '證券名稱': Company, '最低價': min_price, '最低價日期': min_day, '最高價': max_price, '最高價日期': max_day, '年初開盤價': first_open, '年末收盤價': last_close})

st.write(Stock_Annual_Summary)
