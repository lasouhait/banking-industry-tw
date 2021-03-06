# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.set_page_config(page_title="臺灣金融業資訊分析")
st.title("臺灣金融業資訊分析")
st.write("All information is for personal use, and is not aimed to provide suggestion.")
page_nav = st.sidebar.radio("請選取頁面",["營運概況","人力資訊","董監酬勞揭露","股價資訊","金融統計"])

if page_nav == "營運概況":
        st.write("營運概況")
elif page_nav == "股價資訊":
    @st.cache
    def read_file(str):
        df = pd.read_csv(str)
        return df

    ###讀檔

    df_2015 = read_file("大盤_2015.csv")
    df_2016 = read_file("大盤_2016.csv")
    df_2017 = read_file("大盤_2017.csv")
    df_2018 = read_file("大盤_2018.csv")
    df_2019 = read_file("大盤_2019.csv")
    df_2020 = read_file("大盤_2020.csv")
    df_2021 = read_file("大盤_2021.csv")
    df_Bank_2015 = read_file("金融股_2015.csv")
    df_Bank_2016 = read_file("金融股_2016.csv")
    df_Bank_2017 = read_file("金融股_2017.csv")
    df_Bank_2018 = read_file("金融股_2018.csv")
    df_Bank_2019 = read_file("金融股_2019.csv")
    df_Bank_2020 = read_file("金融股_2020.csv")
    df_Bank_2021 = read_file("金融股_2021.csv")
        
    df_divprice_2016 = pd.read_csv("105除權息.csv",encoding='utf-8')[0:-11]
    df_divprice_2017 = pd.read_csv("106除權息.csv",encoding='utf-8')[0:-11]
    df_divprice_2018 = pd.read_csv("107除權息.csv",encoding='utf-8')[0:-11]
    df_divprice_2019 = pd.read_csv("108除權息.csv",encoding='utf-8')[0:-11]
    df_divprice_2020 = pd.read_csv("109除權息.csv",encoding='utf-8')[0:-11]

    @st.cache
    def generate_list():
        Company_List = df_Bank_2015[["證券代號","證券名稱"]].append(df_Bank_2016[["證券代號","證券名稱"]]).append(df_Bank_2017[["證券代號","證券名稱"]]).append(df_Bank_2018[["證券代號","證券名稱"]]).append(df_Bank_2019[["證券代號","證券名稱"]]).append(df_Bank_2020[["證券代號","證券名稱"]]).append(df_Bank_2021[["證券代號","證券名稱"]])
        Company_List = Company_List.sort_values("證券代號")
        Company_List["清單"] = Company_List["證券代號"]+" "+Company_List["證券名稱"]
        Selection_List = Company_List["清單"].unique()
        Selection_Name_Dict = dict(zip(Company_List["清單"],Company_List["證券名稱"]))
        return Selection_List,Selection_Name_Dict

    with st.spinner('計算中'):
        Selection_List,Selection_Name_Dict = generate_list()

    Company = Selection_Name_Dict[st.selectbox("選擇證券名稱",list(Selection_List))]

    #歷年股價

    st.write(Company+" 歷年年間最高、最低股價")
    Stock_Annual_Summary = pd.DataFrame(columns=['年','證券代號','證券名稱','最低價','最低價日期','最高價','最高價日期','年初開盤價','年末收盤價'])
    Stock_PCT = pd.DataFrame(columns=['年','證券代號','證券名稱','收盤價','日期'])

    for i in [df_Bank_2016,df_Bank_2017,df_Bank_2018,df_Bank_2019,df_Bank_2020,df_Bank_2021]:#未放入df_Bank_2015，因僅有最後一個交易日
      try:
        S = i[i["證券名稱"]==Company]
        Year = S['年'].unique()[0]
        Company_Num = S['證券代號'].unique()[0]
        min_record = S[S["最低價"]!="--"]
        min_record = min_record[min_record["最低價"]==min_record["最低價"].min()]
        min_price = min_record['最低價'].iloc[0]
        min_day = min_record['日期'].iloc[0]
        max_record = S[S["最低價"]==S["最低價"].max()]
        max_price = max_record['最低價'].iloc[0]
        max_day = max_record['日期'].iloc[0]
        first_open = S[S["日期"]==S["日期"].min()]["開盤價"].iloc[0]
        last_close = S[S["日期"]==S["日期"].max()]["收盤價"].iloc[0]

        Stock_Annual_Summary = Stock_Annual_Summary.append({'年':Year, '證券代號': Company_Num, '證券名稱': Company, '最低價': min_price, '最低價日期': min_day, '最高價': max_price, '最高價日期': max_day, '年初開盤價': first_open, '年末收盤價': last_close},ignore_index=True)

        Stock_PCT = Stock_PCT.append(S[['年','證券代號','證券名稱','收盤價','日期']])
      except:
        pass  

    # 股價波動分析

    @st.cache
    def append_index():
        index = pd.DataFrame(columns=['收盤指數','日期'])

        for j in [df_2015,df_2016,df_2017,df_2018,df_2019,df_2020,df_2021]:
            j = j[j["指數"]=="發行量加權股價指數"][['收盤指數','日期']]
            j['收盤指數'] = j['收盤指數'].str.replace(",","").str.replace("\"","").astype(float)
            index = index.append(j,ignore_index=True)

        index = index.set_index("日期")
        return index

    with st.spinner('計算中'):
        index = append_index()    
        
    @st.cache
    def append_divprice():
        divprice = pd.DataFrame(columns=['年','股票代號','股票名稱','除權息前收盤價','權值+息值'])
        
        for i in [df_divprice_2016,df_divprice_2017,df_divprice_2018,df_divprice_2019,df_divprice_2020]:
            i["股票代號"] = i["股票代號"].str.replace("\"","").str.replace("=","")
            i["年"] = i['資料日期'].str[0:3].astype(int)+1911
            i["年"] = i["年"].astype(str)
            i = i[['年','股票代號','股票名稱','除權息前收盤價','權值+息值']]
            divprice = divprice.append(i,ignore_index=True)
            
        divprice = divprice.set_index("年")
        return divprice
        
    divprice = append_divprice()
    Stock_PCT = Stock_PCT.join(index,on='日期')
    Stock_Annual_Summary['年'] = Stock_Annual_Summary['年'].astype(str)
    Stock_Annual_Summary = Stock_Annual_Summary.set_index('年')
    try:
        Stock_PCT['收盤價'] = Stock_PCT['收盤價'].astype(float)
    except:
        Stock_PCT = Stock_PCT[Stock_PCT['收盤價']!="--"]
        Stock_PCT['收盤價'] = Stock_PCT['收盤價'].astype(float)
    Stock_PCT["漲跌幅"] = Stock_PCT['收盤價'].pct_change()
    Stock_PCT["大盤波動幅"] = Stock_PCT['收盤指數'].pct_change()
    Stock_PCT = Stock_PCT[1:]
    st.write(Stock_Annual_Summary)

    st.write(Company+" 股價波動分析")
    beta_table = pd.DataFrame(columns=['年','beta 值','個股標準差'])

    for i in [2016,2017,2018,2019,2020,2021]:
        S = Stock_PCT[Stock_PCT["年"]==i]
        try:
            model = sm.OLS(S["漲跌幅"],sm.add_constant(S["大盤波動幅"]))
            results = model.fit()
            beta = results.params
            beta = beta[1]
        except:
            beta = "無法計算"
        std = S['收盤價'].std()
        i = str(i)
        beta_table = beta_table.append({'年':i, 'beta 值': beta, '個股標準差': std},ignore_index=True)

    div_company = divprice[divprice['股票名稱']==Company]
    div_company = div_company[['除權息前收盤價','權值+息值']]
    st.write(div_company)
    beta_table = beta_table.set_index("年")
    beta_table = beta_table.join(div_company)
    beta_table = beta_table.join(Stock_Annual_Summary['年末收盤價'])
    #beta_table["年末填權"] = beta_table.apply(lambda row: "有" if row["除權息前收盤價"]<=row['年末收盤價'] else "無")
    st.write(beta_table)
        
