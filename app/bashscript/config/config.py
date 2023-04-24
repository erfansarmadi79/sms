import json


class ChangeSetting:
    def __init__(self):
        #self.json_file = open('../config/json_config/config.json')
        self.json_file = open('config.json')
        self.json_data = json.loads(self.json_file.read())

    def checkAllow(self):
        return self.json_data['config']['changesetting']['allowed']
