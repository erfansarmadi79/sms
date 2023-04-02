# -*- coding: utf-8 -*-
import time

import falcon
from app import log
import subprocess

from app import ManageLogging

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

ManageLogging.LoggingManager().set_report("rrrr")

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
        self.output_str += "\n"
        self.output_str += self.cpucoreInfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"
        self.output_str += self.hardinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"


        self.output_str += "}"

        return str(self.output_str)

    def memoryinfo(self):
        meminfo = subprocess.run(['bashscript/memory/memory_info.sh'], capture_output=True, text=True, shell=True)

        exitCodeMemory = meminfo.returncode

        if exitCodeMemory == 0:
            return meminfo.stdout
        else:
            return "\"memory\":"+"\"!!!cannot get memory information\"!!!"

    def swapmemory(self):
        swpinfo = subprocess.run(['bashscript/memory/swap_info.sh'], capture_output=True, text=True, shell=True)

        exitCodeswapinfo = swpinfo.returncode

        if exitCodeswapinfo == 0:
            return swpinfo.stdout
        else:
            return "\"swap\":" + "\"!!!cannot get swap information\"!!!"

    def graphicinfo(self):
        grphinfo = subprocess.run(['bashscript/graphic/graphic_info.sh'], capture_output=True, text=True, shell=True)

        exitCodeGraphic = grphinfo.returncode

        if exitCodeGraphic == 0:
            return grphinfo.stdout
        else:
            return "\"graphic\":" + "\"!!!cannot get graphic information\"!!!"

    def cpuInfo(self):
        cpuinfo = subprocess.run(
            ['bashscript/cpu/cpu_info.sh'], capture_output=True, text=True, shell=True)

        exitCodeCpu = cpuinfo.returncode

        if exitCodeCpu == 0:
            return cpuinfo.stdout
        else:
            return "\"CpuInfo\":" + "\"!!!cannot get Cpu information\"!!!"

    def cpucoreInfo(self):
        cpucoreinfo = subprocess.run(
            ['bashscript/cpu/usedCoreCpu.sh'], capture_output=True, text=True, shell=True)

        exitCodeCpuCore = cpucoreinfo.returncode

        if exitCodeCpuCore == 0:
            return cpucoreinfo.stdout
        else:
            return "\"CpuCoreInfo\":" + "\"!!!cannot get CpuCore information\"!!!"

    def hardinfo(self):
        hardinfo = subprocess.run(['bashscript/harddisk/info_hard.sh'], capture_output=True, text=True, shell=True)

        exitCodeHard = hardinfo.returncode

        if exitCodeHard == 0:
            return hardinfo.stdout
        else:
            return "\"Hard_disk\":" + "\"!!!cannot get HardDisk information\"!!!"

class NetWorkViwer:

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


        ipNet = subprocess.run(['bashscript/net/infonet/getip.sh'+ " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeipnet = ipNet.returncode

        if exitCodeipnet == 0:
            return ipNet.stdout
        elif exitCodeipnet == 2:
            return "Interface does not exist."
        else:
            return "{"+"\"error\":"+"\"!!!cannot get ip information!!!\""+"}"

    def getDefaultgetway(self, InterfaceName):
        defaltGetway = subprocess.run(['bashscript/net/infonet/getDefaultgetway.sh'+ " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodedefgetway = defaltGetway.returncode

        if exitCodedefgetway == 0:
            return defaltGetway.stdout
        elif exitCodedefgetway == 2:
            return "Interface does not exist."
        else:
            return "{" + "\"error\":" + "\"!!!cannot get Defaultgetway information!!!\"" + "}"


    def getNetmask(self, InterfaceName):
        netMask = subprocess.run(['bashscript/net/infonet/getNetmask.sh' + " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeNetmask = netMask.returncode

        if exitCodeNetmask == 0:

            return netMask.stdout

        elif exitCodeNetmask == 2:
            return "/home/os1/Desktop/1402/scout-server/app/bashscript/net/infonet/getDNS.sh"
        else:
            return "{" + "\"error\":" + "\"!!!cannot get NetMask information!!!\"" + "}"

    def getDns(self, InterfaceName):
        Dns = subprocess.run(['bashscript/net/infonet/getDNS.sh' + " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeDns = Dns.returncode

        if exitCodeDns == 0:
            return Dns.stdout
        elif exitCodeDns == 2:
            return "Interface does not exist."
        elif exitCodeDns == 3:
            return "DNS is not configured."
        else:
            return "Dns does not exist."

class NetWorkManager:

    def __init__(self):
        self.netViewer = NetWorkViwer()

    def change_config(self, nameinterface, lip, lnetmask, gatway, ldns):
        script_path = "bashscript/net/ip_cahnge.sh"
        changeConfig = subprocess.run([script_path + " " + "\"" + nameinterface + "\"" + " " + "\"" + lip + "\"" + " " + "\"" + lnetmask + "\"" + " " + "\"" + gatway + "\"" + " " + "\"" + ldns + "\""], capture_output=True, text=True, shell=True)

        exitCodechangeConfig = changeConfig.returncode

        if exitCodechangeConfig == 0:
            return "set config"
        elif exitCodechangeConfig == 2:
            return changeConfig.stdout
        elif exitCodechangeConfig == 3:
            return changeConfig.stdout
        elif exitCodechangeConfig == 4:
            return changeConfig.stdout
        elif exitCodechangeConfig == 5:
            return changeConfig.stdout
        elif exitCodechangeConfig == 6:
            return changeConfig.stdout
        else:
            return "do not set config"

    def addNetWork(self, nameinterface):
        script_path = "bashscript/net/addnetwork.sh"
        addnetwork = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodeaddnetwork= addnetwork.returncode

        if exitCodeaddnetwork == 0:
            return "added netnetwork"
        elif exitCodeaddnetwork == 2:
            return addnetwork.stdout
        else:
            return "do not add network"

    def removeNetWork(self, nameinterface):
        script_path = "bashscript/net/removeNetwork.sh"
        removenetwork = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCoderemovenetwork = removenetwork.returncode

        if exitCoderemovenetwork == 0:
            return "removed netnetwork"
        elif exitCoderemovenetwork == 2:
            return removenetwork.stdout
        else:
            return "do not remove network"

    def disableinterface(self, nameinterface):
        script_path = "bashscript/net/disablenet.sh"
        disableinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                       text=True, shell=True)

        exitCodedisableinterface = disableinterface.returncode

        if exitCodedisableinterface == 0:
            return "disable interface"
        elif exitCodedisableinterface == 2:
            return disableinterface.stdout
        else:
            return "do not disable interface"

    def enableinterface(self, nameinterface):
        script_path = "bashscript/net/enablenet.sh"
        enableinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                          text=True, shell=True)

        exitCodeenableinterface = enableinterface.returncode

        if exitCodeenableinterface == 0:
            return "enabled netnetwork"
        elif exitCodeenableinterface == 2:
            return enableinterface.stdout
        else:
            return "do not enable interface"

    def checktypeip(self, nameinterface):
        script_path = "bashscript/net/checkTypeIp.sh"
        checktypeinterface = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True,
                                         text=True, shell=True)

        exitCodechecktypeinterface = checktypeinterface.returncode

        if exitCodechecktypeinterface == 0:
            return checktypeinterface.stdout
        elif exitCodechecktypeinterface == 2:
            return checktypeinterface.stdout
        else:
            return "can not checked interface"

    def changetodhcpnetwork(self, nameinterface):
        script_path = "bashscript/net/netstatic_dhcp.sh"
        changetodhcp = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodechangetodhcp = changetodhcp.returncode

        if exitCodechangetodhcp == 0:
            return "changed to dhcp"
        elif exitCodechangetodhcp == 2:
            return changetodhcp.stdout
        else:
            return "can not change to dhcp"
    def checkstateinterface(self, nameinterface):
        script_path = "bashscript/net/checkstat.sh"
        checkstate = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True,
                                 shell=True)

        exitCodecheckstate = checkstate.returncode

        if exitCodecheckstate == 0:
            return checkstate.stdout
        elif exitCodecheckstate == 2:
            return checkstate.stdout
        else:
            return "can not checking state"

    def getlistinterface(self, nameinterface):
        script_path = "bashscript/net/getlistinterface.sh"
        getlist = subprocess.run([script_path + " " + "\"" + nameinterface + "\""], capture_output=True, text=True, shell=True)

        exitCodegetlist = getlist.returncode

        if exitCodegetlist == 0:
            return getlist.stdout
        elif exitCodegetlist == 2:
            return getlist.stdout
        else:
            return "can not get list"

class APINetWork:

    def __init__(self):
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getIp(req.params['namenet'])
        elif str(req.params['conf']).lower() == "state":
            if 'namenet' in req.params:
                print("")
                #resp.body = self.netviewer.getState(req.params['namenet'])
        elif str(req.params['conf']).lower() == "defaultgetway":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDefaultgetway(req.params['namenet']).replace("\n", "")
        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getNetmask(req.params['namenet'])
        elif str(req.params['conf']).lower() == "dns":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDns(req.params['namenet']).replace("\n", ",")
            # resp.body = self.netviewer.getDns().replace("\n", ",")
        else:
            resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "changeconfig":
            if 'namenet' in req.params:
                if 'listip' in req.params:
                    if 'listnetmask' in req.params:
                        if 'gatway' in req.params:
                            if 'listdns':
                                resp.body = self.netmanager.change_config(req.params['namenet'], req.params['listip'], req.params['listnetmask'], req.params['gatway'], req.params['listdns'])
                            else:
                                resp.status = falcon.HTTP_400
                        else:
                            resp.status = falcon.HTTP_400
                    else:
                        resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_400
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "addnet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.addNetWork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "removenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.removeNetWork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "disablenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.disableinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "enablenet":
            if 'namenet' in req.params:
                resp.body = self.netmanager.enableinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "checkstate":
            if 'namenet' in req.params:
                resp.body = self.netmanager.checkstateinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "checktypeip":
            if 'namenet' in req.params:
                getmes = self.netmanager.checktypeip(req.params['namenet'])
                resp.body = getmes
                ManageLogging.LoggingManager().set_report(str(getmes))
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "changetodhcp":
            if 'namenet' in req.params:
                resp.body = self.netmanager.changetodhcpnetwork(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        elif str(req.params['conf']).lower() == "listintr":
            if 'namenet' in req.params:
                resp.body = self.netmanager.getlistinterface(req.params['namenet'])
            else:
                resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_400

class APISystemInfo:
    def __init__(self):
        self.sys = SystemInfo()
    def on_get(self, req, resp):
        if req.params == {}:
             resp.body = str(self.sys.my_systeminfo())


api = falcon.API()
api.add_route('/v1/systeminfo', APISystemInfo())
api.add_route('/v1/net', APINetWork())




if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('192.168.67.153', 5000, api)
    ManageLogging.LoggingManager().set_report("start API server 192.168.67.153")
    httpd.serve_forever()

