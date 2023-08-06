# -*- coding: utf-8 -*-
from functools import wraps
from collections.abc import Iterable
import sys
import math
import warnings
import tqdm


# test multiprocessing decorator
# 带参数的装饰器的实现方法是再包裹一层函数，来返回装饰器：装饰器生成器（最外层函数）-函数生成器（装饰器）—函数（原函数）

def mp(pool_size=5, batch_size=1, how='process', require_return=False):
    """
    多进程任务，抽象一下，就是一系列参数，得到一系列结果，或者不需要结果。
    原函数的可迭代对象必须是第一个参数
    """

    if how == 'process':
        from multiprocessing import Process, Queue
    elif how == 'thread':
        from multiprocessing.dummy import Process, Queue

    def outer_func(func):

        @wraps(func)
        def decorated_func(*args, **kwargs):

            # 限制参数
            if len(args) != 0:
                raise Exception('期待只接受关键字参数，您可能需要先更改函数参数设计')

            iter_num = 0
            iter_key = list(kwargs.keys())[0]
            for key in kwargs.keys():
                if isinstance(kwargs[key], Iterable):
                    iter_num += 1

            if iter_num < 1:
                raise Exception('未接受到可迭代参数，您可能不需要使用本装饰器')

            elif iter_num > 1:
                warnings.warn('接受到{}个可迭代参数，请确保只通过多进程迭代第一个。'.format(iter_num))

            # 解决报错问题，将原函数注册到__main__中
            func_name = decorated_func.__dict__['__wrapped__']
            sys.modules['__main__'].__dict__[func_name] = decorated_func.__dict__['__wrapped__']

            # 初始化相关数据
            q = Queue(pool_size)
            p_list = []

            if require_return:
                outcome = ['之前生成的' for _ in range(len(kwargs[iter_key]))]
            else:
                outcome = None

            def update_outcome(_start, _stop, _batch_outcome):

                if require_return:
                    for index in range(start, stop):
                        outcome[index] = batch_outcome[index - start]

            # 构造batch_kwarg，并生成batch_p
            batch_num = math.ceil(len(kwargs[iter_key]) / batch_size)

            #
            for batch_index in range(batch_num):

                start = batch_index * batch_size
                stop = (batch_index + 1) * batch_size

                # 如果是最后一个batch或唯一一个batch（batch_size>迭代参数数量时）
                if batch_index == batch_num - 1 or stop > len(kwargs[iter_key]):
                    stop = len(kwargs[iter_key])

                batch_kwarg = kwargs.copy()
                batch_kwarg[iter_key] = kwargs[iter_key][start:stop]

                def batch_func(start_, stop_, batch_kwarg_):
                    batch_outcome_ = func(**batch_kwarg_)
                    q.put((start_, stop_, batch_outcome_))

                p = Process(target=batch_func, args=(start, stop, batch_kwarg))

                p_list.append(p)

            pbar = tqdm.tqdm(
                total=len(kwargs[iter_key]),
                desc='pool_size:{}, batch_size:{} 全局进度'.format(pool_size, batch_size)
            )

            for pi in range(len(p_list)):  # 有多少个子进程，就有多少个返回值

                # 进程池未满的时候，启动子进程。
                if pi < pool_size:
                    p_list[pi].start()

                    # 如果进程池未满就运行完了全部子进程,则每有一个进程运行完毕，就更新一次结果，结束循环。
                    if pi == len(p_list) - 1:
                        for pi_ in range(len(p_list)):
                            p_list[pi_].join()
                            start, stop, batch_outcome = q.get()
                            update_outcome(start, stop, batch_outcome)
                            pbar.update(batch_size)
                        break

                    else:
                        continue

                # 阻塞直到取一个结果，表面一个子进程运行完毕。再启动一个子进程
                start, stop, batch_outcome = q.get()
                update_outcome(start, stop, batch_outcome)
                pbar.update(batch_size)
                p_list[pi].start()

            # 在进程池未满的时候，只启动了进程，没有取值，因此，进程池大小个值没有被取到
            for i in range(pool_size):
                start, stop, batch_outcome = q.get()
                update_outcome(start, stop, batch_outcome)
                pbar.update(batch_size)

            if require_return:
                return outcome

        return decorated_func

    return outer_func


if __name__ == '__main__':

    arg3 = [4, 5, 6, 7, 8]

    @mp(1, 1, require_return=True)
    def demo_func(iter_arg):
        """
        原函数
        """
        out = []
        for i in iter_arg:
            # print(i)
            out.append(i)
        return out

    a = demo_func(iter_arg=arg3)
    print(a)
