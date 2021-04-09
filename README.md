# railway_bot

Solving audio captcha

Steps
---
* `Step1.` Crawl down the audio captcha with pyppeteer.
* `Step2.` Convert mp3 to wav with ffmpeg.
* `Step3.` Seperate letters from wav file according to the waveform.
* `Step3.` Compare to the classifed letter's waveform.
