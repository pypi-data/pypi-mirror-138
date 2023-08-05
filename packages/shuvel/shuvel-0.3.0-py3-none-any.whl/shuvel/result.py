import json

from shuvel.rule import Rule


class Result:
    def __init__(self, rel_file_path: str, line_num: int, line_str: str, rule: Rule):
        self.rel_file_path = rel_file_path
        self.line_num = line_num
        self.line_str = line_str
        self.rule = rule

    def __repr__(self):
        return str(json.dumps(self.__dict__))
