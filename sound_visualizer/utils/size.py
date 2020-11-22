import math

import numpy as np


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def np_get_real_size(obj: np.ndarray) -> int:
    if obj.base is not None:
        return np_get_real_size(obj.base)
    return obj.nbytes
