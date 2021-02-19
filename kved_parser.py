import json
from pprint import pprint

def read_file(path: str) -> dict:
    with open('kved.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

kved_dict = read_file('path')
# pprint(kved_dict)


def create_dictionary(kved_dict: dict, class_code: str):
    new_dict = {}

    division_code = class_code[:2]
    group_code = class_code[:-1]
    print(division_code, group_code)
    print()

    for lst in kved_dict['sections']:
        all_sections = lst

    for section_index in range(len(all_sections)):
        section_code = all_sections[section_index]['sectionCode']

        section_dict = {}
        section_dict['name'] = section_code
        section_dict['type'] = 'section'
        section_dict['num_children'] = len(all_sections[section_index]['divisions'])
        # print(section_dict)

        for division in range(len(all_sections[section_index]['divisions'])):
            # print(all_sections[section_index]['divisions'][division].keys())

            if division_code != all_sections[section_index]['divisions'][division]['divisionCode']:
                continue
            division_name = all_sections[section_index]['divisions'][division]['divisionName']
            division_dict = {}
            division_dict['name'] = division_name
            division_dict['type'] = 'division'
            division_dict['num_children'] = len(all_sections[section_index]['divisions'][division]['groups'])
            division_dict['parent'] = section_dict

            for group in all_sections[section_index]['divisions'][division]['groups']:
                if group_code != group['groupCode']:
                    continue

                group_dict = {}
                group_dict['name'] = group['groupName']
                group_dict['type'] = 'group'
                group_dict['num_children'] = len(group['classes'])
                group_dict['parent'] = division_dict
                
                for class_dict in group['classes']:

                    if class_code == class_dict['classCode']:
                        print(class_dict['className'])
                        new_dict['name'] = class_dict['className']
                        new_dict['type'] = 'class'
                        new_dict['parent'] = group_dict

    return new_dict

class_code = "01.11"
pprint(create_dictionary(kved_dict, class_code))
