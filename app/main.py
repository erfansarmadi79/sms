# -*- coding: utf-8 -*-
import base64

import falcon

import time

from functools import wraps

import ipaddress

from cerberus import Validator

from app import log
import subprocess

from app.middleware.auth import Authorize

from app.middleware.cheking_moving_file import AllowFileMoving

from app import manage_logging
from app.utils.config_manager import ChangeSetting
from app.utils.sqllite_manager import DatabaseSql

from app.manage_logging import LoggingManager

# from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager
# from app.database import db_session, init_session

# from app.api.common import base
# from app.api.v1 import users
# from app.errors import AppError

LOG = log.get_logger()


# class App(falcon.API):
#     def __init__(self, *args, **kwargs):
#         super(App, self).__init__(*args, **kwargs)
#         LOG.info('API Server is starting')
#
#         self.add_route('/', base.BaseResource())
#         self.add_route('/v1/users', users.Collection())
#         self.add_route('/v1/users/{user_id}', users.Item())
#         self.add_route('/v1/users/self/login', users.Self())
#
#         self.add_error_handler(AppError, AppError.handle)
#
# init_session()
# middleware = [AuthHandler(), JSONTranslator(), DatabaseSessionManager(db_session)]
# application = App(middleware=middleware)
#
#


class SystemInfo:
    def __init__(self):
        self.sudo_exe = "sms_sudo_exe"
        self.exe = "sms_exe"

    def my_systeminfo(self):
        self.output_str = "{\n"
        self.output_str += self.memoryinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.swapmemory()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.graphicinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.cpuInfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.cpu_temp()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.cpucoreInfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.hardinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.getdate()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += ",\n"
        self.output_str += self.getversionos()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"

        self.output_str += "}"

        return str(self.output_str)

    def memoryinfo(self):

        meminfo = subprocess.Popen([self.sudo_exe, 'sms_memory_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = meminfo.communicate()

        exitCodeMemory = meminfo.wait()

        if exitCodeMemory == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get memory information")
            return "\"memory\":" + "\"!!!cannot get memory information\"!!!"

    def swapmemory(self):
        swpinfo = subprocess.Popen([self.exe, 'sms_swap_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = swpinfo.communicate()

        exitCodeswapinfo = swpinfo.wait()

        if exitCodeswapinfo == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get swap information")
            return "\"swap\":" + "\"!!!cannot get swap information\"!!!"

    def graphicinfo(self):
        grphinfo = subprocess.Popen([self.exe, 'sms_graphic_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = grphinfo.communicate()

        exitCodeGraphic = grphinfo.wait()

        if exitCodeGraphic == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get graphic information")
            return "\"graphic\":" + "\"!!!cannot get graphic information\"!!!"

    def cpuInfo(self):
        cpuinfo = subprocess.Popen(
            [self.exe, 'sms_cpu_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cpuinfo.communicate()
        exitCodeCpu = cpuinfo.wait()

        if exitCodeCpu == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get Cpu information")
            return "\"CpuInfo\":" + "\"!!!cannot get Cpu information\"!!!"

    def cpucoreInfo(self):
        cpucoreinfo = subprocess.Popen(
            [self.exe, 'sms_cpu_useage'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cpucoreinfo.communicate()
        exitCodeCpuCore = cpucoreinfo.wait()

        if exitCodeCpuCore == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get CpuCore information")
            return "\"CpuCoreInfo\":" + "\"!!!cannot get CpuCore information\"!!!"

    def cpu_temp(self):
        cputemp = subprocess.Popen(
            [self.exe, 'sms_cpu_temperature'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cputemp.communicate()
        exitCodeCpuCore = cputemp.wait()

        if exitCodeCpuCore == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get CpuTemp information")
            return "\"CpuTemp\":" + "\"!!!cannot get CpuTemp information\"!!!"

    def hardinfo(self):
        hardinfo = subprocess.Popen([self.exe, 'sms_hard_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = hardinfo.communicate()

        exitCodeHard = hardinfo.wait()

        if exitCodeHard == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get HardDisk information")
            return "\"Hard_disk\":" + "\"!!!cannot get HardDisk information\"!!!"

    def getdate(self):
        date = subprocess.Popen([self.exe, 'sms_date_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = date.communicate()

        exitCodeDate = date.wait()

        if exitCodeDate == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get Date information")
            return "\"systemtime\":" + "\"!!!cannot get date information\"!!!"

    def getversionos(self):

        versionos = subprocess.Popen([self.exe, 'sms_osinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = versionos.communicate()

        exitCodeversion = versionos.wait()

        if exitCodeversion == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("cannot get versionos information")
            return "\"version-os\":" + "\"!!!cannot get versionos information\"!!!"

    def changeMaualDate(self, date, time):
        changetime = subprocess.Popen([self.sudo_exe, 'sms_date_manual', "\"" + date + "\"", "\"" + time + "\""],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = changetime.communicate()

        exitCodechangetime = changetime.wait()

        if exitCodechangetime == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report(stder.decode('utf-8'))
            return "do not set time"

    def changeAutomaticDate(self, serverip):
        changetime = subprocess.Popen([self.sudo_exe, 'sms_date_auto', "\"" + serverip + "\""],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = changetime.communicate()

        exitCodechangetime = changetime.wait()

        if exitCodechangetime == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report(stder.decode('utf-8'))
            return "do not set time"


class NetWorkViwer:

    def __int__(self):
        self.Runfile = "bashscript/sms_exe"
        self.sudoRunfile = "bashscript/sms_sudo_exe"

    def get_net_info(self):
        net_info = subprocess.Popen(['./sms_sudo_exe', 'sms_net_info'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = net_info.communicate()

        exitCodeaddnetwork = net_info.wait()

        if exitCodeaddnetwork == 0:
            LoggingManager().set_report("net work info:" + stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodeaddnetwork == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not get information network")


class NetWorkManager:

    def __init__(self):
        self.netViewer = NetWorkViwer()

    def change_config(self, nameinterface, lip, lnetmask, gatway, ldns):
        changeConfig = subprocess.Popen(
            ['./sms_sudo_exe', 'sms_net_change_config', "\"" + nameinterface + "\"", "\"" + lip + "\"",
             "\"" + lnetmask + "\"", "\"" + gatway + "\"", "\"" + ldns + "\""], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        stdout, stder = changeConfig.communicate()

        exitCodechangeConfig = changeConfig.wait()

        if exitCodechangeConfig == 0:
            LoggingManager().set_report(
                "change sucess NetWorkinterface (" + nameinterface + ") ips : " + lip + "netmasks : " + lnetmask + "gatway : " + gatway + "dnss : " + ldns)
            return "set config"
        elif exitCodechangeConfig == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 3:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 4:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 5:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 6:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not set config")
            return "do not set config"

    def addNetWork(self, nameinterface):
        addnetwork = subprocess.Popen(['./sms_sudo_exe', 'sms_net_interface_config add', "\"" + nameinterface + "\""],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = addnetwork.communicate()

        exitCodeaddnetwork = addnetwork.wait()

        if exitCodeaddnetwork == 0:
            LoggingManager().set_report("added netnetwork:" + nameinterface)
            return "added netnetwork"
        elif exitCodeaddnetwork == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not add network")
            return "do not add network"

    def removeNetWork(self, nameinterface):
        removenetwork = subprocess.Popen(
            ['./sms_sudo_exe', 'sms_net_interface_config remove', "\"" + nameinterface + "\""],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stder = removenetwork.communicate()
        exitCoderemovenetwork = removenetwork.wait()

        if exitCoderemovenetwork == 0:
            LoggingManager().set_report("remove netnetwork:" + nameinterface)
            return "removed netnetwork"
        elif exitCoderemovenetwork == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not remove network")
            return "do not remove network"

    def disableinterface(self, nameinterface):
        disableinterface = subprocess.Popen(
            ['./sms_sudo_exe', 'sms_net_interface_config disable', "\"" + nameinterface + "\""],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = disableinterface.communicate()

        exitCodedisableinterface = disableinterface.wait()

        if exitCodedisableinterface == 0:
            LoggingManager().set_report("disable interface :" + nameinterface)
            return "disable interface"
        elif exitCodedisableinterface == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not disable interface")
            return "do not disable interface"

    def enableinterface(self, nameinterface):
        enableinterface = subprocess.Popen(
            ['./sms_sudo_exe', 'sms_net_interface_config enable', "\"" + nameinterface + "\""],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = enableinterface.communicate()

        exitCodeenableinterface = enableinterface.wait()

        if exitCodeenableinterface == 0:
            LoggingManager().set_report("enabled interface :" + nameinterface)
            return "enabled netnetwork"
        elif exitCodeenableinterface == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("do not enable interface")
            return "do not enable interface"

    def changetodhcpnetwork(self, nameinterface):
        changetodhcp = subprocess.Popen(['./sms_exe', 'sms_net_change_dhcp', "\"" + nameinterface + "\""],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = changetodhcp.communicate()

        exitCodechangetodhcp = changetodhcp.wait()

        if exitCodechangetodhcp == 0:
            LoggingManager().set_report("changed to dhcp interface : " + nameinterface)
            return "changed to dhcp"
        elif exitCodechangetodhcp == 2:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            LoggingManager().set_report("can not change to dhcp")
            return "can not change to dhcp"


class Check_validation:

    def isstring(self, text):
        # Define the schema for the string
        schema = {'my_string': {'type': 'string'}}

        # Create a validator object and validate the string
        v = Validator(schema)
        if v.validate({'my_string': text}):
            return True
        else:
            return False

    def dateandtime(self, date, time):
        # Define the schema for the string
        schema = {
            'date': {'type': 'string', 'regex': r'^\d{4}-\d{2}-\d{2}$', 'date': '%Y-%m-%d'},
            'time': {'type': 'string', 'regex': r'^\d{2}:\d{2}:\d{2}$', 'time': '%H:%M:%S'}
        }

        # Create a validator object and validate the string
        v = Validator(schema)
        if v.validate({'date': date, 'time': time}):
            return True
        else:
            return False

    def ipandNetmask(self, ips):
        lips = ips.split()

        # Define the Cerberus schema for the IP addresses
        schema = {
            'ip_address': {
                'type': 'string',
                'regex': '^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
                # validate that the string is a valid IP address or subnet
            }
        }

        # Create a Cerberus validator object and validate each IP address against the schema
        v = Validator(schema)
        for ip in lips:
            doc = {'ip_address': ip}
            if v.validate(doc):
                # Extract the IP address or subnet from the validated dictionary
                ip_address = doc['ip_address']
                try:
                    # Try to create an IPv4Network or IPv6Network object from the IP address
                    ip_object = ipaddress.ip_interface(ip_address).network
                    if ip_object.num_addresses == 1:
                        return True
                    else:
                        return True
                except ValueError:
                    return False
            else:
                return False


class Service_Manager:

    def __init__(self):
        self.sudo_exe = "sms_sudo_exe"
        self.exe = "sms_exe"

    def enable_service(self, service_name):
        service_enable = subprocess.Popen([self.sudo_exe, 'sms_service', 'enable', "\"" + service_name + "\""],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = service_enable.communicate()

        exitCode = service_enable.wait()

        if exitCode == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCode == 2:
            LoggingManager().set_report("not exits service")
            return "\"service\":" + "\"!!!not exits service\"!!!"
        else:
            LoggingManager().set_report("cannot enable service")
            return "\"service\":" + "\"cannot enable service\"!!!"

    def disable_service(self, service_name):
        service_disable = subprocess.Popen([self.sudo_exe, 'sms_service', 'disable', "\"" + service_name + "\""],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = service_disable.communicate()

        exitCode = service_disable.wait()

        if exitCode == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCode == 2:
            LoggingManager().set_report("not exits service")
            return "\"service\":" + "\"!!!not exits service\"!!!"
        else:
            LoggingManager().set_report("cannot disable service")
            return "\"service\":" + "\"cannot disable service\"!!!"

    def restart_service(self, service_name):

        service_restart = subprocess.Popen([self.sudo_exe, 'sms_service', 'restart', "\"" + service_name + "\""],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = service_restart.communicate()

        exitCode = service_restart.wait()

        if exitCode == 0:
            LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCode == 2:
            LoggingManager().set_report("not exits service")
            return "\"service\":" + "\"!!!not exits service\"!!!"
        else:
            LoggingManager().set_report("cannot restart service")
            return "\"service\":" + "\"cannot restart service\"!!!"

class FileManager:

    def __init__(self):

        self.permition_file = AllowFileMoving()

    def copyfile(self, src, dis):

        flag = self.permition_file.check_permition_path(src, dis)

        if flag == 0:




    def cutfile(self, src, dis):



class ConectionManager:
    def rate_limited(max_requests=60, window_seconds=60):
        """
        A decorator that limits the rate of requests a client can make.
        """
        # Keep track of request times and count
        request_times = []
        request_count = 0

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal request_times, request_count

                # Remove old requests from the list
                now = time.time()
                request_times = [t for t in request_times if t > now - window_seconds]

                # Check if the client has exceeded the rate limit
                if len(request_times) >= max_requests:
                    raise falcon.HTTPTooManyRequests('Rate limit exceeded')

                # Update the request times and count
                request_times.append(now)
                request_count += 1

                # Call the wrapped function
                result = func(*args, **kwargs)

                return result

            return wrapper

        return decorator


class APINetWork:

    def __init__(self):
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()
        self.conf = ChangeSetting()
        self.db_sql = DatabaseSql()
        self.check = Check_validation()

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.netread:
            if 'conf' in req.params and self.check.isstring(req.params['conf']):
                if str(req.params['conf']).lower() == "net_info":
                    resp.body = self.netviewer.get_net_info()
                else:
                    resp.status = falcon.HTTP_400
                    LoggingManager().set_report("Error 400 : not params conf")
                    raise falcon.HTTPUnauthorized('typeconf parameter is wrong')
            else:
                resp.status = falcon.HTTP_400
                LoggingManager().set_report("Error 400 : not params conf")
                raise falcon.HTTPUnauthorized('typeconf parameter is wrong')
        else:
            LoggingManager().set_report("Error 400 : not params namenet")
            raise falcon.HTTPUnauthorized('Are you not permition!!!')

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.netread:
            if self.conf.get_change_setting():
                if 'conf' in req.params and self.check.isstring(req.params['conf']):
                    if str(req.params['conf']).lower() == "changeconfig":
                        if 'namenet' in req.params and self.check.isstring(req.params['namenet']):
                            if 'listip' in req.params and self.check.ipandNetmask(req.params['listip']):
                                if 'listnetmask' in req.params and self.check.ipandNetmask(req.params['listnetmask']):
                                    if 'gatway' in req.params and self.check.ipandNetmask(req.params['gatway']):
                                        if 'listdns' in req.params and self.check.ipandNetmask(req.params['listdns']):
                                            if ChangeSetting().get_change_setting():
                                                if self.db_sql.get_permition_users().getPermition(self.username):
                                                    resp.body = self.netmanager.change_config(req.params['namenet'],
                                                                                              req.params['listip'],
                                                                                              req.params['listnetmask'],
                                                                                              req.params['gatway'],
                                                                                              req.params['list_dns'])
                                                else:
                                                    resp.status = falcon.HTTP_400
                                                    LoggingManager().set_report(
                                                        "Error 400 : you are not permition")
                                                    raise falcon.HTTPNotImplemented('You haven\'t Permition')
                                            else:
                                                resp.status = falcon.HTTP_400
                                                LoggingManager().set_report(
                                                    "Error 400 : you are not permition")
                                                raise falcon.HTTPNotImplemented('You haven\'t Permition')
                                        else:
                                            resp.status = falcon.HTTP_400
                                            LoggingManager().set_report(
                                                "Error 400 : listdns parameter is wrong")
                                            raise falcon.HTTPUnauthorized('listdns parameter is wrong')
                                    else:
                                        resp.status = falcon.HTTP_400
                                        LoggingManager().set_report(
                                            "Error 400 : gatway parameter is wrong")
                                        raise falcon.HTTPUnauthorized('gatway parameter is wrong')
                                else:
                                    resp.status = falcon.HTTP_400
                                    LoggingManager().set_report(
                                        "Error 400 : listnetmask parameter is wrong")
                                    raise falcon.HTTPUnauthorized('listnetmask parameter is wrong')
                            else:
                                resp.status = falcon.HTTP_400
                                LoggingManager().set_report("Error 400 : listip parameter is wrong")
                                raise falcon.HTTPUnauthorized('listip parameter is wrong')
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "addnet":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.addNetWork(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "removenet":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.removeNetWork(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "disablenet":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.disableinterface(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "enablenet":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.enableinterface(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "checkstate":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.checkstateinterface(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "checktypeip":
                        if 'namenet' in req.params:
                            getmes = self.netmanager.checktypeip(req.params['namenet'])
                            resp.body = getmes
                            LoggingManager().set_report(str(getmes))
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "changetodhcp":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.changetodhcpnetwork(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                            raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                    elif str(req.params['conf']).lower() == "listintr":
                        if 'namenet' in req.params:
                            resp.body = self.netmanager.getlistinterface(req.params['namenet'])
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : typeconf parameter is wrong")
                            raise falcon.HTTPUnauthorized('typeconf parameter is wrong')
                    else:
                        resp.status = falcon.HTTP_400
                        LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                        raise falcon.HTTPUnauthorized('namenet parameter is wrong')
                else:
                    LoggingManager().set_report("Error 400 : not params conf")
                    raise falcon.HTTPUnauthorized('not params conf')

            else:
                raise falcon.HTTPUnauthorized('You are not allowed to try later')
        else:
            LoggingManager().set_report("Error 400 : Are you not permitio")
            raise falcon.HTTPUnauthorized('Are you not permition!!!')



class APIFileManager:

    def __init__(self):
        self.conf = ChangeSetting()
        self.db_sql = DatabaseSql()
        self.check_validation = Check_validation()
        self.file_manager = FileManager()


    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_get(self, req, resp):
        pass

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.netread:
            if 'action' in req.params and self.check.isstring(req.params['action']):
                if str(req.params['action']).lower() == "copy":
                    if 'src' in req.params and self.check.isstring(req.params['src']):
                        if 'dis' in req.params and self.check.isstring(req.params['dis']):
                            if self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 0:

                            elif self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 1:
                                pass
                            elif self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 2:
                                pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif str(req.params['action']).lower() == "cut":
                    if 'src' in req.params and self.check.isstring(req.params['src']):
                        if 'dis' in req.params and self.check.isstring(req.params['dis']):
                            if self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 0:
                                pass
                            elif self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 1:
                                pass
                            elif self.path_permition.check_permition_path(req.params['src'], req.params['dis']) == 2:
                                pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif str(req.params['action']).lower() == "remove":
                    pass
                else:
                    pass
            else:
                pass
        else:
            pass


class APISystemInfo:
    def __init__(self):
        self.username = None
        self.conf = ChangeSetting()
        self.sys = SystemInfo()
        self.db_sql = DatabaseSql()

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_get(self, req, resp):

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.systemInfo:
            if req.params == {}:
                res = self.sys.my_systeminfo()
                resp.body = str(res)
                LoggingManager().set_report(str(res))
            else:
                LoggingManager().set_report("Error 400 : not Arguments")
                raise falcon.HTTPUnauthorized('not Arguments!!!')

        else:
            LoggingManager().set_report("Error 400 : not params namenet")
            raise falcon.HTTPUnauthorized('Are you not permition!!!')

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.netread:
            if self.conf.get_change_setting():
                if 'conf' in req.params and self.check.isstring(req.params['conf']):
                    if str(req.params['conf']).lower() == "setdate":
                        if 'typedate' in req.params and self.check.isstring(req.params['typedate']):
                            if str(req.params['typedate']).lower() == "auto":
                                if 'serverip' in req.params and self.check.ipandNetmask(req.params['serverip']):
                                    self.sys.changeAutomaticDate(req.params['serverip'])
                                else:
                                    resp.status = falcon.HTTP_400
                                    LoggingManager().set_report("Error 400 : ipserver not valid")
                                    raise falcon.HTTPUnauthorized('ipserver not valid')

                            elif str(req.params['typedate']).lower() == "manual":
                                if 'date' in req.params and 'date' in req.params:
                                    if self.check.dateandtime(req.params['date'], req.params['time']):
                                        self.sys.changeMaualDate(req.params['date'], req.params['time'])
                            else:
                                resp.status = falcon.HTTP_400
                                LoggingManager().set_report("Error 400 : date or time not valid")
                                raise falcon.HTTPUnauthorized('date or time not valid')
                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : typedate parameter is wrong")
                            raise falcon.HTTPUnauthorized('typedate parameter is wrong')
                    else:
                        resp.status = falcon.HTTP_400
                        LoggingManager().set_report("Error 400 : conf parameter is wrong")
                        raise falcon.HTTPUnauthorized('conf parameter is wrong')
                else:
                    LoggingManager().set_report("Error 400 : not params conf")
                    raise falcon.HTTPUnauthorized('not params conf')
            else:
                raise falcon.HTTPUnauthorized('You are not allowed to try later')
        else:
            LoggingManager().set_report("Error 400 : Are you not permition")
            raise falcon.HTTPUnauthorized('Are you not permition!!!')


class APIService:
    def __init__(self):
        self.username = None
        self.conf = ChangeSetting()
        self.service = Service_Manager()
        self.db_sql = DatabaseSql()

    @falcon.before(Authorize())
    @ConectionManager.rate_limited(max_requests=60, window_seconds=60)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        _permition = self.db_sql.get_permition_users(self.username)

        if _permition.netread:
            if self.conf.get_change_setting():
                if 'action' in req.params and self.check.isstring(req.params['action']):
                    if str(req.params['action']).lower() == "enable":
                        if 'service_name' in req.params and self.check.isstring(req.params['service_name']):

                            self.service.enable_service(req.params['service_name'])

                        else:
                            resp.status = falcon.HTTP_400
                            LoggingManager().set_report("Error 400 : service_name parameter is wrong")
                            raise falcon.HTTPUnauthorized('service_name parameter is wrong')
                    else:
                        resp.status = falcon.HTTP_400
                        LoggingManager().set_report("Error 400 : action parameter is wrong")
                        raise falcon.HTTPUnauthorized('action parameter is wrong')
                else:
                    LoggingManager().set_report("Error 400 : not params action")
                    raise falcon.HTTPUnauthorized('not params action')
            else:
                raise falcon.HTTPUnauthorized('You are not allowed to try later')
        else:
            LoggingManager().set_report("Error 400 : Are you not permition")
            raise falcon.HTTPUnauthorized('Are you not permition!!!')


api = falcon.API()

api.add_route('/v1/systeminfo', APISystemInfo())
api.add_route('/v1/net', APINetWork())
api.add_route('/v1/service', APIService())
api.add_route('/v1/file_manager', APIFileManager())

if __name__ == "__main__":

    conf = ChangeSetting()

    from wsgiref import simple_server

    if conf.get_global_service():
        httpd = simple_server.make_server('0.0.0.0', 5000, api)
        LoggingManager().set_report("start API server 0.0.0.0:5000")
        httpd.serve_forever()
    else:
        httpd = simple_server.make_server('127.0.0.1', 5000, api)
        LoggingManager().set_report("start API server 127.0.0.1:5000")
        httpd.serve_forever()
