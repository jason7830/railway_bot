import asyncio
import argparse
import logging
from pyppeteer import launch
from pyppeteer.network_manager import Request
import requests
import time
import queue

class crawler:
    def __init__(self,save_dir):
        self.save_dir = save_dir
        self.audio_url = 'https://www.railway.gov.tw/tra-tip-web/tip/player/audio?pageRandom='
        self.output_msg = ''
        self.headers = None
        self.download_links = []

    
    def download_link(self,url,headers,file_name):
        with requests.get(url,allow_redirects=True,headers=headers,stream=True) as r:
            with open(file_name,'wb') as f:
                chunk_size=51200
                for i,chunck in enumerate(r.iter_content(chunk_size=chunk_size)):
                    if chunck:
                        f.write(chunck)
                
    async def inter_requests(self,request):
        if 'audio?pageRandom=' in request.url:
            file_name = self.save_dir+'/audio_{}.mp3'.format(request.url.split('=')[1])
            self.download_link(request.url,request.headers,file_name)
            #self.download_links.append[request.url,request.headers,file_name]
            self.output_msg = '\tDownloaded audio: {}'.format(file_name)
            #print('Downloaded audio: {}'.format(file_name))
        await request.continue_()
    
    async def skipper_(self,request):
        if request.resourceType in ['image', 'stylesheet', 'font']:
            await request.abort()
        else:
            await request.continue_()

    async def intercept_audio(self,request):
        if 'audio' in request.url:    
            num = len(self.audio_rnds)
            urls = [self.audio_url+str(rnd) for rnd in self.audio_rnds.values()]
            for i,u in enumerate(urls):
                file_name = self.save_dir+'/audio_{}.mp3'.format(u.split('=')[1])
                print('Downloading audios {}/{} : {}'.format(i+1,num,file_name))
                self.download_link(u,request.headers,file_name)
                time.sleep(0.5)
        await request.continue_()
        
    async def audios(self,page):
        await page.bringToFront()
        await page.setRequestInterception(True)
        page.on('request',self.inter_requests)
        page.waitForSelector('#playMusic')
        await page.evaluate('$("#playMusic").click();')
        await page.waitFor(500)
        await page.setRequestInterception(False)
    
    async def multi_pager(self,browsers_num,num_ea):
        count = browsers_num*num_ea
        #browsers = queue.Queue(browsers_num)
        browsers = []
        for i in range(browsers_num):
            browser = await launch(headless=True)
            p = await browser.pages()
            await p[0].setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')
            browsers.append(browser)

        async def tmp(b):
            p = await b.pages()
            await p[0].goto('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query')
                
        while count > 0:
            browsers_runner = [tmp(b) for i,b in enumerate(browsers)]
            await asyncio.wait(browsers_runner)
            for i,b in enumerate(browsers):
                p = await b.pages()
                await self.audios(p[0])
                print(' Browser {}. (Audio {}.)'.format(i+1,count)+self.output_msg)
                count -= 1
        for b in browsers:
            await b.close()
        #print(self.download_links)
        print('Done!')

def run(browsers_num,n,save_dir):
    c = crawler(save_dir)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.multi_pager(browsers_num,n))
    loop.close()

def main():
    #logs
    logging.basicConfig(filename='craw.log',level=logging.INFO,format='%(asctime)s - [%(levelname)s] - %(message)s')
    parser = argparse.ArgumentParser(description='Crawl audio captcha.')
    parser.add_argument('-bn', type=int,
        help='Number of browser to crawl at the same time.')
    parser.add_argument('-n', type=int,
        help='Number of audio captchas to crawl for each browser.')
    parser.add_argument('-d','-dir', nargs='?',
        help='Save directory.')
    args = parser.parse_args()

    if args.d == None:
        print('-dir arg neeeded.')
        return 0    
    run(args.bn,args.n,args.d)
    #asyncio.ensure_future(crawler(args.d).multi_pager(args.bn,args.n))

if __name__ == '__main__':
    main()