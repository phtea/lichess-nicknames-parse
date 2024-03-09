import time
import asyncio
import aiohttp
import json

class Fetch:
    def __init__(self, threads: int, json_file: str, base_url: str):
        self.base_url = base_url
        self.counter = 0
        self.json_file = json_file
        self.semaphore = asyncio.Semaphore(threads)

    async def fetch(self, keyword: str, session: aiohttp.ClientSession, retry: int = 5):
        async with self.semaphore:
            url = self.base_url.format(keyword)
            if retry <= 0:
                return None
            try:
                async with session.get(url) as response:
                    await asyncio.sleep(0.001)
                    if response.status != 200:
                        print(f'[X] {url} - {response.status}: {response.reason}. Retries: {retry}')
                        await asyncio.sleep(5)  # Adjust as needed
                        return await self.fetch(keyword, session, retry=retry - 1)
                    self.counter += 1
                    print(f'[+] {self.counter} nicknames checked.', end='\r')
                    result = await response.json()
                    if result is False:
                        print(f'\n[+] {keyword} is free to use!')
                        return keyword
                    return None
            except aiohttp.ClientOSError as e:
                print(f'[X] {url} - Error: {e}. Retries: {retry}')
                await asyncio.sleep(5)
                return await self.fetch(keyword, session, retry=retry - 1)

    async def fetch_all(self, keywords: list[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(keyword, session) for keyword in keywords]
            return await asyncio.gather(*tasks)

    async def main(self):

        with open('words_dictionary.json') as file:
            keywords = json.load(file)

        keywords = list(keywords.keys())
        keywords = [kw for kw in keywords if (3 <= len(kw) <= 5)]
        print(f'[INFO] Keywords to check: {len(keywords)}')

        responses = await self.fetch_all(keywords)

        good_responses = [response for response in responses if response]

        with open(self.json_file, 'w') as file:
            json.dump(good_responses, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    
    base_url = 'https://lichess.org/api/player/autocomplete?term={}&exists=1'
    json_file = 'result.json'
    threads = 10
    
    start_time = time.monotonic()

    fetch_instance = Fetch(threads, json_file, base_url)
    asyncio.run(fetch_instance.main())

    print(f"Total time taken: {time.monotonic() - start_time:.2f} seconds")
