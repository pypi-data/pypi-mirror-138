from os import path
import os
import json
from . import paths
from .myhash import base32


class savedDict(dict):
    opened = dict()

    def open(pth):
        if(pth in savedDict.opened):
            return savedDict.opened[pth]
        else:
            ret = savedDict(pth)
            savedDict.opened[pth] = ret
            return ret

    def __init__(self, pth):
        if(path.exists(pth)):

            with open(pth, 'r', encoding='utf-8') as f:
                texts = f.read()
            if(texts):
                j = json.loads(texts)
                super().__init__(j)

        self.pth = pth
        paths.ensure_dir(pth)
        self.f = open(pth, 'w', encoding='utf-8')
        self._save()

    def _save(self):
        self.f.seek(0)
        json.dump(self, self.f)
        self.f.truncate()

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self._save()

    def __del__(self):
        self.f.close()


class splitedDict:
    # split large dict into multi file
    opened = dict()

    def open(pth):
        if(pth in splitedDict.opened):
            return splitedDict.opened[pth]
        else:
            ret = splitedDict(pth)
            splitedDict.opened[pth] = ret
            return ret

    def __init__(self, pth, hash_func=lambda x: base32(x, length=2)):
        self.pth = pth
        self.hash_func = hash_func

    def get_path(self, key):
        skey = self.hash_func(key)
        return path.join(self.pth, '%s.json' % skey)

    def save_part(self, key):
        D = savedDict.open(self.get_path(key))
        D._save()

    def __setitem__(self, key, value):
        D = savedDict.open(self.get_path(key))
        D[key] = value

    def __getitem__(self, key):
        D = savedDict.open(self.get_path(key))
        return D[key]

    def get(self, key, value=None):
        D = savedDict.open(self.get_path(key))
        return D.get(key, value)

    def __contains__(self, key):
        pth = self.get_path(key)
        if(path.exists(pth)):
            D = savedDict.open(pth)
            return key in D
        else:
            return False


all_editors = ["code --wait", "nano", "gvim"]


def write_file(filename, content):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    return filename


def read_file(filename):
    with open(filename, "r") as f:
        ret = f.read()
    return ret


def input_with_editor(default=""):
    filename = paths.get_temp_file()
    paths.ensure_dir(filename)
    if(default):
        write_file(filename, default)
    has_available_editor = False
    for editor in all_editors:
        retCode = os.system("%s %s" % (editor, filename))
        if(retCode != 0):
            continue
        else:
            has_available_editor = True
            while(not path.exists(filename)):
                print("Please save file after you input")
                retCode = os.system("%s %s" % (editor, filename))
            ret = read_file(filename)
            break
    if(not has_available_editor):
        raise OSError(retCode)
    return ret


if(__name__ == '__main__'):   # for test only
    a = savedDict(r"C:\Users\xiaofan\Downloads\tmp.json")
    a['k'] = "v"

    print(input_with_editor("edit something"))
