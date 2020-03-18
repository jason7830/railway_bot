import asyncio
import argparse
import logging
from pyppeteer import launch
from pyppeteer.network_manager import Request
from pyppeteer.errors import NetworkError
import requests
import time
import queue
import multiprocessing as mp
import re
from classifier import classifier

class Browser:
    def __init__(self,save_dir):
        self.save_dir = save_dir
        self.dt = None
        self.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        pass

    def download_link(self,url,headers,file_name):
        with requests.get(url,allow_redirects=True,headers=headers,stream=True) as r:
            with open(file_name,'wb') as f:
                chunk_size=51200
                for i,chunck in enumerate(r.iter_content(chunk_size=chunk_size)):
                    if chunck:
                        f.write(chunck)

    async def inter_requests(self,request):
        try:
            if request.resourceType in ['stylesheet', 'font'] and (not re.search('.+(google-analytics)|(base64)',request.url)):
                await request.abort()
                return
            if 'audio?pageRandom=' in request.url:
                file_name = self.save_dir+'/audio_{}.mp3'.format(request.url.split('=')[1])
                self.dt = mp.Process(target=self.download_link,args=(request.url,request.headers,file_name))
                self.dt.start()
                self.mp3_file = file_name
                self.downloaded = True
                self.output_msg = '\tDownloaded audio: {}'.format(file_name)
            await request.continue_()
        except NetworkError as ne:
            print(request.url,ne)

    async def inter_skipper(self,request):
        if request.resourceType in ['image', 'stylesheet', 'font']:
            await request.abort()
        else:
            try:
                await request.continue_()
            except NetworkError as ne:
                pass

    def timer(self):
        return '{:.3f}'.format(time.time()-self.init_time)

    async def audios(self,page):
        #await page.bringToFront()
        self.downloaded = False
        await page.waitForSelector('#playMusic')  
        await page.evaluate('$("#playMusic").click();')
        while not self.downloaded:
            await page.waitFor(50)


    async def init(self,url=None,headless=True):
        self.bot = await launch(headless=headless)
        self.pages = await self.bot.pages()
        if url:
            await self.pages[0].setUserAgent(self.userAgent)
            await self.pages[0].goto(url)

    async def loader(self,page,url):
        await page.bringToFront()
        await page.setRequestInterception(True)
        page.on('request',self.inter_requests)        
        async def _():
            await page.setUserAgent(self.userAgent)
            await page.goto(url)
        await asyncio.wait([_(),page.waitForNavigation()])
        print('loading time: {} sec.'.format(self.timer()))

    async def run(self,load=None):
        self.pages = await self.bot.pages()
        page = self.pages[0]        
        if load:
            input('Start!')
            self.init_time = time.time()
            await self.loader(page,load)
        #input('start?')
        await self.audios(page)
        while self.dt.is_alive():
            time.sleep(0.05)
        print('downloading time: {} sec.'.format(self.timer()))
        self.init_time = time.time()
        classifier().load(self.mp3_file)
        print('classified time: {} sec.'.format(self.timer()))

async def main():
    b = Browser('tmp/')
    await b.init(headless=True)
    await b.run(load='https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query')
    


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#loop.close()
