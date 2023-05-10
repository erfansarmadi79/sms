import getpass as gt
import logging

from datetime import datetime
import pytz
from app.utils.config_manager import ChangeSetting


class LoggingManager:

    def __init__(self):
        self.conf = ChangeSetting()
        path_file = self.conf.get_log_path()

        # if os.path.isdir(path_file):
        #     logging.basicConfig(filename=path_file+"sms.log", filemode='a')
        # else:
        #     os.mkdir(path_file, 0o777)
        #     logging.basicConfig(filename=path_file + "sms.log", filemode='a')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(path_file + 'sms.log')
        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def set_report(self, message):
        # logging.warning(str(self.get_username())+" - "+self.get_datetime()+" - "+message)
        self.logger.info(str(self.get_username()) + " - " + self.get_datetime() + " - " + message)

    @staticmethod
    def get_datetime():
        tz = pytz.timezone('Asia/Tehran')
        datetime_current = datetime.now(tz)
        date_time = datetime_current.strftime("%Y-%m-%d %H:%M:%S")
        return str(date_time)

    @staticmethod
    def get_username():
        return str(gt.getuser())
