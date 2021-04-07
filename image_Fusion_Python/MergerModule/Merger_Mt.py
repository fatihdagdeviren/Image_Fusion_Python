import numpy as np
import time
from multiprocessing import Pool, freeze_support
from multiprocessing.sharedctypes import RawArray
import cv2
from datetime import datetime
import timeit

var_dict = {}
X_shape = (1080, 1920,3)
rgbImage = RawArray('d', X_shape[0] * X_shape[1]* X_shape[2])
thImage = RawArray('d', X_shape[0] * X_shape[1]* X_shape[2])
alpha = RawArray('d', X_shape[0] * X_shape[1]* X_shape[2])
resultImage = RawArray('d', X_shape[0] * X_shape[1]* X_shape[2])

def init_worker(X,Y,Z, T,X_shape):
    # Using a dictionary is not strictly necessary. You can also
    # use global variables.
    var_dict['rgbImage'] = X
    var_dict['thImage'] = Y
    var_dict['alpha'] = Z
    var_dict['resultImage'] = T
    var_dict['X_shape'] = X_shape

def worker_func(i):
    # print(i)
    # Simply computes the sum of the i-th row of the input matrix X
    X_np_rgb = np.frombuffer(var_dict['rgbImage']).reshape(var_dict['X_shape'])
    X_np_th = np.frombuffer(var_dict['thImage']).reshape(var_dict['X_shape'])
    X_np_res = np.frombuffer(var_dict['resultImage']).reshape(var_dict['X_shape'])
    X_np_alp = np.frombuffer(var_dict['alpha']).reshape(var_dict['X_shape'])
    X_np_res[i*54:(i*54)+54,:] = np.add(np.multiply(X_np_th[i*54:(i*54)+54,:],X_np_alp[i*54:(i*54)+54,:]),
                                           np.multiply(X_np_rgb[i*54:(i*54)+54,:] , np.subtract(1,X_np_alp[i*54:(i*54)+54,:])))

    #time.sleep(1) # Some heavy computations
    #return np.asscalar(np.sum(X_np[i,:]))


def init(rgbImagem,thImagem,alpham):
    resultIm = np.zeros(rgbImagem.shape, np.uint8)
    rgb_np = np.frombuffer(rgbImage).reshape(X_shape)
    np.copyto(rgb_np, rgbImagem)
    th_np = np.frombuffer(thImage).reshape(X_shape)
    np.copyto(th_np, thImagem)
    res_np = np.frombuffer(resultImage).reshape(X_shape)
    np.copyto(res_np, resultIm)
    alpha_np = np.frombuffer(alpha).reshape(X_shape)
    np.copyto(alpha_np, alpham)


def main():
    freeze_support()
    pools = Pool(processes=10, initializer=init_worker, initargs=(rgbImage, thImage, alpha, resultImage, X_shape))
    t_start = timeit.default_timer()
    pools.map(worker_func, range(20))
    pools.close()
    pools.join()
    t_end = timeit.default_timer()
    print("freeze_supportaa takes {:.5f} second".format((t_end - t_start)))
    return np.asarray(np.frombuffer(resultImage).reshape(X_shape),np.uint8)