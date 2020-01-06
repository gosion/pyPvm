def delegateify(func):
    """装饰器，将普通方法转换为activity的execution"""
    def __inner(next_):
        return lambda token: func(next_, token)

    return __inner
