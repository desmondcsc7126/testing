from flask import Blueprint, render_template, request, url_for, redirect, Flask
from pymysql import connections
import os
import boto3
import json

auth = Blueprint('auth', __name__)
#app = Flask(__name__,template_folder='template')
#auth = Flask(__name__,template_folder='template')

customuser = "desmondcsc"
custompass = "desmondcsc"
customdb = "users"
customhost = "users.cvdg99ehiopr.us-west-2.rds.amazonaws.com" 

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

s3 = boto3.resource(
    's3'
)

s3_client = boto3.client(
    's3'
)

# s3 = boto3.client("s3")
bucketname = 'desmondchongsoonchuen'

# response = s3_client.get_object(Bucket = bucketname, Key = 'testing.json')

# @auth.route('/')
# def homepage():
#     return render_template('login.html')

@auth.route('/registration',methods = ['POST', 'GET'])
def register():
    return render_template('registration.html', myData = "1st")

@auth.route('/registerUser',methods = ['POST','GET'])
def registerUser():
    unArr = []
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # Should check repeated username
    cursor = db_conn.cursor()
    sql = "SELECT username FROM users"
    cursor.execute(sql)
    data = cursor.fetchall()
    data = list(map(list,data))
    cursor.close()

    for n in data:
        unArr.append(n[0])

    if username in unArr:
        return redirect(url_for('auth.register'))

    # Insert
    insert_user = "INSERT INTO users VALUES (%s, %s, %s)"

    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_user,(username, email, password))
        db_conn.commit()

    finally:
        cursor.close()

    return render_template('login.html', success = "True", data = unArr)

@auth.route('/authentication',methods = ['POST','GET'])
def authentication():
    username1 = request.form['username']
    password1 = request.form['password']

    cursor = db_conn.cursor()
    sql = "SELECT password from users where username = %s"
    cursor.execute(sql,(username1, ))
    # cursor.execute(sql)
    data = cursor.fetchone()
    # data = list(map(list,data))
    cursor.close()

    if data != None:
        pw = data[0]
        if password1 != pw:
            return render_template('login.html', success = "False", login = "False")
    else:
        return render_template('login.html', success = "False", login = "False")

    myDictionary = {
        'id':'desmondcsc'
    }

    f = open("sample.json")

    s3.Bucket(bucketname).put_object(Key='testing.json', Body=json.dumps(myDictionary))
    # s3.upload_file('testing.json','desmondchongsoonchuen',f)
    # s3.put_object(Body = json.dumps(myDictionary).encode('UTF-8'), Bucket = 'desmondchongsoonchuen',Key='testing.json')

    return render_template('login.html', success = "False", login = "True")

@auth.route('/uploadfile', methods = ['POST','GET'])
def uploadfile():
    myfile = request.files['myfile']
    fname = myfile.filename
    s3.Bucket(bucketname).put_object(Key=fname, Body=myfile)

    return render_template('login.html')

# print(json.loads(response['Body'].read()))

if __name__ == '__main__':
    auth.run(debug=True)