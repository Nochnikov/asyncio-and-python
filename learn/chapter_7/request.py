import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests

def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code

url = 'https://www.example.com/'

start = time.time()

with ThreadPoolExecutor(max_workers=1000) as executor:
    urls = [url for _ in range(1000)]

    results = executor.map(get_status_code, urls)
    for result in results:
        print(result)

end = time.time()

print(f'finished requests in {end - start} second(s)')