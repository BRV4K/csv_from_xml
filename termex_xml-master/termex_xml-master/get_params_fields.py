import xml.etree.ElementTree as ET

from get_categories import get_categories


def get_max_fields(file_name: str):
    tree = ET.parse(file_name)
    root = tree.getroot()
    fields = {}
    categories = get_categories(file_name)

    for elem in root:
        for subelem in elem:
            if subelem.tag == 'offers':
                for offer in subelem:

                    if offer.attrib['available'] == 'false':
                        continue
                    cat_id = offer.find('categoryId').text
                    parent = categories[cat_id]['parentId']
                    params_names = list(map(lambda x: x.attrib['name'], offer.findall('param')))

                    if categories[parent]['name'] in fields.keys():
                        if len(params_names) > len(fields[categories[parent]['name']]):
                            fields[categories[parent]['name']] = ["Наименование", "Артикул", "Валюта", "Цена, с НДС", "В наличии", "Доступен для заказа",
                      "Краткая информация", "Описание", "Наклейка", "Статус", "Теги", "Meta Title",
                      "Meta Description", "URL", "Срок изготовления", "Доставка", "Производитель",
                      "Серия", "Код товара"] + params_names + ['Изображения']
                    else:
                        fields[categories[parent]['name']] = ["Наименование", "Артикул", "Валюта", "Цена, с НДС", "В наличии", "Доступен для заказа",
                      "Краткая информация", "Описание", "Наклейка", "Статус", "Теги", "Meta Title",
                      "Meta Description", "URL", "Срок изготовления", "Доставка", "Производитель",
                      "Серия", "Код товара"] + params_names + ['Изображения']

    return fields

