from jsonfinder import jsonfinder
import requests
from functools import reduce
import json
from time import sleep
import numpy as np
import csv
import itertools
import reverse_geocoder as rg


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result


def chained_get(dct, *keys):
    entry = object()

    def getter(level, key):
        return 'NA' if level is entry else level.get(key, entry)

    return reduce(getter, keys, dct)


if __name__ == '__main__':
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/83.0.4103.97 Safari/537.36'}
    scrape_main_url = "https://spb.tele2.ru/offices/"
    content = requests.get(scrape_main_url, timeout=5, headers=__headers).text
    for _, __, obj in jsonfinder(content, json_only=True):
        try:
            if obj and isinstance(obj, list) and \
                    isinstance(obj[0], dict) and \
                    {'window.__PRELOADED_STATE__'}.issubset(obj[0]):
                break
        except ValueError:
            print('data not found')

    work_list = chained_get(obj, 'app', 'content', 'regions', 'items')
    reg_list = [d['ipGeoBaseName'] for d in work_list if 'ipGeoBaseName' in d]
    site_wlist = [d['site'] for d in work_list if 'site' in d]
    site_list = [d['productionUrl'] for d in site_wlist if 'productionUrl' in d]
    lend_list = [site.split('.', 1)[0].upper() for site in site_list]
    add_api = ["https://" + s + "/api/offices/locations?tele2Store=true&siteId=site" + l for s, l in zip(site_list, lend_list)]
    tele2_dict = dict(zip(reg_list, add_api))
    # print(len(tele2_dict))
    # with open("tele2_dict.txt", 'w+') as out_file:
    #     out_file.write(json.dumps(tele2_dict, ensure_ascii=False))
    delays = [7, 4, 9, 16, 23, 10, 19]
    tele2_geo = []
    for key, value in tele2_dict.items():
        j_url = value
        geo_response = requests.get(j_url, timeout=15, headers=__headers)
        geo_json = geo_response.json()
        geo_data = geo_json.get('data')
        delay = np.random.choice(delays)
        sleep(delay)
        name_list = [d['name'] for d in geo_data if 'name' in d]
        city_list = [d['city'] for d in geo_data if 'city' in d]
        address_list = [d['address'] for d in geo_data if 'address' in d]
        locType_list = [d['locationType'] for d in geo_data if 'locationType' in d]
        latitude_list = [str(d['latitude']) for d in geo_data if 'latitude' in d]
        longitude_list = [str(d['longitude']) for d in geo_data if 'longitude' in d]
        coords_list = tuple(zip(latitude_list, longitude_list))
        reg_list = [d.get('admin1') for d in reverseGeocode(coords_list)]
        cityrev_list = [d.get('name') for d in reverseGeocode(coords_list)]
        tele2_geo_work = list(zip(itertools.repeat(key), name_list, reg_list, cityrev_list, city_list, address_list, locType_list, latitude_list, longitude_list))
        for shop in tele2_geo_work:
            tele2_geo.append(shop)
        # tele2_geo.append(tele2_geo_work)
        print(f'Выгружен регион {key}')

    # экспорт в файл
    with open("tele2_geo.csv", 'w+', newline='', encoding='utf-16') as geo_file:
        write = csv.writer(geo_file)
        write.writerows(tele2_geo)
