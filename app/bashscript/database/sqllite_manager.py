import sqlite3
import ipaddress

from app.models.Permition import Permition


class DatabaseSql:
    def __init__(self):
        self.con = sqlite3.connect('/home/erfan/Desktop/sms/app/bashscript/database/userdatabase.db')

        self.c = self.con.cursor()

    def InsertUsers(self, fullname, username, passwd, namepermition, ips):

        if self.checkUsername(username):
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

        if self.checkUsername(username) == False:
            try:
                self.c.execute("DELETE FROM users WHERE username = \"" + username + "\"")
                return self.con.commit()
            except:
                return "cannot remove "

        else:
            return "user existed"

    def InsertPermition(self, namepermition, netread, netwrite, systeminfo):

            try:
                # self.c.execute(
                #     #"INSERT INTO userpermition (type ,netread, netwrite, systemInfo) VALUES (\"" + namepermition + "\",\"" + username + "\",\"" + passwd + "\", \"" + type + "\",\"" + ips + "\")")
                #     "INSERT INTO userpermition (type ,netread, netwrite, systemInfo) VALUES (" + namepermition + "," + netread + "," + netwrite + ", " + systeminfo + ")")

                query = "INSERT INTO userpermition (type ,netread, netwrite, systemInfo) VALUES (?, ?, ?, ?)"
                self.c.execute(query, (namepermition, netread, netwrite, systeminfo))

                self.con.commit()
                return "added permition"
            except:
                return "don't permition"

    def DeletePermition(self, namepermition):

            try:
                self.c.execute("DELETE FROM userpermition WHERE type = \"" + namepermition + "\"")
                return self.con.commit()
            except:
                return "cannot remove "

    def UpdatePermition(self, namepermition, netread, netwrite, systeminfo):

        self.c.execute(
            "UPDATE users SET type = netread = " + netread + ", netwrite = " + netwrite + ", systemInfo = " + systeminfo + "\' WHERE type = \"" + namepermition + "\"")
        return self.con.commit()

    def getAllDataUsers(self):
        try:
            self.c.execute("SELECT * FROM users")
            return self.c.fetchall()
        except:
            return "cannot getdata"

    def getAllDataPermition(self):
        try:
            self.c.execute("SELECT * FROM userpermition")
            return self.c.fetchall()
        except:
            return "cannot getdata"


    def checkUsername(self, username):
        self.c.execute("SELECT * FROM users WHERE username = \"" + username + "\"")

        if self.c.fetchone() is None:
            return True
        else:
            return False

    def UserAuthantication(self, username, password):
        self.c.execute(
            "SELECT * FROM users WHERE username = \"" + username + "\" AND " + "passwd = \"" + password + "\"")

        if self.c.fetchone() is not None:
            return True
        else:
            return False

    def validationIpUser(self, username, client_ip):

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

    def _getPermitionUsers(self, username):
        self.c.execute("SELECT type FROM users WHERE username = \"" + username + "\"")

        namepermition = self.c.fetchone()[0]

        self.c.execute("SELECT * FROM userpermition WHERE type = \"" + namepermition + "\"")

        result = self.c.fetchone()

        permition = Permition(result[0], result[1], result[2], result[3], result[4])

        return permition




# db = DatabaseSql()
#
# db.getPermition("erfan01", "netread")

#db.InsertPermition("user", True, False, True)

# db.checkUsername("erfan01")

# db.getData()
#
# db.createtable()
#
# db.validationIpUser("erfan01", "10.42.0.182")
# db.Insert("erfan", "erfan01", "1234", "user", "10.42.0.182/24,192.168.2.3/16")
