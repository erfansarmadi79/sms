# -*- coding: utf-8 -*-

import falcon
from app import log
import subprocess

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

    # def getState(self, InterfaceName):
    #     chkEnbl = subprocess.check_output(['bash', 'checkInterfaceEnable.sh', InterfaceName]).decode('utf-8')
    #     return chkEnbl

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
        netMask = subprocess.run(['bashscript/net/infonet/getNetmask.sh'+ " " +InterfaceName], capture_output=True, text=True, shell=True)

        exitCodeNetmask = netMask.returncode

        if exitCodeNetmask == 0:

            return netMask.stdout

        elif exitCodeNetmask == 2:
            return "/home/os1/Desktop/1402/scout-server/app/bashscript/net/infonet/getDNS.sh"
        else:
            return "{" + "\"error\":" + "\"!!!cannot get NetMask information!!!\"" + "}"

    def getDns(self):
        Dns = subprocess.run(['bashscript/net/infonet/getDNS.sh'], capture_output=True, text=True, shell=True)

        exitCodeDns = Dns.returncode

        if exitCodeDns == 0:
            return Dns.stdout
        elif exitCodeDns == 2:
            return "Interface does not exist."
        else:
            return "Dns does not exist."


class NetWorkManager:

    def __init__(self):
        self.netViewer = NetWorkViwer()

    def change_config(self, nameinterface, lip, lnetmask, gatway, ldns):
        script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeIP.sh"
        subprocess.run([script_path + " " + nameinterface + " " + lip + "" + lnetmask + "" + gatway + "" + ldns],
                       shell=True)

        if False:
            return "config changed"
        else:
            return "config dont changed"

    def disableinterface(self, interfacename):
        pass

    def enableinterface(self, interface):
        pass

    def disconnectinterface(self, interface):
        pass

    def connectinterface(self, interface):
        pass

    # def changeIP(self, nameinterface, ip):
    #     script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeIP.sh"
    #     subprocess.run([script_path+" "+ip+" "+nameinterface], shell=True)
    #     ## check ip changed
    #     getip = self.netViewer.getIp(nameinterface).replace("\n", "")
    #     if str(getip) == ip:
    #         return "ip changed"
    #     else:
    #         return "ip not changed"

    # def changeNetmask(self, nameinterface, netmask, ip=""):
    #
    #     script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeNetmask.sh"
    #
    #     if ip == "":
    #         getip = self.netViewer.getIp(nameinterface).replace("\n", "")
    #         subprocess.run([script_path+" "+nameinterface+" "+str(getip)+" "+netmask], shell=True)
    #
    #     else:
    #         subprocess.run([script_path+" "+nameinterface+" "+ip+" "+netmask], shell=True)
    #
    #
    #     ##check done changed Netmask
    #     getnetmask = self.netViewer.getNetmask(nameinterface).replace("\n", "")
    #     if str(getnetmask) == netmask:
    #         return "Netmask changed"
    #     else:
    #         return "Netmask not changed"

    # def changeDns(self, nameinterface,dnses):
    #     script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeDns.sh"
    #     subprocess.run([script_path + " " + nameinterface + " " + dnses], shell=True)
    #
    # def changeDefaultGetway(self, nameinterface, defway):
    #     script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeDefaultGetway.sh"
    #     subprocess.run([script_path + " " + nameinterface + " " + defway], shell=True)True


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



class ObjNetWork:

    def __init__(self):
        self.sys = SystemInfo()
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if req.params == {}:
             resp.body = str(self.sys.my_systeminfo())
        elif str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getIp(req.params['namenet'])
        elif str(req.params['conf']).lower() == "state":
            if 'namenet' in req.params:
                print ("")
                #resp.body = self.netviewer.getState(req.params['namenet'])
        elif str(req.params['conf']).lower() == "defaultgetway":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDefaultgetway(req.params['namenet']).replace("\n", "")
        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getNetmask(req.params['namenet'])
        elif str(req.params['conf']).lower() == "dns":
            #if 'namenet' in req.params:
                #resp.body = self.netviewer.getDns(req.params['namenet']).replace("\n", ",")
            resp.body = self.netviewer.getDns().replace("\n", ",")


    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "changeconfigInterface":
            if 'namenet' in req.params:
                if 'listip' in req.params:
                    if 'listnetmask' in req.params:
                        if 'gatway' in req.params:
                            if 'listdns':
                                  resp.body = self.netmanager.change_config(req.params['namenet'], req.params['newip'])

    #     elif str(req.params['conf']).lower() == "netmask":
    #         if 'namenet' in req.params:
    #             if 'newnetmask' in req.params:
    #                 if 'newip' in req.params:
    #                     resp.body = self.netManager.changeNetmask(req.params['namenet'], req.params['newnetmask'], req.params['newip'])
    #
    #     elif str(req.params['conf']).lower() == "dns":
    #         if 'namenet' in req.params:
    #             if 'newdns' in req.params:
    #                 resp.body = self.netManager.changeDns(req.params['namenet'], req.params['newdns'])
    #
    #     elif str(req.params['conf']).lower() == "defaultgetway":
    #         if 'namenet' in req.params:
    #             if 'newdefaultgetway' in req.params:
    #                 resp.body = self.netManager.changeDefaultGetway(req.params['namenet'], req.params['newdefaultgetway'])


api = falcon.API()
api.add_route('/', ObjNetWork())
#api.add_route('/net', ObjRequstClass())


if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 5000, api)
    httpd.serve_forever()
