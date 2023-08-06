# 通过封装 train evaluate 来进行基于pytorch的模型训练和保存。
# 提供输出保存以及绘图
# 自动在当前目录生成config

from shutil import copyfile
import os
import time
import pandas as pd
import numpy as np
import torch



class TorchPipline:
    def __init__(self):

        self.config = self.load_config()

        self.epoch_data = pd.DataFrame(
            data=np.zeros(shape=(20000, len(self.config.epoce_data_columns))),
            columns= self.config.epoce_data_columns
        )

    def __train__(self, model, optimizer, dataloder):
        """
        实例化后改写
        """
        pass

    def __loss__(self,pres, labels):
        """
        实例化后改写
        """
        pass

    def load_config(self):
        """
        讲config文件从库文件复制到当前目录，再从当前目录载入。
        这样可以方便查看和修改config
        """
        cur_path = os.path.join(
            os.getcwd(),
            'config_torchpipeline.py'
        )

        ori_path = os.path.join(
            os.path.dirname(os.path.abspath('__file__')),
            'config_torchpipeline.py'
        )

        # 如果在当前目录没有存在config文件，则复制
        if not os.path.exists(cur_path):
            copyfile(ori_path, cur_path)

        # load config 文件
        from . import config_torchpipeline

        return config_torchpipeline

    def __update__(self, update_data):
        """
        每一epoch 更新一次
        更新内容包括： 学习率、是否提前停止训练、保存训练结果、保存模型等
        依据epoch_data判断更新lr，例如学习率衰减。
        """

        # for param_group in optimizer.param_groups:
        #     param_group["lr"] = lr

    def load_model(self, e):
        pass

    def save(self, model, epoch_data):
        pass

    def __evaluate__(self,model,dataloder):
        pass

    def __get_dataloder__(self, mode):
        pass

    def train(self, model, optimizer, epoch, dataloder, breakpoint=-1, test=False):
        """
        breakpoint = 3, 则加载3的权值，从4开始训练。
        """

        for e in range(epoch):

            t = time.time()

            # 断点之前不训练
            if e <= breakpoint:
                continue

            # 到断点下一个epoch的的时候，载入断点权值
            elif e == breakpoint + 1:
                # 如果断点是-1，则e=0,是第一个epoch，则不载入权值
                if e != 0:
                    model = self.load_model(breakpoint)


            # 训练
            model = self.__train__(model, optimizer, dataloder)



            # 模型结果评估
            train_loss, train_eva = self.__evaluate__(model, self.__get_dataloder__('train'))
            dev_loss, dev_eva = self.__evaluate__(model, self.__get_dataloder__('dev'))

            if test:
                test_loss, test_eva = self.__evaluate__(model, self.__get_dataloder__('test'))
            else:
                test_loss, test_eva = 'None', 'None'



            # 根据训练结果更新参数
            update_data = {
                'epoch': e,
                'train_loss': train_loss,
                'train_eva': train_eva,
                'dev_loss': dev_loss,
                'dev_eva': dev_eva,
                'test_loss': test_loss,
                'test_eva': test_eva,
                'lr': optimizer.param_groups[0]['lr']
            }

            optimizer = self.__update__(update_data)

            # 保存训练结果和模型

            torch.save(model.state_dict(), self.save.format(e))



