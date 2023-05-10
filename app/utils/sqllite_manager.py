import sqlite3
import ipaddress

from app.utils.config_manager import ChangeSetting

from app.models.permition import Permition


class DatabaseSql:
    def __init__(self):
        self.conf = ChangeSetting()
        db_path = self.conf.get_database_path()
        # self.con = sqlite3.connect('../../bashscript/database/userdatabase.db')
        self.con = sqlite3.connect(db_path)

        self.c = self.con.cursor()

    def InsertUsers(self, fullname, username, passwd, namepermition, ips):

        if self.check_exist_username(username):
            try:
                self.c.execute(
                    "INSERT INTO users (fullname ,username, passwd, type, iplimited) VALUES (\"" + fullname + "\",\"" + username + "\",\"" + passwd + "\", \"" + namepermition + "\",\"" + ips + "\")")
                self.con.commit()
                return "added user"
            except:
                return "don't added"
        else:
            return "user existed"

    def UpdateUsers(self, username, fullname, passwd, type, ips):

        self.c.execute(
            "UPDATE users SET name = \'" + fullname + "\', passwd = \'" + passwd + "\', type = \'" + type + "\', iplimited = \'" + ips + "\' WHERE username = \"" + username + "\"")
        return self.con.commit()

    def DeleteUsers(self, username):

        if not self.check_exist_username(username):
            try:
                self.c.execute("DELETE FROM users WHERE username = \"" + username + "\"")
                return self.con.commit()
            except:
                return "cannot remove "

        else:
            return "user existed"

    def get_insert_permission(self, namepermition, netread, netwrite, systeminfo):

        try:
            query = "INSERT INTO userpermition (type ,netread, netwrite, systemInfo) VALUES (?, ?, ?, ?)"
            self.c.execute(query, (namepermition, netread, netwrite, systeminfo))

            self.con.commit()
            return "added permition"
        except:
            return "don't permition"

    def delete_permition(self, namepermition):

        try:
            self.c.execute("DELETE FROM userpermition WHERE type = \"" + namepermition + "\"")
            return self.con.commit()
        except:
            return "cannot remove "

    def update_permition(self, namepermition, netread, netwrite, systeminfo):

        self.c.execute(
            "UPDATE users SET type = netread = " + netread + ", netwrite = " + netwrite + ", systemInfo = " + systeminfo + "\' WHERE type = \"" + namepermition + "\"")
        return self.con.commit()

    def get_alldata_users(self):
        try:
            self.c.execute("SELECT * FROM users")
            return self.c.fetchall()
        except:
            return "cannot getdata"

    def get_alldata_permition(self):
        try:
            self.c.execute("SELECT * FROM userpermition")
            return self.c.fetchall()
        except:
            return "cannot getdata"

    def check_exist_username(self, username):
        self.c.execute("SELECT * FROM users WHERE username = \"" + username + "\"")

        if self.c.fetchone() is None:
            return True
        else:
            return False

    def check_user_authentication(self, username, password):
        self.c.execute(
            "SELECT * FROM users WHERE username = \"" + username + "\" AND " + "passwd = \"" + password + "\"")

        if self.c.fetchone() is not None:
            return True
        else:
            return False

    def validation_ip_user(self, username, client_ip):

        try:
            self.c.execute("SELECT iplimited FROM users WHERE username = \"" + username + "\"")
            rows = self.c.fetchone()



        except ValueError as e:
            print(e)

        if rows[0] is not None:

            list_ip = str(rows).replace("(", "").replace("\'", "").replace(")", "").split(",")

            list_ip.pop(len(list_ip) - 1)

            _allowcheking = False

            for ip in list_ip:

                if _allowcheking == False:
                    network = ipaddress.IPv4Network(ipaddress.ip_interface(ip).network)
                    if ipaddress.ip_address(client_ip) in network:
                        _allowcheking = True

            return _allowcheking
        return True

    def get_permition_users(self, username):
        self.c.execute("SELECT type FROM users WHERE username = \"" + username + "\"")

        namepermition = self.c.fetchone()[0]

        self.c.execute("SELECT * FROM userpermition WHERE type = \"" + namepermition + "\"")

        result = self.c.fetchone()

        permition = Permition(result[0], result[1], result[2], result[3], result[4])

        return permition

# db = DatabaseSql()
#
# db.getPermition("erfan01", "netread")

# db.get_insert_permission("user", True, False, True)

# db.check_exist_username("erfan01")

# db.getData()
#
# db.createtable()
#
# db.validation_ip_user("erfan01", "10.42.0.182")
# db.Insert("erfan", "erfan01", "1234", "user", "10.42.0.182/24,192.168.2.3/16")
