import json, falcon

import netManager


class ObjRequstClass:

    def __init__(self):
        self.netviewer = netManager.NetWorkViwer()
        self.netManager = netManager.NetWorkManager()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if req.params == {}:
            resp.body = self.netviewer.getallinfointerface()

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

        if str(req.params['conf']).lower() == "ip":
            if 'namenet' in req.params:
                if 'newip' in req.params:
                    resp.body = self.netManager.changeIP(req.params['namenet'], req.params['newip'])

        elif str(req.params['conf']).lower() == "netmask":
            if 'namenet' in req.params:
                if 'newnetmask' in req.params:
                    if 'newip' in req.params:
                        resp.body = self.netManager.changeNetmask(req.params['namenet'], req.params['newnetmask'], req.params['newip'])

        elif str(req.params['conf']).lower() == "dns":
            if 'namenet' in req.params:
                if 'newdns' in req.params:
                    resp.body = self.netManager.changeDns(req.params['namenet'], req.params['newdns'])

        elif str(req.params['conf']).lower() == "defaultgetway":
            if 'namenet' in req.params:
                if 'newdefaultgetway' in req.params:
                    resp.body = self.netManager.changeDefaultGetway(req.params['namenet'], req.params['newdefaultgetway'])




api = falcon.API()
api.add_route('v1/network', ObjRequstClass())

# Start the API server programmatically
from wsgiref import simple_server

httpd = simple_server.make_server('127.0.0.1', 20001, api)
print("Starting server on http://localhost:8000")
httpd.serve_forever()