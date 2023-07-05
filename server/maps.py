import hashlib
import requests
#import time
import phonenumbers
import json
import random
from flask import Flask, app, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

### MYSQL CONFIG ###
app.config['MYSQL_HOST'] = 'kooltheoutsider.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'kooltheoutsider'
app.config['MYSQL_PASSWORD'] = 'Corrientes818!'
app.config['MYSQL_DB'] = 'kooltheoutsider$default'
mysql = MySQL(app)
### END MYSQL CONFIG ###

def calcPrice(meters):
    value = "5000"
    if meters <= 100000:
        return value
    else:
        segments = meters / 100000
        price = int(round(segments)) * int(value)
        return price

def randomHash():
    random_bits = random.getrandbits(128)
    hash1 = "%032x" % random_bits
    return hash1

def get_my_ip():
    return request.environ['HTTP_X_REAL_IP']

def log(logcode, ip):
    cursorlog = mysql.connection.cursor()
    query = "INSERT INTO logging (code, ip, logging_time) VALUE ('" + logcode.upper() +"', '" + str(ip) + "', CURRENT_TIMESTAMP)";
    cursorlog.execute(query)
    mysql.connection.commit()
    cursorlog.close()
    print("Action Logged")


@app.route('/reqDist', methods =['POST'])
def requestDistance():
    cursor = mysql.connection.cursor()
    if request.method == 'POST' and 'add_from' in request.form and 'add_to' in request.form and 'source' in request.form:
        if request.form['add_from'] == '' or request.form['add_to'] == '' or request.form['source'] == '':
            log("MISSING_FORM_FIELD_VALUE", get_my_ip())
            response = {"status":"MISSING_FORM_FIELD_VALUE", "message":"FROM and/or TO fields are empty."}
            string = "('MISSING_FORM_FIELD_VALUE', '" + str(get_my_ip()) + "', 'MISSING_FORM_FIELD_VALUE', 'MISSING_FORM_FIELD_VALUE')"
            query = "INSERT INTO requests (response, ip, status, source) VALUES " + string
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            return jsonify(response)
        address_from = request.form['add_from']
        address_to = request.form['add_to']
        source = request.form['source']
        api = "AIzaSyAKU2FtrRA5YQpcMxY2Min_NGrbdUli_Jc"
        unit = "metric"
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + address_from + "&destinations=" + address_to + "&units=" + unit + "&key=" + api + ""
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        if response["rows"][0]["elements"][0]["status"] == "NOT_FOUND":
            log("NOT_FOUND", get_my_ip())
            response = {"status":"ADDRESS_ERROR_OR_NOT_FOUND","message": "Please, verify the address ingressed, and make your request again"}
            string = "('" + str(url) +"', '" + str(get_my_ip()) + "', 'ADDRESS_ERROR_OR_NOT_FOUND', '" + str(source) +"')"
            query = "INSERT INTO requests (response, ip, status, source) VALUES " + string
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            return jsonify(response)
        else:
            origen = response["origin_addresses"]
            destino = response["destination_addresses"]
            distancia = response["rows"][0]["elements"][0]["distance"]["text"]
            precio = calcPrice(response["rows"][0]["elements"][0]["distance"]["value"])
            #ip = get_my_ip()
            res = {"status": "SUCCESS","data":[{"origen": origen, "destino": destino, "distancia": distancia, "precio": precio}]}
            string = "('" + str(url) +"', '" + str(get_my_ip()) + "','SUCCESS', '" + str(source) +"')"
            query = "INSERT INTO requests (response, ip, status, source) VALUES " + string
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            log("SUCCESS", get_my_ip())
            return jsonify(res)
    else:
        log("MISSING_FORM_FIELDS", get_my_ip())
        source = request.form['source']
        response = {"status": "MISSING_FORM_FIELDS", "message":"Fields are not being sent on POST method."}
        string = "('MISSING_FORM_FIELDS', '" + str(get_my_ip()) + "','MISSING_FORM_FIELDS', '" + str(source) +"')"
        query = "INSERT INTO requests (response, ip, status, source) VALUES " + string
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return jsonify(response)
@app.route('/newUser', methods =['POST'])
def newUser():
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'email' in request.form and 'password' in request.form and 'confirm_password' in request.form:
        if request.form['nombre'] == '':
            log("NAME_FIELD_EMPTY", get_my_ip())
            response = {"status": "NAME_FIELD_EMPTY", "message":"Name field during registration is empty."}
            return jsonify(response)
        if request.form['apellido'] == '':
            log("LASTNAME_FIELD_EMPTY", get_my_ip())
            response = {"status": "LASTNAME_FIELD_EMPTY", "message":"Last Name field during registration is empty."}
            return jsonify(response)
        if request.form['email'] == '':
            log("EMAIL_FIELD_EMPTY", get_my_ip())
            response = {"status": "EMAIL_FIELD_EMPTY", "message":"Email field during registration is empty."}
            return jsonify(response)
        if request.form['password'] == '':
            log("PASSWORD_FIELD_EMPTY", get_my_ip())
            response = {"status": "PASSWORD_FIELD_EMPTY", "message":"Password field during registration is empty."}
            return jsonify(response)
        if request.form['confirm_password'] == '':
            log("CONFIRMATION_PASSWORD_FIELD_EMPTY", get_my_ip())
            response = {"status": "CONFIRM_PASSWORD_FIELD_EMPTY", "message":"Confirm Password field during registration is empty."}
            return jsonify(response)
        if request.form['password'] != request.form['confirm_password']:
            log("PASSWORD_AND_CONFIRMATION_DOES_NOT_MATCH", get_my_ip())
            response = {"status": "PASSWORD_AND_CONFIRMATION_DOES_NOT_MATCH", "message":"Password and Confirmation does not match."}
            return jsonify(response)
    else:
        log("MISSING_REQUEST_INFO", get_my_ip())
        response = {"status": "MISSING_REQUEST_INFO", "message":"Missing any info on the request."}
        return jsonify(response)
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']
    hashpass = hashlib.md5(password.encode('utf8')).hexdigest()
    temp_hash = hashpass + email
    activ_hash = hashlib.md5(temp_hash.encode('utf8')).hexdigest()
    string = "INSERT INTO accounts (nombre, apellido, email, password, creado, active_hash) VALUES ('" + nombre + "', '" + apellido + "', '" + email + "', '" + hashpass + "', CURRENT_TIMESTAMP, '" + activ_hash + "')"
    cursor = mysql.connection.cursor()
    cursor.execute(string)
    mysql.connection.commit()
    cursor.close()
    log("USER_REGISTRATION_SUCCESS", get_my_ip())
    response = {"status": "USER_REGISTRATION_SUCCESS", "message":"User registered successfully."}
    return jsonify(response)
@app.route('/activateUser', methods =['GET'])
def activateUser():
    if request.method == 'GET' and 'hash' in request.form and 'email' in request.form:
        email = request.form["email"]
        code = request.form["hash"]
        query = "UPDATE accounts SET activado=1 WHERE active_hash='" + code + "' and activado=0 LIMIT 1";
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        log("USER_ACTIVATION_SUCCESS", get_my_ip())
        response = {"status": "USER_ACTIVATION_SUCCESS", "message":"User " + email + " activated successfully."}
        return jsonify(response)
    else:
        log("USER_ACTIVATION_FAILURE", get_my_ip())
        response = {"status": "USER_ACTIVATION_FAILURE", "message":"The user are you trying to activate does not exist, or the hash is incorrect."}
        return jsonify(response)
@app.route('/updatePhone', methods =['POST'])
def updatePhone():
    if request.method == 'POST' and 'hash' in request.form and 'email' in request.form and 'phone' in request.form:
        email = request.form["email"]
        code = request.form["hash"]
        phone = request.form["phone"]
        string_phone_number = str(phone)
        phone_number = phonenumbers.parse(string_phone_number)
        phone_is_possible = str(phonenumbers.is_possible_number(phone_number))
        phone_is_valid = str(phonenumbers.is_valid_number(phone_number))
        if phone_is_possible == "True":
            if phone_is_valid == "True":
                query = "UPDATE accounts SET celular = '" + phone + "' WHERE email='" + email + "' LIMIT 1";
                cursor = mysql.connection.cursor()
                cursor.execute(query)
                mysql.connection.commit()
                cursor.close()
                log("PHONE_UPDATED_SUCCESS", get_my_ip())
                response = {"status": "PHONE_UPDATED_SUCCESS", "message":"Phone updated successfully"}
                return jsonify(response)
            else:
                log("PHONE_NOT_VALID_1", get_my_ip())
                response = {"status": "PHONE_NOT_VALID_1", "message":"Phone is not valid"}
                return jsonify(response)
        else:
            log("PHONE_NOT_VALID_2", get_my_ip())
            response = {"status": "PHONE_NOT_VALID_2", "message":"Phone is not valid"}
            return jsonify(response)
    else:
        log("MISSING_PARAMETERS", get_my_ip())
        response = {"status": "MISSING_PARAMETERS", "message":"Missing parameters on the request"}
        return jsonify(response)

#USERMGM
@app.route('/user/<username>', methods =['GET'])
def getUserInfo(username):
    cursor = mysql.connection.cursor()
    if request.method == 'GET':
        query = "SELECT * FROM accounts WHERE email = %s"
        cursor.execute(query, (username,))
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
        return jsonify(json.dumps(data, sort_keys=False, default=str))
    else:
        log("USER_NOT_FOUND", get_my_ip())
        response = {"status": "USER_NOT_FOUND", "message":"The email you want to search is not on our database."}
        return jsonify(response)
@app.route('/user/logout', methods=['POST'])
def logout():
    cursor = mysql.connection.cursor()
    if request.method == 'POST' and 'email' in request.form and 'session_hash' in request.form:
        query = "UPDATE accounts SET session_hash='' where email=%s and session_hash=%s LIMIT 1"
        email = request.form["email"]
        session_hash = request.form["session_hash"]
        values = (email, session_hash)
        cursor.execute(query, values)
        mysql.connection.commit()
        result = cursor.rowcount
        if cursor.rowcount > 0:
            log("USER_" + email + "_LOGGED_OUT", get_my_ip())
            response = {"status": "USER_LOGGED_OUT_SUCCESSFULLY", "message":"The user has been logged out successfully."}
            cursor.close()
            return jsonify(response)
        else:
            log("USER_" + email + "_IS_NOT_LOGGED", get_my_ip())
            response = {"status": "USER_IS_NOT_LOGGED", "message":"The user you are trying to logout is not logged in previously."}
            cursor.close()
            return jsonify(response)
    else:
        log("MISSING_PARAMETERS_ON_LOGOUT", get_my_ip())
        response = {"status": "MISSING_PARAMETERS_ON_LOGOUT", "message":"Missing parameters on the logout request"}
        return jsonify(response)
@app.route('/user/checkSessionAlive', methods =['POST'])
def checkSessionAlive():
    cursor = mysql.connection.cursor()
    if request.method == 'POST' and 'email' in request.form and 'session_hash' in request.form:
        query = "SELECT * FROM accounts WHERE email = %s AND session_hash = %s LIMIT 1"
        email = request.form["email"]
        session_hash = request.form["session_hash"]
        values = (email, session_hash)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:
            response = {"status": "SESSION_NOT_ALIVE", "message":"The session for the user requested is not alive animore."}
            log("SESSION_NOT_ALIVE", get_my_ip())
            return jsonify(response)
        else:
            response = {"status": "SESSION_ALIVE", "message":"The session for the user requested still alive."}
            log("SESSION_ALIVE", get_my_ip())
            return jsonify(response)
    else:
        response = {"status": "SESSION_CHECK_FAILER", "message":"Unknown session check error"}
        log("SESSION_CHECK_FAILER", get_my_ip())
        return jsonify(response)


@app.route('/user/login', methods =['POST'])
def login():
    cursor = mysql.connection.cursor()
    if request.method == 'POST' and 'email' in request.form and 'pass' in request.form:
        query = "SELECT * FROM accounts WHERE email = %s AND password = %s AND activado=1 LIMIT 1"
        email = request.form["email"]
        passw = hashlib.md5(request.form["pass"].encode('utf8')).hexdigest()
        values = (email, passw)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None:
            session_hash = randomHash()
            query = "UPDATE accounts SET ultimo_ingreso=CURRENT_TIMESTAMP, session_hash=%s where email=%s LIMIT 1"
            cursor.execute(query, (session_hash, email,))
            mysql.connection.commit()
            cursor.close()
            session = {
                "status": "success",
                "email": email,
                "hash": session_hash
            }
            log("USER_" + email + "_LOGGED_IN", get_my_ip())
            return jsonify(session)
        else:
            cursor.close()
            response = {"status": "USER_NOT_FOUND", "message":"The email used to login is not registered, or is not activated."}
            log("USER_" + email + "_NOT_FOUND_OR_NOT_ACTIVATED", get_my_ip())
            return jsonify(response)
    else:
        log("MISSING_PARAMETERS_ON_LOGIN", get_my_ip())
        response = {"status": "MISSING_PARAMETERS_ON_LOGIN", "message":"Missing parameters on the login request"}
        return jsonify(response)
