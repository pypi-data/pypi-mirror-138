import functools
from collections.abc import Mapping
class DictUtils:
    @staticmethod
    def getDictValue(d: dict, k: str):
        if k in d:
            return d[k]
        return None

    @staticmethod
    def copyDicts(d: dict, d1: dict):
        return {**d, **d1}

    @staticmethod
    def createDictTreeByKeysAndValueEdge(keys, edgeValue):
        return functools.reduce((lambda x, y: {y: x}), keys[::-1], edgeValue)

    @staticmethod
    def isKeyInDict(d: dict, k: str) -> bool:
        if k in d:
            return True
        return False

    @staticmethod
    def getValueFromKeyPath(key:str, dictionary: dict):
        keys = key.split(".")
        return functools.reduce(lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None, keys, dictionary)

    @staticmethod
    def mergeDicts(d, u):
        for k, v in u.items():
            if isinstance(d.get(k), dict) and isinstance(v, Mapping):
                d[k] = DictUtils.mergeDicts(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    @staticmethod
    def filterDictByKeysList(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k in visibleKeys }

    @staticmethod
    def filterDictByKeysListNeg(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k not in visibleKeys }

    @staticmethod
    def isAllKeyInDict(d: dict, keys: list) -> bool:
        if all(key in d for key in keys): 
            return True
        return False

    @staticmethod
    def createSubDict(d, keys):
        return {x:d[x] for x in keys}

    @staticmethod
    def createDic(**kwargs):
        return kwargs