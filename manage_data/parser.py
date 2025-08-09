from collections import defaultdict

import chardet


def parse_cp_file(file_path):

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    
    print(f"Detected encoding: {encoding}")

    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()
    

    definitions = {}
    data_sections = defaultdict(list)
    current_section = None
    section_headers = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("[Definition]"):
            current_section = "definition"
            continue

        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].lower()
            current_section = section_name
            continue

        if current_section == "definition":
            # Example: gameinfo=Game;Group;...
            section, fields = line.split("=", 1)
            section = section.strip().lower()
            definitions[section] =  fields.split(";")
        else:
            # It's a data row for a known section
            if current_section in definitions:
                fields = definitions[current_section]
                values = line.split(";")
                row_dict = dict(zip(fields, values))
                data_sections[current_section].append(row_dict)
            else:
                # Unknown section
                continue

    return data_sections

# result = parse_cp_file("cp-files/txt/01.CP")

# from pprint import pprint
# pprint(result["gameinfo"])
