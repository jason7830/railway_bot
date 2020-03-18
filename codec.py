import subprocess as sp
from threading import Thread
from queue import Queue,Empty
from multiprocessing import Manager
import os 
import re
import shutil
import argparse
import logging


def getabit(o,q):
    for c in iter(lambda:o.read(1),b''):
        q.put(c)
#    print('PIPE CLOSED')
    o.close()

def getdata(q):
    r = b''
    while True:
        try:
            c = q.get(False)
            if c.decode() == '\n':
                r+=c
                break
        except Empty:
            return None
        else:
            r += c
    return r
        
def clip_convert(file,start_sec,seconds,output):
    arg = 'ffmpeg -y -i {} -ss {} -t {} {}'.format(file,start_sec,seconds,output)
    #print(arg)
    pobj = sp.Popen(arg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT,shell=True)
    q = Queue()
    t = Thread(target=getabit,args=(pobj.stdout,q))
    t.daemon = True
    t.start()
    """
    s =""
    while True:
        try:
            tmp = getdata(q)
            if tmp is not None:
                s = tmp.decode()
        except UnicodeDecodeError:
            print("UnicodeDecodeError...")
        print(s[:-2],end='\r')
        if (not t.isAlive()) and tmp is None:
            break
    print('\n'+s+'\n'+str(re.match(r'muxing overhead.+',s)))

    """
    return t

def convert(file,save_dir=None,processed_dir=None):
    if save_dir:
        output_file = save_dir+os.path.basename(file)[:-3]+'wav'
    else:
        output_file = file[:-3]+'wav'
    t = clip_convert(file,15.2,14,output_file)
    t.join()
    print('converted: '+output_file)
    if processed_dir:
        shutil.move(file,processed_dir+file)
        print('({}) converted to >> ({})'.format(input_file,output_file))

def convert_all(mp3_dir,save_dir=None,processed_dir=None):
    for file in os.listdir(mp3_dir):
        input_file = mp3_dir+file
        convert(input_file,save_dir,processed_dir)

def main():
    #logs
    logging.basicConfig(filename='craw.log',level=logging.INFO,format='%(asctime)s - [%(levelname)s] - %(message)s')
    parser = argparse.ArgumentParser(description='Crawl audio captcha.')
    parser.add_argument('-td', nargs='?',
        help='target directory where the downloaded mp3 files at.')
    parser.add_argument('-sd', nargs='?',
        help='save directory where to save the converted and clipped wav files. (Means removed the head and the tail parts.)')
    parser.add_argument('-pd', nargs='?',
        help='processed directory where to move and keep the origin mp3 file.')
    args = parser.parse_args()

    if args.d == None:
        print('-dir arg neeeded.')
        return 0    
    mp3_dir = args.td+'/'
    save_dir = args.sd+'/'
    processed_dir = args.pd+'/'
    convert_all(mp3_dir,save_dir,processed_dir)
    
    #asyncio.ensure_future(crawler(args.d).multi_pager(args.bn,args.n))

if __name__ == '__main__':
    main()