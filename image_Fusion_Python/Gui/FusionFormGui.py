# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Asis/image_Fusion_Python/RaspForm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName("GroupBox")
        GroupBox.setWindowModality(QtCore.Qt.WindowModal)
        GroupBox.setEnabled(True)
        GroupBox.resize(315, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GroupBox.sizePolicy().hasHeightForWidth())
        GroupBox.setSizePolicy(sizePolicy)
        GroupBox.setMinimumSize(QtCore.QSize(315, 450))
        GroupBox.setMaximumSize(QtCore.QSize(315, 500))
        GroupBox.setMouseTracking(True)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(GroupBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 291, 471))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setBaseSize(QtCore.QSize(1, 0))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 20, 41, 241))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.horizontalLayout.addWidget(self.verticalSlider)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 181, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_Thermal = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_Thermal.setObjectName("radioButton_Thermal")
        self.verticalLayout.addWidget(self.radioButton_Thermal)
        self.radioButton_ThermalVisible = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_ThermalVisible.setObjectName("radioButton_ThermalVisible")
        self.verticalLayout.addWidget(self.radioButton_ThermalVisible)
        self.radioButton_ThermalVisible_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_ThermalVisible_2.setObjectName("radioButton_ThermalVisible_2")
        self.verticalLayout.addWidget(self.radioButton_ThermalVisible_2)
        self.radioButton_VisibleThermal = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_VisibleThermal.setObjectName("radioButton_VisibleThermal")
        self.verticalLayout.addWidget(self.radioButton_VisibleThermal)
        self.radioButton_CudaMerge = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_CudaMerge.setObjectName("radioButton_CudaMerge")
        self.verticalLayout.addWidget(self.radioButton_CudaMerge)
        self.radioButton_CudaHeatmap = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_CudaHeatmap.setObjectName("radioButton_CudaHeatmap")
        self.verticalLayout.addWidget(self.radioButton_CudaHeatmap)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 20, 49, 241))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_Colors = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_Colors.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_Colors.setObjectName("verticalLayout_Colors")
        self.labelHeatMapImage = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.labelHeatMapImage.setObjectName("labelHeatMapImage")
        self.verticalLayout_Colors.addWidget(self.labelHeatMapImage)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 125))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lbl_XStart_Up = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_XStart_Up.setGeometry(QtCore.QRect(50, 40, 81, 51))
        self.lbl_XStart_Up.setText("")
        self.lbl_XStart_Up.setPixmap(QtGui.QPixmap("Temp/Images/arrows.png"))
        self.lbl_XStart_Up.setScaledContents(True)
        self.lbl_XStart_Up.setObjectName("lbl_XStart_Up")
        self.spinBox_XStart = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_XStart.setGeometry(QtCore.QRect(3, 60, 41, 22))
        self.spinBox_XStart.setMaximum(1920)
        self.spinBox_XStart.setObjectName("spinBox_XStart")
        self.spinBox_XEnd = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_XEnd.setGeometry(QtCore.QRect(138, 60, 41, 22))
        self.spinBox_XEnd.setMaximum(1920)
        self.spinBox_XEnd.setObjectName("spinBox_XEnd")
        self.spinBox_YStart = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_YStart.setGeometry(QtCore.QRect(70, 14, 41, 22))
        self.spinBox_YStart.setMaximum(1920)
        self.spinBox_YStart.setObjectName("spinBox_YStart")
        self.spinBox_YEnd = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_YEnd.setGeometry(QtCore.QRect(70, 94, 41, 22))
        self.spinBox_YEnd.setMaximum(1920)
        self.spinBox_YEnd.setObjectName("spinBox_YEnd")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(200, 40, 81, 80))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_SetThermalConf = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_SetThermalConf.setFont(font)
        self.btn_SetThermalConf.setDefault(False)
        self.btn_SetThermalConf.setFlat(False)
        self.btn_SetThermalConf.setObjectName("btn_SetThermalConf")
        self.verticalLayout_2.addWidget(self.btn_SetThermalConf)
        self.btn_SaveThermalConf = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_SaveThermalConf.setFont(font)
        self.btn_SaveThermalConf.setDefault(False)
        self.btn_SaveThermalConf.setFlat(False)
        self.btn_SaveThermalConf.setObjectName("btn_SaveThermalConf")
        self.verticalLayout_2.addWidget(self.btn_SaveThermalConf)
        self.chk_ShowDemoImages = QtWidgets.QCheckBox(self.groupBox_2)
        self.chk_ShowDemoImages.setGeometry(QtCore.QRect(180, 10, 109, 17))
        self.chk_ShowDemoImages.setObjectName("chk_ShowDemoImages")
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.PauseButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.PauseButton_2.setObjectName("PauseButton_2")
        self.verticalLayout_3.addWidget(self.PauseButton_2)
        self.StartButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.StartButton.setObjectName("StartButton")
        self.verticalLayout_3.addWidget(self.StartButton)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        # GroupBox.setTitle(_translate("GroupBox", "Image Fusion App"))
        self.groupBox.setTitle(_translate("GroupBox", "Options"))
        self.radioButton_Thermal.setText(_translate("GroupBox", "Heatmap"))
        self.radioButton_ThermalVisible.setText(_translate("GroupBox", "Thermal Camera"))
        self.radioButton_ThermalVisible_2.setText(_translate("GroupBox", "Normal Camera"))
        self.radioButton_VisibleThermal.setText(_translate("GroupBox", "Normal + Thermal Camera"))
        self.radioButton_CudaMerge.setText(_translate("GroupBox", "Cuda Merge"))
        self.radioButton_CudaHeatmap.setText(_translate("GroupBox", "Cuda Heatmap"))
        self.labelHeatMapImage.setText(_translate("GroupBox", "TextLabel"))
        self.groupBox_2.setTitle(_translate("GroupBox", "TCC"))
        self.btn_SetThermalConf.setText(_translate("GroupBox", "Apply"))
        self.btn_SaveThermalConf.setText(_translate("GroupBox", "Save"))
        self.chk_ShowDemoImages.setText(_translate("GroupBox", "Use Demo Images"))
        self.PauseButton_2.setText(_translate("GroupBox", "Pause"))
        self.StartButton.setText(_translate("GroupBox", "Start"))

