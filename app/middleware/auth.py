import falcon
import base64
import ipaddress

import app.utils.sqllite_manager as sql_data

class Authorize(object):

    def __init__(self):

        self.sql_db = sql_data.DatabaseSql()

    def auth_basic(self, username, password, client_ip):

        if self.sql_db.check_exist_username(username) != True:
            if self.sql_db.validation_ip_user(username, client_ip):
                if self.sql_db.check_user_authentication(username, password):
                    print('your have access - wellcom')
                else:
                    raise falcon.HTTPNotImplemented('Unauthorized', 'Your access is not allowed ')
            else:
                raise falcon.HTTPUnauthorized('Invalid client IP', 'Please access the API from an allowed IP address')
        else:
            raise falcon.HTTPNotImplemented('Unauthorized', 'Your access does not exist ')

    def __call__(self, req, resp, resource, params):

        print('before trigger - class: Authorize')

        client_ip = req.remote_addr

        if req.auth is not None:

            auth_exp = req.auth.split(' ') if not None else (None, None,)

            if auth_exp[0].lower() == 'basic':
                auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
                username = auth[0]
                password = auth[1]
                self.auth_basic(username, password, client_ip)
            else:
                raise falcon.HTTPNotImplemented('Not Implemented', 'You don\'t use the right auth method')
        else:
            raise falcon.HTTPNotImplemented('Enter Username and Password')

# class ObjResource:
#     @falcon.before(Authorize())
#     def on_get(self, req, resp):
#         print('on_get trigger')
#
#         output = {
#             'method':'get'
#         }
#
#         resp.media = output
#
# api = falcon.API()
#
#
# api.add_route('/test', ObjResource())
#
#
# if __name__ == "__main__":
#     from wsgiref import simple_server
#     httpd = simple_server.make_server('192.168.111.135', 5000, api)
#     httpd.serve_forever()