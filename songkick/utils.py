class ConstantMap(dict):

    def __getattr__(self, key):
        return self.get(key, None)
    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delattr__
