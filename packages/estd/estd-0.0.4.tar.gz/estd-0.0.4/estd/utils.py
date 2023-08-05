import bisect
import threading
import time
from datetime import datetime
from functools import wraps


def logit(func):
    """
    Decorator to log the execution time of a function

    >>> @logit
    ... def func():
    ...     pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread_name = threading.current_thread().name
        print(datetime.now(), "+++", thread_name, func.__name__)
        ts = time.time()
        ret = func(*args, **kwargs)
        te = time.time()
        print(datetime.now(), "---", thread_name, func.__name__)
        print(datetime.now(), "===", thread_name, func.__name__, f"{te-ts:.2f}")
        return ret

    return wrapper


class Thread(threading.Thread):
    """
    Thread with return value

    >>> t1 = Thread(target=func1, kwargs={"seconds": 5})
    >>> t2 = Thread(target=func2, kwargs={"filename": __file__})
    >>> t1.start()
    >>> t2.start()
    >>> r1 = t1.join()
    >>> r2 = t2.join()
    """
    def __init__(self, group=None, target=None, name=None, args=[], kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return


def has_overlap(regions: dict, query: tuple) -> bool:
    """
    Check if a query region overlaps with any of the regions in the sorted regions dict

    >>> regions = {"chr1": [(0, 10), (20, 30), (40, 50)], "chr2": [(10, 20), (30, 40), (50, 60)]}
    >>> has_overlap(regions, ("chr2", 15, 23))
    True
    """
    overlap = False
    contig, start, end = query
    if contig in regions:
        index = bisect.bisect_left(regions[contig], (start, end))
        if index == 0:
            if regions[contig][0][0] <= end:
                overlap = True
        elif index == len(regions[contig]):
            if regions[contig][-1][1] >= start:
                overlap = True
        else:
            last_region = regions[contig][index - 1]
            next_region = regions[contig][index]
            if last_region[1] >= start or next_region[0] <= end:
                overlap = True
    return overlap


import random


def reservoir_sampling(iterator: iter, k):
    ret = []
    for i, c in enumerate(iterator):
        if i < k:
            ret.append(c)
        else:
            j = random.randint(0, i)
            if j < k:
                ret[j] = c
    return ret


def sampling(iterator: iter, k)->iter:
    """
    Sample k elements from an iterator

    params:
        iterator: iter
        k: int or float (0, 1)
    
    return:
        iter

    >>> list(sampling(range(100), 3))
    [64, 79, 52]
    >>> list(sampling(range(100), 0.1))
    [0, 1, 3, 8, 17, 27, 41, 77, 83, 85, 96]
    """
    if isinstance(k, int):
        yield from reservoir_sampling(iterator, k)
    elif isinstance(k, float) and 0 < k < 1:
        for c in iterator:
            if random.random() < k:
                yield c
    else:
        raise ValueError("k must be an integer or a float between 0 and 1")
