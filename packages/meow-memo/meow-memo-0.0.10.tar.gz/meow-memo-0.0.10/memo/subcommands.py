from . import files
import time
from . import algorithms
from . import ioutil
from .files import update_data
import re
import time
from .algorithms import split_paragraph
subcommands = dict()


def deco(func):
    subcommands[func.__name__] = func


@deco
def help(argdict):
    print("meow [key]")
    print("    to search memo for key")
    print("meow add [key] [value]")
    print("    to add (overwrite) [key] 's memo ")
    print("meow app [key] [value]")
    print("    to append a line to the end of  [key] 's memo")  # nopep8
    print("meow edit [key]")
    print("    to open an editor for [key], tool will try invoke vscode, nano, gvim.")    # nopep8
    print("meow awesome")
    print("    to fetch awesome-python memos")


def do_search(key, first=0.15, argdict=None):
    if(argdict is None):
        argdict = dict()
    _debug = argdict.get("debug")
    _use_cache = argdict.get("use_cache")
    if(_debug):
        algorithms._debug = True
    if(_use_cache):
        if(isinstance(_use_cache, list)):
            _use_cache = _use_cache[0]
            if(_use_cache.lower()[0] == 't'):
                algorithms._use_cache = True
            elif(_use_cache.lower()[0] == 'f'):
                algorithms._use_cache = False
        else:
            algorithms._use_cache = _use_cache
        
    start_time = time.time()
    key_len = len(key)
    results = []
    for k, v in files.datas.items():
        if(len(key) > 10 or len(k) > 10):
            common = algorithms.lcs(split_paragraph(key), split_paragraph(k))
        else:
            common = algorithms.lcs(key, k)
        # v_common_len, v_common_str = algorithms.lcs(key, v)
        sb = "%s@%s" % (k, files.times[k])
        common_v = algorithms.lcs(
            split_paragraph(key),
            split_paragraph(v),
            simple_B=sb)
        score = common.common_len + common_v.common_len*0.2
        score = score**2
        results.append((score, k, v, common, common_v))
    results.sort(key=lambda x: -x[0])    # sort by score descending
    sum_score = sum([x[0] for x in results])*first
    for idx, i in enumerate(results[:5]):
        score, k, v, common, common_v = i
        colored_key, colored_k = common.color_common()
        print(colored_key, "->", colored_k, ":")
        _, colored_v = common_v.color_common(foreB="BLUE")
        for i in colored_v.split("\n"):
            print("    ", i, sep="")

        if(argdict.get("debug")):
            print(*common.color_common(), sep="  <-->  ")
            print(common.b_matched)
            print(common.common)
        print()
        sum_score -= score
        if(sum_score < 0):
            break
    print("finished search in %.1f seconds" % (time.time()-start_time))
    return


@deco
def edit(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]  # "edit"
    key = _args[1]  # key
    if(key in files.datas):
        value = files.datas[key]
    else:
        value = None
    value = ioutil.input_with_editor(value)
    update_data(key, value)
    do_search(key, first=0)


@deco
def add(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]    # "add"
    key = _args[1]    # key
    value = _args[2]  # value
    update_data(key, value)
    do_search(key, first=0)


@deco
def app(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]   # "app"
    key = _args[1]   # key
    value = _args[2]  # value
    v = files.datas.get(key, "")
    if(v):
        v = v+"\n"+value
    else:
        v = value
    update_data(key, v)
    do_search(key, first=0)


@deco
def search(argdict):
    _args = argdict.get("positional")
    key = " ".join(_args)
    do_search(key, argdict=argdict)


@deco
def awesome(argdict):
    from . import awesome
    awesome.run(argdict)
