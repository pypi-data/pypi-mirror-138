from jhsp.FunTools.my_split import split


def split_list(ori_list,sep_list):
    temp_list = []
    for i in ori_list:
         temp_list.extend(split(str(i),sep_list))
    return temp_list

