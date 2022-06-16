#!/usr/bin/env python3
#-*- coding:utf -8-*-

import aiosqlite, asyncio, platform

from utils.bin_checker import bin_checker
from concurrent.futures import ThreadPoolExecutor


DATABASE_PATH = 'output/bins.db'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
CLEAN = '\033[0m'


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def insert_bin(item):
    """
    Inserts a bin into the database.

    Args:
        item (int|str): The bin number to insert.
    """

    try:
        async with aiosqlite.connect(DATABASE_PATH) as conn:
            query = await conn.execute('SELECT bin_number FROM bins WHERE bin_number = ?', (item,))
            query = await query.fetchall()

            if query is None or query == [] or query == ():
                check = await bin_checker(item)

                if not check == ('', '', '', '', ''):
                    bank, scheme, level, card_type, country = check
                    await conn.execute('INSERT INTO bins VALUES (?, ?, ?, ?, ?, ?)', (item, bank, scheme, level, card_type, country))
                    await conn.commit()
                    print(f'{BLUE}{item} {YELLOW}| BANK:{CLEAN} {bank if not "" else "N/A"}{YELLOW} - SCHEME:{CLEAN} {scheme if not "" else "N/A"}{YELLOW} - LEVEL:{CLEAN} {level if not "" else "N/A"}{YELLOW} - TYPE:{CLEAN} {card_type if not "" else "N/A"}{YELLOW} - COUNTRY:{CLEAN} {country if not "" else "N/A"}{CLEAN}')
                
                else:
                    print(f'{BLUE}{item} {YELLOW}| Bin not found!{CLEAN}')

    except Exception as e:
        print(f'\n{YELLOW}[ {BLUE}I {YELLOW}]{RED} Error inserting bin into database:{CLEAN}', e)


def sync_insert_bin(item):
    """
    It synchronously calls the database write function.

    Args:
        item (int|str): The bin number to insert.
    """

    asyncio.run(insert_bin(item))


async def create_database():
    """
    Creates the database.
    """

    bin_list = []
    async with aiosqlite.connect(DATABASE_PATH) as conn:
        await conn.execute('CREATE TABLE IF NOT EXISTS bins(bin_number NUMERIC, bank TEXT, scheme TEXT, level TEXT, type TEXT, country TEXT);')
    
    try:
        for bin in range(200000, 699999):
            bin_list.append(bin)
            
        with ThreadPoolExecutor(max_workers=20) as pool:
            pool.map(sync_insert_bin, bin_list)
    
    except Exception as e:
        print(f'\n{YELLOW}[ {BLUE}I {YELLOW}]{RED} Error creating database:{CLEAN}', e)


if __name__ == '__main__':
    try:
        asyncio.run(create_database())
    
    except KeyboardInterrupt:
        print(f'\n{YELLOW}[ {BLUE}I {YELLOW}]{RED} Exiting...{CLEAN}')

    except: pass
    print(f'\n\n{YELLOW}[ {BLUE}I {YELLOW}]{GREEN} Database created successfully!{CLEAN}')




