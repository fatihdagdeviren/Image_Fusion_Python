from timeit import default_timer as time
from MergerModule_Cuda import CudaBusiness

import numpy as np

from numba import cuda
import timeit
import math
import cv2
import numpy as np
#
# Main Program - Buradaki kodu main denemesi icin tutuyorum.
#
N = 120
aIm =  cv2.resize(cv2.imread("D:\\Asis\\image_Fusion_Datasets\\1a\\img_00001.bmp"),(1920,1080))
bIm = cv2.resize(cv2.imread("D:\\Asis\\image_Fusion_Datasets\\1b\\img_00000.bmp"),(1920,1080))
outImage = np.empty((1080,1920,3),dtype=np.uint8)
aImGray = cv2.cvtColor(aIm, cv2.COLOR_BGR2GRAY)
bImGray = cv2.cvtColor(bIm, cv2.COLOR_BGR2GRAY)


A = aIm
B = bIm

A = A.flatten()
B = B.flatten()

# A = np.asarray( [[2,3,4], [5,6,7],[8,9,1],[25, 26, 27]]   ,np.uint8)
# B = np.asarray(  [[33, 34,35,36,37,38,39,40], [41, 42,43,44,45,46,47,48],[49, 50,51,52,53,54,55,56],[57, 58,59,60,61,62,63,64]]   ,np.uint8)

# s =  bIm.flatten()
# sR = s.reshape(1080,1920,3)
# cv2.imshow("bIm",bIm)
# cv2.imshow("sR",sR)
# cv2.waitKey(0)


# A = A[:,:,0]
# B = B[:,:,0]

# threshTH = np.asarray(  [[0, 0,0,0,0,0,0,0], [1, 1,1,1,1,1,1,1],[0, 0,0,0,0,0,0,0], [1, 1,1,1,1,1,1,1],]   ,np.uint8)

thresholdMinVal = 100
retTH, threshTH = cv2.threshold(A, thresholdMinVal, 1, cv2.THRESH_BINARY)
threshTH = threshTH.flatten()
# threshTH = np.concatenate((threshTH,threshTH,threshTH),axis=1)

out = np.empty(shape=A.shape,dtype=np.uint8)
# Controls threads per block and shared memory usage.
# The computation will be done on blocks of TPBxTPB elements.
TPB = 512

print ("matrix multiplication")
# print ("A array size", A.shape[0], "by", A.shape[1])
# print ("B array size", B.shape[0], "by", B.shape[1])
# print ("A array type", A.dtype)
# print ("B array type", B.dtype)
print("\n")


if __name__ =="__main__":
    #
    # Loop Body
    #
    np_loop = 10
    np_matmul = np.empty(np_loop)
    # print ("NumPy blend...")
    # for i in range(np_loop):
    #     # This function is included in NumPy 1.10.0 and higher
    #     t_start = timeit.default_timer()
    #     # out = np.matmul(A, B)
    #     out = MandelBrot.cmb(B, A, threshTH)
    #     # cv2.imshow("out",out)
    #     # cv2.waitKey(0)
    #     t_end = timeit.default_timer()
    #     np_matmul[i] = t_end - t_start
    #     print("np blend takes {:.5f} second".format((t_end - t_start)))

    threadsperblock =  TPB
    blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock))
    blockspergrid = blockspergrid_x

    cuda_loop = 10
    cuda_fast_matmul = np.empty(cuda_loop)
    cuda_matmul = np.empty(cuda_loop)

    stream = cuda.stream()

    print("CUDA blend...")
    for i in range(cuda_loop):
        d_A = cuda.to_device(A, stream=stream)
        d_B = cuda.to_device(B, stream=stream)
        d_Thresh = cuda.to_device(threshTH, stream=stream)
        t_start = timeit.default_timer()
        CudaBusiness.matmul_pixel[blockspergrid, threadsperblock, stream](d_A, d_B, d_Thresh, out)

        outImage = np.reshape(out,(1080,1920,3))
        # outImage[:, :, 0] = out[:, 0:1920]
        # outImage[:, :, 1] = out[:, 1920:3840]
        # outImage[:, :, 2] = out[:, 3840:]

        # print(out)
        t_end = timeit.default_timer()
        cuda_matmul[i] = t_end - t_start
        cv2.imshow("outImage",outImage)
        cv2.waitKey(0)
        print ("matmul takes {:.5f} second".format((t_end -t_start)))
        # d_A.copy_to_host(A, stream=stream)
        # d_B.copy_to_host(B, stream=stream)
        # # data may not be available in an_array
        # stream.synchronize()
        # data available in an_array







