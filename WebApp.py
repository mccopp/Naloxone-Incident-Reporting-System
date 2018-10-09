#Title: Python Flask Web Application
#Desc: Routes users from your server to input.html and passes parameters to Python where it is loaded to SAS CAS (LOADTOCAS), it ends by sending user to results.html
#Author:Jonathan McCopp
#Date: October, 8th, 2018
#Dependencies: Flask Folder Structure, input.html, results.html, LOADTOCAS.py, SQLite3 DB

#%run loadtocas
get_ipython().magic('run LOADTOCAS')
from LOADTOCAS import loadcas
from flask import Flask, render_template, request

#this is starting a sqlite3 database for storing content from the web
import sqlite3

def connect():
    conn=sqlite3.connect("reg.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS naloxone (id INTEGER PRIMARY KEY, firstname text, lastname text, healthstatus text, dose real, zipcode text)")
    conn.commit()
    conn.close()
    
def insert(firstname, lastname, healthstatus, dose, zipcode):
    conn=sqlite3.connect("reg.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO naloxone VALUES (NULL,?,?,?,?,?)",(firstname, lastname, healthstatus, dose, zipcode))
    conn.commit()
    conn.close()
    view()

def view():
    conn=sqlite3.connect("reg.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM naloxone")
    rows=cur.fetchall()
    conn.close()
    return rows

#begin flask, this is a web framework and allows users to start their own web applications
app=Flask(__name__)

#this routes to the home page on your web application at your host address
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("input.html")

#this routes to a second webpage and passes parameters using the GET and POST methods
@app.route('/result', methods=['GET', 'POST'])
def result():
    
    if request.method=='POST':

#passing parameters from web form in input.html to local variables
        result=request.form
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        healthstatus=request.form['healthstatus']
        dose=request.form['dose']
        zipcode=request.form['zipcode']

#pass parameters to database
        connect()
        insert(firstname, lastname, healthstatus, dose, zipcode)

#load to CAS  , call LOADTOCAS Python Program     
        loadcas()
        
#pass parameters to chained webpage result.html
    return render_template("result.html", result=result, firstname=firstname)

if __name__=="__main__":
    app.run(host='<servername>', port=<port_number>, debug=False)

