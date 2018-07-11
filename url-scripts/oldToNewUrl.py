import asyncio
import pandas
from csv import writer as csvwriter
from csv import QUOTE_NONE
from json import loads as jsonload
from multiprocessing import Pool
from sys import argv
from urllib.parse import quote_plus
from aiohttp import ClientSession
from aiohttp import TCPConnector


def rangeFilterValue(start, end):
    if start and end: 
        return str(start) + "_" + str(end) + "_" + str(round(float(start), 1)) + " TO " + str(round(float(end), 1))
    return ''

def mapCB(filterName, filterExtracted):
    start = filterExtracted["start"]
    end = filterExtracted["end"]
    value = rangeFilterValue(start, end)
    if value:
        return filterName + ':' + value
    return ''

def createRangeQuery(filtersObj):
    data = list()
    for x in filtersObj:
        val = mapCB(x, filtersObj[x])
        if val != '':
            data.append(val)
    return "::".join(data)

def getNewUrl(baseUrl, data):
    q = data["q"]
    f = None
    rf = None
    if "f" in data:
        f = data["f"]
    if "rf" in data:
        rf = data["rf"]
    prependUrl = baseUrl + q.strip().replace(' ', '-')
    if f or rf:
        print(f,rf)
        url = prependUrl + "?rf=" + createRangeQuery(rf)
        return url
    #print(prependUrl)
    return prependUrl

async def fetch(url, session, retrycount=0):
    async with session.get(url) as response:
        return await response.read()

async def run(r):
    url = "http://api.myntra.com/assorted/v1/urlrouter/?path={}"
    baseUrl = 'https://www.jabong.com/'
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
        reader = pandas.read_excel('./URL.xlsx')
        rows = reader['URL']
        fetcher = len(rows) / 1000
        while i <= fetcher:
        for row in reader['URL']:
            dataappend(row)
            #queryparams = (quote(i) for i in row)
            urlAppendStr = row.replace(baseUrl, '')
            updatedUrl = url.format(quote_plus(urlAppendStr.strip('/')))
            #print(updatedUrl)
            task = asyncio.ensure_future(
               fetch(updatedUrl, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        with open('OldUrlToNewUrl.csv', 'w+', newline='', encoding='utf-8', buffering=1) as csvoutfile:
            writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                               escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
            index = 0
            for x in data:
                try:
                    jsonStr = jsonload(responses[index])
                    if jsonStr["data"]:
                        a = True
                    writer.writerow([x, getNewUrl(baseUrl, jsonStr["data"])])
                except:
                    writer.writerow([x, "failed"])
                index += 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)
