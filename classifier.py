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
        return (keys[m],acc[m])