import asyncio
from aiohttp_requests import requests
from kumihotools import toDomain
import os

foxhousePath = '/var/rel8ed.to/MQproject/foxhouse/'

async def get_sites(sem,url): 
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

async def scrapeurls(urls, ):
    tasks = []
    sem = asyncio.Semaphore(50)
    for url in urls:
        tasks.append(asyncio.create_task(get_sites(sem,url)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = ['ibm.com','idc.com']
    asyncio.run(scrapeurls(urls))