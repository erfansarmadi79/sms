import subprocess


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


        self.output_str += "}"

        return str(self.output_str)

    def memoryinfo(self):
        meminfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/memory/smsmemory_info.sh']).decode(
            'utf-8')
        return meminfo

    def swapmemory(self):
        swpinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/memory/swap_info.sh']).decode('utf-8')
        return swpinfo

    def graphicinfo(self):
        grphinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/graphic/smsgraphic_info.sh']).decode('utf-8')
        return grphinfo

    def cpucoreinfo(self):
        cpuinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/cpu/smscpu_info.sh']).decode('utf-8')
        return cpuinfo

    def cpuinfo(self):
        cpuinfo = subprocess.check_output(
            ['bash', '/home/admin/scout-server/app/bashscript/cpu/usedCoreCpu.sh']).decode('utf-8')
        return cpuinfo


