import asyncio
from aiohttp_requests import requests
import os, re

def toDomain(url):
    return re.sub(r'^https?://', '', url)


async def get_sites(sem,url,foxhousePath): 
    async with sem:            
        print(url)
        domain = toDomain(url)
        filepath = os.path.join(foxhousePath,domain + '.html')
        try:
            res = await requests.get('http://'+domain, timeout=10)
            page = await res.text()
            with open(filepath,'w') as f:
                f.write(page)
        except Exception as e:
            with open(filepath,'w') as f:
                f.write('timeout')
            print(e)
        os.chmod(filepath,0o666)

async def scrapeurls(urls, foxhousePath='websites_foxhouse'):
    if not os.path.exists(foxhousePath):
        os.mkdir(foxhousePath)
    tasks = []
    sem = asyncio.Semaphore(50)
    for url in urls:
        tasks.append(asyncio.create_task(get_sites(sem,url,foxhousePath)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = ['ibm.com','idc.com']
    asyncio.run(scrapeurls(urls))