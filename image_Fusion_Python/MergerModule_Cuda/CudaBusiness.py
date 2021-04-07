from numba import cuda, float32
import numpy as np
import math
import timeit
import ConfigurationModule as configModule

def matmul_py(A, B):
    """Perform square matrix multiplication of out = A * B
    """
    out = np.empty([A.shape[0], B.shape[1]], A.dtype)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            tmp = 0.
            for k in range(A.shape[1]):
                tmp += A[i, k] * B[k, j]
            out[i, j] = tmp
    return out

def cmb(fg, bg, a):
    m_fg = np.multiply(fg, a)
    m_a = np.multiply(bg, np.subtract(1, a))
    # fg * a + bg * (1 - a)
    return np.add(m_fg, m_a)

#
# CUDA AlphaBlending
#
@cuda.jit
def matmul_pixel(Foregr, Backgr,thresholdValue ,myLookUp,C):
    """AlphaBlending
    """
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    if Foregr[pos] <= thresholdValue:
        C[pos] = Backgr[pos]
    else:
        val = Foregr[pos]
        #C[pos] =  Backgr[pos]*0.20 + myLookUp[val][pos%3]*0.80 # overlay vermek icin
        C[pos] =myLookUp[val][pos % 3] #sadece lookupdan gelsin denirse
        # C[pos] = val
    # print(pos)
    # C[i, j] = (A[i, j] * Alpha[i,j]) + (B[i, j] * (1-Alpha[i,j]))
        # C[i, j] = tmp

def CudaBlend(A,B, threshTH,out,streamGlobal,lookupTable,TPB,configuration):
    threadsperblock =  TPB
    blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock))
    blockspergrid = blockspergrid_x
    # d_A = cuda.to_device(A, stream=streamGlobal)
    # d_B = cuda.to_device(B, stream=streamGlobal)
    # d_Thresh = cuda.to_device(threshTH, stream=streamGlobal)
    # t_start = timeit.default_timer()
    matmul_pixel[blockspergrid, threadsperblock, streamGlobal](A, B, threshTH,lookupTable ,out)
    streamGlobal.synchronize()
    # t_end = timeit.default_timer()
    # print("CudaBlend reshape takes {:.5f} second".format((t_end - t_start)))

    #reshape diger tarafa
    # return out
    reshape = np.reshape(out,(configuration.rows,configuration.cols,configuration.dims))
    return reshape

#
# END CUDA AlphaBlending
#

#
# CUDA HeatMap
#
@cuda.jit
def GetHeatMapValue(Image,  myLookUp,C):
    """AlphaBlending
    """
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    deger = Image[pos]
    C[pos] = myLookUp[deger][pos%3]

def CudaHeatMap(A,out,streamGlobal,lookupTable,TPB,configuration):
    threadsperblock =  TPB
    blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock))
    blockspergrid = blockspergrid_x
    GetHeatMapValue[blockspergrid, threadsperblock, streamGlobal](A,lookupTable ,out)
    streamGlobal.synchronize()
    reshape = np.reshape(out,(configuration.rows,configuration.cols,configuration.dims))
    return reshape

#
# END CUDA HeatMap
#