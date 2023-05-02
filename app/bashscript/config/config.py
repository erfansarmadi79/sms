import json


class ChangeSetting:
    def __init__(self):
        #self.json_file = open('../config/json_config/config.json')
        #self.json_file = open('config.json')
        self.json_file = open('/home/admin/1402.02.11/sms/app/bashscript/config/config.json')
        self.json_data = json.loads(self.json_file.read())

    def permition_changeallow(self):
        res = self.json_data['config']['changesetting']['allowed']
        if res.lower() == "true":
            return True
        elif res.lower() == "false":
            return False

    def gettypeserver(self):
        res = self.json_data['config']['server']['type']

        if res.lower() == "true":
            return True
        elif res.lower() == "false":
            return False
    def get_pathlog(self):
        return self.json_data['config']['loger']['path_file']



