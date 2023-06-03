import aiohttp
import asyncio
from bs4 import BeautifulSoup

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
    'referer': 'https://www.google.com/',
    'cookie': 'DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0'
}

async def get_page(session, url):
    async with session.get(url, headers = headers) as r:
        return await r.text()

async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data

def parse(results):
    for html in results:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('span', attrs={'id': 'productTitle'}).text
        print(title)

if __name__ == '__main__':
    urls = [
        'https://www.amazon.in/OnePlus-Nord-Lite-128GB-Storage/dp/B09WQYFLRX/ref=sr_1_1?pd_rd_r=8d69c16a-c302-4aee-a764-2485bd6c9da8&pd_rd_w=0EY0m&pd_rd_wg=QDYsE&pf_rd_p=6e9c5ebb-d370-421b-8375-bf50155e0300&pf_rd_r=PV5FBP56ZTD6AZ1J0T5T&refinements=p_36%3A1000100-2500000%2Cp_n_condition-type%3A8609960031&s=electronics&sr=1-1',
        'https://www.amazon.in/OnePlus-Nord-Chromatic-128GB-Storage/dp/B0BY8MCQ9S/ref=sr_1_2?pd_rd_r=8d69c16a-c302-4aee-a764-2485bd6c9da8&pd_rd_w=0EY0m&pd_rd_wg=QDYsE&pf_rd_p=6e9c5ebb-d370-421b-8375-bf50155e0300&pf_rd_r=PV5FBP56ZTD6AZ1J0T5T&refinements=p_36%3A1000100-2500000%2Cp_n_condition-type%3A8609960031&s=electronics&sr=1-2&th=1',
        'https://www.amazon.in/OnePlus-Nord-Pastel-128GB-Storage/dp/B0BY8JZ22K/ref=sr_1_3?pd_rd_r=8d69c16a-c302-4aee-a764-2485bd6c9da8&pd_rd_w=0EY0m&pd_rd_wg=QDYsE&pf_rd_p=6e9c5ebb-d370-421b-8375-bf50155e0300&pf_rd_r=PV5FBP56ZTD6AZ1J0T5T&refinements=p_36%3A1000100-2500000%2Cp_n_condition-type%3A8609960031&s=electronics&sr=1-3'
    ]

    results = asyncio.run(main(urls))
    parse(results)