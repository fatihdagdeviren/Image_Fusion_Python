* �rnek Resimler a�a��daki linklerden indirilmi�tir. 
http://www02.smt.ufrj.br/~fusion/#VID1.1


http://vcipl-okstate.org/pbvs/bench/Data/03/download.html

* Sistemde �rnek olarak g�sterilen resimler sisteme kaydedilmi�tir. Programdaki resimler �u anda 
de�i�tirilememektedir.

* 4 farkl� kamera g�rseli mevcuttur. 
  1) Heatmap -> Termal kameras�ndan gelen goruntuye g�re �s� haritas�n� olusturmaktad�r
  2) Normal G�r�nt� -> Normal kameradan gelen RGB g�r�nt�y� yans�tmaktad�r.
  3) Termal G�r�nt� -> Termal kameradan gelen g�r�nt� yans�lt�lmaktad�r.
  4) Normal + Termal G�r�nt� -> Normal g�r�nt� (RGB g�r�nt�) ile termal kameradan elde edilen heatmap g�r�nt�s� birle�tirilmektedir. Threshold de�erine g�re renklendirme yap�lmaktad�r. 

******************************** Cuda Exe i�in *******************************************************
NUMBAPRO_NVVM = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\bin\nvvm64_31_0.dll

NUMBAPRO_LIBDEVICE = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.1\nvvm\libdevice\

export NUMBAPRO_NVVM=/usr/local/cuda-9.0/nvvm/lib64/libnvvm.so
export NUMBAPRO_LIBDEVICE=/usr/local/cuda-9.0/nvvm/libdevice/



** Cuda Toolkit kurulmal�d�r.
** Yukar�dakilerin Sistem ve Ortam de�i�kenlerine eklenmesi gerekmektedir.
******************************** Cuda Exe i�in *******************************************************
