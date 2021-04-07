import json
from sklearn.externals import joblib
import pickle
import numpy as np
def pickleOlustur(fileName,object,method=None):
    try:
        if method is None:
            with open(fileName, 'w') as fp:
                json.dump(object, fp)
        elif method == 1:
            np.save(fileName, object)
        return '0'
    except BaseException as e:
        print(str(e))
        return '-1'

def pickleYukle(fileName,method=None):
    #data =joblib.load(fileName)
    if method is None:
        with open(fileName, 'r') as fp:
            data = json.loads(fp.read())
    elif method == 1:
        data =np.load(fileName)
    return data