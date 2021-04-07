import json



class Configuration:
    """
      Configs.json dosyasindan konfigurasyon verilerini okuyan static yapi.
      ** Cuda uzerinden gittigimiz icin boyutlar onemli. Eger Koordinatlari degistiriyorsak
         Width ve Height degerlerini de set etmemiz gerekiyor.
    """
    configurations = ""
    rows = ""
    cols = ""
    dims = ""
    normalStreamPath = ""
    thermalStreamPath = ""
    thermalCalibrationParameters_thermalWidth  = None
    thermalCalibrationParameters_thermalHeight = None
    thermalCalibrationParameters_thermal_XStart = None
    thermalCalibrationParameters_thermal_XEnd = None
    thermalCalibrationParameters_thermal_YStart = None
    thermalCalibrationParameters_thermal_YEnd = None
    datasetDemoNormalPath = None
    datasetDemoThermalPath = None
    cudaBlockThreadCount = None
    @staticmethod
    def setVariables(path):
        try:
            with open(path) as data_file:
                Configuration.configurations = json.load(data_file)
                Configuration.datasetDemoNormalPath = Configuration.configurations['datasetDemoNormalPath']
                Configuration.datasetDemoThermalPath = Configuration.configurations['datasetDemoThermalPath']
                Configuration.cudaBlockThreadCount = int(Configuration.configurations['cudaBlockThreadCount'])
                Configuration.rows = Configuration.configurations['shape']['rows']
                Configuration.cols = Configuration.configurations['shape']['cols']
                Configuration.dims = Configuration.configurations['shape']['dims']
                Configuration.normalStreamPath = Configuration.configurations['normalStreamPath']
                Configuration.thermalStreamPath = Configuration.configurations['thermalStreamPath']
                Configuration.thermalCalibrationParameters_thermal_XStart = \
                Configuration.configurations['thermalParameters']['thermal_XStart']
                Configuration.thermalCalibrationParameters_thermal_XEnd = \
                Configuration.configurations['thermalParameters']['thermal_XEnd']
                Configuration.thermalCalibrationParameters_thermal_YStart = \
                Configuration.configurations['thermalParameters']['thermal_YStart']
                Configuration.thermalCalibrationParameters_thermal_YEnd = \
                    Configuration.configurations['thermalParameters']['thermal_YEnd']
                Configuration.thermalCalibrationParameters_thermalWidth = int(Configuration.thermalCalibrationParameters_thermal_XEnd) - int(Configuration.thermalCalibrationParameters_thermal_XStart)
                Configuration.thermalCalibrationParameters_thermalHeight = int(Configuration.thermalCalibrationParameters_thermal_YEnd) - int(Configuration.thermalCalibrationParameters_thermal_YStart)

        except BaseException as e:
            print(str(e))

    @staticmethod
    def set_variables_from_tccParams(arr):
        Configuration.thermalCalibrationParameters_thermal_XStart = arr[0]
        Configuration.thermalCalibrationParameters_thermal_XEnd = arr[1]
        Configuration.thermalCalibrationParameters_thermal_YStart = arr[2]
        Configuration.thermalCalibrationParameters_thermal_YEnd = arr[3]
        Configuration.thermalCalibrationParameters_thermalWidth = int(
            Configuration.thermalCalibrationParameters_thermal_XEnd) - int(
            Configuration.thermalCalibrationParameters_thermal_XStart)
        Configuration.thermalCalibrationParameters_thermalHeight = int(
            Configuration.thermalCalibrationParameters_thermal_YEnd) - int(
            Configuration.thermalCalibrationParameters_thermal_YStart)

    # @staticmethod
    # def setVariables():
    #     try:
    #         with open('../ConfigurationModule/Configs.json') as data_file:
    #             configurations = json.load(data_file)
    #             rows = configurations['shape']['rows']
    #             cols = configurations['shape']['cols']
    #             dims = configurations['shape']['dims']
    #             normalStreamPath = configurations['normalStreamPath']
    #             thermalStreamPath = configurations['thermalStreamPath']
    #     except BaseException as e:
    #         print(str(e))