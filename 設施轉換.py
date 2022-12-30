import pandas as pd
import geopy.distance
import sys
import traceback

class facilitytransform03():
    def __init__(self, filename):
        # 載入房屋交易csv檔
        self.pre_f = pd.read_csv(filename, encoding="utf-8")

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

    #1.大公園
    def bigpark(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
      self.pre_f["固定範圍(大公園)"]=radius/1000
      self.pre_f["大公園數量"]=""
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.大公園_dh,radius)
          self.pre_f.at[i,"大公園數量"] = times
      return times,df

    # 2.公園
    def park(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(公園)"] = radius / 1000
        self.pre_f["公園數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.公園_dh, radius)
            self.pre_f.at[i, "公園數量"] = times
        return times, df

    # 3.小公園
    def smallpark(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(小公園)"] = radius / 1000
        self.pre_f["小公園數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.小公園_dh, radius)
            self.pre_f.at[i, "小公園數量"] = times
        return times, df

    # 4.大綠地
    def biggr(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(大綠地)"] = radius / 1000
        self.pre_f["大綠地數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.大綠地_dh, radius)
            self.pre_f.at[i, "大綠地數量"] = times
        return times, df


    # 5.小綠地
    def smallgr(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(小綠地)"] = radius / 1000
        self.pre_f["小綠地數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.小綠地_dh, radius)
            self.pre_f.at[i, "小綠地數量"] = times
        return times, df

    # 6.大廣場
    def bigsq(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(大廣場)"] = radius / 1000
        self.pre_f["大廣場數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.大廣場_dh, radius)
            self.pre_f.at[i, "大廣場數量"] = times
        return times, df

    # 7.小廣場
    def smallsq(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(小廣場)"] = radius / 1000
        self.pre_f["小廣場數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.小廣場_dh, radius)
            self.pre_f.at[i, "小廣場數量"] = times
        return times, df

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

    # 11.幼稚園數
    def kinder(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(幼稚園)"] = radius / 1000
        self.pre_f["幼稚園數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.幼稚園_dh, radius)
            self.pre_f.at[i, "幼稚園數量"] = times
        return times, df
    
    # 12.國小數
    def ele(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(國小)"] = radius / 1000
        self.pre_f["國小數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.國小_dh, radius)
            self.pre_f.at[i, "國小數量"] = times
        return times, df
    
    # 13.國中數
    def jun(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(國中)"] = radius / 1000
        self.pre_f["國中數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.國中_dh, radius)
            self.pre_f.at[i, "國中數量"] = times
        return times, df
    
    # 14.高中職
    def sen(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(高中職)"] = radius / 1000
        self.pre_f["高中職數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.高中職_dh, radius)
            self.pre_f.at[i, "高中職數量"] = times
        return times, df
    
    # 15.大學
    def coll(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(大學)"] = radius / 1000
        self.pre_f["大學數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.大學_dh, radius)
            self.pre_f.at[i, "大學數量"] = times
        return times, df
    
    # 16.消防大隊
    def fireb(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(消防大隊)"] = radius / 1000
        self.pre_f["消防大隊數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.消防大隊_dh, radius)
            self.pre_f.at[i, "消防大隊數量"] = times
        return times, df
    
    # 17.消防中隊
    def firem(self,radius):
        # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="公園")
        self.pre_f["固定範圍(消防中隊)"] = radius / 1000
        self.pre_f["消防中隊數量"] = ""
        # with open('公園座標.poi', 'w',encoding='utf8') as f:
        for i in range(len(self.pre_f)):
            times, df = self.countdeviceandoutput(self.pre_f.loc[i], self.消防中隊_dh, radius)
            self.pre_f.at[i, "消防中隊數量"] = times
        return times, df

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
      self.pre_f["固定範圍(西醫)"]=500/1000
      self.pre_f["西醫數量"]=""
      # with open('診所座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.西醫_dh,radius)
          self.pre_f.at[i,"西醫數量"] = times
      return times,df

    #29.中醫
    def clinice(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療診所")
      self.pre_f["固定範圍(中醫)"]=500/1000
      self.pre_f["中醫數量"]=""
      # with open('診所座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.中醫_dh,radius)
          self.pre_f.at[i,"中醫數量"] = times
      return times,df

    #30.藥局
    def pharmacy(self,radius):
      # dh = pd.read_excel("設施座標表Ver2.xlsx", sheet_name="醫療藥局")
      self.pre_f["固定範圍(藥局)"]=500/1000
      self.pre_f["藥局數量"]=""
      # with open('藥局座標.poi', 'w',encoding='utf8') as f:
      for i in range(len(self.pre_f)):
          times,df=  self.countdeviceandoutput(self.pre_f.loc[i],self.藥局_dh,radius)
          self.pre_f.at[i,"藥局數量"] = times
      return times,df
    #主程式
    def processall(self):
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

    def savecsv(self, filename):
        """# 儲存檔案"""
        # 目前剩下的欄位 ['主要建材', '土地位置建物門牌', '建物型態', '建物現況格局-廳', '建物現況格局-房', '建物現況格局-衛',
        #  '有無管理組織', '移轉層次', '總價元', '總樓層數', '車位類別', '鄉鎮市區', '電梯', '屋齡', '建物移轉總坪數', 經度, 緯度
        # f.columns
        self.pre_f.to_csv(filename, encoding="utf_8_sig", index=False)
