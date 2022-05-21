import aiosqlite, asyncio

from bin_checker import bin_checker
from concurrent.futures import ThreadPoolExecutor


async def create_conn():
    conn = await aiosqlite.connect('bins.db')
    await conn.execute('CREATE TABLE IF NOT EXISTS bins (bin_number NUMERIC, bank TEXT, scheme TEXT, level TEXT, card_type TEXT, country TEXT)')
    await conn.commit()
    return conn


conn = asyncio.run(create_conn())


async def insert_bin(i):
    try:
        query = await conn.execute('SELECT bin_number FROM bins WHERE bin_number = ?', (i,))
        query = await query.fetchall()
        if query is None or query == [] or query == ():
            check = bin_checker(i)
            if not check == ('', '', '', '', ''):
                bank, scheme, level, card_type, country = check
                await conn.execute('INSERT INTO bins VALUES (?, ?, ?, ?, ?, ?)', (i, bank, scheme, level, card_type, country))
                await conn.commit()
                print(f'{i} | Banco: {bank if not "" else "N/A"} - Bandeira:{scheme if not "" else "N/A"} - Nível: {level if not "" else "N/A"} - Tipo: {card_type if not "" else "N/A"} - País: {country if not "" else "N/A"}')
            else:
                print(f'{i} | Bin não existente')
    except Exception as e:
        print('Erro ao inserir bin no banco de dados:', e)


def sync_insert_bin(i):
    asyncio.run(insert_bin(i))


async def create_database():
    bin_list = []
    try:
        for c in range(200000, 699999):
            bin_list.append(c)
            
        with ThreadPoolExecutor(max_workers=10) as pool:
            pool.map(sync_insert_bin, bin_list)
    except Exception as e:
        print('Erro ao criar banco de dados:', e)
        
    await conn.close()


if __name__ == '__main__':
    try:
        asyncio.run(create_database())
    except: pass
    
    asyncio.run(conn.close())
    print('Banco de dados criado com sucesso!')

