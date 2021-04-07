* Örnek Resimler aþaðýdaki linklerden indirilmiþtir. 
http://www02.smt.ufrj.br/~fusion/#VID1.1


http://vcipl-okstate.org/pbvs/bench/Data/03/download.html

* Sistemde örnek olarak gösterilen resimler sisteme kaydedilmiþtir. Programdaki resimler þu anda 
deðiþtirilememektedir.

* 4 farklý kamera görseli mevcuttur. 
  1) Heatmap -> Termal kamerasýndan gelen goruntuye göre ýsý haritasýný olusturmaktadýr
  2) Normal Görüntü -> Normal kameradan gelen RGB görüntüyü yansýtmaktadýr.
  3) Termal Görüntü -> Termal kameradan gelen görüntü yansýltýlmaktadýr.
  4) Normal + Termal Görüntü -> Normal görüntü (RGB görüntü) ile termal kameradan elde edilen heatmap görüntüsü birleþtirilmektedir. Threshold deðerine göre renklendirme yapýlmaktadýr. 

******************************** Cuda Exe için *******************************************************
NUMBAPRO_NVVM = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\bin\nvvm64_31_0.dll

NUMBAPRO_LIBDEVICE = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\libdevice\

export NUMBAPRO_NVVM=/usr/local/cuda-9.0/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/usr/local/cuda-9.0/nvvm/libdevice/



** Cuda Toolkit kurulmalýdýr.
** Yukarýdakilerin Sistem ve Ortam deðiþkenlerine eklenmesi gerekmektedir.
******************************** Cuda Exe için *******************************************************
