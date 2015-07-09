#-*- coding: utf-8 -*-
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
    def __init__(self, dbArgs):
        #dbArgs : dbhost, dbuser, dbpasswd, dbname
        try:
            print '\nChecking MySQL connection...'
            self.db = MySQLdb.connect(dbArgs[0], dbArgs[1], dbArgs[2], dbArgs[3])                   
            #self.cursor.execute('select version()')
            print 'Connection OK, proceeding.'
        except MySQLdb as error:
            print 'Error: %s ' %error + '\nStop.\n'
            sys.exit()
        
    def insert(self, query):
        self.execute(query)
        self.db.commit()
        print 'Inserted data.'
                        
    def select(self, query):       
        #self.cursor.execute('set names utf8') 
        self.execute(query)        
        result = self.cursor.fetchall()
        print 'Selected data.'        
        return result    
            
    def execute(self, sqlStatement, args = None):
        self.callCursor()
        if args == None:
            self.cursor.execute(sqlStatement)
        else:
            self.cursor.execute(sqlStatement, args)
            
    def callCursor(self):
        self.cursor = self.db.cursor()
        self.cursor.execute('set names utf8')           
         
    def __del__(self):
        print '\nFinishing operations...'
        self.cursor.close()
        self.db.close()
        print 'Done.\n'