#!/usr/bin/env python3
#-*- coding:utf -8-*-

import aiohttp
from utils.bin_data_filters import *


async def bin_checker_binsws(bin_number):
    """
    Bins.ws bin checker function.
    
    Args:
        bin_number (str|int): Bin number.

    Returns:
        tuple: Tuple with the results of the search.
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bins-ws-api.deta.dev/api/{bin_number}', timeout=2) as r:
                r = await r.json()
                return bank_filter(r['bank']), scheme_filter(r['vendor']), level_filter(r['level'], r['vendor']), type_filter(r['type']), country_filter(r['pais'])
    except: pass
    return '', '', '', '', ''


async def bin_checker_binlist(bin_number):
    """
    BinList.net bin checker function.
    
    Args:
        bin_number (str|int): Bin number.

    Returns:
        tuple: Tuple with the results of the search.
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://lookup.binlist.net/{bin_number}', timeout=2) as r:
                r = await r.json()
                return bank_filter(r['bank']['name']), scheme_filter(r['scheme']), level_filter(r['brand'], r['scheme']), type_filter(r['type']), country_filter(r['country']['name'])
    except: pass
    return '', '', '', '', ''


async def bin_checker_bins_su(bin_number):
    """
    Bins-su bin checker function.
    
    Args:
        bin_number (str|int): Bin number.

    Returns:
        tuple: Tuple with the results of the search.
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bins-su-api.vercel.app/api/{bin_number}', timeout=2) as r:
                r = await r.json()
                r = r['data']
                return bank_filter(r['bank']), scheme_filter(r['vendor']), level_filter(r['level'], r['vendor']), type_filter(r['type']), country_filter(r['country'])
    except: pass
    return '', '', '', '', ''


async def bin_checker_binlistio(bin_number):
    """
    BinList.io bin checker function.
    
    Args:
        bin_number (str|int): Bin number.

    Returns:
        tuple: Tuple with the results of the search.
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://binlist.io/lookup/{bin_number}/', timeout=2) as r:
                r = await r.json()
                return bank_filter(r['bank']['name']), scheme_filter(r['scheme']), level_filter(r['category'], r['scheme']), type_filter(r['type']), country_filter(r['country']['name'])
    except: pass
    return '', '', '', '', ''


async def bin_checker(bin_number):
    """
    Main bin checker function.
    
    Args:
        bin_number (str|int): Bin number.

    Returns:
        tuple: Tuple with the results of the search.
    """
    
    if len(str(bin_number)) > 6:
        bin_number = str(bin_number)[6:]
    
    bank, scheme, level, card_type, country = '', '', '', '', ''
    bank_1, scheme_1, level_1, card_type_1, country_1 = await bin_checker_binsws(bin_number)
    
    bank, scheme, level, card_type, country = bank_1 if not bank_1 == '' else bank, scheme_1 if not scheme_1 == '' else scheme, level_1 if not level_1 == '' else level, card_type_1 if not card_type_1 == '' else card_type, country_1 if not country_1 == '' else country
    if bank == '' or scheme == '' or level == '' or card_type == '' or country == bank:
        bank_2, scheme_2, level_2, card_type_2, country_2 = await bin_checker_bins_su(bin_number)
        
        bank, scheme, level, card_type, country = bank_2 if not bank_2 == '' else bank, scheme_2 if not scheme_2 == '' else scheme, level_2 if not level_2 == '' else level, card_type_2 if not card_type_2 == '' else card_type, country_2 if not country_2 == '' else country
        if bank == '' or scheme == '' or level == '' or card_type == '' or country == bank:
            bank_3, scheme_3, level_3, card_type_3, country_3 = await bin_checker_binlistio(bin_number)

            bank, scheme, level, card_type, country = bank_3 if not bank_3 == '' else bank, scheme_3 if not scheme_3 == '' else scheme, level_3 if not level_3 == '' else level, card_type_3 if not card_type_3 == '' else card_type, country_3 if not country_3 == '' else country
            if bank == '' or scheme == '' or level == '' or card_type == '' or country == '':
                bank_4, scheme_4, level_4, card_type_4, country_4 = await bin_checker_binlist(bin_number)

                bank, scheme, level, card_type, country = bank_4 if not bank_4 == '' else bank, scheme_4 if not scheme_4 == '' else scheme, level_4 if not level_4 == '' else level, card_type_4 if not card_type_4 == '' else card_type, country_4 if not country_4 == '' else country

    return bank, scheme, level, card_type, country 


