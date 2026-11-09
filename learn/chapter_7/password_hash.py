import asyncio
import hashlib
import os
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

from util.async_timer import async_timed


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))

passwords = [random_password(10) for _ in range(10000)]

def hash_password(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))

# start = time.time()
#
# for password in passwords:
#     hash_password(password)
#
# end = time.time()
# print(end - start)

@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    tasks = []

    with ThreadPoolExecutor() as executor:
        for password in passwords:
            tasks.append(
                loop.run_in_executor(executor, hash_password, password)
            )


    await asyncio.gather(*tasks)

asyncio.run(main())