import getopt
import sys
import threading
import time
import subprocess



def load_config(config_file, args_dict, cmd, load_time=1, inplace=False):
    """
    一个用于从命令行获取参数，更新配置的命令。
    config_file:配置文件路径
    args_dict:需要动态加载的配置字典，如 {'user':'-u','port':'-p'}
    cmd:动态加载配置后执行的命令
    load_time: 配置需要被加载的次数，默认为1. django需要加载两次
    inplace：执行命令后是否保留配置的改变。BOOL类型
    """

    args = ':'.join(list(args_dict.values()))
    args += ':'     # 最后一个参数没有’：‘，所以要加上

    opts = getopt.getopt(sys.argv[1:], args)
    opts = {i[0]: i[1] for i in opts[0]}

    new_config_data = ''
    old_config_data = ''
    with open(config_file, 'r', encoding='utf-8') as f:
        for l in f.readlines():

            old_config_data += l

            for key in args_dict.keys():
                if key in l:
                    _l = l.replace(' ', '')
                    if key+'=' in _l and key+'==' not in _l:   # 排除对参数的判断行,且只匹配赋值行
                        l = "{} = '{}'".format(key, opts[args_dict[key]]) + '\n'
                        break

            new_config_data += l

    # 在new_config_data 末尾增加  在本文件追加一段特殊字符的行，以在文件被加载后确保其被访问（python导入模块，模块的访问时间不改变）
    mark = '##*&@'
    end_line = '''\nwith open('{}', 'a') as f: \n\tf.write("{}")\n'''.format(config_file, mark)
    new_config_data += end_line

    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(new_config_data)

    def check_load():
        for i in range(3):
            time.sleep(1)
            with open(config_file, 'r', encoding='utf-8') as f:
                if mark * load_time in f.readlines()[-1]:  # 被加载几次，mark就会被写入几次
                    break

        if not inplace:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(old_config_data)

    # 检测配置是否加载
    t = threading.Thread(target=check_load)
    t.start()

    # 执行cmd命令
    subprocess.call(cmd, shell=True)

    return None