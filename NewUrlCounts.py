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

async def fetch(url, session, data):
    print(url, data)
    try:
        async with session.post(url, data=data) as response:
            return await response.read()
    except:
        return await "failed"

async def run(r):
    url = 'http://search.myntra.com/search-service/searchservice/search/getresults/'
    tasks = []
    headers = {}
    headers['Accept'] = 'application/json'
    headers['Content-type'] = 'application/json'
    headers['postman-token'] = 'ca64e43a-1444-41bf-099e-f604ac515b52'
    headers['x-mynt-ctx'] = 'storeid=4603'

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    connector = TCPConnector(verify_ssl=False)
    async with ClientSession(connector=connector,headers=headers) as session:
        data = list()
        dataappend = data.append
        reader = pandas.read_csv('./OldUrlToNewUrl.csv')
        for row in reader['new_urls']:
            dataappend(row)
            updatedKey = row.replace('https://www.jabong.com/', '')
            query = {}
            query['query'] = updatedKey.replace('-', ' ')
            postData = json.dumps(query)
            task = asyncio.ensure_future(
                fetch(url, session, postData))
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
                    print(x, jsonStr.keys())
                    if jsonStr["response"]:
                        a = True
                    writer.writerow([x, jsonStr["response"]["totalCount"]])
                except:
                    writer.writerow([x, "failed"])
                index += 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)
