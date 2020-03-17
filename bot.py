import asyncio
from pyppeteer import launch
from pyppeteer.network_manager import Request
import requests
import time
import queue
import audio_crawler as crawler
import codec
import wav
import numpy as np
import os
from classifier import classifier

class Browser:
    def __init__(self,save_dir):
        self.save_dir = save_dir
        self.file_name = ''
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
        if request.resourceType in ['image', 'stylesheet', 'font']:
            await request.abort()
            return
        if 'audio?pageRandom=' in request.url:
            self.file_name = self.save_dir+'/audio_{}.mp3'.format(request.url.split('=')[1])
            self.download_link(request.url,request.headers,self.file_name)
            #self.download_links.append[request.url,request.headers,file_name]
            self.output_msg = '\tDownloaded audio: {}'.format(self.file_name)
            #print('Downloaded audio: {}'.format(file_name))
        await request.continue_()

    async def audios(self,page):
        page.waitForSelector('#playMusic')
        await page.evaluate('$("#playMusic").click();')
        await page.waitFor(500)
        

    async def preload(self,url=None,headless=True):
        self.bot = await launch(headless=headless)
        self.pages = await self.bot.pages()
        if url:
            await self.pages[0].setUserAgent(self.userAgent)
            await self.pages[0].goto(url)

    async def run(self,load=None):
        pages = await self.bot.pages()
        page = pages[0]
        await page.bringToFront()
        await page.setRequestInterception(True)
        page.on('request',self.inter_requests)
        if load:
            await page.setUserAgent(self.userAgent)
            await page.goto(load)
            self.init_time = time.time()
        await self.audios(self.pages[0])
        print(time.time()-self.init_time)
        classifier().load(self.file_name)
        input()

async def main():
    b = Browser('tmp/')
    await b.preload(headless=False)
    await b.run(load='https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
