import json
from pprint import pprint
from collections import OrderedDict


def read_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def create_subdict(name: str, type_value: str, num_children: int, parent: str) -> dict:
    subdict = OrderedDict()
    subdict['name'] = name
    subdict['type'] = type_value
    if num_children:
        subdict['num_children'] = num_children
    if parent:
        subdict['parent'] = parent
    return subdict


def create_dictionary(kved_dict: dict, class_code: str):
    division_code = class_code[:2]
    group_code = class_code[:-1]

    for lst in kved_dict['sections']:
        all_sections = lst

    for section_index in range(len(all_sections)):
        section_code = all_sections[section_index]['sectionCode']
        num_children = len(all_sections[section_index]['divisions'])
        section_dict = create_subdict(
            section_code, 'section', num_children, None)

        for division in range(len(all_sections[section_index]['divisions'])):
            if division_code != all_sections[section_index]['divisions'][division]['divisionCode']:
                continue
            division_name = all_sections[section_index]['divisions'][division]['divisionName']
            num_children = len(
                all_sections[section_index]['divisions'][division]['groups'])
            division_dict = create_subdict(
                division_name, 'division', num_children, section_dict)

            for group in all_sections[section_index]['divisions'][division]['groups']:
                if group_code != group['groupCode']:
                    continue
                group_name = group['groupName']
                num_children = len(group['classes'])
                group_dict = create_subdict(
                    group_name, 'group', num_children, division_dict)

                for class_dict in group['classes']:
                    if class_code == class_dict['classCode']:
                        class_name = class_dict['className']
                        final_dict = create_subdict(
                            class_name, 'class', None, group_dict)

    return final_dict


def write_file(kved_dict: dict):
    with open('kved_results.json', 'w', encoding='UTF-8') as file:
        json.dump(kved_dict, file, indent=4, ensure_ascii=False)


def parse_kved(class_code: str):
    kved_dict = read_file('kved.json')
    final_dict = dict(create_dictionary(kved_dict, class_code))
    write_file(final_dict)
    return final_dict
