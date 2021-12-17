from flask import Flask
from flask import request
from flask import render_template
from flask import flash,redirect,url_for,send_file
import os
import difflib
import sqlite3
import hashlib
import random
import json
from json import load
import datetime
import time

app =Flask(__name__)

# PATHs DEFINITION
SERVICE_PATH = '/home/bilal/Desktop/fatim1/project/service/'

# 3
@app.route('/postexample', methods=['POST'])
def postexample():
    name_file = "test.png"
    if request.method == 'POST':
        file = request.files['file']
        file.save('./'+name_file)
        return send_file("result.png",mimetype='image/png')
    
    return "NOK"

@app.route('/postarg',methods=['POST'])
def postarg():
    if request.headers['Content-Type']=='text/plain':
        return"OBWK: "+str(request.data)
    elif request.headers['Content-Type']=='application/json':
        try :
            if request.json["login"]!='' and request.json["password"]!='':
                with open('data.json','w') as file:
                    file.write(str(request.json))
                return 'comtpe en attente de validation'
        except:
            return"NOK"
    return"NOK"

@app.route('/addmanu',methods=['POST'])
def addmanu():
    if request.headers['Content-Type']!='application/json':
        return "NOK, use json data to insert name TEXT, addr TEXT, city TEXT, pin TEXT "
    else:
        try :
            if (request.json["name"]!='' and request.json["addr"]!='' and request.json["city"]!='' and request.json["pin"]!=''):
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()  
                item = (request.json["name"], request.json["addr"], request.json["city"], request.json["pin"])
                print(cursor.execute('SELECT * FROM students WHERE name=? AND addr=? AND city=? AND pin=?',item).fetchall())
                if cursor.execute('SELECT * FROM students WHERE name=? AND addr=? AND city=? AND pin=?',item).fetchall() == []:
                    cursor.execute('INSERT INTO students VALUES (?,?,?,?)', item)
                    conn.commit()
                    conn.close()
                    return 'OK'
                conn.close()
                return 'NOK'
        except:
            return"NOK"
            
@app.route('/deleteStudent',methods=['POST'])
def deleteStudent():
    if request.headers['Content-Type']!='application/json':
        return "NOK, use json data to delete with name TEXT, addr TEXT, city TEXT, pin TEXT "
    else:
        try :
            if (request.json["name"]!='' and request.json["addr"]!='' and request.json["city"]!='' and request.json["pin"]!=''):
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                item = (request.json["name"], request.json["addr"], request.json["city"], request.json["pin"])
                cursor.execute('DELETE FROM students WHERE name=? AND addr=? AND city=? AND pin=?',item)
                print(item, 'was deleted')
                conn.commit()
                conn.close()
                return 'OK'
        except:
            return"NOK"

@app.route('/signin',methods=['POST'])
def signin():
    conn =sqlite3.connect('database.db')
    cursor = conn.cursor()
    print("Opened database successfully")
    print(request.json)
    if request.headers['Content-Type']!='application/json':
        conn.close()
        return 'NOK'
    pwd = hashlib.sha256(request.json["password"].encode()).hexdigest()
    
    item = (request.json["id"],pwd,random.randint(0,20),random.randint(0,20),random.randint(0,20))
    cursor.execute('INSERT INTO notes VALUES (?,?,?,?,?)',item) 
    conn.commit()        
    conn.close()
    return 'successfuly signed in'

def countOccurrencesFromList(l):
    """
    Creates a dict of elements with their nb of occurences

    :param l: the list to count
    :type l: list
    :return: the count
    :rtype: dict
    """
    return {h:l.count(h) for h in l}
        
def dictdiff(dict1, dict2): 
    return {key:[dict1[key], dict2[key]] for key in dict1 if dict1[key] != dict2[key]}
            

def main():
    commands = []
    for cmd in commands:
        print('\n>> ' + cmd)
        os.system(cmd)
        print()

if __name__ == "__main__":
    main()
