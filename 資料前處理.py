import os
import pandas as pd

class dataprepare01():
    def __init__(self, apikey):
        self.googlemapapikey = apikey
        self.loadrawdata()

    def loadrawdata(self):
        dirs = [d for d in os.listdir('datas') if d.startswith('real_') and d.endswith('csv')]
        dfs = []
        for d in dirs:
            # print(d)
            fname=os.path.join('datas',d,'a_lvr_land_a.csv')
            # print(fname)
            if not os.path.exists(fname):
              print(f"{fname} 不存在")
              continue
            df = pd.read_csv(fname, index_col=False)
            dfs.append(df.iloc[1:])
        self.df = pd.concat(dfs, sort=True)

    def drop備註(self):
        self.df = self.df[self.df['備註'].isnull()] # 刪除有備註的欄位
        self.df = self.df.reset_index(drop=True)

    def extract交易年(self):
        # 將交易年份取出，新增到交易年欄位
        self.df ["交易年"] = 0
        for i in range(len(self.df)):
          if len(self.df ["交易年月日"][i]) == 7:
            self.df.at[i, "交易年"] = self.df["交易年月日"][i][0:3]
          elif len(self.df["交易年月日"][i]) == 6:
            self.df.at[i, "交易年"] = self.df["交易年月日"][i][0:2]

        self.df['交易年'] = self.df['交易年'].astype('int')
        # 去除交易年為0的欄位

        # for i in range(len(self.df)):
        #   if self.df["交易年"][i] == 0:
        #     self.df = self.df.drop(i)
        self.df = self.df.reset_index(drop=True)

    def filter近期年份(self):
        """# 保留2016~ 的數據"""
        # print(self.df.shape)
        self.df['交易年'] = self.df['交易年'].astype('int')
        self.df = self.df[self.df["交易年"] >= 105]
        self.df = self.df.reset_index(drop=True)
        # print(self.df.shape)
        # for i in range(len(self.df)):
        #   # if int(self.df["交易年"][i]) not in range(105, 111):
        #   if (self.df["交易年"][i]< 105):
        #     self.df = self.df.drop(i)
        #
        # self.df= self.df.reset_index(drop=True)

    def prepare建築年(self):
        """# 處理建築完成年月"""
        # 如果有的話，將建築完成年份取出，新增到建築年欄位
        self.df["建築年"] = 0
        # self.df["建築完成年月"] = self.df["建築完成年月"].astype('string')
        for i in range(len(self.df)):
            if self.df["建築完成年月"].isna()[i] == False:
                if len(self.df.at[i,"建築完成年月"]) == 7:
                  self.df.at[i, "建築年"] =int( self.df.at[i,"建築完成年月"][0:3])
                elif len(self.df["建築完成年月"][i]) == 6:
                  self.df.at[i, "建築年"] =int( self.df.at[i,"建築完成年月"][0:2])

        self.df['建築年'] = self.df['建築年'].astype('int')
        # 將建築年=0的值帶入建築年的中位數
        for i in range(len(self.df)):
          if self.df.at[i,"建築年"] == 0:
            self.df.at[i, "建築年"] = self.df["建築年"].median()

    def insert屋齡(self):
        """# 新增屋齡"""
        # 新增屋齡欄位，並將交易年-建築年，得到屋齡
        self.df["屋齡"] = 0
        for i in range(len(self.df)):
          self.df.at[i, "屋齡"] = 111 - int(self.df["建築年"][i])

        # 去除屋齡<0的房屋
        for i in range(len(self.df)):
          if self.df["屋齡"][i] <= 0:
            self.df = self.df.drop(i)

        self.df = self.df.reset_index(drop=True)

    def drop不必要欄位(self):
        """# 移除不必要欄位
        [單價元平方公尺]只有算住的地方；[總價元]是有含車位價格
        """
        # 移除交易標的 土地
        self.df = self.df[self.df["交易標的"] != "土地"]
        # 重設index
        self.df = self.df.reset_index(drop=True)
        # 移除交易標的 車位
        self.df = self.df[self.df["交易標的"] != "車位"]
        # 重設index
        self.df = self.df.reset_index(drop=True)
        # 移除不必要欄位
        self.df = self.df.drop([
                "土地移轉總面積平方公尺","交易標的", "都市土地使用分區",
                "非都市土地使用分區", "非都市土地使用編定", "交易筆棟數",
                "建物現況格局-隔間", "車位移轉總面積(平方公尺)",
                "車位總價元", "主建物面積", "附屬建物面積", "陽台面積",
                "備註", "移轉編號", "編號", "交易年月日", "建築完成年月",
                "交易年", "建築年"
                ], axis = 1)

    def process住家用(self):
        """# 留下主要用途為住家用"""
        for i in range(len(self.df)):
          if self.df["主要用途"][i] != "住家用":
            self.df = self.df.drop(i)
        self.df = self.df.reset_index(drop=True)
        self.df = self.df.drop(["主要用途"], axis=1)

    def process車位(self):
        """# 處理車位類別"""
        self.df["車位類別"] = self.df["車位類別"].fillna("無車位")
        for i in range(len(self.df)):
          if self.df["車位類別"][i] == "其他":
            self.df = self.df.drop(i)
        self.df = self.df.reset_index(drop=True)

    tf_dict = {"有": 1, "無": 0}
    """# 處理TF欄位(有無管理組織、電梯)"""
    def process電梯(self):
        self.df["電梯"] = self.df["電梯"].fillna(0)
        # 將電梯轉成0和1
        self.df = self.df.replace({"電梯": self.tf_dict})

    def process管委會(self):
        self.df["有無管理組織"] = self.df["有無管理組織"].fillna(0)
        # 將有無管理組織轉成0和1
        self.df = self.df.replace({"有無管理組織": self.tf_dict})

    def process平方公尺轉為坪(self):
        """# 將平方公尺轉為坪"""
        for i in range(len(self.df)):
          self.df.at[i, "建物移轉總坪數"] = float(self.df["建物移轉總面積平方公尺"][i]) * 0.3025

        self.df = self.df.drop(["建物移轉總面積平方公尺", "單價元平方公尺"], axis=1)

    def process建物型態(self):
        """# 處理建物型態"""
        # 保留四類建築型態
        list = ["住宅大樓(11層含以上有電梯)", "華廈(10層含以下有電梯)", "公寓(5樓含以下無電梯)", "套房(1房1廳1衛)"]
        for i in range(len(self.df )):
          if self.df["建物型態"][i] not in list:
            self.df = self.df.drop(i)
        self.df = self.df.reset_index(drop=True)

    def process樓層(self):
        """# 處理樓層"""
        column_dict = {"--":None, "":None, None:0, '陽台':1, '平台':1, '屋頂突出物':1, '夾層':1,
                '電梯樓梯間':1, '騎樓':1, '陽臺':1, '地下三層':0, '地下二層':0, '地下一層':0, '地下層':0, '全':100,
                '一層':1, '二層':2, '三層':3, '四層':4, '五層':5, '六層':6, '七層':7, '八層':8, '九層':9, '十層':10,
                '十一層':11, '十二層':12, '十三層':13, '十四層':14, '十五層':15, '十六層':16, '十七層':17, '十八層':18,
                '十九層':19, '二十層':20, '二十一層':21, '二十二層':22, '二十三層':23, '二十四層':24, '二十五層':25,
                '二十六層':26, '二十七層':27, '二十八層':28, '二十九層':29, '三十層':30, '三十一層':31, '三十二層':32,
                '三十三層':33, '三十四層':34, '三十五層':35, '三十六層':36, '三十七層':37, '三十八層':38, '三十九層':39,
                '四十層':40, '四十一層':41, '四十二層':42, '四十三層':43, '四十四層':44, '四十五層':45, '四十六層':46,
                '四十七層':47, '四十八層':48, '四十九層':49, '五十層':50}

        # 留下只交易一層的房屋
        for i in range(len(self.df)):
          if len(self.df["移轉層次"][i].split("，")) > 1:
            self.df = self.df.drop(i)

        self.df = self.df.reset_index(drop=True)
        self.df = self.df.replace({"移轉層次": column_dict})
        self.df = self.df.replace({"總樓層數": column_dict})

    def process主要建材(self):
        """# 處理主要建材"""
        self.df["主要建材"].unique()
        cons_list = ["鋼筋混凝土造", "加強磚造", "鋼骨造"]

        for i in range(len(self.df)):
          if self.df["主要建材"][i] not in cons_list:
            self.df = self.df.drop(i)
        self.df = self.df.reset_index(drop=True)


    def process行政區域(self):
        """# 新增經度緯度欄位"""
        # 修正地址跟鄉鎮市區不同的欄位
        for i in range(len(self.df)):
          if self.df["土地位置建物門牌"][i][0:3] == "臺北市":
            if self.df["土地位置建物門牌"][i][3:6] != self.df["鄉鎮市區"][i]:
              self.df.at[i, "鄉鎮市區"] = self.df["土地位置建物門牌"][i][3:6]

        # 補上臺北市+行政區
        for i in range(len(self.df)):
          if self.df["土地位置建物門牌"][i][0:3] != "臺北市":
            self.df.at[i, "土地位置建物門牌"] = "臺北市" + self.df["鄉鎮市區"][i] + self.df["土地位置建物門牌"][i]

    def insert經緯度(self):
        """# 地址轉經緯度"""
        # 地址轉經緯度
        import googlemaps

        self.df["緯度"] = 0.0
        self.df["經度"] = 0.0

        for i in range(len(self.df)):
          gmaps = googlemaps.Client(key=self.googlemapapikey)   # 輸入google maps API 金鑰
          address = self.df["土地位置建物門牌"][i]
          geocode = gmaps.geocode(address=address)
          (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

          self.df.at[i,"緯度"] = (lat, lng)[0]
          self.df.at[i,"經度"] = (lat, lng)[1]

    def processall(self):
        # self.loadrawdata()
        self.drop備註()
        self.extract交易年()
        self.filter近期年份()
        self.prepare建築年()
        self.insert屋齡()
        self.drop不必要欄位()
        self.process住家用()
        self.process車位()
        self.process管委會()
        self.process平方公尺轉為坪()
        self.process建物型態()
        self.process樓層()
        self.process主要建材()
        self.process行政區域()
        self.insert經緯度()

    def savecsv(self,filename):
        """# 儲存檔案"""
        # 目前剩下的欄位 ['主要建材', '土地位置建物門牌', '建物型態', '建物現況格局-廳', '建物現況格局-房', '建物現況格局-衛',
              #  '有無管理組織', '移轉層次', '總價元', '總樓層數', '車位類別', '鄉鎮市區', '電梯', '屋齡', '建物移轉總坪數', 經度, 緯度
        # f.columns
        self.df.to_csv(filename, encoding="utf_8_sig", index=False)
        # self.df.to_csv("/content/drive/My Drive/Tibame_03期_第二組團專/整理後的資料/每年每季房屋交易資料/台北市房屋交易_model_1205_未正規化.csv", encoding="utf-8", index=False)

