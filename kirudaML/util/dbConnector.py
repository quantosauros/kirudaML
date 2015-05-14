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
                
    def insert(self, query):        
        self.execute(query)             
        self.db.commit()
                    
    def select(self, query):
        self.execute(query)        
        result = self.cursor.fetchall()        
        return result
            
    def execute(self, sqlStatement, args = None):
        if args == None:
            self.cursor.execute(sqlStatement)
        else:
            self.cursor.execute(sqlStatement, args)
                            
    def __del__(self):
        print '\nFinishing operations...'
        self.cursor.close()
        self.db.close()
        print 'Done.\n'