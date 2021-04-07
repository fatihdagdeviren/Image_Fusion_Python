import CameraModule as cm
import cv2
# rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/201/
# termal: 201  normal: 101
import datetime
import ConfigurationModule.Configuration as configModule
import numpy as np



if __name__ == "__main__" :
    # configModule.Configuration.setVariables('../ConfigurationModule/Configs.json')
    # normalImage = cv2.imread('Example_Images/frameN.jpeg')
    # thermalImage = cv2.imread('Example_Images/frameT.jpeg')
    #
    # outArr = np.empty(shape=(configModule.Configuration.rows *
    #                 configModule.Configuration.cols * configModule.Configuration.dims)
    #          , dtype=np.uint8)
    #
    # thermalImageResized = cv2.resize(thermalImage,(1370,930))
    #
    # thermalOut = np.empty(shape=(configModule.Configuration.rows ,
    #                 configModule.Configuration.cols , configModule.Configuration.dims)
    #          , dtype=np.uint8)
    #
    # thermalOut[
    # configModule.Configuration.thermalCalibrationParamaters_thermal_YStart:configModule.Configuration.thermalCalibrationParamaters_thermal_YEnd
    # ,
    # configModule.Configuration.thermalCalibrationParamaters_thermal_XStart:configModule.Configuration.thermalCalibrationParamaters_thermal_XEnd] = thermalImageResized
    #
    # cv2.imshow("retIm",thermalOut)
    # cv2.imshow("normalImage", normalImage)
    # cv2.imshow("thermalOut", thermalOut)
    # cv2.waitKey(0)


    vs1 = cv2.VideoCapture("rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101")
    # vs2 = cv2.VideoCapture("rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/201")
    while True:
         gr, frameN = vs1.read()
         #gr, frameT = vs2.read()
         cv2.imshow('frameN', frameN)
         #cv2.imshow('frameT', frameT)
    #     cv2.imwrite('frameT.jpeg', frameT)
         cv2.imwrite('frameN.jpeg', frameN)
         if cv2.waitKey(1) == 27:
             break



    # configModule.Configuration.setVariables('../ConfigurationModule/Configs.json')
    # vsNormal = cm.VideoStream(configModule.Configuration.normalStreamPath,configModule).start()
    # vsThermal = cm.VideoStream(configModule.Configuration.thermalStreamPath, configModule,isThermal_=True).start()
    # while True:
    #     frameN = vsNormal.readImage()
    #     frameT = vsThermal.readImage()
    #
    #
    #
    #     cv2.imshow('frameT', frameT)
    #     cv2.imshow('frameN', frameN)
    #     # print(datetime.datetime.now())
    #
    #     if cv2.waitKey(1) == 27:
    #         break
    #
    # vsNormal.stop()
    # vsThermal.stop()
cv2.destroyAllWindows()

