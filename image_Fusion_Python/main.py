from Gui import FusionFormGuiEvents as gui
from PyQt5 import QtWidgets
import sys
import os


if __name__ == "__main__":
    Program = QtWidgets.QApplication(sys.argv)
    MyProg = gui.Prog()
    MyProg.show()
    sys.exit(Program.exec_())

    #m = MergerModule.MergerModule()
    #m.imagesRGBPath=  "D:/Asis/Image_Fusion_Datasets/1b"
    #m.imagesTHPath = "D:\\Asis\\Image_Fusion_Datasets\\1a"
    #m.Process()
