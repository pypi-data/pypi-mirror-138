import json


class ptjsonlib:
    def __init__(self, json):
        self.json = json
        self.json_list = []

    def add_json(self, name):
       json_template = {"test_code": name, "status": "null", "vulnerable": "null", "data": {}}
       self.json_list.append(json_template)
       return len(self.json_list) - 1

    def del_json(self, position):
        self.json_list.pop(position)

    def add_data(self, position, data):
        self.json_list[position]['data'].update(data)

    def set_testcode(self, position, testcode):
        self.json_list[position].update({"testcode": testcode})

    def set_status(self, position, status, error_message = ""):
        self.json_list[position].update({"status": status})
        if status == "error":
            self.json_list[position].update({"message": error_message})

    def set_vulnerable(self, position, vulnerable):
        self.json_list[position].update({"vulnerable": vulnerable})

    def get_json(self, position):
        return json.dumps(self.json_list[position])

    def get_all_json(self):
        return json.dumps(self.json_list)

    def get_status(self, position):
        return self.json_list[position]["status"]
