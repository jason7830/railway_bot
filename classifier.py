import audio_crawler as crawler
import codec
import wav
import numpy as np
import os

class classifier:
    def __init__(self):
        self.labels = {}
        for l in os.listdir('data/labels/'):
            self.labels[l[0]] = wav.wav('data/labels/'+l).wave_data[0]
        self.keys = list(self.labels.keys())


    def get_class(self,data):
        acc = []
        for v in self.labels.values():
            acc.append((np.mean(v==data)))
        m = np.argmax(acc)
        return (self.keys[m],acc[m])

    def load(self,target):
        codec.convert(target)
        self.labels_dir = os.path.join(os.path.dirname(target),wav.labels_segment(target[:-3]+'wav'))
        print(self.labels_dir)
        for i in range(6):
            file = (self.labels_dir+'/{}.wav').format(i)
            data = wav.wav(file).wave_data[0]
            ans = self.get_class(data)
            print('{}.wav: {} - ( {:.2f}% )'.format(i,ans[0],float(ans[1])*100))
