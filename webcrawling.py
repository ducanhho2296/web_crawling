import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import nest_asyncio


nest_asyncio.apply()

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None

async def crawl_webpage_async(url, max_depth, current_depth=0):
    if current_depth > max_depth:
        return []

    try:
        async with aiohttp.ClientSession() as session:
            response_text = await fetch_url(session, url)
            if not response_text:
                return []

            soup = BeautifulSoup(response_text, 'html.parser')
            text_content = []
            for element in soup.find_all(string=True):
                if element.parent.name not in ['script', 'style']:
                    text_content.append(element.strip())
            webpage_text = ' '.join(text_content)

            print(f"Depth {current_depth}: {url}")

            links = [link['href'] for link in soup.find_all('a', href=True)]
            extracted_texts = [webpage_text]

            tasks = []
            for link in links:
                absolute_link = urljoin(url, link)
                tasks.append(crawl_webpage_async(absolute_link, max_depth, current_depth + 1))

            extracted_texts += await asyncio.gather(*tasks)

            return extracted_texts

    except aiohttp.ClientError as e:
        print(f"Error crawling {url}: {e}")
        return []

if __name__ == "__main__":
    start_url = 'https://www.t-systems.com/de/de'
    loop = asyncio.get_event_loop()
    extracted_texts = loop.run_until_complete(crawl_webpage_async(start_url, max_depth=1))
        #storing texts 
    # for i, text in enumerate(extracted_texts):
    #     filename = f"./data/doc_{i}.txt"
    # with open(filename, "w") as f:
    #     f.write(text)