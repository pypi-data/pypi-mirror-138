import copy

def LP(fun):
    """
    to isolate parameters
    """
    def new_fun(*args,**kwargs):
        args_ = copy.deepcopy(args)
        kwargs_ = copy.deepcopy(kwargs)
        fun(*args_,**kwargs_)
    return new_fun