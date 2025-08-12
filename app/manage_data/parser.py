from collections import defaultdict
import chardet

class CpFileParser:
    def __init__(self):
        self.cached_file_name = None
        self.cached_data = {}

    def parse(self, file_content: bytes, file_name: str):

        result = chardet.detect(file_content)
        encoding = result['encoding']
        lines = file_content.decode(encoding).splitlines()
        if self.cached_file_name == file_name:
            return self._update_data(lines)
        else:
            return self._full_parse(file_name, lines)

    def _full_parse(self, file_name: str, lines: list[str]):
        self.cached_file_name = file_name
        definitions = {}
        data_sections = defaultdict(list)
        current_section = None
        action_lines_count = 0
        actions_start_line = -1

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            if line.startswith("[Definition]"):
                current_section = "definition"
                continue

            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1].lower()
                current_section = section_name
                if current_section == "actions":
                    actions_start_line = i
                continue

            if current_section == "definition":
                section, fields = line.split("=", 1)
                section = section.strip().lower()
                definitions[section] = fields.split(";")
            else:
                if current_section in definitions:
                    if current_section == "actions":
                        action_lines_count += 1
                    fields = definitions[current_section]
                    values = line.split(";")
                    row_dict = dict(zip(fields, values))
                    data_sections[current_section].append(row_dict)

        self.cached_data = {
            "definitions": definitions,
            "actions_start_line": actions_start_line,
            "action_lines_count": action_lines_count,
        }
        return data_sections

    def _update_data(self, lines: list[str]):
        definitions = self.cached_data["definitions"]
        last_action_lines_count = self.cached_data["action_lines_count"]
        actions_start_line = self.cached_data["actions_start_line"]

        # Reset all sections except actions
        new_data_sections = defaultdict(list)

        current_section = None

        # Re-parse the file up to the actions section
        for line in lines[:actions_start_line]:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1].lower()
                if section_name != "definition":
                    current_section = section_name
                continue
            if current_section and current_section != "actions" and current_section in definitions:
                fields = definitions[current_section]
                values = line.split(";")
                row_dict = dict(zip(fields, values))
                new_data_sections[current_section].append(row_dict)

        # Parse only new actions
        new_actions = lines[actions_start_line +last_action_lines_count+ 1:]
        
        for line in new_actions:
            line = line.strip()
            if not line:
                continue
            fields = definitions["actions"]
            values = line.split(";")
            row_dict = dict(zip(fields, values))
            new_data_sections["actions"].append(row_dict)

        self.cached_data["action_lines_count"] += len(new_actions)

        return new_data_sections


