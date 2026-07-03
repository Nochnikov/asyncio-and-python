import asyncio
import concurrent
import functools
import time

freqs = {}

def partition(
    data: list,
    chunk_size: int,
):
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]

def map_frequencies(chunks: list[str]) -> dict[str, int]:
    counter = {}
    for chunk in chunks:
        word, _, count, _ = chunk.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)

    return counter

def merge_dictionaries(
    first: dict[str, int],
    second: dict[str, int],
) -> dict[str, int]:
    merged = first

    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged

async def main(partition_size: int):
    with open(r'learn/chapter_6/googlebooks-eng-all-1gram-20120701-a', encoding='utf8') as f:
        lines = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()

        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(lines, partition_size):
                tasks.append(
                    loop.run_in_executor(
                    pool,
                    functools.partial(map_frequencies, chunk)
                )
                )

            intermediate_results = await asyncio.gather(*tasks)
            final_results = functools.reduce(merge_dictionaries, intermediate_results)
            print(f'Aardvark has appeared {final_results["Aardvark"]} times.')
            end = time.time()

            print(f'Total time: {end - start}')

        end = time.time()
        print(f'{end - start:.4f}')


if __name__ == '__main__':
    asyncio.run(main(partition_size=60000))
