import xml.etree.ElementTree as ET


def get_categories(file_name: str):
    tree = ET.parse(file_name)
    root = tree.getroot()
    categories = {}

    for elem in root:
        for subelem in elem:
            if subelem.tag == 'categories':
                for category in subelem:
                    if len(category.attrib) == 1:
                        categories[category.attrib['id']] = {'name': category.text, 'parentId': category.attrib['id']}
                    else:
                        categories[category.attrib['id']] = {'name': category.text, 'parentId': category.attrib['parentId']}

    return categories

