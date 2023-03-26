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
            json_str += "\t\t\t  " + '"Dns": ' + '"' + self.getDns(i).replace("\n", "") + '"' + "\n" + "\t\t\t  },\n"
        json_str = json_str[:-2]
        json_str += "\n\t\t}"
        json_str += "\n}"
        return json_str

    def getIp(self, InterfaceName):
        ipNet = subprocess.check_output(['bash', 'getIp.sh', InterfaceName]).decode('utf-8')
        return ipNet

    def getState(self, InterfaceName):
        chkEnbl = subprocess.check_output(['bash', 'checkInterfaceEnable.sh', InterfaceName]).decode('utf-8')
        return chkEnbl

    def getDefaultgetway(self, InterfaceName):
        defaltGetway = subprocess.check_output(['bash', 'getDefaultgetway.sh', InterfaceName]).decode('utf-8')
        return defaltGetway

    def getNetmask(self, InterfaceName):
        Netmask = subprocess.check_output(['bash', 'getNetmask.sh', InterfaceName]).decode('utf-8')
        return Netmask

    def getDns(self, InterfaceName):
        Dns = subprocess.check_output(['bash', 'getDNS.sh', InterfaceName]).decode('utf-8')
        return Dns


class NetWorkManager:

    def __init__(self):
        self.netViewer = NetWorkViwer()

    def change_config(self, nameinterface, lip, lnetmask, gatway, ldns):
        script_path = "/home/os1/Desktop/falcon_https/falcon_https/changeconfignet/changeIP.sh"
        subprocess.run([script_path + " " + nameinterface + " " + lip + "" + lnetmask + "" + gatway + "" + ldns],
                       shell=True)


        if True:
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

    def my_systemindo(self):
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
        self.output_str += self.cpucoreinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"
        self.output_str += self.cpuinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"
        self.output_str += self.hardinfo()
        self.output_str = self.output_str[:len(self.output_str) - 1]
        self.output_str += "\n"


        self.output_str += "}"

        return str(self.output_str)

    def memoryinfo(self):
        meminfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/memory/memory_info.sh']).decode('utf-8')
        return meminfo

    def swapmemory(self):
        swpinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/memory/swap_info.sh']).decode('utf-8')
        return swpinfo

    def graphicinfo(self):
        grphinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/graphic/graphic_info.sh']).decode('utf-8')
        return grphinfo

    def cpucoreinfo(self):
        cpuinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/cpu/cpu_info.sh']).decode('utf-8')
        return cpuinfo

    def cpuinfo(self):
        cpuinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/cpu/usedCoreCpu.sh']).decode('utf-8')
        return cpuinfo

    def hardinfo(self):
        hardinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/harddisk/info_hard.sh']).decode('utf-8')
        return hardinfo


class ObjNetWork:

    def __init__(self):
        self.sys = SystemInfo()
        self.netviewer = NetWorkViwer()
        self.netmanager = NetWorkManager()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if req.params == {}:
             resp.body = str(self.sys.my_systemindo())
        elif str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getIp(req.params['namenet'])
        elif str(req.params['conf']).lower() == "state":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getState(req.params['namenet'])
        elif str(req.params['conf']).lower() == "defaultgetway":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDefaultgetway(req.params['namenet']).replace("\n", ",")
        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getNetmask(req.params['namenet'])
        elif str(req.params['conf']).lower() == "dns":
            if 'namenet' in req.params:
                resp.body = self.netviewer.getDns(req.params['namenet']).replace("\n", ",")


    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        if str(req.params['conf']).lower() == "changeconfig":
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
    httpd = simple_server.make_server('10.42.0.213', 5000, api)
    httpd.serve_forever()
