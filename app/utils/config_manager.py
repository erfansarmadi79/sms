import json


class ChangeSetting:
    def __init__(self):
        self.json_file = open('/etc/sms/sms.conf')
        self.json_data = json.loads(self.json_file.read())

    def get_change_setting(self):
        res = self.json_data['config']['change_setting']
        return res

    def get_global_service(self):
        res = self.json_data['config']['global_service']
        return res

    def get_log_path(self):
        return self.json_data['config']['log_path']

    def get_database_path(self):
        return self.json_data['config']['db_path']
