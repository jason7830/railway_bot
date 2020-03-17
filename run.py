import audio_crawler as crawler
import codec
import wav
import numpy as np
import os
from classifier import classifier
target_dir = 'tmp/'
crawler.run(1,1,target_dir)

for f in os.listdir(target_dir):
    if '.mp3' in f:
        codec.convert(target_dir+f)
        labels_dir = target_dir+wav.labels_segment(f[:-3]+'wav')
classer = classifier()

for i in range(6):
    file = (labels_dir+'/{}.wav').format(i)
    data = wav.wav(file).wave_data[0]
    ans = classer.get_class(data)
    print('{}.wav: {} - ( {:.2f}% )'.format(i,ans[0],float(ans[1])*100))
