import asyncio
from csv import reader as csvreader
from csv import writer as csvwriter
from csv import QUOTE_NONE
from json import loads as jsonload
from multiprocessing import Pool
from sys import argv
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from aiohttp import ClientSession


async def fetch(url, session, retrycount=0):
    print(url)
    try:
        async with session.get(url) as response:
            return await response.read()
    except:
        retrycount += 1
        if retrycount <= 100:
            fetch(url, session, retrycount)
        else:
            return await "failed"


async def run(r):
    url = "https://gw.jabong.com/v1/search/?url={}"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        data = list()
        dataappend = data.append
        with open('golden_search_terms', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csvreader(csvfile, lineterminator='\n', delimiter=',', quotechar='"',
                               escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
            for row in reader:
                dataappend(row)
                queryparams = (quote(i) for i in row)
                urlAppendStr = quote(
                    '/find/'+row[0]+'/?q='+'&q='.join(queryparams))
                task = asyncio.ensure_future(
                    fetch(url.format(urlAppendStr), session))
                tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        with open('golden_count.csv', 'w', newline='', encoding='utf-8', buffering=1) as csvoutfile:
            writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                               escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
            index = 0
            for x in data:
                try:
                    jsonStr = jsonload(responses[index])
                    if jsonStr["data"]:
                        a = True
                    writer.writerow([x[0], jsonStr["data"]["summary"]["productCnt"]])
                except:
                    writer.writerow([x[0], "failed"])
                index += 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)
