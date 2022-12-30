import time
import os
import glob
from urllib.error import URLError
import streamlit as st
import folium # 匯入 folium 套件
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
import pydeck as pdk
import pickle
import 預測

apikey="AIzaSyAsy9v8A2nnNX2usekYPAc9f0zXj3SuEKQ"


st.set_page_config(
    page_title="AI資料工程師班-團專第二組",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="auto",
)
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]
BLUE_RGB = [0, 0, 250, 40]
colors = ['red','blue','gray','darkred','lightred','orange','beige','green','darkgreen','lightgreen','darkblue','lightblue','purple','darkpurple','pink','cadetblue','lightgray','black',
          'orangered','burlywood','aqua','aquamarine4','azure3','azure4','blueviolet','brick','brown','burlywood4','burntumber','chartreuse2','darkolivegreen']
icon = ['tree-conifer','leaf','tree-deciduous','stop','search','book','road','pencil','fire','bullhorn','envelope','usd','euro','header','plus','plus-sign']
# 設定網頁標題
# st.title('團專第二組，房價預測模型')
"""
#  團專第二組-房價預測模型
"""
if '房屋地址' not in st.session_state:
    st.session_state.房屋地址 = "民生東路三段36號"
    st.session_state.行政區域 ="中山區"


if 'modelpredict' not in st.session_state:
    st.session_state.modelpredict = 預測.preparepredict(apikey)
    print("init Model1")

with st.expander("輸入房屋相關資訊",expanded=True):
    left_column0, middle_column0, right_column0 = st.columns(3)
    行政區域_option = left_column0.selectbox('請選擇行政區域', (
    "中山區", "中正區", "信義區", "內湖區", "北投區", "南港區", "士林區", "大同區", "大安區", "文山區", "松山區",
    "萬華區"), key='行政區域')

    房屋地址 = middle_column0.text_input('請輸入房屋街道門號地址',key='房屋地址')
    # st.session_state.房屋地址
    # 房屋地址 = st.text_input('請輸入房屋地址', '臺北市中山區民生東路三段36號',key='houseaddr')
    left_column1, middle_column1, right_column1 = st.columns(3)
    建物型態_option=left_column1.selectbox('請挑選建物型態',('公寓','套房','華廈','住宅大樓'),index=0,key='建物型態')
    管委會_option=middle_column1.selectbox('請選擇有無管理組織',('有','無'),index=0,key='管委會')
    車位類別_option = right_column1.selectbox('請選擇車位類別',('無車位', '坡道平面', '升降平面', '升降機械', '塔式車位'), index=0,key='車位類別')

    left_column3, middle_column3, right_column3 = st.columns(3)
    # 樓層 = middle_column3.text_input('請輸入樓層')
    樓層 = left_column3.slider('樓層',value=5,key='樓層')
    # 總樓層 = right_column3.text_input('請輸入總樓層')
    總樓層 = middle_column3.slider('總樓層',value=5,key='總樓層')
    電梯_option = right_column3.selectbox('請選擇有無電梯', ('無', '有'),index=1,key='電梯')

    left_column5, middle_column5, right_column5 = st.columns(3)
    權狀坪數 = left_column5.text_input('請輸入權狀坪數', "30", key='權狀坪數')
    屋齡 = middle_column5.text_input('請輸入屋齡',"10",key='屋齡')

    # mbm_dict = {"加強磚造": "主要建材_加強磚造", "鋼筋混凝土造": "主要建材_鋼筋混凝土造", "鋼骨造": "主要建材_鋼骨造", }
    主要建材_option=right_column5.selectbox('請選擇主要建材',('加強磚造','鋼筋混凝土造','鋼骨造'),index=0,key='主要建材')

    left_column7, middle_column7, right_column7 = st.columns(3)
    廳數 = left_column7.text_input('請輸入廳數:',"2",key='廳數')
    房數 = middle_column7.text_input('請輸入房數:',"3",key='房數')
    衛浴 = right_column7.text_input('請輸入衛浴數量:',"2",key='衛浴')

    submitted = st.button("預測房價")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# if(not st.session_state.submitted):
#     try:
#         for f in glob.glob("*.poi"):
#             os.remove(f)
#     except:
#         pass
        # print("Error while deleting file ", filePath)

if 'result' not in st.session_state:
    st.session_state.result = ""

if 'info' not in st.session_state:
    st.session_state.info= []

if 'devicecountresult' not in st.session_state:
    st.session_state.devicecountresult = ""

if 'latlng' not in st.session_state:
    st.session_state.latlng = (25.0, 121.5)

sidebar_left_column1, sidebar_right_column1 = st.sidebar.columns(2)
sidebar_left_column2, sidebar_right_column2 = st.sidebar.columns(2)
sidebar_left_column3, sidebar_right_column3 = st.sidebar.columns(2)
sidebar_left_column4, sidebar_right_column4 = st.sidebar.columns(2)
sidebar_left_column5, sidebar_right_column5 = st.sidebar.columns(2)
sidebar_left_column6, sidebar_right_column6 = st.sidebar.columns(2)
sidebar_left_column7, sidebar_right_column7 = st.sidebar.columns(2)
sidebar_left_column8, sidebar_right_column8 = st.sidebar.columns(2)
sidebar_left_column9, sidebar_right_column9 = st.sidebar.columns(2)
sidebar_left_column10, sidebar_right_column10 = st.sidebar.columns(2)
sidebar_left_column11, sidebar_right_column11 = st.sidebar.columns(2)
sidebar_left_column12, sidebar_right_column12 = st.sidebar.columns(2)
sidebar_left_column13, sidebar_right_column13 = st.sidebar.columns(2)
sidebar_left_column14, sidebar_right_column14 = st.sidebar.columns(2)
sidebar_left_column15, sidebar_right_column15 = st.sidebar.columns(2)


placeholder1 = sidebar_left_column1.empty()
placeholder2 = sidebar_right_column1.empty()
placeholder3 = sidebar_left_column2.empty()
placeholder4 = sidebar_right_column2.empty()
placeholder5 = sidebar_left_column3.empty()
placeholder6 = sidebar_right_column3.empty()
placeholder7 = sidebar_left_column4.empty()
placeholder8 = sidebar_right_column4.empty()
placeholder9 = sidebar_left_column5.empty()
placeholder10 = sidebar_right_column5.empty()
placeholder11 = sidebar_left_column6.empty()
placeholder12 = sidebar_right_column6.empty()
placeholder13 = sidebar_left_column7.empty()
placeholder14 = sidebar_right_column7.empty()
placeholder15 = sidebar_left_column8.empty()
placeholder16 = sidebar_right_column8.empty()
placeholder17 = sidebar_left_column9.empty()
placeholder18 = sidebar_right_column9.empty()
placeholder19 = sidebar_left_column10.empty()
placeholder20 = sidebar_right_column10.empty()
placeholder21 = sidebar_left_column11.empty()
placeholder22 = sidebar_right_column11.empty()
placeholder23 = sidebar_left_column12.empty()
placeholder24 = sidebar_right_column12.empty()
placeholder25 = sidebar_left_column13.empty()
placeholder26= sidebar_right_column13.empty()
placeholder27 = sidebar_left_column14.empty()
placeholder28 = sidebar_right_column14.empty()
placeholder29 = sidebar_left_column15.empty()
placeholder30 = sidebar_right_column15.empty()

# placeholder1 = st.sidebar.empty()
# placeholder2 = st.sidebar.empty()
# placeholder3 = st.sidebar.empty()
# placeholder4 = st.sidebar.empty()
# placeholder5 = st.sidebar.empty()
# placeholder6 = st.sidebar.empty()
# placeholder7 = st.sidebar.empty()
# placeholder8 = st.sidebar.empty()
# placeholder9 = st.sidebar.empty()
# placeholder10 = st.sidebar.empty()
# placeholder11 = st.sidebar.empty()
# placeholder12 = st.sidebar.empty()
# placeholder13 = st.sidebar.empty()
# placeholder14 = st.sidebar.empty()
# placeholder15 = st.sidebar.empty()
# placeholder16 = st.sidebar.empty()
# placeholder17 = st.sidebar.empty()
# placeholder18 = st.sidebar.empty()
# placeholder19 = st.sidebar.empty()
# placeholder20 = st.sidebar.empty()
# placeholder21 = st.sidebar.empty()
# placeholder22 = st.sidebar.empty()
# placeholder23 = st.sidebar.empty()
# placeholder24 = st.sidebar.empty()
# placeholder25 = st.sidebar.empty()
# placeholder26 = st.sidebar.empty()
# placeholder27 = st.sidebar.empty()
# placeholder28 = st.sidebar.empty()
# placeholder29 = st.sidebar.empty()
# placeholder30 = st.sidebar.empty()
# placeholder31 = st.sidebar.empty()

# print(st.session_state.latlng)
# fmap = folium.Map(location=st.session_state.latlng, zoom_start=14, control_scale=True)
# folium.Marker(st.session_state.latlng, popup=st.session_state.房屋地址, icon=folium.Icon(color=colors[0])).add_to(fmap)

def add_info():
    ser_distinct = str(st.session_state.行政區域)
    ser_address = str(st.session_state.房屋地址)
    ser_area = str(st.session_state.權狀坪數)
    ser_age = str(st.session_state.屋齡)
    ser_money = round(st.session_state.one,2)
    info_dict = {}
    info_dict['行政區'] = ser_distinct
    info_dict['地址'] = ser_address
    info_dict['坪數'] = ser_area
    info_dict['屋齡'] = ser_age
    info_dict['單價'] = ser_money
    st.session_state.info.append(info_dict)

if submitted:
    st.session_state.submitted=True

    # reg = pickle.load(open("reg_model.sav", "rb"))
    if 'modelpredict' not in st.session_state:
        st.session_state.modelpredict = 預測.preparepredict(apikey)
        print("init Model2")
    predict=st.session_state.modelpredict
    # 使用者輸入資訊
    # address = "臺北市萬華區漢口街二段36號"
    # b_type = "華廈"
    # manage = "有"
    # floor = 9
    # p_type = "無車位"
    # dist = "萬華區"
    # ele = "有"
    # age = 10
    # trans = 25.46748

    address = "台北市"+ st.session_state.行政區域+st.session_state.房屋地址
    b_type = st.session_state.建物型態
    manage = st.session_state.管委會
    floor = int(st.session_state.樓層)
    p_type = st.session_state.車位類別
    dist = st.session_state.行政區域
    ele = st.session_state.電梯
    age = float(st.session_state.屋齡)
    trans =float( st.session_state.權狀坪數)
    tfloor = int(st.session_state.總樓層)
    mbm = st.session_state.主要建材
    hall = int(st.session_state.廳數)
    room = int(st.session_state.房數)
    bathroom = int(st.session_state.衛浴)

    predict.user_input(address,b_type,manage,floor,p_type,dist,ele,age,trans,tfloor,mbm,hall,room,bathroom)
    # 新增經緯度
    st.session_state.latlng= predict.lat_lng()
    # # 新增距離設施
    公園個數, 公園park_df = predict.park(500)
    小公園個數, 小公園smallpark_df = predict.smallpark(500)
    大公園個數, 大公園bigpark_df = predict.bigpark(500)
    小綠地個數, 小綠地smallgr_df = predict.smallgr(500)
    大綠地個數, 大綠地biggr_df = predict.biggr(500)
    小廣場個數, 小廣場smallsq_df = predict.smallsq(500)
    大廣場個數, 大廣場bigsq_df = predict.bigsq(500)
    博物館個數, 博物館mu_df = predict.mu(500)
    圖書館個數, 圖書館lib_df = predict.lib(500)
    捷運出口個數, 捷運出口mrt_df = predict.mrt(500)
    幼稚園個數, 幼稚園kinde_df = predict.kinder(500)
    國小個數, 國小ele_df = predict.ele(500)
    國中個數, 國中jun_df = predict.jun(500)
    高中職個數, 高中職sen_df = predict.sen(500)
    大學個數, 大學coll_df = predict.coll(500)
    消防大隊個數, 消防大隊fireb_df = predict.fireb(500)
    消防中隊個數, 消防中隊firem_df = predict.firem(500)
    消防分隊個數, 消防分隊fires_df = predict.fires(500)
    禮儀個數, 禮儀dead_df = predict.dead(500)
    警察局個數, 警察局pold_df = predict.pold(500)
    警察隊個數, 警察隊polt_df = predict.polt(500)
    派出所個數, 派出所pols_df = predict.pols(500)
    郵局個數, 郵局post_df = predict.post(500)
    銀行個數, 銀行bank_df = predict.bank(500)
    證券個數, 證券securities_df = predict.securities(500)
    信用合作社個數, 信用合作社coop_df = predict.coop(500)
    醫院個數, 醫院hosp_df = predict.hosp(500)
    西醫個數, 西醫clinicw_df = predict.clinicw(500)
    中醫個數, 中醫clinice_df = predict.clinice(500)
    藥局個數, 藥局phar_df = predict.pharmacy(500)

    st.session_state.公園_df = 公園park_df
    st.session_state.小公園_df = 小公園smallpark_df
    st.session_state.大公園_df = 大公園bigpark_df
    st.session_state.小綠地_df = 小綠地smallgr_df
    st.session_state.大綠地_df = 大綠地biggr_df
    st.session_state.小廣場_df = 小廣場smallsq_df
    st.session_state.大廣場_df = 大廣場bigsq_df
    st.session_state.博物館_df = 博物館mu_df
    st.session_state.圖書館_df = 圖書館lib_df
    st.session_state.捷運出口_df = 捷運出口mrt_df
    st.session_state.幼稚園_df = 幼稚園kinde_df
    st.session_state.國小_df = 高中職sen_df
    st.session_state.國中_df = 國中jun_df
    st.session_state.高中職_df = 高中職sen_df
    st.session_state.大學_df = 大學coll_df
    st.session_state.消防大隊_df = 消防大隊fireb_df
    st.session_state.消防中隊_df = 消防中隊firem_df
    st.session_state.消防分隊_df = 消防分隊fires_df
    st.session_state.禮儀_df = 禮儀dead_df
    st.session_state.警察局_df = 警察局pold_df
    st.session_state.警察隊_df = 警察隊polt_df
    st.session_state.派出所_df = 派出所pols_df
    st.session_state.郵局_df = 郵局post_df
    st.session_state.銀行_df = 銀行bank_df
    st.session_state.證券_df = 證券securities_df
    st.session_state.信用合作社_df = 信用合作社coop_df
    st.session_state.醫院_df = 醫院hosp_df
    st.session_state.西醫_df = 西醫clinicw_df
    st.session_state.中醫_df = 中醫clinice_df
    st.session_state.藥局_df = 藥局phar_df

    # 公園, 博物館, 圖書館, 捷運出口, 學校, 消防, 禮儀, 警察, 郵局, 金融, 醫院, 診所, 藥局
    # =========================

    # 預測價錢
    # st.session_state.單價, result=predict.pred()
    st.session_state.one, outputdata1, outputdata2, outputdata3, outputdata10=predict.pred()
    result="\n".join([outputdata1,outputdata2,outputdata3,outputdata10])
    st.session_state.result=result
    add_info()

    # st.write(st.session_state.result)
    # result_textbox = st.empty()

    # devicecountresult= f"公園:{公園個數}\n博物館:{博物館個數}\n圖書館:{圖書館個數}\n捷運出口:{捷運出口個數}\n學校:{學校個數}\n消防:{消防局個數}\n禮儀:{禮儀個數}\n警察局:{警察局個數}\n郵局:{郵局個數}\n金融:{金融個數}\n醫院:{醫院個數}\n診所:{診所個數}\n藥局:{藥局個數}\n"

    devicecountresult= f"公園:{公園個數}，小公園:{小公園個數}，大公園:{大公園個數}，小綠地:{小綠地個數}，大綠地:{大綠地個數}，小廣場:{小廣場個數}，大廣場:{大廣場個數}，博物館:{博物館個數}，圖書館:{圖書館個數}，捷運出口:{捷運出口個數}，\n" \
                       f"幼稚園:{幼稚園個數}，國小:{國小個數}，國中:{國中個數}，高中職:{高中職個數}，大學:{大學個數}，\n" \
                       f"消防大隊:{消防大隊個數}，消防中隊:{消防中隊個數}，消防分隊:{消防分隊個數}，禮儀:{禮儀個數}，警察局:{警察局個數}，警察隊:{警察隊個數}，派出所:{派出所個數}，郵局:{郵局個數}，\n" \
                       f"銀行:{銀行個數}，證券:{證券個數}，信用合作社:{信用合作社個數}，醫院:{醫院個數}，西醫:{西醫個數}，中醫:{中醫個數}，藥局:{藥局個數}"
    st.session_state.devicecountresult=devicecountresult

    # devicecountresult_textbox = st.empty()
    # st.write(st.session_state.devicecountresult)

    # st.write("預測中")
    # latest_iteration = st.empty()
    # bar = st.progress(0)
    # for i in range(100):
    #     latest_iteration.text(f'目前進度 {i+1} %')
    #     bar.progress(i + 1)
    #     time.sleep(0.1)
    # y_pre = reg.predict(x_test)
    # print(f"預測值: {y_pre[0]}")
    # print(f"真實值: {y_test.iloc[0]}"
    # '''
    # 輸出內容包含：
    # 1. 預測的價格
    # 2. 單價：  萬/坪
    # 3. 地圖(可顯示使用者輸入的地址)
    # 4. 地圖可呈現某距離(距離可調，以公尺為單位)內的設施位置，設施可供選擇(公園,博物館,圖書館,捷運出口,學校,消防,禮儀,警察,郵局,金融,醫院,診所,藥局)
    # '''

# result_textbox.text(st.session_state.result)
# devicecountresult_textbox.text(st.session_state.devicecountresult)
if (st.session_state.submitted):
    # print(latlng)
    with st.expander("展開觀看預測結果"):
        st.text(st.session_state.result)
    with st.expander("附近設施數量"):
        # facilitydataframe = st.empty()
        facility = st.text(st.session_state.devicecountresult)
        # facilitydataframe.dataframe(st.session_state.devicecountresult.h)

    with st.expander("歷史查詢紀錄"):
        placeholderdataframe = st.empty()
        cleared = st.button("清空歷史紀錄")
        if cleared:
            st.session_state.info.clear()
        else:
            placeholderdataframe.dataframe(st.session_state.info)

# def getdata(datafilename):
#     try:
#         data=pd.read_csv(datafilename, encoding="utf-8")
#     except:
#         data=pd.DataFrame()
#
#     return data

        #
        # ser_result = st.text(st.session_state.result)
        #
        # my_dict = []
        # my_dict.append(ser_result)

if (not st.session_state.submitted):
    公園checkbox = placeholder1.checkbox("1公園")
    小公園checkbox = placeholder2.checkbox("2小公園")
    大公園checkbox = placeholder3.checkbox("3大公園")
    小綠地checkbox = placeholder4.checkbox("4小綠地")
    大綠地checkbox = placeholder5.checkbox("5大綠地")
    小廣場checkbox = placeholder6.checkbox("6小廣場")
    大廣場checkbox = placeholder7.checkbox("7大廣場")
    博物館checkbox = placeholder8.checkbox("8博物館")
    圖書館checkbox = placeholder9.checkbox("9圖書館")
    捷運出口checkbox = placeholder10.checkbox("10捷運出口")
    幼稚園checkbox = placeholder11.checkbox("11幼稚園")
    國小checkbox = placeholder12.checkbox("12國小")
    國中checkbox = placeholder13.checkbox("13國中")
    高中職checkbox = placeholder14.checkbox("14高中職")
    大學checkbox = placeholder15.checkbox("15大學")
    消防大隊checkbox = placeholder16.checkbox("16消防大隊")
    消防中隊checkbox = placeholder17.checkbox("17消防中隊")
    消防分隊checkbox = placeholder18.checkbox("18消防分隊")
    禮儀checkbox = placeholder19.checkbox("19禮儀")
    警察局checkbox = placeholder20.checkbox("20警察局")
    警察隊checkbox = placeholder21.checkbox("21警察隊")
    派出所checkbox = placeholder22.checkbox("22派出所")
    郵局checkbox = placeholder23.checkbox("23郵局")
    銀行checkbox = placeholder24.checkbox("24銀行")
    證券checkbox = placeholder25.checkbox("25證券")
    信用合作社checkbox = placeholder26.checkbox("26信用合作社")
    醫院checkbox = placeholder27.checkbox("27醫院")
    西醫checkbox = placeholder28.checkbox("28西醫")
    中醫checkbox = placeholder29.checkbox("29中醫")
    藥局checkbox = placeholder30.checkbox("30藥局")
else:
    # 公園_data = pd.read_csv("公園座標.poi", encoding="utf-8")
    公園_data = st.session_state.公園_df
    小公園_data = st.session_state.小公園_df
    大公園_data = st.session_state.大公園_df
    小綠地_data = st.session_state.小綠地_df
    大綠地_data = st.session_state.大綠地_df
    小廣場_data = st.session_state.小廣場_df
    大廣場_data = st.session_state.大廣場_df
    博物館_data = st.session_state.博物館_df
    圖書館_data = st.session_state.圖書館_df
    捷運出口_data = st.session_state.捷運出口_df
    幼稚園_data = st.session_state.幼稚園_df
    國小_data = st.session_state.國小_df
    國中_data = st.session_state.國中_df
    高中職_data = st.session_state.高中職_df
    大學_data = st.session_state.大學_df
    消防大隊_data = st.session_state.消防大隊_df
    消防中隊_data = st.session_state.消防中隊_df
    消防分隊_data = st.session_state.消防分隊_df
    禮儀_data = st.session_state.禮儀_df
    警察局_data = st.session_state.警察局_df
    警察隊_data = st.session_state.警察隊_df
    派出所_data = st.session_state.派出所_df
    郵局_data = st.session_state.郵局_df
    銀行_data = st.session_state.銀行_df
    證券_data = st.session_state.證券_df
    信用合作社_data = st.session_state.信用合作社_df
    醫院_data = st.session_state.醫院_df
    西醫_data = st.session_state.西醫_df
    中醫_data = st.session_state.中醫_df
    藥局_data = st.session_state.藥局_df

    公園checkbox = placeholder1.checkbox("1公園：" + str(len(公園_data)), value=True)
    小公園checkbox = placeholder2.checkbox("2小公園：" + str(len(小公園_data)), value=True)
    大公園checkbox = placeholder3.checkbox("3大公園：" + str(len(大公園_data)), value=True)
    小綠地checkbox = placeholder4.checkbox("4小綠地：" + str(len(小綠地_data)), value=True)
    大綠地checkbox = placeholder5.checkbox("5大綠地：" + str(len(大綠地_data)), value=True)
    小廣場checkbox = placeholder6.checkbox("6小廣場：" + str(len(小廣場_data)), value=True)
    大廣場checkbox = placeholder7.checkbox("7大廣場：" + str(len(大廣場_data)), value=True)
    博物館checkbox = placeholder8.checkbox("8博物館：" + str(len(博物館_data)), value=True)
    圖書館checkbox = placeholder9.checkbox("9圖書館：" + str(len(圖書館_data)), value=True)
    捷運出口checkbox = placeholder10.checkbox("10捷運出口：" + str(len(捷運出口_data)), value=True)
    幼稚園checkbox = placeholder11.checkbox("11幼稚園：" + str(len(幼稚園_data)), value=True)
    國小checkbox = placeholder12.checkbox("12國小：" + str(len(國小_data)), value=True)
    國中checkbox = placeholder13.checkbox("13國中：" + str(len(國中_data)), value=True)
    高中職checkbox = placeholder14.checkbox("14高中職：" + str(len(高中職_data)), value=True)
    大學checkbox = placeholder15.checkbox("15大學：" + str(len(大學_data)), value=True)
    消防大隊checkbox = placeholder16.checkbox("16消防大隊：" + str(len(消防大隊_data)), value=True)
    消防中隊checkbox = placeholder17.checkbox("17消防中隊：" + str(len(消防中隊_data)), value=True)
    消防分隊checkbox = placeholder18.checkbox("18消防分隊：" + str(len(消防分隊_data)), value=True)
    禮儀checkbox = placeholder19.checkbox("19禮儀：" + str(len(禮儀_data)), value=True)
    警察局checkbox = placeholder20.checkbox("20警察局：" + str(len(警察局_data)), value=True)
    警察隊checkbox = placeholder21.checkbox("21警察隊：" + str(len(警察隊_data)), value=True)
    派出所checkbox = placeholder22.checkbox("22派出所：" + str(len(派出所_data)), value=True)
    郵局checkbox = placeholder23.checkbox("23郵局：" + str(len(郵局_data)), value=True)
    銀行checkbox = placeholder24.checkbox("24銀行：" + str(len(銀行_data)), value=True)
    證券checkbox = placeholder25.checkbox("25證券：" + str(len(證券_data)), value=True)
    信用合作社checkbox = placeholder26.checkbox("26信用合作社：" + str(len(信用合作社_data)), value=True)
    醫院checkbox = placeholder27.checkbox("27醫院：" + str(len(醫院_data)), value=True)
    西醫checkbox = placeholder28.checkbox("28西醫：" + str(len(西醫_data)), value=True)
    中醫checkbox = placeholder29.checkbox("29中醫：" + str(len(中醫_data)), value=True)
    藥局checkbox = placeholder30.checkbox("30藥局：" + str(len(藥局_data)), value=True)

    fmap = folium.Map(location=st.session_state.latlng, zoom_start=16, control_scale=True)
    folium.Marker(st.session_state.latlng, popup=st.session_state.房屋地址,icon = folium.Icon(color =colors[0])).add_to(fmap)

    if 公園checkbox:
        # fmap = folium.Map(location=[公園_data.lat.mean(), 公園_data.lng.mean()], zoom_start=14, control_scale=True)
        for index, location_info in 公園_data.iterrows():
            # folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],fill_color="red").add_to(fmap)
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[1],icon_color = 'yellow',icon=icon[0])).add_to(fmap)
        # data = 公園_data[["lat", "lng"]].values.tolist()
        # fmap.add_child(HeatMap(data=data))
        # st_folium(fmap, width=725, returned_objects=[])
    if 小公園checkbox:
        for index, location_info in 小公園_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[2],icon_color = 'yellow', icon = icon[1])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 大公園checkbox:
        for index, location_info in 大公園_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[3],icon_color = 'yellow', icon = icon[2])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 小綠地checkbox:
        for index, location_info in 小綠地_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[4],icon_color = 'black', icon = icon[1])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 大綠地checkbox:
        for index, location_info in 大綠地_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[5],icon_color = 'yellow', icon = icon[1])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 小廣場checkbox:
        for index, location_info in 小廣場_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[6],icon_color = 'yellow', icon = icon[3])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 大廣場checkbox:
        for index, location_info in 大廣場_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[7],icon_color = 'yellow', icon = icon[3])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 博物館checkbox:
        for index, location_info in 博物館_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[8],icon_color = 'yellow', icon = icon[4])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 圖書館checkbox:
        for index, location_info in 圖書館_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup="圖書館"+location_info["名稱"],icon = folium.Icon(color=colors[9],icon_color = 'black', icon = icon[5])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 捷運出口checkbox:
        for index, location_info in 捷運出口_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[10],icon_color = 'yellow', icon = icon[6])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 幼稚園checkbox:
        for index, location_info in 幼稚園_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[11],icon_color = 'black', icon = icon[7])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 國小checkbox:
        for index, location_info in 國小_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[12],icon_color = 'yellow', icon = icon[7])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 國中checkbox:
        for index, location_info in 國中_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],
                          icon=folium.Icon(color=colors[13], icon_color='yellow', icon=icon[7])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 高中職checkbox:
        for index, location_info in 高中職_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[14],icon_color = 'black', icon = icon[7])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 大學checkbox:
        for index, location_info in 大學_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[15],icon_color = 'yellow', icon = icon[7])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 消防大隊checkbox:
        for index, location_info in 消防大隊_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[16],icon_color = 'yellow', icon = icon[8])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 消防中隊checkbox:
        for index, location_info in 消防中隊_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[17],icon_color = 'yellow', icon = icon[8])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 消防分隊checkbox:
        for index, location_info in 消防分隊_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[1],icon_color = 'yellow', icon = icon[8])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 禮儀checkbox:
        for index, location_info in 禮儀_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[2],icon_color = 'yellow', icon = 'cloud')).add_to(fmap)
        禮儀data = 禮儀_data[["lat", "lng"]].values.tolist()
        fmap.add_child(HeatMap(data=禮儀data))
        # st_folium(fmap, width=725, returned_objects=[])
    if 警察局checkbox:
        for index, location_info in 警察局_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[3],icon_color = 'yellow', icon = icon[9])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 警察隊checkbox:
        for index, location_info in 警察隊_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[4],icon_color = 'yellow', icon = icon[9])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 派出所checkbox:
        for index, location_info in 派出所_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[5],icon_color = 'yellow', icon = icon[9])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 郵局checkbox:
        for index, location_info in 郵局_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[6],icon_color = 'black', icon = icon[10])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 銀行checkbox:
        for index, location_info in 銀行_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[7],icon_color = 'yellow', icon = "usd")).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 證券checkbox:
        for index, location_info in 證券_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[8],icon_color = 'yellow', icon = 'indent-right')).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 信用合作社checkbox:
        for index, location_info in 信用合作社_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[9],icon_color = 'black', icon = icon[12])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 醫院checkbox:
        for index, location_info in 醫院_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color='white',icon_color = 'red', icon = icon[13])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 西醫checkbox:
        for index, location_info in 西醫_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color="red",icon_color = 'white', icon = icon[14])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 中醫checkbox:
        for index, location_info in 中醫_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[12],icon_color = 'yellow', icon = icon[14])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])
    if 藥局checkbox:
        for index, location_info in 藥局_data.iterrows():
            folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["名稱"],icon = folium.Icon(color=colors[11],icon_color = 'black', icon = icon[15])).add_to(fmap)
        # st_folium(fmap, width=725, returned_objects=[])

    st_folium(fmap, width=725, returned_objects=[])
    # st.balloons()
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })
#
# df

# if st.button('確認'):
#     st.write(house_addr)
# 加入 pandas 資料表格
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))

# 公園_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 博物館_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 圖書館_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 捷運出口_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 學校_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 消防_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 禮儀_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 警察_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 郵局_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 醫療_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])
# 金融_data = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [25.0, 121.5],columns=['lat', 'lon'])

# if st.checkbox('顯示地圖'):
# try:
#     ALL_LAYERS = {
#         "1公園": pdk.Layer(
#             "HexagonLayer",
#             data=公園_data,
#             get_position=["lng", "lat"],
#             get_color=GREEN_RGB,
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             extruded=True,
#         ),
#         "2博物館": pdk.Layer(
#             "ScatterplotLayer",
#             data=博物館_data,
#             get_position=["lng", "lat"],
#             get_color=BLUE_RGB,
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "3圖書館": pdk.Layer(
#             "ScatterplotLayer",
#             data=圖書館_data,
#             get_position=["lng", "lat"],
#             get_color=RED_RGB,
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "4捷運出口": pdk.Layer(
#             "ScatterplotLayer",
#             data=捷運出口_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 255, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "5學校": pdk.Layer(
#             "ScatterplotLayer",
#             data=學校_data,
#             get_position=["lng", "lat"],
#             get_color=GREEN_RGB,
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "6消防": pdk.Layer(
#             "ScatterplotLayer",
#             data=消防局_data,
#             get_position=["lng", "lat"],
#             get_color=RED_RGB,
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "7禮儀": pdk.Layer(
#             "ScatterplotLayer",
#             data=禮儀_data,
#             get_position=["lng", "lat"],
#             get_color=BLUE_RGB,
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "8警察": pdk.Layer(
#             "ScatterplotLayer",
#             data=警察局_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "9郵局": pdk.Layer(
#             "ScatterplotLayer",
#             data=郵局_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "10金融": pdk.Layer(
#             "ScatterplotLayer",
#             data=金融_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "11醫院": pdk.Layer(
#             "ScatterplotLayer",
#             data=醫院_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "12診所": pdk.Layer(
#             "ScatterplotLayer",
#             data=診所_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#         "13藥局": pdk.Layer(
#             "ScatterplotLayer",
#             data=藥局_data,
#             get_position=["lng", "lat"],
#             get_color=[200, 30, 0, 160],
#             # get_radius="[exits]",
#             radius_scale=100,
#         ),
#     }
#     # st.sidebar.markdown("### Map Layers")
#     st.sidebar.header('鄰近設施')
#     selected_layers = [
#         layer
#         for layer_name, layer in ALL_LAYERS.items()
#         if st.sidebar.checkbox(layer_name, True)
#     ]
#     if selected_layers:
#         st.pydeck_chart(
#             pdk.Deck(
#                 map_style=None,
#                 initial_view_state={
#                     "latitude": 25.0,
#                     "longitude": 121.5,
#                     "zoom": 11,
#                     "pitch": 50,
#                 },
#                 layers=selected_layers,
#             )
#         )
#     else:
#         st.error("Please choose at least one layer above.")
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )

# left_column, right_column = st.columns(2)
# left_column.write("這是左邊欄位。")
# right_column.write("這是右邊欄位。")
#
# expander = st.expander("點擊來展開...")
# expander.write("如果你要顯示很多文字，但又不想佔大半空間，可以使用這種方式。")

# 增加一個空白元件，等等要放文字
# latest_iteration = st.empty()
# bar = st.progress(0)
# for i in range(100):
#     latest_iteration.text(f'目前進度 {i+1} %')
#     bar.progress(i + 1)
#     time.sleep(0.1)
