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
            try :
                self.c.execute("INSERT INTO usermanager VALUES (\'" + name + "\',\'" + username + "\',\'" + passwd + "\',\'" + type + "\',\'" + ips + "\')")
                self.con.commit()
                return "added user"
            except:
                return "don't added"
        else:
            return "user existed"

    def Delete(self, username):

        if self.checkUsername(username) == False:
            try:
                self.c.execute("DELETE FROM usermanager WHERE username = \"" + username + "\"")
                return self.con.commit()
            except:
                return "cannot remove "

        else:
            return "user existed"

    def Update(self, username, name, passwd, type, ips):

        self.c.execute("UPDATE usermanager SET name = \'" + name + "\', passwd = \'" + passwd + "\', type = \'" + type + "\', iplimited = \'" + ips + "\' WHERE username = \"" + username + "\"")
        return self.con.commit()

    def getData(self):
        try:
            self.c.execute("SELECT * FROM usermanager")
            return self.c.fetchone()
        except:
            return "cannot getdata"

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
        rows = str(self.c.fetchone()).replace("(", "").replace(")", "").replace("\'", "").split(",")

        rows.pop(len(rows)-1)
        ip_list = [row for row in rows]

        if ip in ip_list:
            return True
        else:
            return False

    def getPermition(self, username):
        self.c.execute(
            "SELECT type FROM usermanager WHERE username = \"" + username + "\"")

        result = self.c.fetchone()[0]

        if result == "admin":
            return True
        elif result == "user":
            return False

