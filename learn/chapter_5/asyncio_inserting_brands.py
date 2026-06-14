import os

import asyncpg
import asyncio
from typing import Union
from random import sample
from dotenv import load_dotenv

load_dotenv()

def load_common_words() -> list[str]:
    with open("common_words.txt") as common_words:
        return common_words.readlines()

def generate_brand_names(words: list[str]) -> list[tuple[Union[str, ]]]:
    return [(words[index],) for index in sample(range(100), 100)]

async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)

    insert_brands = 'INSERT INTO brand VALUES (DEFAULT, $1)'
    return await connection.executemany(insert_brands, brands)

async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        database=os.getenv("POSTGRES_DB"),
        password=os.getenv("POSTGRES_PASSWORD", 'postgres'),
    )
    await insert_brands(common_words, connection)

asyncio.run(main())
