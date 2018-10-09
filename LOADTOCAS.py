#Title: SAS SWAT for CAS, LOAD to CAS
#Desc: Loads CSV to CAS Server for SAS Viya Applications
#Author:Jonathan McCopp
#Date: October, 8th, 2018

def loadcas():

#note user should always start a fresh environment manager session in SAS to look for loaded tables
    import sqlite3
    import swat
    from swat.cas import datamsghandlers as dmh

#connect to CAS
    conn=swat.CAS('<server_name>', <port_number>, '<sas username>', '<sas password>')
    out = conn.serverstatus()

#set active session for a CASLIB
    conn.setsessopt(caslib='Public')

#convert database table to CSV prior to load to CAS
    import csv
    import pandas.io.sql as sql

    def convertcsv():
        con = sqlite3.connect('reg.db')
        table = sql.read_sql('select id, firstname, lastname, healthstatus, dose, zipcode from naloxone', con)
        table.to_csv("<path and csv name... viya_reg.csv>")

    convertcsv()

#check for table, 0=none, 1=inmem local, 2=inmem global
    rc=conn.table.tableExists(caslib="public", name='viya_reg')
    out=rc['exists']
    print(out)
    
#load csv to CAS and LOAD into memory immediately so it is seen in environment manager
    if out>0:
        rc=conn.table.dropTable(caslib="public",name='viya_reg')
        print('Table Dropped')
        rc=conn.table.loadtable(caslib="public",path='viya_reg.csv', readAhead='TRUE', promote='True', vars=['id','firstname', 'lastname', 'healthstatus', 'dose', 'zipcode'])
        print('Table Added')
                                
    else: 
        rc=conn.table.loadtable(caslib="public",path='viya_reg.csv', readAhead='TRUE', promote='True', vars=['id','firstname', 'lastname', 'healthstatus', 'dose', 'zipcode'])
        print('Table Added')







