from threading import Thread, Lock
import cv2
import json

from numba import cuda
import numpy as np
import timeit
import datetime
import time

class VideoStream :
    def __init__(self,framePath,configModule,isThermal_=False) :
        self.configModule = configModule
        # t_start = timeit.default_timer()
        self.isThermal = isThermal_
        self.streamCuda = cuda.stream()
        self.thermalOutImage = np.empty(shape=(self.configModule.Configuration.rows,
                                     self.configModule.Configuration.cols, self.configModule.Configuration.dims)
                              , dtype=np.uint8)
        # self.streamNormal.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.streamNormal.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        #
        # self.streamThermal.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.streamThermal.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        (self.grabbedNormal, self.frameNormal) =   True,np.empty(shape=(self.configModule.Configuration.rows ,
                                                                        self.configModule.Configuration.cols , self.configModule.Configuration.dims)
                 , dtype=np.uint8)


        normalImageRavel = np.ravel(self.frameNormal)
        self.cudaFrameNormal = cuda.to_device(normalImageRavel, self.streamCuda)


        self.started = False
        self.read_lock = Lock()

        self.framePath = framePath
        self.streamNormal = cv2.VideoCapture(self.framePath)


        # t_end = timeit.default_timer()
        # print("Baslangic takes {:.5f} second".format((t_end - t_start)))

    def refreshConfiguration(self,configsModule):
        # print("Refres Config....")
        self.read_lock.acquire()
        # self.thermalOutImage = np.empty(shape=(configsModule.rows,
        #                                        configsModule.cols,
        #                                        configsModule.dims)
        #                                 , dtype=np.uint8)

        self.thermalOutImage.fill(0)
        self.read_lock.release()


    def start(self) :
        if self.started :
            print ("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())

        # count = self.streamNormal.get(cv2.CAP_PROP_FRAME_COUNT)
        # self.streamNormal.set(cv2.CAP_PROP_POS_FRAMES, count - 100)

        self.thread.start()
        return self

    def update(self) :
        while self.started :
            try:
                (grabbedN, frameN) = self.streamNormal.read()
                self.read_lock.acquire()
                self.grabbedNormal, self.frameNormal = grabbedN, frameN
                self.read_lock.release()
                # self.grabbedNormal, self.frameNormal = grabbedN, cv2.resize(frameN,(configModule.Configuration.cols,configModule.Configuration.rows))
                # self.grabbedThermal, self.frameThermal = grabbedT, cv2.resize(frameT,(configModule.Configuration.cols,configModule.Configuration.rows))

                # print("update {0}".format(datetime.datetime.now()))
            except BaseException as e:
                print("Thread Hata - {0}".format(str(e)))
                pass

    def read(self) :
        try:
            self.read_lock.acquire()
            # frameN = self.cudaFrameNormal.bind(self.streamCuda)
            # frameT = self.cudaFrameThermal.bind(self.streamCuda)
            # normalImageRavel = np.ravel(self.frameNormal)
            # thermalImageRavel = np.ravel(self.frameThermal)
            if self.isThermal:
                # print("Thermal size {0}-{1}".format(self.frameNormal.shape[0],self.frameNormal.shape[1]))
                thermalImageResized = cv2.resize(self.frameNormal, (self.configModule.Configuration.thermalCalibrationParameters_thermalWidth, self.configModule.Configuration.thermalCalibrationParameters_thermalHeight))
                self.thermalOutImage[
                self.configModule.Configuration.thermalCalibrationParameters_thermal_YStart:self.configModule.Configuration.thermalCalibrationParameters_thermal_YEnd
                ,
                self.configModule.Configuration.thermalCalibrationParameters_thermal_XStart:self.configModule.Configuration.thermalCalibrationParameters_thermal_XEnd] = thermalImageResized
                normalImageRavel = self.thermalOutImage
            else :
                normalImageRavel = cv2.resize(self.frameNormal, ( self.configModule.Configuration.cols,  self.configModule.Configuration.rows))

            # normalImageRavel = np.copy(cv2.cvtColor(normalImageRavel, cv2.COLOR_BGR2RGB))
            normalImageRavel = np.copy(normalImageRavel)

            self.read_lock.release()

            # normalImageRavel = np.ravel(
            #     cv2.resize(normalImageRavel, ( self.configModule.Configuration.cols,  self.configModule.Configuration.rows)))


            self.cudaFrameNormal = cuda.to_device( np.ravel(normalImageRavel), self.streamCuda)

        except BaseException as e:
            pass
        return self.cudaFrameNormal

    def readImage(self) :
        self.read_lock.acquire()

        if self.isThermal:
            print("Thermal size {0}-{1}".format(self.frameNormal.shape[0], self.frameNormal.shape[1]))
            thermalImageResized = cv2.resize(self.frameNormal, (
            self.configModule.Configuration.thermalCalibrationParameters_thermalWidth,
            self.configModule.Configuration.thermalCalibrationParameters_thermalHeight))
            self.thermalOutImage[
            self.configModule.Configuration.thermalCalibrationParameters_thermal_YStart:self.configModule.Configuration.thermalCalibrationParameters_thermal_YEnd
            ,
            self.configModule.Configuration.thermalCalibrationParameters_thermal_XStart:self.configModule.Configuration.thermalCalibrationParameters_thermal_XEnd] = thermalImageResized
            frameN = self.thermalOutImage.copy()
        else:

            self.frameNormal = cv2.resize(self.frameNormal,
                                          (self.configModule.Configuration.cols, self.configModule.Configuration.rows))
            frameN = self.frameNormal.copy()

        # self.cudaFrameNormal = cuda.to_device(frameT, self.streamCuda)
        # self.cudaFrameThermal = cuda.to_device(frameN, self.streamCuda)
        self.read_lock.release()
        return frameN

    def stop(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

