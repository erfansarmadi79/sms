# -*- coding: utf-8 -*-
import base64

import falcon

from app import log
import subprocess

from auth import Authorize

from app import ManageLogging
from app.bashscript.config.config import ChangeSetting

import config.config

import database.sqllite_manager as db

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
        self.output_str += "\n"

        self.output_str += "}"

        return str(self.output_str)

    def memoryinfo(self):

        meminfo = subprocess.Popen(['./smssudo_runfile', 'smsmemory_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = meminfo.communicate()

        exitCodeMemory = meminfo.wait()

        if exitCodeMemory == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get memory information")
            return "\"memory\":"+"\"!!!cannot get memory information\"!!!"

    def swapmemory(self):
        swpinfo = subprocess.Popen(['./smsrunfile', 'smsmemory_swapinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = swpinfo.communicate()

        exitCodeswapinfo = swpinfo.wait()

        if exitCodeswapinfo == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get swap information")
            return "\"swap\":" + "\"!!!cannot get swap information\"!!!"

    def graphicinfo(self):
        grphinfo = subprocess.Popen(['./smsrunfile', 'smsgraphic_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = grphinfo.communicate()

        exitCodeGraphic = grphinfo.wait()

        if exitCodeGraphic == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get graphic information")
            return "\"graphic\":" + "\"!!!cannot get graphic information\"!!!"

    def cpuInfo(self):
        cpuinfo = subprocess.Popen(
            ['./smsrunfile', 'smscpu_info.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cpuinfo.communicate()
        exitCodeCpu = cpuinfo.wait()

        if exitCodeCpu == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get Cpu information")
            return "\"CpuInfo\":" + "\"!!!cannot get Cpu information\"!!!"

    def cpucoreInfo(self):
        cpucoreinfo = subprocess.Popen(
            ['./smsrunfile', 'smscpu_usedcore'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cpucoreinfo.communicate()
        exitCodeCpuCore = cpucoreinfo.wait()

        if exitCodeCpuCore == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get CpuCore information")
            return "\"CpuCoreInfo\":" + "\"!!!cannot get CpuCore information\"!!!"

    def cpu_temp(self):
        cputemp = subprocess.Popen(
            ['./smsrunfile', 'smscpu_temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cputemp.communicate()
        exitCodeCpuCore = cputemp.wait()

        if exitCodeCpuCore == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get CpuTemp information")
            return "\"CpuTemp\":" + "\"!!!cannot get CpuTemp information\"!!!"

    def hardinfo(self):
        hardinfo = subprocess.Popen(['./smsrunfile', 'smshard_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = hardinfo.communicate()

        exitCodeHard = hardinfo.wait()

        if exitCodeHard == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("cannot get HardDisk information")
            return "\"Hard_disk\":" + "\"!!!cannot get HardDisk information\"!!!"

class NetWorkViwer:


    def __int__(self):
        self.Runfile = "bashscript/smsrunfile"
        self.sudoRunfile = "bashscript/smssudo_runfile"

    def getallinfointerface(self):
        json_str = ""

        json_str += "{"
        json_str += "\n\t" + '"interfaces": {' + "\n"
        interfaces = subprocess.check_output(['bash', 'list_connectednetwork.sh']).decode('utf-8')
        list_interface = interfaces.split()
        for i in list_interface:
            json_str += "\t\t"
            json_str += '"' + i + '": {'
            json_str += '"ip": ' + '"' + self.getIp(i).replace("\n", "") + '"' + ',' + "\n"
            json_str += "\t\t\t  " + '"state": ' + '"' + self.getState(i).replace("\n", "") + '"' + ',' + "\n"
            json_str += "\t\t\t  " + '"DefaultGetway": ' + '"' + self.getDefaultgetway(i).replace("\n",
                                                                                                  "") + '"' + ',' + "\n"
            json_str += "\t\t\t  " + '"Netmask": ' + '"' + self.getNetmask(i).replace("\n", "") + '"' + ',' + "\n"
            json_str += "\t\t\t  " + '"Dns": ' + '"' + self.getDns().replace("\n", ",") + '"' + "\n" + "\t\t\t  },\n"
        json_str = json_str[:-2]
        json_str += "\n\t\t}"
        json_str += "\n}"
        return json_str

    def getIp(self, InterfaceName):


        ipNet = subprocess.Popen(['./smsrunfile', 'smsnet_getip', InterfaceName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = ipNet.communicate()

        exitCodeipnet = ipNet.wait()

        if exitCodeipnet == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodeipnet == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get ip information")
            return "{"+"\"error\":"+"\"!!!cannot get ip information!!!\""+"}"

    def getDefaultgetway(self, InterfaceName):
        defaltGetway = subprocess.Popen(['./smsrunfile', 'smsnet_getDefaultgetway', InterfaceName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = defaltGetway.communicate()

        exitCodedefgetway = defaltGetway.wait()

        if exitCodedefgetway == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodedefgetway == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get Defaultgetway information")
            return "{" + "\"error\":" + "\"!!!cannot get Defaultgetway information!!!\"" + "}"


    def getNetmask(self, InterfaceName):
        netMask = subprocess.Popen(['bash', './smsrunfile', 'smsnet_getNetmask', InterfaceName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = netMask.communicate()

        exitCodeNetmask = netMask.wait()

        if exitCodeNetmask == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))

            return stdout.decode('utf-8')

        elif exitCodeNetmask == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get NetMask information.")
            return "{" + "\"error\":" + "\"!!!cannot get NetMask information!!!\"" + "}"

    def getDns(self, InterfaceName):
        Dns = subprocess.run(['bash', './smsrunfile', 'smsnet_getDNS', InterfaceName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        exitCodeDns = Dns.returncode

        if exitCodeDns == 0:
            ManageLogging.LoggingManager().set_report(Dns.stdout.decode('utf-8'))
            return Dns.stdout.decode('utf-8')
        elif exitCodeDns == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        elif exitCodeDns == 3:
            ManageLogging.LoggingManager().set_report("DNS is not configured.")
            return "DNS is not configured."
        else:
            ManageLogging.LoggingManager().set_report("Dns does not exist.")
            return "Dns does not exist."

class NetWorkManager:

    def __init__(self):
        self.netViewer = NetWorkViwer()

    def change_config(self, nameinterface, lip, lnetmask, gatway, ldns):
        changeConfig = subprocess.Popen(['./smssudo_runfile', 'smsnet_ip_cahnge', "\"" + nameinterface + "\"", "\"" + lip + "\"", "\"" + lnetmask + "\"", "\"" + gatway + "\"", "\"" + ldns + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = changeConfig.communicate()

        exitCodechangeConfig = changeConfig.wait()

        if exitCodechangeConfig == 0:
            return "set config"
            ManageLogging.LoggingManager().set_report("change sucess NetWorkinterface ("+nameinterface+") ips : "+lip+"netmasks : "+lnetmask+"gatway : "+gatway+"dnss : "+ldns)
        elif exitCodechangeConfig == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 3:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 4:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 5:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechangeConfig == 6:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("do not set config")
            return "do not set config"

    def addNetWork(self, nameinterface):
        addnetwork = subprocess.Popen(['./smssudo_runfile', 'smsnet_addnetwork', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = addnetwork.communicate()

        exitCodeaddnetwork= addnetwork.wait()

        if exitCodeaddnetwork == 0:
            ManageLogging.LoggingManager().set_report("added netnetwork:" + nameinterface)
            return "added netnetwork"
        elif exitCodeaddnetwork == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("do not add network")
            return "do not add network"

    def removeNetWork(self, nameinterface):
        removenetwork = subprocess.Popen(['./smssudo_runfile', 'smsnet_removeNetwork', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stder = removenetwork.communicate()
        exitCoderemovenetwork = removenetwork.wait()

        if exitCoderemovenetwork == 0:
            ManageLogging.LoggingManager().set_report("remove netnetwork:" + nameinterface)
            return "removed netnetwork"
        elif exitCoderemovenetwork == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("do not remove network")
            return "do not remove network"

    def disableinterface(self, nameinterface):
        disableinterface = subprocess.Popen(['./smssudo_runfile', 'smsnet_disablenet', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = disableinterface.communicate()

        exitCodedisableinterface = disableinterface.wait()

        if exitCodedisableinterface == 0:
            ManageLogging.LoggingManager().set_report("disable interface :" + nameinterface)
            return "disable interface"
        elif exitCodedisableinterface == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("do not disable interface")
            return "do not disable interface"

    def enableinterface(self, nameinterface):
        enableinterface = subprocess.Popen(['./smssudo_runfile', 'smsnet_enablenet', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = enableinterface.communicate()

        exitCodeenableinterface = enableinterface.wait()

        if exitCodeenableinterface == 0:
            ManageLogging.LoggingManager().set_report("enabled interface :" + nameinterface)
            return "enabled netnetwork"
        elif exitCodeenableinterface == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("do not enable interface")
            return "do not enable interface"

    def checktypeip(self, nameinterface):
        checktypeinterface = subprocess.Popen(['./smsrunfile', 'smsnet_checkTypeIp', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = checktypeinterface.communicate()

        exitCodechecktypeinterface = checktypeinterface.wait()

        if exitCodechecktypeinterface == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodechecktypeinterface == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("can not checked interface")
            return "can not checked interface"

    def changetodhcpnetwork(self, nameinterface):
        changetodhcp = subprocess.Popen(['./smsrunfile', 'smsnet_changestatic_dhcp', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = changetodhcp.communicate()

        exitCodechangetodhcp = changetodhcp.wait()

        if exitCodechangetodhcp == 0:
            ManageLogging.LoggingManager().set_report("changed to dhcp interface : " + nameinterface)
            return "changed to dhcp"
        elif exitCodechangetodhcp == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("can not change to dhcp")
            return "can not change to dhcp"
    def checkstateinterface(self, nameinterface):
        checkstate = subprocess.Popen(['./smsrunfile', 'smsnet_checkstat', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = checkstate.communicate()

        exitCodecheckstate = checkstate.wait()

        if exitCodecheckstate == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodecheckstate == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("can not checking state")
            return "can not checking state"

    def getlistinterface(self, nameinterface):
        getlist = subprocess.Popen(['./smsrunfile', 'smsnet_getlistinterface', "\"" + nameinterface + "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stder = getlist.communicate()

        exitCodegetlist = getlist.wait()

        if exitCodegetlist == 0:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        elif exitCodegetlist == 2:
            ManageLogging.LoggingManager().set_report(stdout.decode('utf-8'))
            return stdout.decode('utf-8')
        else:
            ManageLogging.LoggingManager().set_report("can not get list")
            return "can not get list"



class APINetWork:

    def __init__(self):
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()
        self.conf = ChangeSetting()

    @falcon.before(Authorize())
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getIp(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : not params namenet")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')
        elif str(req.params['conf']).lower() == "state":
            if 'namenet' in req.params:
                print("")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : not params namenet")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')
        elif str(req.params['conf']).lower() == "defaultgatway":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDefaultgetway(req.params['namenet']).replace("\n", "")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : not params namenet")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')
        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getNetmask(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : not params namenet")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')
        elif str(req.params['conf']).lower() == "dns":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDns(req.params['namenet']).replace("\n", ",")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : not params namenet")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')
        else:
            resp.status = falcon.HTTP_400
            ManageLogging.LoggingManager().set_report("Error 400 : not params typeconf")
            raise falcon.HTTPUnauthorized('typeconf parameter is wrong')

    @falcon.before(Authorize())
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        if self.conf.permition_changeallow():

            if str(req.params['conf']).lower() == "changeconfig":
                if 'namenet' in req.params:
                    if 'listip' in req.params:
                        if 'listnetmask' in req.params:
                            if 'gatway' in req.params:
                                if 'listdns':
                                    if config.config().ChangeSetting():
                                        if db.DatabaseSql().getPermition(self.username):
                                            resp.body = self.netmanager.change_config(req.params['namenet'],
                                                                                      req.params['listip'],
                                                                                      req.params['listnetmask'],
                                                                                      req.params['gatway'],
                                                                                      req.params['listdns'])
                                        else:
                                            resp.status = falcon.HTTP_400
                                            ManageLogging.LoggingManager().set_report("Error 400 : you are not permition")
                                            raise falcon.HTTPNotImplemented('You haven\'t Permition')
                                    else:
                                        resp.status = falcon.HTTP_400
                                        ManageLogging.LoggingManager().set_report("Error 400 : you are not permition")
                                        raise falcon.HTTPNotImplemented('You haven\'t Permition')
                                else:
                                    resp.status = falcon.HTTP_400
                                    ManageLogging.LoggingManager().set_report("Error 400 : listdns parameter is wrong")
                                    raise falcon.HTTPUnauthorized('listdns parameter is wrong')
                            else:
                                resp.status = falcon.HTTP_400
                                ManageLogging.LoggingManager().set_report("Error 400 : gatway parameter is wrong")
                                raise falcon.HTTPUnauthorized('gatway parameter is wrong')
                        else:
                            resp.status = falcon.HTTP_400
                            ManageLogging.LoggingManager().set_report("Error 400 : listnetmask parameter is wrong")
                            raise falcon.HTTPUnauthorized('listnetmask parameter is wrong')
                    else:
                        resp.status = falcon.HTTP_400
                        ManageLogging.LoggingManager().set_report("Error 400 : listip parameter is wrong")
                        raise falcon.HTTPUnauthorized('listip parameter is wrong')
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "addnet":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.addNetWork(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "removenet":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.removeNetWork(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "disablenet":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.disableinterface(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "enablenet":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.enableinterface(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "checkstate":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.checkstateinterface(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "checktypeip":
                if 'namenet' in req.params:
                    getmes = self.netmanager.checktypeip(req.params['namenet'])
                    resp.body = getmes
                    ManageLogging.LoggingManager().set_report(str(getmes))
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "changetodhcp":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.changetodhcpnetwork(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                    raise falcon.HTTPUnauthorized('namenet parameter is wrong')
            elif str(req.params['conf']).lower() == "listintr":
                if 'namenet' in req.params:
                    resp.body = self.netmanager.getlistinterface(req.params['namenet'])
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 400 : typeconf parameter is wrong")
                    raise falcon.HTTPUnauthorized('typeconf parameter is wrong')
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 400 : namenet parameter is wrong")
                raise falcon.HTTPUnauthorized('namenet parameter is wrong')

        else:
            raise falcon.HTTPUnauthorized('You are not allowed to try later')

class APISystemInfo:
    def __init__(self):
        self.sys = SystemInfo()

    @falcon.before(Authorize())
    def on_get(self, req, resp):
        if req.params == {}:
            resp.body = str(self.sys.my_systeminfo())
            ManageLogging.LoggingManager().set_report(str(self.sys.my_systeminfo()))


api = falcon.API()
api.add_route('/v1/systeminfo', APISystemInfo())
api.add_route('/v1/net', APINetWork())




if __name__ == "__main__":

    conf = ChangeSetting()

    from wsgiref import simple_server

    if conf.gettypeserver():
        httpd = simple_server.make_server('0.0.0.0', 5000, api)
        ManageLogging.LoggingManager().set_report("start API server 0.0.0.0:5000")
        httpd.serve_forever()
    else:
        httpd = simple_server.make_server('127.0.0.1', 5000, api)
        ManageLogging.LoggingManager().set_report("start API server 0.0.0.0:5000")
        httpd.serve_forever()

