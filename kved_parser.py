"""
GitHub link: https://github.com/alorthius/lab_3_kved_parser
"""
import json
from collections import OrderedDict


def read_file(path: str) -> dict:
    """
    Read json file from its path and return it as a dictionary.
    Return None if path argument is not a string.

    >>> read_file(['path'])

    """
    if not isinstance(path, str):
        return None

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def create_subdict(name: str, type_value: str, num_children: int, parent: dict) -> OrderedDict:
    """
    Create a dictionary with the following keys:
    compulsory: 'name', 'type'
    optional: 'num_children', 'parent'
    Return None if either of the arguments name or type_value is not a string.

    >>> create_subdict('Вирощування зернових культур', 'class', None, 'other dict')
    OrderedDict([('name', 'Вирощування зернових культур'), ('type', 'class'),\
 ('parent', 'other dict')])

    >>> create_subdict('A', 'section', 3, None)
    OrderedDict([('name', 'A'), ('type', 'section'), ('num_children', 3)])
    """
    if not isinstance(name, str) or not isinstance(type_value, str):
        return None

    subdict = OrderedDict()
    subdict['name'] = name
    subdict['type'] = type_value
    if num_children:
        subdict['num_children'] = num_children
    if parent:
        subdict['parent'] = parent
    return subdict


def create_dictionary(kved_dict: dict, class_code: str) -> OrderedDict:
    """
    Find information about class and its parents in the dictionary.
    Return new dictionary with all information found.
    Return None if either of the arguments kved_dict or class_code is not a string.

    >>> create_dictionary({'keys': 'values'}, 11.11)
    """
    if not isinstance(kved_dict, dict) or not isinstance(class_code, str):
        return None

    division_code = class_code[:2]
    group_code = class_code[:-1]

    for lst in kved_dict['sections']:
        all_sections = lst

    for section_index in range(len(all_sections)):
        section_name = all_sections[section_index]['sectionName']
        num_children = len(all_sections[section_index]['divisions'])
        section_dict = create_subdict(
            section_name, 'section', num_children, None)

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
    try:
        return final_dict
    except UnboundLocalError:  # found no class like class_code
        return None


def write_file(kved_dict: dict):
    """
    Convert dictionary into json object and save it in the file.
    Return None if the argument kved_dict is not a dictionary.

    >>> write_file({'not a dict'})

    """
    if not isinstance(kved_dict, dict):
        return None

    with open('kved_results.json', 'w', encoding='UTF-8') as file:
        json.dump(kved_dict, file, indent=4, ensure_ascii=False)


def parse_kved(class_code: str):
    """
    Main function to find the class information in the file 'kved.json'
    and save it as a json object.
    Return None if the argument class_code is not a string.

    >>> parse_kved(11.11)

    """
    if not isinstance(class_code, str):
        return None

    kved_dict = read_file('kved.json')
    final_dict = create_dictionary(kved_dict, class_code)
    write_file(final_dict)
