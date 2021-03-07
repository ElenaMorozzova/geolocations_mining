import requests
import csv
import reverse_geocoder as rg


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result

if __name__ == '__main__':
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/83.0.4103.97 Safari/537.36'}
    scrape_main_url = "https://www.megafon.ru/api/store-locator//map-tile/b2c/"
    geo_response = requests.get(scrape_main_url, timeout=25, headers=__headers)
    geo_json = geo_response.json()
    geo_data = dict(geo_json.get('offices'))
    id_list = list(geo_data.keys())
    work_list = list(geo_data.values())
    filial_list = [d['filialID'] for d in work_list if 'filialID' in d]
    region_list = [str(d['subject']) for d in work_list if 'subject' in d]
    city_list = [str(d['place']) for d in work_list if 'place' in d]
    # worktime_list = [d['worktime'] for d in work_list if 'worktime' in d]
    adress_list = [str(d['title']) for d in work_list if 'title' in d]
    type_list = [str(d['officeType']) for d in work_list if 'officeType' in d]
    coords_list = [d['coords'] for d in work_list if 'coords' in d]
    tuple_coords = [tuple(c) for c in coords_list]
    print('Геокодинг начать')
    reg_list = [d.get('admin1') for d in reverseGeocode(tuple_coords)]
    cityrev_list = [d.get('name') for d in reverseGeocode(tuple_coords)]
    lat_list = [str(item[0]) for item in coords_list]
    lng_list = [str(item[1]) for item in coords_list]
    shop_wlist = list(zip(filial_list, region_list, city_list, id_list, reg_list, cityrev_list, adress_list, type_list, lat_list, lng_list))
    shop_list = sorted(shop_wlist, key=lambda x: x[1])
    with open("mega_geo.csv", 'w+', newline='', encoding='utf-16') as geo_file:
        write = csv.writer(geo_file)
        write.writerows(shop_list)



