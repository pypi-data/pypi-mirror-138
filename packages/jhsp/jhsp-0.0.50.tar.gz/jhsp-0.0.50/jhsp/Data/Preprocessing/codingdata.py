import pandas as pd
import os
import warnings
import sys
import tqdm

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

# 因为在进行编码的时候，会对一些汉字描述的特征进行编码，如：轻度编码为1，重度编码为2。
# 在进行DataFrame的筛选时，就会出现比较 汉字str与编码int的情况，因此会出现警告信息。
# 这个警告信息可以忽略。
warnings.filterwarnings(action='ignore',message='elementwise comparison failed')

class CodingData():
    """
    这是一个编码数据的类，包括将one数据转换为onehot数据，将onehot数据转化为one数据，编码分类信息，编码等级信息等。
    本类中所有函数的参数都以列表形式传入。
    """
    def __init__(self):
        pass

    def onehot2one(self,onehot_data_):

        if not isinstance(onehot_data_,pd.DataFrame):
            onehot_data = pd.DataFrame(onehot_data_)
        else:
            onehot_data = onehot_data_
            onehot_data.columns = [i for i in range(onehot_data.shape[1])]


        onehot_data['one@#$%^'] = 0

        for row in range(onehot_data.shape[0]):

            onehot_data.iloc[row,-1] = int(onehot_data.iloc[row,:].idxmax()) + 1


        return  onehot_data['one@#$%^']

    @staticmethod
    def one2onehot(data,column_name):
        """
        这个函数将一列，转化为onehot编码的多列
        :param one_columns:
        :return:
        """

        data = data.copy()

        # 将这个列的值作为转化后onehot列的列名
        columns = set(data.loc[:,column_name].values.flatten())
        new_columns = []

        for column in columns:   # 遍历每一个将要新建的onehot列名

            new_column = column_name + str(column) # 为了便于区分，onehot列名之前要加上原列的列名
            new_columns.append(new_column)

            # 用定义的列名，新建一个onehot列，其值为0
            data.loc[:,new_column] = pd.Series([0 for i in range(data.shape[0])])

            # 筛选出原列中，值为新建列列名的行，在新建列中将该行赋值为1
            data.loc[data[column_name]==column,new_column] = 1

        data.drop(column_name, axis=1, inplace=True)

        return data,data.loc[:,new_columns]

    def grades22(self,regulations):
        """
        本函数是将分级数据转化为二分类数据，参数是转化规则，本质是一个列表，列表元素是元组如：【（‘轻度’，0），（“重度”，1）】

        """
        # 遍历所有列
        for column in self.data.columns.values:
            for item in regulations:
                # 对每一列，遍历规则，改为2分类数据
                self.data.loc[self.data[column] == item[0],[column]] = item[1]

    def coding_y(self,y_column):
        """
        本函数功能是将y进行编码，并将编码关系储存到数据目录下。参数为一个列表：【‘列名’】
        :param y_column:
        :return:
        """
        y_names = set(self.data.loc[:, y_column].values.flatten())

        coded_relationship = []
        for i,y_name in enumerate(y_names):
            self.data.loc[self.data[y_column[0]]==y_name,[y_column[0]]] = i
            coded_relationship.append((i, y_name))

        save_dir = os.path.join(self.save_dir,'coded_relationship.txt')
        with open(save_dir,'w',encoding='utf-8') as f:
            for item in coded_relationship:
                f.write(str(item[0]) + ': ' + item[1] + '\n')

    @staticmethod
    def content2features(data,content_column_name,sep=','):

        # 获取所有的特征列表
        features_list = []
        for row in range(data.shape[0]):
            features_list.extend(data.loc[row,content_column_name].split(sep=sep))

        features_list = list(set(features_list))

        try:
            features_list.remove('')
        except ValueError:
            pass

        # 生cheng特征列，默认值为0
        for feature in features_list:
            data[str(feature)] = 0


        #
        for row in tqdm.tqdm(range(data.shape[0])):
            row_features_list =  data.loc[row, content_column_name].split(sep=sep)
            for row_feature in row_features_list:
                data.loc[row,row_feature] = 1


        del data[content_column_name]


        return data,data.loc[:,features_list],features_list

    def save(self):
        self.data.to_excel(self.save_path,index=False)


    def ML22classification(self,data,content_column_name,sep=','):
        temp_data = data.copy()

        # 获取所有的特征列表
        features_list = []
        for row in range(temp_data.shape[0]):
            features_list.extend(temp_data.loc[row, content_column_name].split(sep=sep))

        features_list = list(set(features_list))

        twoclassification_dict = {}
        for feature in features_list:
            temp_data[str(feature)] = 0
            for row in range(temp_data.shape[0]):
                if feature in temp_data.loc[row, content_column_name]:
                    temp_data.loc[row, str(feature)] = 1

            twoclassification_dict[str(feature)] = temp_data.loc[:,feature]

        return twoclassification_dict