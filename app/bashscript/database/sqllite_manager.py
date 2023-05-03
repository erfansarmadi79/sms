import sqlite3
import ipaddress


class DatabaseSql:
    def __init__(self):
        self.con = sqlite3.connect('/home/admin/1402.02.11/sms/app/bashscript/database/userdatabase.db')

        self.c = self.con.cursor()

    def createUserTable(self):

        self.c.execute("""CREATE TABLE users (
                    id INTEGER,
                    fullname text,
                    username text,
                    passwd text,
                    type text,
                    iplimited text
                    )""")

    def Insert(self, fullname, username, passwd, type, ips):

        if self.checkUsername(username):
            try:
                self.c.execute(
                    "INSERT INTO users (fullname ,username, passwd, type, iplimited) VALUES (\"" + fullname + "\",\"" + username + "\",\"" + passwd + "\", \"" + type + "\",\"" + ips + "\")")
                self.con.commit()
                return "added user"
            except:
                return "don't added"
        else:
            return "user existed"

    def Delete(self, username):

        if self.checkUsername(username) == False:
            try:
                self.c.execute("DELETE FROM users WHERE username = \"" + username + "\"")
                return self.con.commit()
            except:
                return "cannot remove "

        else:
            return "user existed"

    def Update(self, username, fullname, passwd, type, ips):

        self.c.execute(
            "UPDATE users SET name = \'" + fullname + "\', passwd = \'" + passwd + "\', type = \'" + type + "\', iplimited = \'" + ips + "\' WHERE username = \"" + username + "\"")
        return self.con.commit()

    def getData(self):
        try:
            self.c.execute("SELECT * FROM users")
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

        global rows
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

    def getPermition(self, username):
        self.c.execute(
            "SELECT type FROM users WHERE username = \"" + username + "\"")

        result = self.c.fetchone()[0]

        if result == "admin":
            return True
        elif result == "user":
            return False

# db = DatabaseSql()
#
# db.checkUsername("erfan01")

# db.getData()
#
# db.createtable()
#
# db.validationIpUser("erfan01", "10.42.0.182")
# db.Insert("erfan", "erfan01", "1234", "user", "10.42.0.182/24,192.168.2.3/16")
