import pygame as pygame
import os
import time
import mmap
class player:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096) #frequency, size, channels, buffersize
        pygame.mixer.init() #turn all of pygame on.
        self.clock = pygame.time.Clock()
        
    def load_to_mem(self,file):
        with open(file) as f: 
            self.m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    
    def play(self,music_file,mem_loader=True):
        '''
        stream music with mixer.music module in blocking manner
        this will stream the sound from disk while playing
        '''
        try:
            if mem_loader:
                self.load_to_mem(music_file)
                pygame.mixer.music.load(self.m)
            else:
                pygame.mixer.music.load(music_file)
            #print("Music file {} loaded!".format(music_file))
        except pygame.error:
            print("File {} not found! {}".format(music_file, pygame.get_error()))
            return

        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.5)
        #clock.tick(10)
        #while pygame.mixer.music.get_busy():
            #clock.tick(10)
            
    def stop(self):
        pygame.mixer.music.stop()
        self.m.close()
    
    def quit(self):
        pygame.quit()

import shutil

def run():
    seg_dir = 'segmented/'
    labeled_dir = seg_dir+'labeled/'
    p = player()
    if not os.path.isdir(labeled_dir):
            os.mkdir(labeled_dir)
    for no in os.listdir(seg_dir):
        curr = seg_dir+no + '/'
        print('Start : ' + curr)
        label = ''
        files = list(os.listdir(seg_dir+no))
        if len(files) != 7:
            print('File number error.')
            return
        i = 0
        while i <= 5:
            p.play(os.path.abspath(curr+files[i]))
            print('File '+str(i)+': ',end='')
            tmp = input()
            if tmp == '':
                print('Replay.')
                p.stop()
                continue
            elif tmp == 'xx':
                print('Stopped')
                p.stop()
                return
            elif tmp == 'zz':
                print('Previous')
                p.stop()
                label = label[:-1]
                i-=1
                continue
            label += tmp
            #shutil.move(curr+f,labeled_dir+str(i)+'_'+label+'.wav')
            p.stop()
            #shutil.move(curr+f,curr+str(i)+'_'+label+'.wav')
            i+=1
        dst = labeled_dir+no+'_'+label
        shutil.move(curr,dst)
        print(dst + ' (moved.)')
    p.quit()
run()