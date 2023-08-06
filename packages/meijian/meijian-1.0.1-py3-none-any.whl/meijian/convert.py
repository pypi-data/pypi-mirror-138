from dev_utils import MongoDB
from copy import deepcopy


class ConvertSize(object):
    def __init__(self, string):
        self.old_string = string.strip().lower().replace(",", ".")
        self.old_string_copy = deepcopy(self.old_string)
        self.dimension = ["ø", "h", "w", "d", "l"]
        self.marry()
        self.old_size_list = self.old_string.split()

    def convert(self):
        if not self.old_string:
            return ""
        new_items = []
        for index, o in enumerate(self.old_size_list):
            if self.is_special(o) is True:
                new_items.append(str(int(float(o) * 10)))
            else:
                new_one = self.one(o)
                new_items.append(new_one)
        _new = " ".join(new_items)
        return _new

    def marry(self):
        for d in self.dimension:
            self.old_string = self.old_string.replace("{} ".format(d), "{}".format(d))

    def one(self, item):
        if item == "cm":
            return "mm"
        for _ in self.dimension:
            if item.startswith(_):
                target = item[1:]
                try:
                    target = float(target)
                    target = int(target * 10)
                    return "{}{}".format(_.upper(), target)
                except:
                    pass
        else:
            return item

    def is_special(self, item):
        float_item = None
        try:
            float_item = float(item)
        except:
            pass
        if float_item is None:
            return False
        flag = False
        try:
            new_item = self.old_size_list[self.old_size_list.index(item) + 1]
            if new_item in ["cm", "x"]:
                flag = True
        except:
            pass
        return flag


class Convert:
    def __init__(self):
        pass

    @staticmethod
    def convert(size):
        new_items = []
        for _ in size.split("\n"):
            new_items.append(ConvertSize(_).convert())
        return "\n".join(new_items)
