import wave
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
rate = 44100
class wav:
    def __init__(self,path):
        self.path = path
        self.file_name = path.split('/')[-1]
        f = wave.open(path, "rb")
        self.params = f.getparams()
        self.nchannels, self.sampwidth, self.frame_rate, self.nframes = self.params[:4]
        self.wave_data = np.frombuffer(f.readframes(self.nframes),dtype=np.short).reshape(-1,2).T
        self.time = np.arange(0, self.nframes) * (1.0 / self.frame_rate)
        f.close()
        
    def show_wav(self):
        # 绘制波形
        plt.subplot(211) 
        plt.plot(self.time, self.wave_data[0])
        plt.subplot(212) 
        plt.plot(self.time, self.wave_data[1], c="g")
        plt.xlabel("time (seconds)")
        plt.show()

    def clip_by_vol(self,n,sec=1):
        left,right = self.wave_data
        dlen = len(right)
        index = 0
        clips = []
        while len(clips) < 6:
            tmp = right[index:index+self.frame_rate]
            start_index = np.argwhere(tmp > n)
            if len(start_index) != 0:
                si = start_index[0,0]+index
                ei = si+int(self.frame_rate*sec)
                clips.append(right[si:ei])
                index = ei
            else:
                index += self.frame_rate
        return clips
    
    def write_wav(self,data,save_path):
        f = wave.open(save_path, "wb")
        # 配置声道数、量化位数和取样频率
        f.setnchannels(1)
        f.setsampwidth(self.sampwidth)
        f.setframerate(self.frame_rate)
        f.writeframes(data.tostring())
        f.close()


def labels_segment(file,save_dir=None):
    w = wav(file)
    t = w.clip_by_vol(5000,1)
    rnd_code = file.split('_')[-1][:-4]
    if not save_dir:
        save_dir = os.path.dirname(file)+'/'
    save_dir = save_dir + rnd_code + '/'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for i,d in enumerate(t):
        w.write_wav(d,save_dir+'{}.wav'.format(str(i)))
    shutil.move(file,save_dir+os.path.basename(file))
    print('({}) segmented.'.format(file))
    return rnd_code

