import audio_crawler as crawler
import codec
import wav
import numpy as np
import os
from classifier import classifier
target_dir = 'tmp/'
crawler.run(1,1,target_dir)

for f in os.listdir(target_dir):
    codec.convert(target_dir+f)
    labels_dir = target_dir+wav.labels_segment('tmp/'+f[:-3]+'wav')
classer = classfier()
"""
for i in range(6):
    file = (target_dir+'/{}.wav').format(i)
    print(labels[wav.wav(file).wave_data.tostring()])"""
"""
for no in os.listdir('segmented/'):
    target_dir = 'segmented/'+no
    ans = ''
    print(no)
    for i in range(6):
        file = (target_dir+'/{}.wav').format(i)
        data = wav.wav(file).wave_data[0]
        print(classer.get_class(data))"""