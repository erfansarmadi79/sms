# -*- coding: utf-8 -*-
import base64

import falcon

from app import log
import subprocess

from auth import Authorize

from app import ManageLogging

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
        meminfo = subprocess.run(['./sudo_runfile memory_info'], capture_output=True, text=True, shell=True)

        exitCodeMemory = meminfo.returncode

        if exitCodeMemory == 0:
            ManageLogging.LoggingManager().set_report(meminfo.stdout)
            return meminfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get memory information")
            return "\"memory\":"+"\"!!!cannot get memory information\"!!!"

    def swapmemory(self):
        swpinfo = subprocess.run(['./runfile memory_swapinfo'], capture_output=True, text=True, shell=True)

        exitCodeswapinfo = swpinfo.returncode

        if exitCodeswapinfo == 0:
            ManageLogging.LoggingManager().set_report(swpinfo.stdout)
            return swpinfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get swap information")
            return "\"swap\":" + "\"!!!cannot get swap information\"!!!"

    def graphicinfo(self):
        grphinfo = subprocess.run(['./runfile graphic_info'], capture_output=True, text=True, shell=True)

        exitCodeGraphic = grphinfo.returncode

        if exitCodeGraphic == 0:
            ManageLogging.LoggingManager().set_report(grphinfo.stdout)
            return grphinfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get graphic information")
            return "\"graphic\":" + "\"!!!cannot get graphic information\"!!!"

    def cpuInfo(self):
        cpuinfo = subprocess.run(
            ['./runfile cpu_info.sh'], capture_output=True, text=True, shell=True)

        exitCodeCpu = cpuinfo.returncode

        if exitCodeCpu == 0:
            ManageLogging.LoggingManager().set_report(cpuinfo.stdout)
            return cpuinfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get Cpu information")
            return "\"CpuInfo\":" + "\"!!!cannot get Cpu information\"!!!"

    def cpucoreInfo(self):
        cpucoreinfo = subprocess.run(
            ['./runfile cpu_usedcore'], capture_output=True, text=True, shell=True)

        exitCodeCpuCore = cpucoreinfo.returncode

        if exitCodeCpuCore == 0:
            ManageLogging.LoggingManager().set_report(cpucoreinfo.stdout)
            return cpucoreinfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get CpuCore information")
            return "\"CpuCoreInfo\":" + "\"!!!cannot get CpuCore information\"!!!"

    def cpu_temp(self):
        cputemp = subprocess.run(
            ['./runfile cpu_temp'], capture_output=True, text=True, shell=True)

        exitCodeCpuCore = cputemp.returncode

        if exitCodeCpuCore == 0:
            ManageLogging.LoggingManager().set_report(cputemp.stdout)
            return cputemp.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get CpuTemp information")
            return "\"CpuTemp\":" + "\"!!!cannot get CpuTemp information\"!!!"

    def hardinfo(self):
        hardinfo = subprocess.run(['./runfile hard_info'], capture_output=True, text=True, shell=True)

        exitCodeHard = hardinfo.returncode

        if exitCodeHard == 0:
            ManageLogging.LoggingManager().set_report(hardinfo.stdout)
            return hardinfo.stdout
        else:
            ManageLogging.LoggingManager().set_report("cannot get HardDisk information")
            return "\"Hard_disk\":" + "\"!!!cannot get HardDisk information\"!!!"




class NetWorkViwer:


    def __int__(self):
        self.Runfile = "bashscript/runfile"
        self.sudoRunfile = "bashscript/sudo_runfile"

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


        ipNet = subprocess.run(["./runfile net_getip"+ " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeipnet = ipNet.returncode

        if exitCodeipnet == 0:
            ManageLogging.LoggingManager().set_report(ipNet.stdout)
            return ipNet.stdout
        elif exitCodeipnet == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get ip information")
            return "{"+"\"error\":"+"\"!!!cannot get ip information!!!\""+"}"

    def getDefaultgetway(self, InterfaceName):
        defaltGetway = subprocess.run(['./runfile net_getDefaultgetway'+ " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodedefgetway = defaltGetway.returncode

        if exitCodedefgetway == 0:
            ManageLogging.LoggingManager().set_report(defaltGetway.stdout)
            return defaltGetway.stdout
        elif exitCodedefgetway == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get Defaultgetway information")
            return "{" + "\"error\":" + "\"!!!cannot get Defaultgetway information!!!\"" + "}"


    def getNetmask(self, InterfaceName):
        netMask = subprocess.run(['./runfile net_getNetmask' + " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeNetmask = netMask.returncode

        if exitCodeNetmask == 0:
            ManageLogging.LoggingManager().set_report(netMask.stdout)

            return netMask.stdout

        elif exitCodeNetmask == 2:
            ManageLogging.LoggingManager().set_report("Interface does not exist.")
            return "Interface does not exist."
        else:
            ManageLogging.LoggingManager().set_report("cannot get NetMask information.")
            return "{" + "\"error\":" + "\"!!!cannot get NetMask information!!!\"" + "}"

    def getDns(self, InterfaceName):
        Dns = subprocess.run(['./runfile net_getDNS' + " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeDns = Dns.returncode

        if exitCodeDns == 0:
            ManageLogging.LoggingManager().set_report(Dns.stdout)
            return Dns.stdout
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
        script_path = "./sudo_runfile net_ip_cahnge"
        changeConfig = subprocess.run([script_path + " " + "\"" + nameinterface + "\"" + " " + "\"" + lip + "\"" + " " + "\"" + lnetmask + "\"" + " " + "\"" + gatway + "\"" + " " + "\"" + ldns + "\""], capture_output=True, text=True, shell=True)

        exitCodechangeConfig = changeConfig.returncode

        if exitCodechangeConfig == 0:
            return "set config"
            ManageLogging.LoggingManager().set_report("change sucess NetWorkinterface ("+nameinterface+") ips : "+lip+"netmasks : "+lnetmask+"gatway : "+gatway+"dnss : "+ldns)
        elif exitCodechangeConfig == 2:
            ManageLogging.LoggingManager().set_report(changeConfig.stdout)
            return changeConfig.stdout
        elif exitCodechangeConfig == 3:
            ManageLogging.LoggingManager().set_report(changeConfig.stdout)
            return changeConfig.stdout
        elif exitCodechangeConfig == 4:
            ManageLogging.LoggingManager().set_report(changeConfig.stdout)
            return changeConfig.stdout
        elif exitCodechangeConfig == 5:
            ManageLogging.LoggingManager().set_report(changeConfig.stdout)
            return changeConfig.stdout
        elif exitCodechangeConfig == 6:
            ManageLogging.LoggingManager().set_report(changeConfig.stdout)
            return changeConfig.stdout
        else:
            ManageLogging.LoggingManager().set_report("do not set config")
            return "do not set config"

    def addNetWork(self, nameinterface):
        script_path = "./sudo_runfile net_addnetwork"
        addnetwork = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodeaddnetwork= addnetwork.returncode

        if exitCodeaddnetwork == 0:
            ManageLogging.LoggingManager().set_report("added netnetwork:" + nameinterface)
            return "added netnetwork"
        elif exitCodeaddnetwork == 2:
            ManageLogging.LoggingManager().set_report(addnetwork.stdout)
            return addnetwork.stdout
        else:
            ManageLogging.LoggingManager().set_report("do not add network")
            return "do not add network"

    def removeNetWork(self, nameinterface):
        script_path = "./sudo_runfile net_removeNetwork"
        removenetwork = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCoderemovenetwork = removenetwork.returncode

        if exitCoderemovenetwork == 0:
            ManageLogging.LoggingManager().set_report("remove netnetwork:" + nameinterface)
            return "removed netnetwork"
        elif exitCoderemovenetwork == 2:
            ManageLogging.LoggingManager().set_report(removenetwork.stdout)
            return removenetwork.stdout
        else:
            ManageLogging.LoggingManager().set_report("do not remove network")
            return "do not remove network"

    def disableinterface(self, nameinterface):
        script_path = "./sudo_runfile net_disablenet"
        disableinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                       text=True, shell=True)

        exitCodedisableinterface = disableinterface.returncode

        if exitCodedisableinterface == 0:
            ManageLogging.LoggingManager().set_report("disable interface :" + nameinterface)
            return "disable interface"
        elif exitCodedisableinterface == 2:
            ManageLogging.LoggingManager().set_report(disableinterface.stdout)
            return disableinterface.stdout
        else:
            ManageLogging.LoggingManager().set_report("do not disable interface")
            return "do not disable interface"

    def enableinterface(self, nameinterface):
        script_path = "./sudo_runfile net_enablenet"
        enableinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                          text=True, shell=True)

        exitCodeenableinterface = enableinterface.returncode

        if exitCodeenableinterface == 0:
            ManageLogging.LoggingManager().set_report("enabled interface :" + nameinterface)
            return "enabled netnetwork"
        elif exitCodeenableinterface == 2:
            ManageLogging.LoggingManager().set_report(enableinterface.stdout)
            return enableinterface.stdout
        else:
            ManageLogging.LoggingManager().set_report("do not enable interface")
            return "do not enable interface"

    def checktypeip(self, nameinterface):
        script_path = "./runfile net_checkTypeIp"
        checktypeinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                         text=True, shell=True)

        exitCodechecktypeinterface = checktypeinterface.returncode

        if exitCodechecktypeinterface == 0:
            ManageLogging.LoggingManager().set_report(checktypeinterface.stdout)
            return checktypeinterface.stdout
        elif exitCodechecktypeinterface == 2:
            ManageLogging.LoggingManager().set_report(checktypeinterface.stdout)
            return checktypeinterface.stdout
        else:
            ManageLogging.LoggingManager().set_report("can not checked interface")
            return "can not checked interface"

    def changetodhcpnetwork(self, nameinterface):
        script_path = "./runfile net_changestatic_dhcp"
        changetodhcp = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodechangetodhcp = changetodhcp.returncode

        if exitCodechangetodhcp == 0:
            ManageLogging.LoggingManager().set_report("changed to dhcp interface : " + nameinterface)
            return "changed to dhcp"
        elif exitCodechangetodhcp == 2:
            ManageLogging.LoggingManager().set_report(changetodhcp.stdout)
            return changetodhcp.stdout
        else:
            ManageLogging.LoggingManager().set_report("can not change to dhcp")
            return "can not change to dhcp"
    def checkstateinterface(self, nameinterface):
        script_path = "./runfile net_checkstat"
        checkstate = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True,
                                 shell=True)

        exitCodecheckstate = checkstate.returncode

        if exitCodecheckstate == 0:
            ManageLogging.LoggingManager().set_report(checkstate.stdout)
            return checkstate.stdout
        elif exitCodecheckstate == 2:
            ManageLogging.LoggingManager().set_report(checkstate.stdout)
            return checkstate.stdout
        else:
            ManageLogging.LoggingManager().set_report("can not checking state")
            return "can not checking state"

    def getlistinterface(self, nameinterface):
        script_path = "./runfile net_getlistinterface"
        getlist = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodegetlist = getlist.returncode

        if exitCodegetlist == 0:
            ManageLogging.LoggingManager().set_report(getlist.stdout)
            return getlist.stdout
        elif exitCodegetlist == 2:
            ManageLogging.LoggingManager().set_report(getlist.stdout)
            return getlist.stdout
        else:
            ManageLogging.LoggingManager().set_report("can not get list")
            return "can not get list"



class APINetWork:

    def __init__(self):
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()

    @falcon.before(Authorize())
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getIp(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "state":
            if 'namenet' in req.params:
                print("")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
                #resp.body = self.netviewer.getState(req.params['namenet'])
        elif str(req.params['conf']).lower() == "defaultgetway":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDefaultgetway(req.params['namenet']).replace("\n", "")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getNetmask(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "dns":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDns(req.params['namenet']).replace("\n", ",")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
            # resp.body = self.netviewer.getDns().replace("\n", ",")
        else:
            resp.status = falcon.HTTP_400
            ManageLogging.LoggingManager().set_report("Error 404 : not params typeconf")

    @falcon.before(Authorize())
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        auth_exp = req.auth.split(' ') if not None else (None, None,)

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            self.username = auth[0]

        if str(req.params['conf']).lower() == "changeconfig":
            if 'namenet' in req.params:
                if 'listip' in req.params:
                    if 'listnetmask' in req.params:
                        if 'gatway' in req.params:
                            if 'listdns':
                                if config.config().ChangeSetting():
                                    if db.DatabaseSql().getPermition(self.username):
                                        resp.body = self.netmanager.change_config(req.params['namenet'], req.params['listip'], req.params['listnetmask'], req.params['gatway'], req.params['listdns'])
                                    else:
                                        raise falcon.HTTPNotImplemented('Not Permition',
                                                                        'You haven\'t Permition')
                                else:
                                    raise falcon.HTTPNotImplemented('Not Permition',
                                                                    'You haven\'t Permition')
                            else:
                                resp.status = falcon.HTTP_400
                                ManageLogging.LoggingManager().set_report("Error 404 : not params listdns")
                        else:
                            resp.status = falcon.HTTP_400
                            ManageLogging.LoggingManager().set_report("Error 404 : not params gatway")
                    else:
                        resp.status = falcon.HTTP_400
                        ManageLogging.LoggingManager().set_report("Error 404 : not params listnetmask")
                else:
                    resp.status = falcon.HTTP_400
                    ManageLogging.LoggingManager().set_report("Error 404 : not params listip")
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "addnet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.addNetWork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "removenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.removeNetWork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "disablenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.disableinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "enablenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.enableinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "checkstate":
            if 'namenet' in req.params:
                resp.body = self.netmanager.checkstateinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "checktypeip":
            if 'namenet' in req.params:
                getmes = self.netmanager.checktypeip(req.params['namenet'])
                resp.body = getmes
                ManageLogging.LoggingManager().set_report(str(getmes))
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "changetodhcp":
            if 'namenet' in req.params:
                resp.body = self.netmanager.changetodhcpnetwork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        elif str(req.params['conf']).lower() == "listintr":
            if 'namenet' in req.params:
                resp.body = self.netmanager.getlistinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
                ManageLogging.LoggingManager().set_report("Error 404 : not params namenet")
        else:
            resp.status = falcon.HTTP_400
            ManageLogging.LoggingManager().set_report("Error 404 : not params typeconf")

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
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 5000, api)
    ManageLogging.LoggingManager().set_report("start API server 192.168.67.153:5000")
    httpd.serve_forever()

