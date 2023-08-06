# cf_clearance
Reference from [playwright_stealth](https://github.com/AtuboDad/playwright_stealth) and [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

Purpose To make a cloudflare challenge pass successfully, Can be use cf_clearance bypassed by cloudflare, However, with the cf_clearance, make sure you use the same IP and UA as when you got it.

## Warning
Please use interface mode, You must add headless=False.  
If you use it on linux or docker, use XVFB.

## Install

```
$ pip install cf_clearance
```

## Usage
### sync
```python
from playwright.sync_api import sync_playwright
from cf_clearance import sync_retry, stealth_sync
import requests

# not use cf_clearance, cf challenge is fail
proxies = {
    "all": "socks5://localhost:7890"
}
res = requests.get('https://nowsecure.nl', proxies=proxies)
if '<title>Please Wait... | Cloudflare</title>' in res.text:
    print("cf challenge fail")
# get cf_clearance
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"})
    page = browser.new_page()
    stealth_sync(page)
    page.goto('https://nowsecure.nl')
    res = sync_retry(page)
    if res:
        cookies = page.context.cookies()
        for cookie in cookies:
            if cookie.get('name') == 'cf_clearance':
                cf_clearance_value = cookie.get('value')
                print(cf_clearance_value)
        ua = page.evaluate('() => {return navigator.userAgent}')
        print(ua)
    else:
        print("cf challenge fail")
    browser.close()
# use cf_clearance, must be same IP and UA
headers = {"user-agent": ua}
cookies = {"cf_clearance": cf_clearance_value}
res = requests.get('https://nowsecure.nl', proxies=proxies, headers=headers, cookies=cookies)
if '<title>Please Wait... | Cloudflare</title>' not in res.text:
    print("cf challenge success")
```
### async
```python
import asyncio
from playwright.async_api import async_playwright
from cf_clearance import async_retry, stealth_async
import requests


async def main():
    # not use cf_clearance, cf challenge is fail
    proxies = {
        "all": "socks5://localhost:7890"
    }
    res = requests.get('https://nowsecure.nl', proxies=proxies)
    if '<title>Please Wait... | Cloudflare</title>' in res.text:
        print("cf challenge fail")
    # get cf_clearance
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy={"server": "socks5://localhost:7890"})
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto('https://nowsecure.nl')
        res = await async_retry(page)
        if res:
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie.get('name') == 'cf_clearance':
                    cf_clearance_value = cookie.get('value')
                    print(cf_clearance_value)
            ua = await page.evaluate('() => {return navigator.userAgent}')
            print(ua)
        else:
            print("cf challenge fail")
        await browser.close()
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get('https://nowsecure.nl', proxies=proxies, headers=headers, cookies=cookies)
    if '<title>Please Wait... | Cloudflare</title>' not in res.text:
        print("cf challenge success")

asyncio.get_event_loop().run_until_complete(main())
```