from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.neural_network import MLPRegressor

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle

class modeltrain04():
    def __init__(self, filename):
        # 載入房屋交易csv檔
        self.df = pd.read_csv(filename, encoding="utf-8")

    def train(self,modelname):
        # drop 掉 固定範圍欄位
        cols = [c for c in self.df.columns if not c.lower().startswith('固定範圍')]
        self.df = self.df[cols]

        x = self.df .drop(["土地位置建物門牌", "總價元", "每坪單價", "每坪單價_正規化", "平均隔間坪數", "緯度", "經度"], axis = 1)  # 訓練特徵
        y = self.df["每坪單價_正規化"]  # 目標(每坪單價_正規化)

        self.dftrain = x.copy()
        print(self.dftrain.columns)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)  # 切分資料
        estimators = [
            ('rf', RandomForestRegressor(random_state=42)),
            ('svr', svm.SVR()),
            ('knn', KNeighborsRegressor()),
            ('dt', DecisionTreeRegressor(random_state=42))
        ]
        clf = StackingRegressor(
            estimators=estimators, final_estimator=MLPRegressor(activation="relu", alpha=0.1, hidden_layer_sizes=(8, 8),
                                                                learning_rate="constant", max_iter=2000,
                                                                random_state=1000)
        )

        clf.fit(x_train, y_train)

        # modelname = "stacking_121101.sav"
        pickle.dump(clf, open(modelname, "wb"))

# 共95欄
# ['建物現況格局-廳', '建物現況格局-房', '建物現況格局-衛', '移轉層次', '總樓層數', '屋齡', '建物移轉總坪數',
      #  '鄉鎮市區_中山區', '鄉鎮市區_中正區', '鄉鎮市區_信義區', '鄉鎮市區_內湖區', '鄉鎮市區_北投區', '鄉鎮市區_南港區',
      #  '鄉鎮市區_士林區', '鄉鎮市區_大同區', '鄉鎮市區_大安區', '鄉鎮市區_文山區', '鄉鎮市區_松山區', '鄉鎮市區_萬華區',
      #  '建物型態_住宅大樓', '建物型態_公寓', '建物型態_套房', '建物型態_華廈', '車位類別_一樓平面', '車位類別_升降平面',
      #  '車位類別_升降機械', '車位類別_坡道平面', '車位類別_坡道機械', '車位類別_塔式車位', '車位類別_無車位',
      #  '有無管理組織_0', '有無管理組織_1', '電梯_0', '電梯_1', '主要建材_加強磚造', '主要建材_鋼筋混凝土造',
      #  '主要建材_鋼骨造', '固定範圍(大公園)', '大公園數量', '固定範圍(公園)', '公園數量', '固定範圍(小公園)',
      #  '小公園數量', '固定範圍(大綠地)', '大綠地數量', '固定範圍(小綠地)', '小綠地數量', '固定範圍(大廣場)',
      #  '大廣場數量', '固定範圍(博物館)', '博物館數量', '固定範圍(圖書館)', '圖書館數量', '固定範圍(捷運出口)',
      #  '捷運出口數量', '固定範圍(幼稚園)', '幼稚園數量', '固定範圍(國小)', '國小數量', '固定範圍(國中)', '國中數量',
      #  '固定範圍(高中職)', '高中職數量', '固定範圍(大學)', '大學數量', '固定範圍(消防大隊)', '消防大隊數量',
      #  '固定範圍(消防中隊)', '消防中隊數量', '固定範圍(消防分隊)', '消防分隊數量', '固定範圍(禮儀)', '禮儀數量',
      #  '固定範圍(警察局)', '警察局數量', '固定範圍(警察隊)', '警察隊數量', '固定範圍(派出所)', '派出所數量',
      #  '固定範圍(郵局)', '郵局數量', '固定範圍(銀行)', '銀行數量', '固定範圍(證券)', '證券數量',
      #  '固定範圍(信用合作社)', '信用合作社數量', '固定範圍(醫院)', '醫院數量', '固定範圍(西醫)', '西醫數量',
      #  '固定範圍(中醫)', '中醫數量', '固定範圍(藥局)', '藥局數量']

