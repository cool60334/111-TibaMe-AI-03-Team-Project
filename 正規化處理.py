import csv
import pandas as pd
import os
import numpy as np
from sklearn import preprocessing

class dataprepare02():
  def __init__(self,filename):
    self.df = pd.read_csv(filename, encoding = "utf-8")

  def drop套房異常值(self):
    """# 去除異常值"""
    # 去除套房坪數 < 5 坪
    # self.df['建物移轉總坪數'] = self.df['建物移轉總坪數'].astype('float')
    for i in range(len(self.df)):
      if self.df["建物型態"][i] == "套房(1房1廳1衛)":
        if self.df["建物移轉總坪數"][i] < 5.0:
          self.df = self.df.drop(i)

    self.df = self.df.reset_index(drop=True)

  def drop非套房異常值(self): #非套房且小於10坪且屋齡>35
    # 去除非套房坪數 < 10 坪 且 屋齡大於35
    for i in range(len(self.df)):
      if self.df["建物型態"][i] != "套房(1房1廳1衛)":
        if (self.df["建物移轉總坪數"][i] < 10.0) and (self.df["屋齡"][i] > 35):
          self.df = self.df.drop(i)

    self.df = self.df.reset_index(drop=True)

  def drop非房廳交易異常值(self):
    for i in range(len(self.df)):
      if (self.df["建物現況格局-房"][i] == 0) and (self.df["建物現況格局-廳"][i] == 0):
          self.df = self.df.drop(i)

    self.df = self.df.reset_index(drop=True)

  def drop平均坪數太低異常值(self):
    # 計算平均隔間坪數
    for i in range(len(self.df)):
      self.df.at[i, "平均隔間坪數"] = self.df["建物移轉總坪數"][i] / (self.df["建物現況格局-廳"][i] + self.df["建物現況格局-房"][i])

    # 去除平均隔間坪數 < 3
    for i in range(len(self.df)):
      if self.df["平均隔間坪數"][i] < 3.0:
        self.df = self.df.drop(i)
    self.df = self.df.reset_index(drop=True)

  def drop每坪單價極值(self):
    """# 去除每坪單價極值"""
    # 計算每坪單價
    self.df["每坪單價"] = self.df["總價元"] / self.df["建物移轉總坪數"]
    # sns.set(rc={'figure.figsize':(10,10)})
    # sns.distplot(df["每坪單價"], bins=50)
    # plt.show()

    p4 = self.df["每坪單價"].quantile(0.04)
    p995 = self.df["每坪單價"].quantile(0.995)
    # 去除大於第995分位數的值
    for i in range(len(self.df)):
      if self.df["每坪單價"][i] > p995:
        df = self.df.drop(i)

    self.df = self.df.reset_index(drop=True)
    # 去除小於第4分位數的值
    for i in range(len(self.df)):
      if self.df["每坪單價"][i] < p4:
        self.df = self.df.drop(i)

    self.df = self.df.reset_index(drop=True)

  def MaxMin正規化處理(self):
    """ Max Min 正規化處理 """
    minmax = preprocessing.MinMaxScaler()
    # " 每坪單價 Max Min 正規化處理 "
    # df["每坪單價_正規化"] = 0.0
    values = self.df['每坪單價'].values
    values = values.reshape((len(values), 1))
    self.df["每坪單價_正規化"] = minmax.fit_transform(values)

  def one_hotencoding(self):
    """# one-hot encoding
    類別值:鄉鎮市區、交易標的、都市土地使用分區、建物型態、主要用途、主要建材、有無管理組織、車位類別、電梯
    """
    """ One-Hot Encoding """
    self.df = pd.get_dummies(self.df, columns = ["鄉鎮市區", "建物型態", "車位類別", "有無管理組織", "電梯", "主要建材"])
    # 將建物型態欄位重新命名
    self.df = self.df.rename(columns={"建物型態_住宅大樓(11層含以上有電梯)": "建物型態_住宅大樓", "建物型態_公寓(5樓含以下無電梯)": "建物型態_公寓",
                            "建物型態_套房(1房1廳1衛)": "建物型態_套房", "建物型態_華廈(10層含以下有電梯)": "建物型態_華廈"})

  def processall(self):
    self.drop套房異常值()
    self.drop非套房異常值()
    self.drop非房廳交易異常值()
    self.drop平均坪數太低異常值()
    self.drop每坪單價極值()
    self.MaxMin正規化處理()
    self.one_hotencoding()

  def savecsv(self, filename):
    """# 儲存檔案"""
    # 目前剩下的欄位 ['主要建材', '土地位置建物門牌', '建物型態', '建物現況格局-廳', '建物現況格局-房', '建物現況格局-衛',
    #  '有無管理組織', '移轉層次', '總價元', '總樓層數', '車位類別', '鄉鎮市區', '電梯', '屋齡', '建物移轉總坪數', 經度, 緯度
    # f.columns
    self.df.to_csv(filename, encoding="utf_8_sig", index=False)
