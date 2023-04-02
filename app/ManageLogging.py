import getpass as gt
import logging
import os
from datetime import datetime
import pytz

class LoggingManager:

    def __init__(self):
        path_file = "/var/log/remote/"
        if os.path.isdir(path_file):
            logging.basicConfig(filename=path_file+"apprmt.log", filemode='a')
        else:
            os.mkdir(path_file, 0o777)
            logging.basicConfig(filename=path_file + "apprmt.log", filemode='a')

    def set_report(self, message):
        logging.warning(str(self.get_username())+" - "+self.get_datetime()+" - "+message)

    def get_datetime(self):
         tz_NY = pytz.timezone('Asia/Tehran')
         datetime_NY = datetime.now(tz_NY)
         datetime_NY = datetime_NY.strftime("%Y-%m-%d %H:%M:%S")
         return str(datetime_NY)
    def get_username(self):
        return str(gt.getuser())
