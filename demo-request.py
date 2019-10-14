import asyncio
import aiohttp
import logging
import json
import time
from multiprocessing import Pool

class AsnycStress(object):
    def __init__(self, url_list, max_threads):
        self.urls = url_list
        self.correct = 0
        self.max_threads = max_threads

    async def post_request(self, data, url):
        headers = {'Content-Type': 'application/json'}
        timeout = aiohttp.ClientTimeout(total=5 * 60)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, timeout=timeout, headers=headers) as response:
                if response.status == 200:
                    self.correct += 1
                    html = await response.read()
                    return response.url, html

    async def get_request(self, data, url):
        headers = {'Content-Type': 'application/json'}
        timeout = aiohttp.ClientTimeout(total=5 * 60)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, timeout=timeout, headers=headers) as response:
                if response.status == 200:
                    self.correct += 1
                    html = await response.read()
                    return response.url, html

    def __parse_results(self, url, html):
        try:
            jsonobj = json.loads(html)
            print(jsonobj)
        except Exception as e:
            raise e

    async def get_results(self, data, url):
        url, html = await self.post_request(data, url)
        self.__parse_results(url, html)
        return 'Completed'

    async def handle_tasks_post(self, task_id):
        try:
            userName = 'admin'
            jsonreq = {'userName': userName}
            '''生成json字符串'''
            data = json.dumps(jsonreq)
            print('data=', data)
            task_status = await self.get_results(data, target_url)
        except Exception as e:
            logging.exception('Error for {}'.format(target_url), exc_info=True)

    async def handle_tasks_get(self, task_id):
        try:
            userName = 'admin'
            url = target_url + '?userName=' + userName
            print('url=', url)
            task_status = await self.get_results([], url)
        except Exception as e:
            logging.exception('Error for {}'.format(target_url), exc_info=True)

    def eventloop(self):
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks_post(task_id) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

def start_test(args=()):
    start_milli_time = int(time.time() * 1000)
    async_example = AsnycStress([target_url], threadcount)
    async_example.eventloop()
    end_milli_time = int(time.time() * 1000)
    print('Time %d msc, total %d, correct %d' % (end_milli_time - start_milli_time, threadcount, async_example.correct))

if __name__ == '__main__':

    target_url = 'https://api.scaffold.local/api/api/demo'
    processcount = 2
    threadcount = 1

    all_start_milli_time = int(time.time() * 1000)
    for i in range(processcount):
        p = Pool(processcount)
        for i in range(processcount):
            p.apply_async(start_test, (threadcount,))
        p.close()
        p.join()
    all_end_milli_time = int(time.time() * 1000)
    print('All-time %d msc, count %d ' % (all_end_milli_time - all_start_milli_time, threadcount * processcount))
