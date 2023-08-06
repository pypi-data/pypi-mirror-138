import os
import sys
import numpy as np
import pickle
from sklearn.model_selection import KFold
import pandas as pd

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

class GetXY():
    """

    """
    def __init__(self):
        pass

    @staticmethod
    def GetCrossXY(x,y,k,random_state=2021,save_path=False):

        kf = KFold(n_splits=k, shuffle=True, random_state=random_state)

        xy_cross_val_list = []

        for train_index,val_index in kf.split(x):

            # 如果y没有进行onehot的话，就只有一列，是array类型。
            if isinstance(y,pd.DataFrame):
                xy_cross_val_list.append((x.iloc[train_index,:],
                                          y.iloc[train_index, :],
                                          x.iloc[val_index, :],
                                          y.iloc[val_index, :],
                                          ))
            else:
                xy_cross_val_list.append((x.iloc[train_index, :],
                                          y[train_index],
                                          x.iloc[val_index, :],
                                          y[val_index],
                                          ))
        if save_path:
            with open(save_path,'wb') as f:
                pickle.dump(xy_cross_val_list,f)

        return xy_cross_val_list

    @staticmethod
    def LoadCrossXY(path):
        with open(path,'rb') as f:
            xy_cross_val_list = pickle.load(f)
            return xy_cross_val_list










