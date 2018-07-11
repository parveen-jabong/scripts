import asyncio
import pandas
from csv import writer as csvwriter
from csv import QUOTE_NONE
import json
from json import loads as jsonload
from multiprocessing import Pool
from sys import argv
from urllib.parse import quote_plus
from aiohttp import ClientSession
from aiohttp import TCPConnector
from math import ceil

# count of request to fetch in one go
counter = 500

async def fetch(url, session):
    print(url)
    try:
        async with session.get(url) as response:
            return await response.read()
    except:
        return await "failed"

async def run(r):
    url = 'http://api.myntra.com/v1/search/'
    tasks = []
    headers = {}
    headers['Accept'] = 'application/json'
    headers['Content-type'] = 'application/json'
    headers['postman-token'] = 'ca64e43a-1444-41bf-099e-f604ac515b52'
    headers['clientid'] = 'jabong-a6aafa2f-ed53-4cb0-8db0-46f8c94f99b5'
    headers['at'] = 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqZ2lMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTWpSaU56Wm1PV0l0TldVM09DMHhNV1U0TFdKa09XTXRNREl3TVRCaE5UUm1OVGRsSWl3aVkybGtlQ0k2SW1waFltOXVaeTFoTm1GaFptRXlaaTFsWkRVekxUUmpZakF0T0dSaU1DMDBObVk0WXprMFpqazVZalVpTENKaGNIQk9ZVzFsSWpvaWFtRmliMjVuSWl3aWMzUnZjbVZKWkNJNklqUTJNRE1pTENKbGVIQWlPakUxTkRJMk1qVXdOek1zSW1semN5STZJa2xFUlVFaWZRLlZZS1gzZVNlOVRSakVtVkVFX0kxcThvb2l6RWZnMm5IR085Z3ZKeUExV1U='
    headers['X-MYNTRA-KNUTH'] = "yes"

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    connector = TCPConnector(verify_ssl=False)
    async with ClientSession(connector=connector,headers=headers) as session:
        data = list()
        dataappend = data.append
        reader = pandas.read_csv('./OldUrlToNewUrl.csv')
        rows = reader['new_urls']
        length = len(rows)
        fetcher = ceil(length / counter)
        i = 0
        offset = 0
        while i < fetcher:
            for j in range(1, counter + 1):
                if (i*counter + j) >= length:
                    break
                row = rows[i*counter + j]
                dataappend(row)
                updatedKey = row.replace('https://www.jabong.com/', '')
                task = asyncio.ensure_future(
                    fetch(url + updatedKey + '?o=0&rows=52', session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            # you now have all response bodies in this variable
            with open('NewUrlCounts.csv', 'w', newline='', encoding='utf-8', buffering=1) as csvoutfile:
                writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                                escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
                index = 0
                for x in data:
                    try:
                        jsonStr = jsonload(responses[index])
                        #print(x, jsonStr.keys())
                        if jsonStr["totalCount"]:
                            a = True
                        writer.writerow([x, jsonStr["totalCount"]])
                    except:
                        writer.writerow([x, "failed"])
                    index += 1
            i += 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)
