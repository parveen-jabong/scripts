import asyncio
import pandas
from csv import writer as csvwriter
from csv import QUOTE_NONE
from json import loads as jsonload
from multiprocessing import Pool
from sys import argv
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from aiohttp import ClientSession
from aiohttp import TCPConnector

async def fetch(url, session, retrycount=0):
    print(url)
    async with session.get(url) as response:
        print(response)
        return await response.read()

async def run(r):
    url = "https://gw.jabong.com/v1/search/?url={}"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    connector = TCPConnector(verify_ssl=False)
    async with ClientSession(connector=connector) as session:
        data = list()
        dataappend = data.append
        # with open('2000URLs', 'r', newline='', encoding='utf-8') as csvfile:
        #     reader = csvreader(csvfile, lineterminator='\n', delimiter=',', quotechar='"',
        #                        escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
        reader = pandas.read_excel('./2000URLs.xlsx')
        for row in reader['Address']:
            dataappend(row)
            #queryparams = (quote(i) for i in row)
            urlAppendStr = row.replace('https://www.jabong.com', '')
            task = asyncio.ensure_future(
                fetch(url.format(urlAppendStr), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        with open('OldUrlCounts.csv', 'w', newline='', encoding='utf-8', buffering=1) as csvoutfile:
            writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                               escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
            index = 0
            for x in data:
                try:
                    jsonStr = jsonload(responses[index])
                    if jsonStr["data"]:
                        a = True
                    writer.writerow([x, jsonStr["data"]["summary"]["productCnt"]])
                except:
                    writer.writerow([x, "failed"])
                index += 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)
