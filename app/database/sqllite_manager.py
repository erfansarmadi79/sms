import sqlite3


class DatabaseSql:
    def __init__(self):
        self.con = sqlite3.connect('userdatabase.db')

        self.c = self.con.cursor()

        # self.c.execute("""CREATE TABLE usermanager (
        #             name text,
        #             username text,
        #             passwd text,
        #             type text,
        #             iplimited text
        #             )""")

    def Insert(self, name, username, passwd, type, ips):

        if self.checkUsername(username):
            self.c.execute(
                "INSERT INTO usermanager VALUES (\'" + name + "\',\'" + username + "\',\'" + passwd + "\',\'" + type + "\',\'" + ips + "\')")
            self.con.commit()
            return "added user"
        else:
            return "existed user"

    def Delete(self, id):
        pass

    def Update(self, id, name, uusername, passwd, type, ips):
        pass

    def getData(self):
        self.c.execute("SELECT * FROM usermanager")
        return self.c.fetchone()

    def checkUsername(self, username):
        self.c.execute(
            "SELECT * FROM usermanager WHERE username = \"" + username + "\"")

        if self.c.fetchone() is None:
            return True
        else:
            return False

    def UserAuthantication(self, username, password):
        self.c.execute(
            "SELECT * FROM usermanager WHERE username = \"" + username + "\" AND " + "passwd = \"" + password + "\"")

        if self.c.fetchone() is not None:
            return True
        else:
            return False

    def validationIpUser(self, username, ip):
        self.c.execute(
            "SELECT iplimited FROM usermanager WHERE username = \"" + username + "\"")
        rows = self.c.fetchall()
        ip_list = [row[0] for row in rows]

        if ip in ip_list:
            return True
        else:
            return False

da = DatabaseSql()

da.validationIpUser("sarmadi123", "192.168.111.1")


