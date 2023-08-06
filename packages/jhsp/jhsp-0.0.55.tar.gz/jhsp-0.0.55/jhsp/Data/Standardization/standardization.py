import pandas as pd


class StandardizeSym():
    def __init__(self,config_path):
        self.config = {}
        data = pd.read_excel(config_path,header=0)
        for row in range(data.shape[0]):
            if not pd.isna(data.loc[row,'标准化症状']):
                self.config[data.loc[row,'原症状']] = ','.join(data.loc[row,'标准化症状'].split('；'))
            else:
                self.config[data.loc[row, '原症状']] = data.loc[row, '原症状']

    def StandardizeSyms(self,syms_list):
        config = self.config.copy()
        fail_syms = set(syms_list) - set(config.keys())


        if fail_syms:
            for i in fail_syms:
                config[i] = i

        standardize_syms_list = [config[sym] for sym in syms_list]
        return standardize_syms_list,list(fail_syms)



class StandardizeDiags():
    def __init__(self, config_path):

        self.all = []
        data = pd.read_excel(config_path, header=0)
        elements_dict = data.to_dict()
        for i_dict in elements_dict.values():
            self.all.extend(list(i_dict.values()))

        self.k = list(data.loc[:,'证基空间'])
        self.w = list(data.loc[:, '证基物质'])
        self.y = list(data.loc[:, '证基运动'])



    def StandardizeDiag(self, diags,sep='|',mode='all'):
        diag_list = str(diags).split(sep)

        if mode == 'all':
            config = self.all.copy()
        elif mode =='k':
            config = self.k.copy()
        elif mode =='w':
            config = self.w.copy()
        elif mode =='y':
            config = self.y.copy()
        else:
            config = self.all.copy()

        temp_list = []


        for i in range(len(diag_list)):
            for element in config:
                element = str(element)
                if element in diag_list[i]:
                    temp_list.append(element)
                    diag_list[i] = diag_list[i].replace(element,'')


        #返回分割后的三基元素列表；剩余的未能成功标准化分割的列表
        return temp_list,diag_list

