import cv2
import numpy as np
import os
import time
from datetime import datetime
import math
import  MergerModule.FileOperations as fp
import json
import timeit
import MergerModule.Merger_Mt as mt
import copy
import ConfigurationModule as configModule

cudaImport = True
try:
    from numba import cuda
    import MergerModule_Cuda.CudaBusiness as cudaB
except BaseException as e:
    cudaImport = False

class MergerClass:
    def __init__(self,configModule):
        self.imagesRGB = []
        self.imagesTH = []
        self.imagesRGBCuda = []
        self.imagesTHCuda = []
        self._imagesRGBPath = None
        self._imagesTHPath = None
        self.myHeatMapLookup = self.createHeatMapLookUp()
        self.CudaEnabled = cudaImport
        self.configurations =  configModule.Configuration
        self.outArr = np.empty(shape=(int(self.configurations.rows)*
                                      int(self.configurations.cols)*int(self.configurations.dims))
                               , dtype=np.uint8)
        self.refreshConfigModule  = False

        if self.CudaEnabled:
            self.streamCuda = cuda.stream()
            self.myHeatMapLookupCuda = cuda.to_device(self.myHeatMapLookup,self.streamCuda)
        try:
            self.imagesRGBPath = self.configurations.datasetDemoNormalPath
            self.imagesTHPath = self.configurations.datasetDemoThermalPath
        except BaseException as e:
            print("Dataset Yükleme hata oluştu. Konfigürasyon Dosyasını kontrol edin.{}", str(e))

    @property
    def imagesRGBPath(self):
        return self._imagesRGBPath
    @imagesRGBPath.setter
    def imagesRGBPath(self,value):
        self._imagesRGBPath = value
        pathList1 = [self._imagesRGBPath+"/"+x for x in sorted(os.listdir(self._imagesRGBPath))][:15]
        self.imagesRGB = [np.asarray(cv2.resize(cv2.imread(x),(self.configurations.cols,self.configurations.rows)))
                          for x in pathList1]
        if self.CudaEnabled:
            for image in self.imagesRGB:
                i = np.ravel(image)
                d_A = cuda.to_device(i,self.streamCuda)
                self.imagesRGBCuda.append(d_A)


    @property
    def imagesTHPath(self):
        return self._imagesTHPath

    @imagesTHPath.setter
    def imagesTHPath(self, value):
        self._imagesTHPath = value
        pathList2 = [self._imagesTHPath + "/" + x for x in sorted(os.listdir(self._imagesTHPath))][:15]
        self.imagesTH = [np.asarray(cv2.resize(cv2.imread(x),(self.configurations.cols
                                                              ,self.configurations.rows))) for x in pathList2]
        if self.CudaEnabled:
            for image in self.imagesTH:
                i = np.ravel(image)
                d_A = cuda.to_device(i,self.streamCuda)
                # ary = np.empty(shape=d_ary.shape, dtype=d_ary.dtype) # read eden thread yapicak.
                # d_ary.copy_to_host(ary)
                self.imagesTHCuda.append(d_A)


    def cmb(self,fg, bg, a):
        m_fg = np.multiply(fg, a)
        m_a = np.multiply(bg, np.subtract(1, a))
        #fg * a + bg * (1 - a)
        return np.add(m_fg,m_a)


    def ProcessMerge(self,index,thresholdMinVal=60,mode=3,videoStreamNormal = None,videoStreamThermal =  None,showDemoImages = True):
        if mode == 6 or  mode==5 :
            if showDemoImages:
                imageRGB = self.imagesRGBCuda[index]
                imageTH = self.imagesTHCuda[index]
            else:
                if self.refreshConfigModule:
                    videoStreamNormal.refreshConfiguration(self.configurations)
                    videoStreamThermal.refreshConfiguration(self.configurations)
                    self.refreshConfigModule = False
                imageRGB = videoStreamNormal.read()
                imageTH = videoStreamThermal.read()
        else:
            imageRGB = self.imagesRGB[index]  # su anlik ekledim sonra kalkicak
            imageTH = self.imagesTH[index]

        if mode == 1:
            # retTH, threshTH = cv2.threshold(imageTH, thresholdMinVal, 255, cv2.THRESH_BINARY)
            # gray_image = cv2.cvtColor(imageTH, cv2.COLOR_BGR2GRAY)
            # heatImage_opencv = self.applyColorMap(gray_image)
            # heatImage_opencv = cv2.applyColorMap(imageTH, cv2.COLORMAP_RAINBOW)
            heatImage_opencv = cv2.cvtColor(cv2.applyColorMap(imageTH, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
            #heatImage_opencv = cv2.applyColorMap(imageTH,cv2.COLORMAP_JET)
            return heatImage_opencv
        elif mode==2:
            return imageTH
        elif mode==3:
            return imageRGB
        elif mode==4 or not self.CudaEnabled:
            # heatImage = cv2.cvtColor(cv2.applyColorMap(imageTH, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
            # heatImage = cv2.applyColorMap(imageTH, cv2.COLORMAP_JET)
            print("*****************************************************************************")

            t_start = timeit.default_timer()
            gray_image = cv2.cvtColor(imageTH, cv2.COLOR_BGR2GRAY)
            t_end = timeit.default_timer()
            print("gray_image takes {:.5f} second".format((t_end - t_start)))

            t_start = timeit.default_timer()
            # heatImage = self.applyColorMap(gray_image)

            heatImage = cv2.applyColorMap(imageTH, cv2.COLORMAP_JET)
            t_end = timeit.default_timer()
            print("heatImage takes {:.5f} second".format((t_end - t_start)))
            retTH, threshTH = cv2.threshold(imageTH, thresholdMinVal, 1, cv2.THRESH_BINARY)
            t_start = timeit.default_timer()
            # imageRGB[0::2,1::2] = self.cmb(heatImage[0::2,1::2], imageRGB[0::2,1::2], threshTH[0::2,1::2])
            imageRGB = self.cmb(heatImage, imageRGB, threshTH)
            t_end = timeit.default_timer()
            print("cmb takes {:.5f} second".format((t_end - t_start)))
            print("*****************************************************************************")
            # mt.init(imageRGB, imageTH, threshTH)
            # blended = mt.main()
            return imageRGB
        elif mode==5 and self.CudaEnabled :
            retImage = cudaB.CudaBlend(imageTH,imageRGB,thresholdMinVal,self.outArr,self.streamCuda ,self.myHeatMapLookupCuda,self.configurations.cudaBlockThreadCount,self.configurations)
            return retImage
        elif mode==6:
            # t_start = timeit.default_timer()
            retImage = cudaB.CudaHeatMap(imageTH, self.outArr, self.streamCuda, self.myHeatMapLookupCuda,
                                         1024, self.configurations)
            # t_end = timeit.default_timer()
            # print("matmul takes {:.5f} second".format((t_end - t_start)))
            return retImage




    def createHeatMapLookUp(self):
        mx = 256  # if gray.dtype==np.uint8 else 65535
        lut = np.empty(shape=(256, 3))
        # cmap = (
        #     (0, (2, 9, 147)),
        #     (0.2, (0, 108, 255)),
        #     (0.4, (0, 255, 0)),
        #     (0.6, (255, 255, 0)),
        #     (0.8, (255, 127, 0)),
        #     (1.0, (148, 0, 0))
        # )
        cmap = (
            (0, (255, 0, 0)),
            (0.25, (255, 255, 0)),
            (0.50, (0, 255, 0)),
            (0.75, (0, 255, 255)),
            (1.0, (0, 0, 255))
        )
        # build lookup table:
        lastval, lastcol = cmap[0]
        for step, col in cmap[1:]:
            val = int(step * mx)
            for i in range(3):
                lut[lastval:val, i] = np.linspace(
                    lastcol[i], col[i], val - lastval)
            lastcol = col
            lastval = val
        return np.asarray(lut,np.uint8)
        # fp.pickleOlustur("myHeatMapLookup.pkl",lut)

    def applyColorMap(self,gray, cmap='flame'):
        s0, s1 = gray.shape
        out = np.empty(shape=(s0, s1, 3), dtype=np.uint8)
        for i in range(3):
            out[..., i] = cv2.LUT(gray, self.myHeatMapLookup[:, i])
        return out





