'''
Created on 2015. 5. 13.

@author: Jay
'''
import MySQLdb
import sys

class dbConnector:
    '''
    classdocs
    '''
    def __init__(self, dbhost, dbuser, dbpasswd, dbname):        
        try:
            print '\nChecking MySQL connection...'
            self.db = MySQLdb.connect(dbhost, dbuser, dbpasswd, dbname)
            self.cursor = self.db.cursor()
            self.cursor.execute('select version()')
            print 'Connection OK, proceeding.'
        except MySQLdb as error:
            print 'Error: %s ' %error + '\nStop.\n'
            sys.exit()
        
    def connect(self):
        query = self.cursor.execute()
        self.execute(query)        
        row = self.cursor.fetchone()
        print(row[0])        
            
    def insert(self, dbTable, dbColumn, dbValue):
        query = "INSERT INTO " + dbTable + "(" + dbColumn[0] + ", " + dbColumn[1] + ", " + dbColumn[2] + ", " + dbColumn[3] + ") VALUES (%s,%s,%s,%s)"
        
        self.execute1(query, dbValue)             
        self.db.commit()
                    
    def select(self, dbcolumn, dbtable, dbcondition ):
   
        query = "SELECT " + dbcolumn + " FROM " + dbtable; 
        print(query)
        self.execute(query)
        
        result = self.cursor.fetchall()
        
        print(result[0])
        print(result[1])        
        
    def execute(self, sqlStatement):
        self.cursor.execute(sqlStatement)
        
    def execute1(self, query, args):
        self.cursor.execute(query, args)
        print 'done'
            
    def __del__(self):
        print '\nFinishing operations...'
        self.cursor.close()
        self.db.close()
        print 'Done.\n'