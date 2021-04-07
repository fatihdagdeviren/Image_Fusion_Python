from PyQt5 import QtCore, QtGui, QtWidgets
from Gui import FusionFormGui
from MergerModule import Merger
import time

from MergerModule.FileOperations import *
import timeit
import CameraModule.CameraModule as cm
import datetime
import ConfigurationModule.Configuration as configModule
from threading import Thread, Lock
import cv2

class Prog(QtWidgets.QMainWindow):
    left_clicked = QtCore.pyqtSignal(int)
    right_clicked = QtCore.pyqtSignal(int)
    configModule.Configuration.setVariables('ConfigurationModule/Configs.json')
    def __init__(self):

        # self.configuration = configModule
        self.merger = Merger.MergerClass(configModule=configModule)


        # self.merger.imagesRGB = pickleYukle("Dataset\\1b.npy",1)
        # self.merger.imagesTH = pickleYukle("Dataset\\1a.npy",1)
        #image save
        # fp.pickleOlustur("1b",self.merger.imagesRGB,1)
        # fp.pickleOlustur("1a", self.merger.imagesTH, 1)
        #end image save

        super().__init__()
        self.ui = FusionFormGui.Ui_GroupBox()
        self.ui.setupUi(self)
        self.start = None
        self.end = None
        self.ui.verticalSlider.valueChanged.connect(self.verticalSliderValueChanged)
        self.ui.verticalSlider.setMaximum(255)
        self.ui.StartButton.clicked.connect(self.StartTimer)
        self.ui.PauseButton_2.clicked.connect(self.PauseTimer)
        self.index = 0

        self.videoStreamNormal = None
        self.videoStreamThermal = None


        oImage = QtGui.QImage("Temp//Images//ColorMapJet.png")
        pixmap01 = QtGui.QPixmap.fromImage(oImage)
        pixmap_image = QtGui.QPixmap(pixmap01)
        self.ui.labelHeatMapImage.setPixmap(pixmap_image)
        self.ui.labelHeatMapImage.setScaledContents(True)


        #comboboxlar ayarlaniyor

        self.modeList = {
                  "HeatMap": 1,
                  "Thermal": 2,
                  "Normal": 3,
                  "Normal+Thermal": 4,
                  "Cuda/Normal+Thermal": 5,
                  "Cuda Heatmap": 6
                }
        self.mode_v = self.modeList["Normal+Thermal"]
        self.ui.radioButton_Thermal.clicked.connect(lambda checked, text=self.modeList["HeatMap"]: self.radioClicked(text))
        self.ui.radioButton_ThermalVisible.clicked.connect(
            lambda checked, text=self.modeList["Thermal"]: self.radioClicked(text))
        self.ui.radioButton_ThermalVisible_2.clicked.connect(
            lambda checked, text=self.modeList["Normal"]: self.radioClicked(text))
        self.ui.radioButton_VisibleThermal.clicked.connect(
            lambda checked, text=self.modeList["Normal+Thermal"]: self.radioClicked(text))
        self.ui.radioButton_CudaMerge.clicked.connect(
            lambda checked, text=self.modeList["Cuda/Normal+Thermal"]: self.radioClicked(text))
        self.ui.radioButton_CudaHeatmap.clicked.connect(
            lambda checked, text=self.modeList["Cuda Heatmap"]: self.radioClicked(text))


        # comboboxlar ayarlandi.
        #Reader, Writer Timer
        self._status_update_timer = QtCore.QTimer(self)
        self._status_update_timer.setInterval(5)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(self.Process)

        self._status_update_timer_reader = QtCore.QTimer(self)
        self._status_update_timer_reader.setInterval(1)
        self._status_update_timer_reader.setSingleShot(False)
        self._status_update_timer_reader.timeout.connect(self.show_image)

        self._status_update_timer_waitKey = QtCore.QTimer(self)
        self._status_update_timer_waitKey.setInterval(1)
        self._status_update_timer_waitKey.setSingleShot(False)
        self._status_update_timer_waitKey.timeout.connect(self.check_configuration)

        self.ui.verticalSlider.setVisible(False)
        self.ui.labelHeatMapImage.setVisible(False)


        #double click icin ekliyorum
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0

        #Demo Resimleri icin checkbox event
        self.ui.chk_ShowDemoImages.stateChanged.connect(self.ShowDemoImages_state_changed)

        #fullscreen icin variable
        self.isFullScreen = False

        # Thermal Configuration kismi
        self.ui.chk_ShowDemoImages.setChecked(True)
        self.ui.spinBox_XStart.setValue(configModule.Configuration.thermalCalibrationParameters_thermal_XStart)
        self.ui.spinBox_XEnd.setValue(configModule.Configuration.thermalCalibrationParameters_thermal_XEnd)
        self.ui.spinBox_YStart.setValue(configModule.Configuration.thermalCalibrationParameters_thermal_YStart)
        self.ui.spinBox_YEnd.setValue(configModule.Configuration.thermalCalibrationParameters_thermal_YEnd)
        self.ui.spinBox_XStart.valueChanged.connect(
            lambda changed, spinBoxName="XStart": self.thermalSpinBoxChanged(spinBoxName))
        self.ui.spinBox_XEnd.valueChanged.connect(
            lambda changed, spinBoxName="XEnd": self.thermalSpinBoxChanged(spinBoxName))
        self.ui.spinBox_YStart.valueChanged.connect(
            lambda changed, spinBoxName="YStart": self.thermalSpinBoxChanged(spinBoxName))
        self.ui.spinBox_YEnd.valueChanged.connect(
            lambda changed, spinBoxName="YEnd": self.thermalSpinBoxChanged(spinBoxName))
        self.ui.btn_SetThermalConf.clicked.connect(self.apply_thermal_configuration)
        self.configCoorParams  = [configModule.Configuration.thermalCalibrationParameters_thermal_XStart,
                                  configModule.Configuration.thermalCalibrationParameters_thermal_XEnd,
                                  configModule.Configuration.thermalCalibrationParameters_thermal_YStart,
                                  configModule.Configuration.thermalCalibrationParameters_thermal_YEnd]
        self.isConfChanged = False


        self.returnImage = np.empty(shape=(int(configModule.Configuration.rows) *
                        int(configModule.Configuration.cols) * int(configModule.Configuration.dims))
                 , dtype=np.uint8)
    def apply_thermal_configuration(self):
        configModule.Configuration.set_variables_from_tccParams(self.configCoorParams)
        self.merger.refreshConfigModule = True


    def ShowDemoImages_state_changed(self):
        if self.ui.chk_ShowDemoImages.isChecked() and self.mode_v == self.modeList['Cuda/Normal+Thermal'] and  self.videoStreamNormal is not  None and  self.videoStreamThermal is not None:
            self.videoStreamNormal.stop()
            self.videoStreamThermal.stop()
        elif not self.ui.chk_ShowDemoImages.isChecked() and self.mode_v == self.modeList[
                'Cuda/Normal+Thermal'] and self.videoStreamNormal is not None and self.videoStreamThermal is not None:
            self.videoStreamNormal.start()
            self.videoStreamThermal.start()
            print("start")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
            if self.left_click_count == 2:
                self.isFullScreen = not self.isFullScreen
                cv2.destroyAllWindows()
            if self.left_click_count ==3:
                configModule.Configuration.setVariables('ConfigurationModule/Configs.json')
                # self.configModule = configModule
                # self.merger.configurations = self.configModule
                self.merger.refreshConfigModule = True
                # self.configuration = configModule
        if event.button() == QtCore.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        # self.merger.refreshConfiguration(self.configuration)

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

    def radioClicked(self,text):
        self.mode_v = text
        visible_vertical = False
        if self.mode_v == 4 or self.mode_v == 5:
            visible_vertical = True
        self.ui.verticalSlider.setVisible(visible_vertical)
        self.ui.labelHeatMapImage.setVisible(visible_vertical)

    def thermalSpinBoxChanged(self,spinBoxName):
        if spinBoxName == "XStart":
            self.configCoorParams[0] =  int(self.ui.spinBox_XStart.value())
        elif spinBoxName == "XEnd":
            self.configCoorParams[1] = int(self.ui.spinBox_XEnd.value())
        elif spinBoxName == "YStart":
            self.configCoorParams[2] = int(self.ui.spinBox_YStart.value())
        elif spinBoxName == "YEnd":
            self.configCoorParams[3] =  int(self.ui.spinBox_YEnd.value())


    def createLayout_Container(self):
        self.scrollarea = QtWidgets.QScrollArea(self)
        self.scrollarea.setFixedWidth(150)
        self.scrollarea.setWidgetResizable(True)
        widget = QtWidgets.QWidget()
        self.layout_SArea = QtWidgets.QVBoxLayout(widget)
        for i in range(5):
            self.layout_SArea.addWidget(QtWidgets.QPushButton("Merhaba"))
        self.layout_SArea.addStretch(1)
        self.ui.gridLayout_Colors.addWidget(widget)
        self.scrollarea.setWidget(widget)

    def colorClicked(self,color):
        self.systemColor = color

    def verticalSliderValueChanged(self):
        x=2
        # print(self.ui.verticalSlider.value())

    def PauseTimer(self):
        self._status_update_timer.stop()
        self._status_update_timer_reader.stop()
        self._status_update_timer_waitKey.stop()
        if self.mode_v == self.modeList['Cuda/Normal+Thermal']:
            self.videoStreamNormal.stop()
            self.videoStreamThermal.stop()
        cv2.destroyAllWindows()

    def StartTimer(self):
        if self.mode_v == self.modeList['Cuda/Normal+Thermal']:
             self.videoStreamNormal = cm.VideoStream(configModule.Configuration.normalStreamPath,configModule).start()
             self.videoStreamThermal = cm.VideoStream(configModule.Configuration.thermalStreamPath, configModule,isThermal_=True).start()

        # if self.videoStream is None:
        self._status_update_timer.start()
        self._status_update_timer_reader.start()
        self._status_update_timer_waitKey.start()
        # self.videoStream = cm.VideoStream()

        # for i in range(len(self.merger.imagesRGB)) :
        #     returnImage = self.merger.ProcessMerge(self.merger.imagesRGB[i], self.merger.imagesTH[i],
        #                                            self.systemColor
        #                                            , thresholdMinVal=self.ui.verticalSlider.value(), mode=3,
        #                                            useCuda=False)
        #

    def show_image(self):
        print("showImage Basladi {0}".format(datetime.datetime.now()))
        if self.isFullScreen:
            cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Image", self.returnImage)


        print("showImage Bitti {0}".format(datetime.datetime.now()))

    def check_configuration(self):
        if self.isConfChanged:
            configModule.Configuration.set_variables_from_tccParams(self.configCoorParams)
            self.merger.refreshConfigModule = True


    def Process(self):
        print("Process Basladi {0}".format(datetime.datetime.now()))

        self.returnImage = self.merger.ProcessMerge(self.index,thresholdMinVal=self.ui.verticalSlider.maximum()- self.ui.verticalSlider.value()
                                                   ,mode=self.mode_v,videoStreamNormal=self.videoStreamNormal,videoStreamThermal=self.videoStreamThermal
                                               ,showDemoImages=self.ui.chk_ShowDemoImages.isChecked())
        key = str(cv2.waitKey(1))
        # print(str(key))
        self.isConfChanged = False
        if key == "119":
            # print("w")
            if self.configCoorParams[2] > 5:
                self.configCoorParams[2] = self.configCoorParams[2] - 5
                self.configCoorParams[3] = self.configCoorParams[3] - 5
                self.isConfChanged = True
        elif key == "97":
            # print("a")
            if self.configCoorParams[0] > 5:
                self.configCoorParams[0] = self.configCoorParams[0] - 5
                self.configCoorParams[1] = self.configCoorParams[1] - 5
                self.isConfChanged = True
        elif key == "115":
            # print("s")
            if self.configCoorParams[3] < configModule.Configuration.rows - 10:
                self.configCoorParams[2] = self.configCoorParams[2] + 5
                self.configCoorParams[3] = self.configCoorParams[3] + 5
                self.isConfChanged = True
        elif key == "100":
            # print("d")
            if self.configCoorParams[1] < configModule.Configuration.cols - 10:
                self.configCoorParams[0] = self.configCoorParams[0] + 5
                self.configCoorParams[1] = self.configCoorParams[1] + 5
                self.isConfChanged = True

        if key == "27":
            self.isFullScreen = False
            cv2.destroyAllWindows()

        print("Process Bitti {0}".format(datetime.datetime.now()))
        # self.showImage(returnImage)

        # t_start = timeit.default_timer()


        # height, width, channel = returnImage.shape
        # bytesPerLine = 3 * width
        # qImg = QtGui.QImage(returnImage.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        # pixmap01 = QtGui.QPixmap.fromImage(qImg)
        # pixmap_image = QtGui.QPixmap(pixmap01)
        # self.ui.imageLabel.setPixmap(pixmap_image)
        # self.ui.imageLabel.setScaledContents(True)



        # t_end = timeit.default_timer()
        # print("Ekrana Basma takes {:.5f} second".format((t_end - t_start)))
        #self.ui.imageLabel.update()
        #self.ui.imageLabel.setText(str(self.index))
        # if self.index == len(self.merger.imagesRGB)-1:
        #     self._status_update_timer.stop()
        #     self.index = 0
        #     self._status_update_timer.start()
        # self.index += 1
