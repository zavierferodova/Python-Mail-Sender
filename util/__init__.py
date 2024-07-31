import os
import numpy as np

def var_parser(item, s):
    key, value = item
    s = s.replace(f"{{{{{key}}}}}", str(value))
    s = s.replace("\{", "{")
    s = s.replace("\}", "}")
    return s

def check_attachment(path):
    return os.path.isfile(path)

np_lower = np.vectorize(lambda s: s.lower())
