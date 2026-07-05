import asyncio
import functools
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Value

from learn.chapter_6.frequencles_of_words import partition, merge_dictionaries

map_counter: Value

def init(counter: Value):
    global map_counter
    map_counter = counter

def map_frequencies(chunk: list[str]) -> dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')

        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)

    with map_counter.get_lock():
        map_counter.value += 1

    return counter

async def progress_report(total_partitions: int):
    while map_counter.value < total_partitions:
        print(f'Finished {map_counter.value}/{total_partitions} map operations')
        await asyncio.sleep(1)

async def main(partiton_size: int):
    global map_counter

    with open(r'learn/chapter_6/googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()

        tasks = []

        map_counter = Value('i', 0)

        with ProcessPoolExecutor(
            initializer=init,
            initargs=(map_counter,),
        ) as pool:
            total_partitions = len(contents) // partiton_size
            report = asyncio.create_task(progress_report(total_partitions))

            for chuck in partition(contents, partiton_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(
                    map_frequencies, chuck)))

            counters = await asyncio.gather(*tasks)

            await report

            final_result = functools.reduce(merge_dictionaries, counters)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")

if __name__ == '__main__':
    asyncio.run(main(partiton_size=60000))



