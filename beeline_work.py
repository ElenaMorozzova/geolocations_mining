import requests
import csv
from time import sleep
import numpy as np
import reverse_geocoder as rg
import json


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result


if __name__ == '__main__':
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/83.0.4103.97 Safari/537.36'}
    scrape_main_url = 'https://spb.beeline.ru/customers/beeline-map/getpoints/?'
    url_end1 = '&lon1=70.00880&lon2=180.911798&forDisabled=false'
    url_end2 = '&lon1=19.00880&lon2=70.0089&forDisabled=false'

    lat_list1 = [40.0, 43.0, 43.5, 45.0, 48.0, 48.5, 50.5, 51.5, 52.0, 52.2, 52.4, 52.8,
                 53.0, 53.2, 53.3, 53.35, 53.5, 53.6, 53.7, 53.8,
                 54.5, 54.8, 54.9, 54.95, 55.0,
                 55.1, 55.3, 55.7, 55.9, 55.95, 56.0, 56.1,
                 56.2, 56.5, 57.5, 61.0, 64.0, 79.0]


    # lat_list2 = [40.0, 42.0, 42.5, 42.7, 43.0, 43.1, 43.2, 43.25, 43.3, 43.4, 43.5, 43.6, 44.0, 44.1, 44.3, 44.6, 44.8,
    #              45.0, 45.02, 45.05, 45.1, 45.2, 45.5, 46.0, 46.3, 46.35, 46.5, 47.0, 47.2, 47.25, 47.4,
    #              47.9, 48.5, 48.7, 48.75, 48.9, 50.0, 50.5, 50.9, 51.2, 51.3, 51.5, 51.55, 51.6,
    #              51.65, 51.7, 51.75, 51.8, 52.0, 52.2, 52.5, 52.6, 52.7, 52.8, 52.9, 53.0, 53.1, 53.15,
    #              53.2, 53.22, 53.25, 53.3, 53.4, 53.5, 53.6, 53.9, 54.0, 54.1, 54.2, 54.3, 54.4,
    #              54.5, 54.6, 54.65, 54.7, 54.73, 54.76]

    # lat_list3 = [54.8, 54.9, 55.0, 55.1, 55.15, 55.2, 55.3, 55.4, 55.45, 55.5, 55.55, 55.6,
    #              55.62, 55.64, 55.66, 55.68, 55.7, 55.71, 55.73, 55.74, 55.75, 55.76, 55.78,
    #              55.79, 55.8, 55.81, 55.82, 55.83, 55.84, 55.86, 55.88, 55.9, 55.92, 55.95, 56.0,
    #              56.05, 56.1, 56.12, 56.15, 56.2, 56.25, 56.3, 56.35, 56.4, 56.6, 56.7,
    #              56.8, 56.82, 56.85, 56.87, 56.9, 57.0, 57.1, 57.2, 57.5, 57.6, 57.7, 57.8, 58.0,
    #              58.2, 58.5, 58.7, 59.2, 59.6, 59.8, 59.85, 59.9, 59.93, 59.96, 60.0, 60.05, 60.1, 61.5, 64.5, 68.5, 80.0]
    beeline_geo1 = []
    coords_list1 = []
    delays = [7, 4, 9, 10, 5]
    i = 0
    for i, lat in enumerate(lat_list1):
        while (i + 2) <= len(lat_list1):
            delay = np.random.choice(delays)
            sleep(delay)
            lat1 = lat_list1[i]
            lat2 = lat_list1[i+1]
            url_var = 'lat1=' + str(lat1) + '&lat2=' + str(lat2)
            scrape_url = scrape_main_url + url_var + url_end1
            geo_response = requests.get(scrape_url, timeout=25, headers=__headers)
            #geo_json = geo_response.json()
            geo_json_ = geo_response.content.decode('utf-8-sig')
            geo_json = json.loads(geo_json_)
            geo_clusters = geo_json.get('clusters')
            if not geo_clusters:
                geo_data = geo_json.get('points')
                id_list = [d.get('id') for d in geo_data]
                latitude_list = [d.get('lat') for d in geo_data]
                longitude_list = [d.get('lon') for d in geo_data]
                coords_list_i = list(zip(latitude_list, longitude_list))
                reg_list = [d.get('admin1') for d in reverseGeocode(coords_list_i)]
                city_list = [d.get('name') for d in reverseGeocode(coords_list_i)]
                opened_list = [d.get('opened') for d in geo_data]
                geo_places = [d.get('place') for d in geo_data]
                address_list = [d.get('address') for d in geo_places]
                type_list = [d.get('name') for d in geo_places]
                # note_list = [d.get('addressNote') for d in geo_places]
                shop_list_i = list(zip(id_list, reg_list, city_list, address_list, type_list, opened_list, latitude_list, longitude_list))
                coords_list1.extend(coords_list_i)
                for shop in shop_list_i:
                    beeline_geo1.append(shop)
                i += 1
            else:
                print(f'Точки сгруппированы в кластеры между {lat1} и {lat2}')
                with open("beeline_geo1.csv", 'w+', newline='', encoding='utf-16') as geo_file1:
                    write = csv.writer(geo_file1)
                    write.writerows(beeline_geo1)
                    print(f'Записаны в csv часть выгрузки до lat {lat1} долгота 70-180')
                break
        print(f'Выгружены долгота 70-180')
        break

    with open("beeline_geo1.csv", 'w+', newline='', encoding='utf-16') as geo_file1:
        write = csv.writer(geo_file1)
        write.writerows(beeline_geo1)
        print(f'Записаны в csv долгота 70-180')
    
    # beeline_geo2 = []
    # coords_list2 = []
    # delays = [7, 4, 9, 10, 5]
    # i = 0
    # for i, lat in enumerate(lat_list2):
    #     while (i + 2) <= len(lat_list2):
    #         delay = np.random.choice(delays)
    #         sleep(delay)
    #         lat1 = lat_list2[i]
    #         lat2 = lat_list2[i+1]
    #         url_var = 'lat1=' + str(lat1) + '&lat2=' + str(lat2)
    #         scrape_url = scrape_main_url + url_var + url_end2
    #         geo_response = requests.get(scrape_url, timeout=25, headers=__headers)
    #        # geo_json = geo_response.json()
    #         geo_json_ = geo_response.content.decode('utf-8-sig')
    #         geo_json = json.loads(geo_json_)
    #         geo_clusters = geo_json.get('clusters')
    #         if not geo_clusters:
    #             geo_data = geo_json.get('points')
    #             id_list = [d.get('id') for d in geo_data]
    #             latitude_list = [d.get('lat') for d in geo_data]
    #             longitude_list = [d.get('lon') for d in geo_data]
    #             coords_list_i = list(zip(latitude_list, longitude_list))
    #             reg_list = [d.get('admin1') for d in reverseGeocode(coords_list_i)]
    #             city_list = [d.get('name') for d in reverseGeocode(coords_list_i)]
    #             opened_list = [d.get('opened') for d in geo_data]
    #             geo_places = [d.get('place') for d in geo_data]
    #             address_list = [d.get('address') for d in geo_places]
    #             type_list = [d.get('name') for d in geo_places]
    #             # note_list = [d.get('addressNote') for d in geo_places]
    #             shop_list_i = list(zip(id_list, reg_list, city_list, address_list, type_list, opened_list, latitude_list, longitude_list))
    #             coords_list2.extend(coords_list_i)
    #             for shop in shop_list_i:
    #                 beeline_geo2.append(shop)
    #             i += 1
    #         else:
    #             print(f'Точки сгруппированы в кластеры между {lat1} и {lat2}')
    #             with open("beeline_geo2.csv", 'w+', newline='', encoding='utf-16') as geo_file2:
    #                 write = csv.writer(geo_file2)
    #                 write.writerows(beeline_geo2)
    #                 print(f'Записаны в csv часть выгрузки до lat {lat1} долгота (1) 20-70')
    #             break
    #     print(f'Выгружены долгота (1) 20-70')
    #     break

    # with open("beeline_geo2.csv", 'w+', newline='', encoding='utf-16') as geo_file2:
    #     write = csv.writer(geo_file2)
    #     write.writerows(beeline_geo2)
    #     print(f'Записаны в csv долгота (1) 20-70')
    #
    # beeline_geo3 = []
    # coords_list3 = []
    # i = 0
    # for i, lat in enumerate(lat_list3):
    #     while (i + 2) <= len(lat_list3):
    #         delay = np.random.choice(delays)
    #         sleep(delay)
    #         lat1 = lat_list3[i]
    #         lat2 = lat_list3[i+1]
    #         url_var = 'lat1=' + str(lat1) + '&lat2=' + str(lat2)
    #         scrape_url = scrape_main_url + url_var + url_end2
    #         geo_response = requests.get(scrape_url, timeout=25, headers=__headers)
    #         # geo_json = geo_response.json()
    #         geo_json_ = geo_response.content.decode('utf-8-sig')
    #         geo_json = json.loads(geo_json_)
    #         geo_clusters3 = geo_json.get('clusters')
    #         if not geo_clusters3:
    #             geo_data = geo_json.get('points')
    #             id_list = [d.get('id') for d in geo_data]
    #             latitude_list = [d.get('lat') for d in geo_data]
    #             longitude_list = [d.get('lon') for d in geo_data]
    #             coords_list_i = list(zip(latitude_list, longitude_list))
    #             reg_list = [d.get('admin1') for d in reverseGeocode(coords_list_i)]
    #             city_list = [d.get('name') for d in reverseGeocode(coords_list_i)]
    #             opened_list = [d.get('opened') for d in geo_data]
    #             geo_places = [d.get('place') for d in geo_data]
    #             address_list = [d.get('address') for d in geo_places]
    #             type_list = [d.get('name') for d in geo_places]
    #             # note_list = [d.get('addressNote') for d in geo_places]
    #             shop_list_i = list(zip(id_list, reg_list, city_list, address_list, type_list, opened_list, latitude_list, longitude_list))
    #             coords_list3.extend(coords_list_i)
    #             for shop in shop_list_i:
    #                 beeline_geo3.append(shop)
    #             i += 1
    #         else:
    #             print(f'Точки сгруппированы в кластеры между {lat1} и {lat2}')
    #             with open("beeline_geo3.csv", 'w+', newline='', encoding='utf-16') as geo_file3:
    #                 write = csv.writer(geo_file3)
    #                 write.writerows(beeline_geo3)
    #                 print(f'Записана часть выгрузки до lat {lat1} долгота (2) 20-70')
    #             break
    #     print(f'Выгружены долгота (2) 20-70')
    #     break
    #
    # with open("beeline_geo3.csv", 'w+', newline='', encoding='utf-16') as geo_file3:
    #     write = csv.writer(geo_file3)
    #     write.writerows(beeline_geo3)
    #     print(f'Записаны в csv долгота (2) 20-70')







