import pandas as pd
import numpy as np
import geopy.distance
import googlemaps
import pickle
import sys
import traceback

"""# 使用者輸入資訊"""

class preparepredict():
    pre_f = pd.DataFrame(columns=[
                                  "土地位置建物門牌", "建物現況格局-廳", "建物現況格局-房", "建物現況格局-衛", 
                                  "移轉層次", "總樓層數", "屋齡", "建物移轉總坪數", 
                                  "鄉鎮市區_中山區", "鄉鎮市區_中正區", "鄉鎮市區_信義區",
                                  "鄉鎮市區_內湖區", "鄉鎮市區_北投區", "鄉鎮市區_南港區",
                                  "鄉鎮市區_士林區", "鄉鎮市區_大同區", "鄉鎮市區_大安區", 
                                  "鄉鎮市區_文山區", "鄉鎮市區_松山區", "鄉鎮市區_萬華區", 
                                  "建物型態_住宅大樓", "建物型態_公寓", "建物型態_套房","建物型態_華廈",
                                  "車位類別_一樓平面", "車位類別_升降平面", "車位類別_升降機械", "車位類別_坡道平面",
                                  "車位類別_坡道機械", "車位類別_塔式車位", "車位類別_無車位",
                                  "有無管理組織_0", "有無管理組織_1",
                                  "電梯_有", "電梯_無",
                                  "主要建材_加強磚造","主要建材_鋼筋混凝土造","主要建材_鋼骨造"
                                    ], index=[0])

    user_list = [ "地址", 
        0, 0, 0, 0, 0, 0,
        0.0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0
        ]

    def __init__(self,apikey):
        self.googlemapapikey = apikey
        self.pre_f = self.pre_f.fillna(0)
        # self.pre_f.iloc[0] = self.user_list
        self.大公園_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="大公園")
        self.公園_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="公園")
        self.小公園_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="小公園")
        self.大綠地_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="大綠地")
        self.小綠地_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="小綠地")
        self.大廣場_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="大廣場")
        self.小廣場_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="小廣場")
        self.博物館_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="博物館")
        self.圖書館_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="圖書館")
        self.捷運出口_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="捷運出口")
        self.幼稚園_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="幼稚園")
        self.國小_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="國小")
        self.國中_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="高中職")
        self.高中職_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="大學")
        self.大學_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="消防大隊")
        self.消防大隊_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="消防中隊")
        self.消防中隊_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="消防分隊")
        self.消防分隊_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="消防分隊")
        self.禮儀_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="禮儀")
        self.警察局_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="警察局")
        self.警察隊_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="警察隊")
        self.派出所_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="派出所")
        self.郵局_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="郵局")
        self.銀行_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="銀行")
        self.證券_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="證券")
        self.信用合作社_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="信用合作社")
        self.醫院_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="醫療醫院")
        self.西醫_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="西醫")
        self.中醫_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="中醫")
        self.藥局_dh = pd.read_excel("設施座標表Ver4.xlsx", sheet_name="藥局")

    def user_input(self,u_address,u_b_type,u_manage,u_floor,u_p_type,u_dist,u_ele,u_age,u_trans,u_tfloor,u_mbm,u_hall,u_room,u_bathroom):
      # 使用者輸入的內容
      # address = "臺北市中山區民生東路三段36號"
      # b_type = "華廈"
      # manage = "有"
      # floor = 3
      # p_type = "無車位"
      # dist = "中山區"
      # ele = "有"
      # age = 30
      # trans = 20.8

      # address = "臺北市萬華區漢口街二段36號"
      # b_type = "華廈"
      # manage = "有"
      # floor = 9
      # p_type = "無車位"
      # dist = "萬華區"
      # ele = "有"
      # age = 10
      # trans = 25.46748

      address = u_address
      b_type = u_b_type
      manage = u_manage
      mbm = u_mbm # 主要建材
      tfloor = u_tfloor #總樓層數
      floor = u_floor
      hall = u_hall   #廳
      room = u_room   #房
      bathroom = u_bathroom #衛
      p_type = u_p_type
      dist = u_dist
      ele = u_ele
      age = u_age
      trans = u_trans

      # 將土地位置建物門牌轉換至表格
      self.pre_f.loc[0,"土地位置建物門牌"] = str(address)

      #================================================
      # 將建物型態轉換至表格
      b_type_dict = {"住宅大樓": "建物型態_住宅大樓", "公寓": "建物型態_公寓",
              "套房": "建物型態_套房", "華廈": "建物型態_華廈",
              }

      b = b_type_dict[b_type]

      if b in self.pre_f.columns.tolist():
        self.pre_f[b] = 1

      #================================================

      # 將有無管理組織轉換至表格
      man_dict = {"有": "有無管理組織_1", "無": "有無管理組織_0"}

      man = man_dict[manage]

      if man in self.pre_f.columns.tolist():
        self.pre_f[man] = 1

      #================================================

      # 將移轉層次轉換至表格
      self.pre_f.at[0, "移轉層次"] = int(floor)

      #================================================

      # 將車位類別轉換至表格
      p_type_dict = {"一樓平面": "車位類別_一樓平面", "升降平面": "車位類別_升降平面", "升降機械": "車位類別_升降機械",
              "坡道平面": "車位類別_坡道平面", "坡道機械": "車位類別_坡道機械", "塔式車位": "車位類別_塔式車位",
              "無車位": "車位類別_無車位"}

      p = p_type_dict[p_type]

      if p in self.pre_f.columns.tolist():
        self.pre_f[p] = 1

      #================================================

      # 將鄉鎮市區轉換至表格
      dist_dict = {"中山區": "鄉鎮市區_中山區", "中正區": "鄉鎮市區_中正區", "信義區": "鄉鎮市區_信義區",
              "內湖區": "鄉鎮市區_內湖區", "北投區": "鄉鎮市區_北投區", "南港區": "鄉鎮市區_南港區",
              "士林區": "鄉鎮市區_士林區", "大同區": "鄉鎮市區_大同區", "大安區": "鄉鎮市區_大安區",
              "文山區": "鄉鎮市區_文山區", "松山區": "鄉鎮市區_松山區", "萬華區": "鄉鎮市區_萬華區",}

      d = dist_dict[dist]

      if d in self.pre_f.columns.tolist():
        self.pre_f[d] = 1
      #================================================
      # 將電梯轉換至表格
      ele_dict = {"有": "電梯_1", "無": "電梯_0"}
      e = ele_dict[ele]

      if e in self.pre_f.columns.tolist():
        self.pre_f[e] = 1
      #================================================
      # 將屋齡轉換至表格
      self.pre_f.at[0, "屋齡"] = int(age)
      #================================================

      # 將建物移轉總坪數轉換至表格
      self.pre_f.at[0, "建物移轉總坪數"] = float(trans)

      #================================================

      # 將 總樓層 轉換至表格
      self.pre_f.at[0, "總樓層數"] = int(tfloor)

      #================================================

      # 將 房 轉換至表格
      self.pre_f.at[0, "建物現況格局-房"] = int(hall)

      #================================================

      # 將 廳 轉換至表格
      self.pre_f.at[0, "建物現況格局-廳"] = int(room)

      #================================================

      # 將 衛 轉換至表格
      self.pre_f.at[0, "建物現況格局-衛"] = int(bathroom)

      #================================================

      # 建物構造
      mbm_dict = {"加強磚造": "主要建材_加強磚造",
                    "鋼筋混凝土造": "主要建材_鋼筋混凝土造",
                    "鋼骨造": "主要建材_鋼骨造", 
                    }
      
      mbm_value = mbm_dict[mbm]

      if mbm_value in self.pre_f.columns.tolist(): 
          self.pre_f[mbm_value] = 1

      return self.pre_f


    # pd.set_option('display.max_columns', 100)
    # pre_f

    def printerror(self,e):
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print(errMsg)

    """# 新增經緯度"""

    def lat_lng(self):
        self.pre_f["緯度"] = 0.0
        self.pre_f["經度"] = 0.0
        # print(f"apikey:{self.googlemapapikey}")
        for i in range(len(self.pre_f)):
            gmaps = googlemaps.Client(key=self.googlemapapikey) # 輸入google maps API 金鑰
            address = self.pre_f["土地位置建物門牌"][i]
            geocode = gmaps.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))
            self.pre_f.at[i, "緯度"] = (lat, lng)[0]
            self.pre_f.at[i, "經度"] = (lat, lng)[1]
            print(address)
            print(lat, lng)
            self.latlng= (lat, lng)
            return self.latlng

    """# 新增設施"""
    def countdeviceandoutput(self,maincenter,dh,deviceradius):
        times = 0
        origin_lat = str(maincenter["緯度"])
        origin_long = str(maincenter["經度"])
        origin = (origin_lat, origin_long)
        # f.writelines(','.join(["名稱", "地址", "lat", "lng"]))
        # f.write('\n')
        df = pd.DataFrame({'名稱': pd.Series(dtype='str'),
                           '地址': pd.Series(dtype='str'),
                           'lat': pd.Series(dtype='float'),
                           'lng': pd.Series(dtype='float')})
        for j in range(len(dh)):
            destination_lat = str(dh["lat"][j])
            destination_long = str(dh["lng"][j])
            destination = (destination_lat, destination_long)
            distance = geopy.distance.geodesic(origin, destination).km
            try:
                if distance <= deviceradius / 1000:
                    times = times + 1
                    # f.writelines(','.join([str(dh["名稱"][j]), str(dh["地址"][j]).replace(',', '_'), destination_lat, destination_long]))
                    # f.write('\n')
                    tmplist = [str(dh["名稱"][j]), str(dh["地址"][j]).replace(',', '_'), dh["lat"][j], dh["lng"][j]]
                    df.loc[len(df)] = tmplist
            except Exception as e:
                self.printerror(e)
        return times,df

    # drive.mount('/content/drive')
    # os.chdir('/content/drive/My Drive/Tibame_03期_第二組團專/整理後的資料/每年每季房屋交易資料') #切換該目錄
    # os.listdir()

    #1.大公園
    def bigpark(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(大公園)"]=radius/1000
      self.pre_f["大公園數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.大公園_dh,radius)
          self.pre_f.at[i,"大公園數量"] = times
      return times,df

    #2.公園
    def park(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(公園)"]=radius/1000
      self.pre_f["公園數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.公園_dh,radius)
          self.pre_f.at[i,"公園數量"] = times
      return times,df

    #3.小公園
    def smallpark(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(小公園)"]=radius/1000
      self.pre_f["小公園數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.小公園_dh,radius)
          self.pre_f.at[i,"小公園數量"] = times
      return times,df

    #4.大綠地
    def biggr(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(大綠地)"]=radius/1000
      self.pre_f["大綠地數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.大綠地_dh,radius)
          self.pre_f.at[i,"大綠地數量"] = times
      return times,df

    #5.小綠地
    def smallgr(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(小綠地)"]=radius/1000
      self.pre_f["小綠地數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.小綠地_dh,radius)
          self.pre_f.at[i,"小綠地數量"] = times
      return times,df

    #6.大廣場
    def bigsq(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(大廣場)"]=radius/1000
      self.pre_f["大廣場數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.大廣場_dh,radius)
          self.pre_f.at[i,"大廣場數量"] = times
      return times,df

    #7.小廣場
    def smallsq(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(小廣場)"]=radius/1000
      self.pre_f["小廣場數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.小廣場_dh,radius)
          self.pre_f.at[i,"小廣場數量"] = times
      return times,df

    # def park2(self):
    #   dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
    #   self.pre_f["固定範圍(公園)"]=3000/1000
    #   self.pre_f["公園數量"]=""
    #   with open('公園座標.poi', 'w',encoding='utf8') as f:
    #       for i in range(len(self.pre_f)):
    #           times = 0
    #           origin_lat = str(self.pre_f["緯度"][i])
    #           origin_long = str(self.pre_f["經度"][i])
    #           origin = (origin_lat, origin_long)
    #           for j in range(len(dh)):
    #               destination_lat = str(dh["lat"][j])
    #               destination_long = str(dh["lng"][j])
    #               destination = (destination_lat, destination_long)
    #               distance=geopy.distance.geodesic(origin, destination).km
    #               try:
    #                   if distance <= 3000/1000:
    #                       times = times + 1
    #                       f.writelines(','.join([str(dh["名稱"][j]),str(dh["地址"][j]),destination_lat, destination_long]))
    #                       f.write('\n')
    #               except Exception as e:
    #                   self.printerror(e)
    #           self.pre_f.at[i,"公園數量"] = times
    #   return times

    #8.博物館
    def mu(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="博物館")
      self.pre_f["固定範圍(博物館)"]=radius/1000
      self.pre_f["博物館數量"]=""
      # with open('博物館座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.博物館_dh,radius)
          self.pre_f.at[i,"博物館數量"] = times
      return times,df

    #9.圖書館
    def lib(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="圖書館")
      self.pre_f["固定範圍(圖書館)"]=radius/1000
      self.pre_f["圖書館數量"]=""
      # with open('圖書館座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.圖書館_dh,radius)
          self.pre_f.at[i,"圖書館數量"] = times
      return times,df

    #10.捷運出口數
    def mrt(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="捷運出口")
      self.pre_f["固定範圍(捷運出口)"]=radius/1000
      self.pre_f["捷運出口數量"]=""
      # with open('捷運出口座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.捷運出口_dh,radius)
          self.pre_f.at[i,"捷運出口數量"] = times
      return times,df

    #11.幼稚園數
    def kinder(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(幼稚園)"]=radius/1000
      self.pre_f["幼稚園數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.幼稚園_dh,radius)
          self.pre_f.at[i,"幼稚園數量"] = times
      return times,df

    #12.國小數
    def ele(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(國小)"]=radius/1000
      self.pre_f["國小數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.國小_dh,radius)
          self.pre_f.at[i,"國小數量"] = times
      return times,df

    #13.國中數
    def jun(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(國中)"]=radius/1000
      self.pre_f["國中數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.國中_dh,radius)
          self.pre_f.at[i,"國中數量"] = times
      return times,df

    #14.高中職
    def sen(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(高中職)"]=radius/1000
      self.pre_f["高中職數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.高中職_dh,radius)
          self.pre_f.at[i,"高中職數量"] = times
      return times,df

    #15.大學
    def coll(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(大學)"]=radius/1000
      self.pre_f["大學數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.大學_dh,radius)
          self.pre_f.at[i,"大學數量"] = times
      return times,df

    #16.消防大隊
    def fireb(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(消防大隊)"]=radius/1000
      self.pre_f["消防大隊數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.消防大隊_dh,radius)
          self.pre_f.at[i,"消防大隊數量"] = times
      return times,df

    #17.消防中隊
    def firem(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(消防中隊)"]=radius/1000
      self.pre_f["消防中隊數量"]=""
      # with open('公園座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.消防中隊_dh,radius)
          self.pre_f.at[i,"消防中隊數量"] = times
      return times,df

    # def edu(self):
    #   # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="學校")
    #   self.pre_f["固定範圍(學校)"]=500/1000
    #   self.pre_f["學校數量"]=""
    #   # with open('學校座標.poi', 'w',encoding='utf8') as f:
    #   for i in range(len(self.pre_f)):
    #       times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.學校_dh,500)
    #       self.pre_f.at[i,"學校數量"] = times
    #   return times,df


    #18.消防分隊
    def fires(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="消防")
      self.pre_f["固定範圍(消防分隊)"]=radius/1000
      self.pre_f["消防分隊數量"]=""
      # with open('消防局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.消防分隊_dh,radius)
          self.pre_f.at[i,"消防分隊數量"] = times
      return times,df

    #19.禮儀
    def dead(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="禮儀")
      self.pre_f["固定範圍(禮儀)"]=radius/1000
      self.pre_f["禮儀數量"]=""
      # with open('禮儀座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.禮儀_dh,radius)
          self.pre_f.at[i,"禮儀數量"] = times
      return times,df

    #20.警察局
    def pold(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="警察")
      self.pre_f["固定範圍(警察局)"]=radius/1000
      self.pre_f["警察局數量"]=""
      # with open('警察局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.警察局_dh,radius)
          self.pre_f.at[i,"警察局數量"] = times
      return times,df

    #21.警察隊
    def polt(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="警察")
      self.pre_f["固定範圍(警察隊)"]=radius/1000
      self.pre_f["警察隊數量"]=""
      # with open('警察局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.警察隊_dh,radius)
          self.pre_f.at[i,"警察隊數量"] = times
      return times,df

    #22.派出所
    def pols(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="警察")
      self.pre_f["固定範圍(派出所)"]=radius/1000
      self.pre_f["派出所數量"]=""
      # with open('警察局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.派出所_dh,radius)
          self.pre_f.at[i,"派出所數量"] = times
      return times,df

    #23.郵局
    def post(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="郵局")
      self.pre_f["固定範圍(郵局)"]=radius/1000
      self.pre_f["郵局數量"]=""
      # with open('郵局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.郵局_dh,radius)
          self.pre_f.at[i,"郵局數量"] = times
      return times,df

    #24.銀行
    def bank(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="金融")
      self.pre_f["固定範圍(銀行)"]=radius/1000
      self.pre_f["銀行數量"]=""
      # with open('金融座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.銀行_dh,radius)
          self.pre_f.at[i,"銀行數量"] = times
      return times,df

    #25.證卷
    def securities(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(證券)"] = radius / 1000
        self.pre_f["證券數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.證券_dh, radius)
            self.pre_f.at[i, "證券數量"] = times
        return times, df

    #26.信用合作社
    def coop(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(信用合作社)"] = radius / 1000
        self.pre_f["信用合作社數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.信用合作社_dh, radius)
            self.pre_f.at[i, "信用合作社數量"] = times
        return times, df

    #27.醫療醫院
    def hosp(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療醫院")
      self.pre_f["固定範圍(醫院)"]=radius/1000
      self.pre_f["醫院數量"]=""
      # with open('醫院座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.醫院_dh,radius)
          self.pre_f.at[i,"醫院數量"] = times
      return times,df

    #28.西醫
    def clinicw(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療診所")
      self.pre_f["固定範圍(西醫)"]=radius/1000
      self.pre_f["西醫數量"]=""
      # with open('診所座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.西醫_dh,radius)
          self.pre_f.at[i,"西醫數量"] = times
      return times,df

    #29.中醫
    def clinice(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療診所")
      self.pre_f["固定範圍(中醫)"]=radius/1000
      self.pre_f["中醫數量"]=""
      # with open('診所座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.中醫_dh,radius)
          self.pre_f.at[i,"中醫數量"] = times
      return times,df

    #30.藥局
    def pharmacy(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療藥局")
      self.pre_f["固定範圍(藥局)"]=radius/1000
      self.pre_f["藥局數量"]=""
      # with open('藥局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.藥局_dh,radius)
          self.pre_f.at[i,"藥局數量"] = times
      return times,df

    def processall(self,radius):
        公園個數, 公園park_df = self.park(500)
        小公園個數, 小公園smallpark_df = self.smallpark(500)
        大公園個數, 大公園bigpark_df = self.bigpark(500)
        小綠地個數, 小綠地smallgr_df = self.smallgr(500)
        大綠地個數, 大綠地biggr_df = self.biggr(500)
        小廣場個數, 小廣場smallsq_df = self.smallsq(500)
        大廣場個數, 大廣場bigsq_df = self.bigsq(500)
        博物館個數, 博物館mu_df = self.mu(500)
        圖書館個數, 圖書館lib_df = self.lib(500)
        捷運出口個數, 捷運出口mrt_df = self.mrt(500)
        幼稚園個數, 幼稚園kinde_df = self.kinder(500)
        國小個數, 國小ele_df = self.ele(500)
        國中個數, 國中jun_df = self.jun(500)
        高中職個數, 高中職sen_df = self.sen(500)
        大學個數, 大學coll_df = self.coll(500)
        消防大隊個數, 消防大隊fireb_df = self.fireb(500)
        消防中隊個數, 消防中隊firem_df = self.firem(500)
        消防分隊個數, 消防分隊fires_df = self.fires(500)
        禮儀個數, 禮儀dead_df = self.dead(500)
        警察局個數, 警察局pold_df = self.pold(500)
        警察隊個數, 警察隊polt_df = self.polt(500)
        派出所個數, 派出所pols_df = self.pols(500)
        郵局個數, 郵局post_df = self.post(500)
        銀行個數, 銀行bank_df = self.bank(500)
        證券個數, 證券securities_df = self.securities(500)
        信用合作社個數, 信用合作社coop_df = self.coop(500)
        醫院個數, 醫院hosp_df = self.hosp(500)
        西醫個數, 西醫clinicw_df = self.clinicw(500)
        中醫個數, 中醫clinice_df = self.clinice(500)
        藥局個數, 藥局phar_df = self.pharmacy(500)

    """# 載入模型進行預測"""

    def pred(self):
        # drop 掉 固定範圍欄位
        cols = [c for c in self.pre_f.columns if not c.lower().startswith('固定範圍')]
        self.pre_f = self.pre_f[cols]

        outputdata1="地址："+ self.pre_f.loc[0, "土地位置建物門牌"]
        經緯度 = self.pre_f.loc[0, ["緯度", "經度"]].values.tolist()
        outputdata2="座標："+','.join(str(x) for x in 經緯度)
        outputdata3="坪數："+str(self.pre_f.loc[0, "建物移轉總坪數"])+" ，"+"屋齡："+str(self.pre_f.loc[0, "屋齡"])

        # data = 公園_data[["lat", "lng"]].values.tolist()
        print(outputdata2)
        print(outputdata3)
        self.pre_f = self.pre_f.drop(["土地位置建物門牌", "緯度", "經度"], axis=1)

        print(self.pre_f.columns)
        # print(self.pre_f.shape)

        reg = pickle.load(open("stacking_121101.sav", "rb"))  # 載入模型
        # print(self.pre_f)
        y_pre = reg.predict(self.pre_f)  # 進行預測

        # print(y_pre)
        # 反正規化處理，求預測價格

        # p_max = 64500000
        # p_min = 5300000

        p_max = 2368756
        p_min = 381733

        p_one_price = (y_pre[0] * (p_max - p_min) + p_min) / 10000 # 預測的價格
        p_total_price=p_one_price*self.pre_f.loc[0, "建物移轉總坪數"]

        outputdata10 = f"單價：{p_one_price:.2f} 萬/坪，總價：{p_total_price:.2f} 萬"
        # print(outputdata10)
        # output="\n".join([outputdata1,outputdata2,outputdata3,outputdata10])
        # return one[0],output
        return p_total_price,outputdata1,outputdata2,outputdata3,outputdata10
        # return p_total_price[0]
        # return '''
        # 輸出內容包含：
        # 1. 預測的價格
        # 2. 單價：  萬/坪
        # 3. 地圖(可顯示使用者輸入的地址)
        # 4. 地圖可呈現某距離(距離可調，以公尺為單位)內的設施位置，設施可供選擇(公園,博物館,圖書館,捷運出口,學校,消防,禮儀,警察,郵局,金融,醫院,診所,藥局)
        # '''

