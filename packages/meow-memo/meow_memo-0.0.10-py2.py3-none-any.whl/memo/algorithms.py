# algorithms

from .ioutil import splitedDict
from .util import colored
from dataclasses import dataclass, asdict
import re
import inspect
from os import path
from .paths import pth
from . import myhash

_debug = False
_use_cache = True


def split_paragraph(s):
    pattern = r"[\n \t\r]"
    spliter = re.findall(pattern, s)
    splited = re.split(pattern, s)
    ret = []
    # print(spliter)
    # print(splited)
    for idx, i in enumerate(splited):
        if(idx):
            ret.append(spliter[idx-1])
        ret.append(i)
    return ret


def ndarray(dims, fill=0):
    if(len(dims) == 1):
        n = dims[0]
        return [fill for i in range(n)]
    else:
        return [ndarray(dims[1:], fill=fill) for i in range(dims[0])]


def _eq(a, b):
    if(isinstance(a, str) and isinstance(b, str)):
        if(len(a) > 4 and len(b) > 4):
            rate = lcs(a, b).common_ratio
            return rate > 0.7
        else:
            return a.lower() == b.lower()
    else:
        return a == b


def _element_similarity(a, b):
    if(a in " \r\n"):
        return 0
    if(b in " \r\n"):
        return 0

    if(isinstance(a, str) and isinstance(b, str)):
        if(len(a) >= 3 and len(b) >= 3):
            return lcs(a, b).common_ratio
        else:
            return 1 if a.lower() == b.lower() else 0
    else:
        return 1 if a == b else 0


def cached_func(func):
    # not used because I found it slow.
    fingerprint = myhash.base32(inspect.getsource(_element_similarity))
    cache = path.join(pth, "func_cache", "%s" % fingerprint)
    cache = splitedDict(cache)

    def inner(*args, **kwargs):
        nonlocal cache
        tmp = []
        tmp.extend(args)
        for k, v in kwargs.items():
            tmp.append((k, v))
        key = ", ".join([str(i) for i in tmp])
        if(key in cache):
            return cache[key]["ret"]
        else:
            ret = func(*args, **kwargs)
            save = {"args": args, "kwargs": kwargs, "ret": ret}
            cache[key] = save
            return ret
    return inner


def element_similarity(A, B):
    # intended to add debug or cache here
    # but not used
    global _debug, _use_cache
    return _element_similarity(A, B)


def _color_common(a, common, fore="RED"):
    idx = 0
    ret = []
    for ch in a:
        if(idx < len(common) and _eq(common[idx], ch.lower())):
            ret.append(str(colored(ch, fore=fore)))
            idx += 1
        else:
            ret.append(ch)
    return ''.join(ret)


@dataclass
class _lcs:
    A: str
    B: str
    common: str
    common_ratio_a: float
    common_ratio_b: float
    common_ratio: float
    common_len: int
    a_matched: list
    b_matched: list

    def calc(A, B):
        global _debug
        n = len(A)
        m = len(B)
        dp = ndarray((n, m))
        a_matched = ndarray((n,), False)
        b_matched = ndarray((m,), False)
        dp_from = ndarray((n, m), (-1, -1))
        for i in range(n):
            for j in range(m):
                '''if(A[i] in 'Aa' and B[j] in 'Aa' and A[i]!=B[j]):
                    print(A[i],B[j],A[i].lower() == B[j].lower())'''
                mx = 0
                _dp_from = (-1, -1)

                # match A[i], B[j]
                score = dp[i-1][j-1] if (i and j) else 0
                score1 = element_similarity(A[i], B[j])

                if(score1):

                    if(score+score1 >= mx):
                        mx = score+score1
                        _dp_from = (i-1, j-1)
                if(i):
                    if(dp[i-1][j] >= mx):
                        mx = dp[i-1][j]
                        _dp_from = (i-1, j)
                if(j):
                    if(dp[i][j-1] >= mx):
                        mx = dp[i][j-1]
                        _dp_from = (i, j-1)
                dp[i][j] = mx
                dp_from[i][j] = _dp_from
        u, v = n-1, m-1
        common = []
        while(u >= 0 and v >= 0):

            u1, v1 = dp_from[u][v]
            ''' if(_debug):
                print(u, v, 'from', u1, v1) '''
            if(u1 == u-1 and v1 == v-1):
                if(element_similarity(A[u], B[v]) > 0.5):
                    common.append(A[u])
                    '''if(_debug):
                        print("matching", A[u], B[v])'''
                    a_matched[u] = True
                    b_matched[v] = True
            u, v = u1, v1

        common = common[::-1]
        '''#self.A = A
        self.B = B
        self.common = common  # list
        common_ratio_a = dp[n-1][m-1]/len(A)
        common_ratio_b = dp[n-1][m-1]/len(B)
        self.common_ratio = self.common_ratio_a*self.common_ratio_b
        self.common_len = dp[n-1][m-1]'''
        common_len = dp[n-1][m-1]
        common_ratio_a = common_len/len(A)
        common_ratio_b = common_len/len(B)
        return _lcs(A, B, common, common_ratio_a, common_ratio_b, common_ratio_a*common_ratio_b, common_len, a_matched, b_matched)

    def color_common(self, foreA="RED", foreB="GREEN"):
        retA = []
        for idx, i in enumerate(self.A):
            if(self.a_matched[idx]):
                retA.append(str(colored(i, fore=foreA)))
            else:
                retA.append(i)
        retA = "".join(retA)

        retB = []
        for idx, i in enumerate(self.B):
            if(self.b_matched[idx]):
                retB.append(str(colored(i, fore=foreB)))
            else:
                retB.append(i)
        retB = "".join(retB)
        return retA, retB

    def asdict(self, preserve_AB=False):
        D = asdict(self)
        if(not preserve_AB):
            D.pop("A")
            D.pop("B")
        D["a_matched"] = "".join(['1' if i else '0' for i in self.a_matched])
        D["b_matched"] = "".join(['1' if i else '0' for i in self.b_matched])
        return D

    def fromdict_A_B(D, A, B):
        D['a_matched'] = [bool(int(i)) for i in D["a_matched"]]
        D['b_matched'] = [bool(int(i)) for i in D["b_matched"]]
        return _lcs(A=A, B=B, **D)


algorithms_fingerprint = myhash.hashi(inspect.getsource(_lcs))
algorithms_fingerprint = algorithms_fingerprint ^ myhash.hashi(
    inspect.getsource(_element_similarity))
algorithms_fingerprint = myhash.base32(algorithms_fingerprint)
cache_file = splitedDict(path.join(pth, "cache-version=%s" %
                                   algorithms_fingerprint),hash_func=lambda x:myhash.base32(x[1:5],length=2))


def lcs(A, B, simple_B=None, simple_A=None):
    global cache_file, _debug
    if(_use_cache and (simple_A or simple_B)):
        key = str([simple_A or A, simple_B or B])
        if(key in cache_file):
            D = cache_file[key]
            return _lcs.fromdict_A_B(D, A, B)

        ret = _lcs.calc(A, B)
        D = ret.asdict()
        cache_file[key] = D
        if(_debug):
            print(simple_A or simple_B)
        return ret
    else:
        return _lcs.calc(A, B)


algorithms_fingerprint = myhash.hashi(inspect.getsource(_lcs))
algorithms_fingerprint = algorithms_fingerprint ^ myhash.hashi(
    inspect.getsource(_element_similarity))
algorithms_fingerprint = algorithms_fingerprint ^ myhash.hashi(
    inspect.getsource(lcs))

algorithms_fingerprint = myhash.base32(algorithms_fingerprint)
cache_file = splitedDict(path.join(pth, "cache-version=%s" %
                                   algorithms_fingerprint))
if(__name__ == '__main__'):
    debug = True
    import inspect
    print(inspect.getsource(_element_similarity))
