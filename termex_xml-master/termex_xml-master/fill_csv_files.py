import xml.etree.ElementTree as ET
from csv import DictWriter

from get_categories import get_categories
from get_params_fields import get_max_fields
from create_csv_files import create_blank_csv
from create_description import create_desc


def fill_csv_files(file_name: str):
    tree = ET.parse(file_name)
    root = tree.getroot()
    fields = get_max_fields(file_name)
    create_blank_csv(fields)
    for elem in root:
        for subelem in elem:
            if subelem.tag == 'offers':
                for offer in subelem:

                    if offer.attrib['available'] == 'false':
                        continue

                    name = offer.find('name').text
                    price = int(offer.find('price').text) * 0.83 * 1.07
                    categories = get_categories(file_name)
                    cat_id = offer.find('categoryId').text
                    series = categories[cat_id]['name'].replace('Серия ', '')
                    parentId = categories[cat_id]['parentId']
                    cat_name = categories[parentId]['name']
                    url = name.replace(' ', '_').lower()
                    url = url.replace('/', '_')
                    url = url.replace('(', '')
                    url = url.replace(')', '')
                    params = list(map(lambda x: x.text, offer.findall('param')))
                    params_names = list(map(lambda x: x.attrib['name'], offer.findall('param')))

                    description = create_desc(name)

                    params_dict = {}
                    for i in range(len(params_names)):
                        params_dict[params_names[i]] = params[i]

                    pictures = offer.find('pictures')
                    pictures_list = []
                    for picture in pictures:
                        pictures_list.append(picture.text)

                    row = {'Наименование': name, 'Валюта': 'RUB', 'Цена, с НДС': price, 'В наличии': 0,
                           'Доступен для заказа': 1, 'Описание': description, 'Статус': 1,
                           'Meta Title': f"{name} с доставкой на uralenergotel.ru", 'Meta Description': f'{name} по низким ценам у официального дилера завода ТД УЭТ',
                           'URL': url, 'Срок изготовления': "уточняйте у менеджера", "Доставка": "Доставка со склада в Москве",
                           "Производитель": 'Thermex', 'Серия': series, 'Код товара': name.replace('THERMEX ', '')}
                    for i in range(len(params_names)):
                        row[params_names[i]] = params[i]

                    if len(pictures_list) != 0:
                        row['Изображения'] = pictures_list[0]
                    else:
                        continue

                    with open(f'files/{cat_name}.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = DictWriter(file, fieldnames=fields[cat_name], extrasaction='ignore')
                        writer.writerow(row)

