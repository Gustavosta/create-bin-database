import requests
from filters import *


def bin_checker_lengo(bin_number):
    try:
        r = requests.get(f'http://34.125.141.104/search/?bin={bin_number}', timeout=2).json()
        if not r['nivel'].lower() == 'indefinido':
            return bank_filter(r['banco']), scheme_filter(r['bandeira']), level_filter(r['nivel'], r['bandeira']), type_filter(r['type']), country_filter(r['pais'])
    
    except Exception as e:
        pass

    return '', '', '', '', ''


def bin_checker_binlist(bin_number):
    try:
        r = requests.get(f'https://lookup.binlist.net/{bin_number}', timeout=2).json()
        return bank_filter(r['bank']['name']), scheme_filter(r['scheme']), level_filter(r['brand'], r['scheme']), type_filter(r['type']), country_filter(r['country']['name'])
    
    except Exception as e:
        pass

    return '', '', '', '', ''


def bin_checker_bins_su(bin_number):
    try:
        r = requests.get(f'https://bins-su-api.vercel.app/api/{bin_number}', timeout=2).json()['data']
        return bank_filter(r['bank']), scheme_filter(r['vendor']), level_filter(r['level'], r['vendor']), type_filter(r['type']), country_filter(r['country']
    )
    except Exception as e:
        pass

    return '', '', '', '', ''


def bin_checker_binlistio(bin_number):
    try:
        r = requests.get(f'https://binlist.io/lookup/{bin_number}/', timeout=2).json()
        return bank_filter(r['bank']['name']), scheme_filter(r['scheme']), level_filter(r['category'], r['scheme']), type_filter(r['type']), country_filter(r['country']['name'])
    
    except Exception as e:
        pass

    return '', '', '', '', ''


def bin_checker(bin_number):
    bank, scheme, level, card_type, country = '', '', '', '', ''
    bank_a, scheme_a, level_a, card_type_a, country_a = bin_checker_lengo(bin_number)

    bank, scheme, level, card_type, country = bank_a if not bank_a == '' else bank, scheme_a if not scheme_a == '' else scheme, level_a if not level_a == '' else level, card_type_a if not card_type_a == '' else card_type, country_a if not country_a == '' else country
    if bank == '' or scheme == '' or level == '' or card_type == '' or country == bank:
        bank_b, scheme_b, level_b, card_type_b, country_b = bin_checker_bins_su(bin_number)

        bank, scheme, level, card_type, country = bank_b if not bank_b == '' else bank, scheme_b if not scheme_b == '' else scheme, level_b if not level_b == '' else level, card_type_b if not card_type_b == '' else card_type, country_b if not country_b == '' else country
        if bank == '' or scheme == '' or level == '' or card_type == '' or country == '':
            bank_c, scheme_c, level_c, card_type_c, country_c = bin_checker_binlistio(bin_number)

            bank, scheme, level, card_type, country = bank_c if not bank_c == '' else bank, scheme_c if not scheme_c == '' else scheme, level_c if not level_c == '' else level, card_type_c if not card_type_c == '' else card_type, country_c if not country_c == '' else country
            if bank == '' or scheme == '' or level == '' or card_type == '' or country == '':
                bank_d, scheme_d, level_d, card_type_d, country_d = bin_checker_binlist(bin_number)

                bank, scheme, level, card_type, country = bank_d if not bank_d == '' else bank, scheme_d if not scheme_d == '' else scheme, level_d if not level_d == '' else level, card_type_d if not card_type_d == '' else card_type, country_d if not country_d == '' else country

    return bank, scheme, level, card_type, country 

