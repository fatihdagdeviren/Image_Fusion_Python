* Örnek Resimler aşağıdaki linklerden indirilmiştir. 
http://www02.smt.ufrj.br/~fusion/#VID1.1


http://vcipl-okstate.org/pbvs/bench/Data/03/download.html

* Sistemde örnek olarak gösterilen resimler sisteme kaydedilmiştir. Programdaki resimler şu anda 
değiştirilememektedir.

* 4 farklı kamera görseli mevcuttur. 
  1) Heatmap -> Termal kamerasından gelen goruntuye göre ısı haritasını olusturmaktadır
  2) Normal Görüntü -> Normal kameradan gelen RGB görüntüyü yansıtmaktadır.
  3) Termal Görüntü -> Termal kameradan gelen görüntü yansıltılmaktadır.
  4) Normal + Termal Görüntü -> Normal görüntü (RGB görüntü) ile termal kameradan elde edilen heatmap görüntüsü birleştirilmektedir. Threshold değerine göre renklendirme yapılmaktadır. 

******************************** Cuda Exe için *******************************************************
NUMBAPRO_NVVM = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\bin\nvvm64_31_0.dll

NUMBAPRO_LIBDEVICE = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\libdevice\

export NUMBAPRO_NVVM=/usr/local/cuda-9.0/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/usr/local/cuda-9.0/nvvm/libdevice/



** Cuda Toolkit kurulmalıdır.
** Yukarıdakilerin Sistem ve Ortam değişkenlerine eklenmesi gerekmektedir.
******************************** Cuda Exe için *******************************************************
