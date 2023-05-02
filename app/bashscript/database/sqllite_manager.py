import ipaddress
import sqlite3


class DatabaseSql:
    def __init__(self):
        self.con = sqlite3.connect('userdatabase.db')

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

    def validationIpUser(self, username, ip):

        try:
            self.c.execute("SELECT iplimited FROM users WHERE username = \"" + username + "\"")
            rows = self.c.fetchone()

            if rows[0] != None:
                rows = str(rows).replace("(", "").replace(")", "").replace("\'", "")
        except:
            return 2

        if rows[0] != None:

            rows.pop(len(rows) - 1)
            ip_list = [row for row in rows]

            client_ip = ipaddress.ip_address(ip)
            allowed_network = ipaddress.ip_network(rows[0])

            if client_ip in allowed_network:
                return True
            else:
                return False
        else:
            return True

            # if ip in ip_list:
            #     return True
            # else:
            #     return False

    def getPermition(self, username):
        self.c.execute(
            "SELECT type FROM users WHERE username = \"" + username + "\"")

        result = self.c.fetchone()[0]

        if result == "admin":
            return True
        elif result == "user":
            return False


db = DatabaseSql()

#db.getData()
#
#db.createtable()
#
db.validationIpUser("erfan159", "10.42.0.211")
# db.Insert("erfan", "erfan159", "1234", "user", "10.42.0.182,")
