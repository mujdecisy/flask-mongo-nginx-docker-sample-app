from datetime import datetime
import copy


class Pojo:
    def __init__(self, data :dict = None, fromclass = None):
        if data != None:
            self.from_dict(data, fromclass)

    def from_dict(self, data: dict, fromclass) -> None:
        if fromclass == None:
            for k, v in data.items():
                self.__setattr__(k, v)
        else :
            for k, v in data.items():
                if k in fromclass.__dict__["__annotations__"].keys():
                    self.__setattr__(k, v)


    def create_obj(self, data:object) -> None:
        if isinstance(data, dict):
            for k, v in data.items():
                self.__setattr__(k, v)
        else:
            self.recursive_attribute = data

    def to_dict(self) -> dict:
        obj = copy.deepcopy(self)

        try:
            recur_attr = obj.__getattribute__("recursive_attribute")
            if recur_attr != None:
                obj = recur_attr
        except AttributeError:
            pass
            
        if self.is_primitive(obj):
            return obj

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, list):
            for i, v in enumerate(obj):
                if self.is_primitive(v):
                    obj[i] = v
                else:
                    temp = Pojo(v)
                    obj[i] = temp.to_dict()
            return obj

        if isinstance(obj, object):
            filtering = lambda x: not x.startswith("__") and not hasattr(obj.__getattribute__(x), "__call__")
            obj_dict = { k: obj.__getattribute__(k) for k in list(filter(filtering, obj.__dir__()))}

        if isinstance(obj, dict):
            obj_dict = obj

        for k, v in obj_dict.items():
            temp = Pojo()
            temp.create_obj(v)
            obj_dict[k] = temp.to_dict()
        
        return obj_dict

    def is_primitive(self, v):
        if isinstance(v, int) or isinstance(v, str) or isinstance(v, float) or isinstance(v, bool):
            return True
        else:
            return False

class Entity(Pojo):
    def check_self(self):
        return