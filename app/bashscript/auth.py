import falcon
import base64

import database.sqllite_manager as sql_data

class Authorize(object):

    def __init__(self):

        self.sql_db = sql_data.DatabaseSql()

        self.user_accounts = {
            'test': 'mypassword'
        }

    def auth_basic(self, username, password, client_ip):

        if self.sql_db.validationIpUser(username, client_ip):
            if self.sql_db.UserAuthantication(username, password):
                print('your have access - welcom')
            else:
                raise falcon.HTTPNotImplemented('Unauthorized', 'Your access is not allowed ')
        else:
            raise falcon.HTTPUnauthorized('Invalid client IP', 'Please access the API from an allowed IP address')

    def __call__(self, req, resp, resource, params):
        ALLOWED_IPS = ['127.0.0.1', '192.168.0.1', '192.168.111.2', '192.168.111.1']
        print('before trigger - class: Authorize')

        client_ip = req.remote_addr

        auth_exp = req.auth.split(' ') if not None else (None, None, )

        if auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            username = auth[0]
            password = auth[1]
            self.auth_basic(username, password, client_ip)
        else:
            raise falcon.HTTPNotImplemented('Not Implemented', 'You don\'t use the right auth method')

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