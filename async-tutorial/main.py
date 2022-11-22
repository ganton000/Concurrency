#one thread and one process
import asyncio
import time
import requests
import aiohttp


async def get_url_response(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			return await response.text()

async def main():
	urls = [
		"https://python.org",
		"https://medium.com/",
		"https://wikipedia.org/wiki/Concurrency",
		"https://google.com",
		"https://pypl.org/project/requests"
	]

	start_time = time.time()
	sync_text_response = []
	for url in urls:
		sync_text_response.append(requests.get(url).text)

	end_time = time.time()
	print("Requests took:", end_time - start_time)

	start_time = time.time()
	tasks = []
	for url in urls:
		tasks.append(asyncio.create_task(get_url_response(url)))

	async_text_response = await asyncio.gather(*tasks)

	end_time = time.time()
	print("Async Requests took:", end_time - start_time)

if __name__ == "__main__":
	asyncio.run(main())