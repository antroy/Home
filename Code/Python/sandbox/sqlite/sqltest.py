#!/usr/bin/python
#:folding=indent:collapseFolds=2:

from pysqlite2 import dbapi2 as sql

class Main:
    
    COL_WIDTH = 10
    DB_CLEANUP = ['drop table contacts']
    
    query = """select f_name, l_name from contacts
                   where category = "Family"
            """
    
    def __init__(self):
        self.con = sql.connect("ab.db")
        self.cur = self.con.cursor()
        
    def loadData(self):
        #self.executeFile("tabs.sql")        
        self.importData("abook.csv", "contacts")
        #self.importData("abtest.csv", "contacts")
        self.con.commit()
        print "OK"
    
    def executeFile(self, filename):
        filetext = ""
        f = file(filename)
        for line in f:
            filetext += line
        f.close()
        commandArr = filetext.split(";")
        for cmd in commandArr:
            self.cur.execute(cmd)
       
    def importData(self, filename, table):
        f = file(filename)
        compound = ""
        for line in f:
            compound += line.rstrip()
            if not compound.rstrip().endswith('"'):
                compound += "; "
                continue
            statement =  "insert into " + table + ' values('
            statement += compound + ');'
            #print "S:", statement
            self.cur.execute(statement)
            compound = ""
        f.close()
        
       
    def run(self):
        self.cur.execute(Main.query)
        
        for colName in self.cur.description:
            print colName[0].ljust(Main.COL_WIDTH),
        print
        print "-" * 78
        
        indices = range(len(self.cur.description))
        
        for row in self.cur:
            for index in indices:
                value = str(row[index])
                print value.ljust(Main.COL_WIDTH),
            print ""
    
    def cleanup(self):
        for i in range(len(Main.DB_CLEANUP)):
            self.cur.execute(Main.DB_CLEANUP[i])
        self.cur.close()
        self.con.close()
            
        
def main():
    m = Main()
    #m.loadData()
    #m.cleanup()
    m.run()
        
if __name__ == "__main__":
    main()