import audio_crawler as crawler
import codec
import wav
import numpy as np
import os
"""
crawler.run(1,1,'tmp/')
target_dir = ''

for f in os.listdir('tmp/'):
    codec.convert('tmp/'+f)
    target_dir = 'tmp/'+wav.labels_segment('tmp/'+f[:-3]+'wav')
"""
labels = {}
for l in os.listdir('data/labels/'):
    labels[l[0]] = wav.wav('data/labels/'+l).wave_data[0]
keys = list(labels.keys())
"""
for i in range(6):
    file = (target_dir+'/{}.wav').format(i)
    print(labels[wav.wav(file).wave_data.tostring()])"""

for no in os.listdir('segmented/'):
    target_dir = 'segmented/'+no
    ans = ''
    print(no)
    for i in range(6):
        file = (target_dir+'/{}.wav').format(i)
        acc = []
        for v in labels.values():
            acc.append((np.mean(v==wav.wav(file).wave_data[0])))
        m = np.argmax(acc)
        print(keys[m],acc[m])
    #print(no+': '+ans)
    input()