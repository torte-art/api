from flask_cors import cross_origin
from werkzeug.utils import redirect
from flask import jsonify
import mysql.connector
import sys
import hashlib
from flask import abort, request
from app import app
import config_file


@app.server.route("/")
@app.server.route("/index")
@cross_origin()
def index():
    return redirect("https://app.swaggerhub.com/apis-docs/meintest/Api-Fiat2Defichain/1")


# GET User
@app.server.route('/api/v1/user/<address>', methods=['GET'])
@cross_origin()
def getUser(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address = %s AND signature = %s"
    val = (address, signature)
    cur.execute(sql, val)
    rv = cur.fetchall()
    if len(rv) > 0:
        row_headers = [x[0] for x in cur.description]
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        json_data[0]['created'] = json_data[0]['created'].strftime("%Y-%m-%dT%H:%M:%S")
        json_data[0]['ref'] = str(json_data[0]['ref']).zfill(6)[0:3] + '-' + str(json_data[0]['ref']).zfill(6)[3:7]
        json_data[0]['used_ref'] = str(json_data[0]['used_ref']).zfill(6)[0:3] + '-' + str(
            json_data[0]['used_ref']).zfill(6)[3:7]
        return jsonify(json_data[0])
    else:
        abort(404, 'No User with that legacy address and signature found!')


# Update User
@app.server.route('/api/v1/user/<address>', methods=['PUT'])
@cross_origin()
def updateUser(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address = %s AND signature = %s"
    val = (address, signature)
    cur.execute(sql, val)
    rv = cur.fetchall()
    json_data = []
    if len(rv) > 0:
        row_headers = [x[0] for x in cur.description]
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        json_data[0]['created'] = json_data[0]['created'].strftime("%Y-%m-%dT%H:%M:%S")
        if 'mail' in request.json:
            if not isParameterSQL(request.json['mail']):
                if '@' in request.json['mail']:
                    json_data[0]['mail'] = request.json['mail']
                    sql = "UPDATE users SET mail = %s WHERE address = %s"
                    val = (request.json['mail'], address)
                    cur.execute(sql, val)
                    conn.commit()
                else:
                    abort(400, 'Invalid mail')
        if 'wallet_id' in request.json:
            if not isParameterSQL(request.json['wallet_id']):
                json_data[0]['wallet_id'] = int(request.json['wallet_id'])
                sql = "UPDATE users SET wallet_id = %s WHERE address = %s"
                val = (request.json['wallet_id'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'used_ref' in request.json:
            if not isParameterSQL(request.json['used_ref']):
                json_data[0]['used_ref'] = int(request.json['used_ref'].replace('-',""))
                sql = "UPDATE users SET used_ref = %s WHERE address = %s"
                val = (request.json['used_ref'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'firstname' in request.json:
            if not isParameterSQL(request.json['firstname']):
                json_data[0]['firstname'] = request.json['firstname']
                sql = "UPDATE users SET firstname = %s WHERE address = %s"
                val = (request.json['firstname'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'surname' in request.json:
            if not isParameterSQL(request.json['surname']):
                json_data[0]['surname'] = request.json['surname']
                sql = "UPDATE users SET surname = %s WHERE address = %s"
                val = (request.json['surname'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'street' in request.json:
            if not isParameterSQL(request.json['street']):
                json_data[0]['street'] = request.json['street']
                sql = "UPDATE users SET street = %s WHERE address = %s"
                val = (request.json['street'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'location' in request.json:
            if not isParameterSQL(request.json['location']):
                json_data[0]['location'] = request.json['location']
                sql = "UPDATE users SET location = %s WHERE address = %s"
                val = (request.json['location'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'zip' in request.json:
            if not isParameterSQL(request.json['zip']):
                json_data[0]['zip'] = request.json['zip']
                sql = "UPDATE users SET zip = %s WHERE address = %s"
                val = (request.json['zip'], address)
                cur.execute(sql, val)
                conn.commit()
        if 'phone_number' in request.json:
            if not isParameterSQL(request.json['phone_number']):
                json_data[0]['phone_number'] = request.json['phone_number']
                sql = "UPDATE users SET phone_number = %s WHERE address = %s"
                val = (request.json['phone_number'], address)
                cur.execute(sql, val)
                conn.commit()
    return jsonify(getUser(address).json)


# Add User
@app.server.route('/api/v1/user', methods=['POST'])
@cross_origin()
def addUser():
    signature = request.json['signature']
    checkAddressAndSignature(request.json['address'], signature)
    newUser = {}
    newUser["address"] = request.json['address']
    ip = request.json['ip']
    executeString = "SELECT * FROM users"
    conn = createDBConnection()
    cur = conn.cursor()
    cur.execute(executeString)
    rv = cur.fetchall()
    newUser["signature"] = request.json['signature']
    newUser["IP"] = ip
    sql = "INSERT INTO users (address, signature, IP) VALUES (%s, %s, %s)"
    val = (newUser["address"],  newUser["signature"], newUser["IP"])
    cur.execute(sql, val)
    conn.commit()
    if 'mail' in request.json:
        if not isParameterSQL(request.json['mail']) and '@' in request.json['mail']:
            newUser["mail"] = request.json['mail']
            sql = "UPDATE users SET mail =%s WHERE address =%s"
            val = (request.json['mail'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'wallet_id' in request.json:
        if not isParameterSQL(request.json['wallet_id']):
            newUser["wallet_id"] = int(request.json['wallet_id'])
            sql = "UPDATE users SET wallet_id =%s WHERE address =%s"
            val = (request.json['wallet_id'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'used_ref' in request.json:
        if not isParameterSQL(request.json['used_ref']):
            newUser["used_ref"] = int(request.json['used_ref'].replace("-", ""))
            sql = "UPDATE users SET used_ref =%s WHERE address =%s"
            val = (newUser['used_ref'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'firstname' in request.json:
        if not isParameterSQL(request.json['firstname']):
            newUser['firstname'] = request.json['firstname']
            sql = "UPDATE users SET firstname = %s WHERE address = %s"
            val = (request.json['firstname'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'surname' in request.json:
        if not isParameterSQL(request.json['surname']):
            newUser['surname'] = request.json['surname']
            sql = "UPDATE users SET surname = %s WHERE address = %s"
            val = (request.json['surname'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'street' in request.json:
        if not isParameterSQL(request.json['street']):
            newUser['street'] = request.json['street']
            sql = "UPDATE users SET street = %s WHERE address = %s"
            val = (request.json['street'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'location' in request.json:
        if not isParameterSQL(request.json['location']):
            newUser['location'] = request.json['location']
            sql = "UPDATE users SET location = %s WHERE address = %s"
            val = (request.json['location'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'zip' in request.json:
        if not isParameterSQL(request.json['zip']):
            newUser['zip'] = request.json['zip']
            sql = "UPDATE users SET zip = %s WHERE address = %s"
            val = (request.json['zip'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    if 'phone_number' in request.json:
        if not isParameterSQL(request.json['phone_number']):
            newUser['phone_number'] = request.json['phone_number']
            sql = "UPDATE users SET phone_number = %s WHERE address = %s"
            val = (request.json['phone_number'], request.json['address'])
            cur.execute(sql, val)
            conn.commit()
    return jsonify(getUserInternal(newUser["address"], newUser["signature"]).json)


# GET registrations
@app.server.route('/api/v1/user/<address>/registration', methods=['GET'])
@cross_origin()
def getRegistration(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    json_all = {"fiat2crypto": [], "crypto2fiat": []}
    json_all['fiat2crypto'] = getFiat2Crypto(address).json
    json_all['crypto2fiat'] = getCrypto2Fiat(address).json
    return jsonify(json_all)


# GET registrations
@app.server.route('/api/v1/user/<address>/fiat2crypto', methods=['GET'])
@cross_origin()
def getFiat2Crypto(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address=%s AND signature=%s"
    val = (address, signature)
    cur.execute(sql, val)
    if cur.arraysize > 0:
        conn.close()
        connReg = createDBConnection()
        curReg = connReg.cursor()
        sqlReg = "SELECT * FROM fiat2crypto WHERE address=%s"
        curReg.execute(sqlReg, (address,))
        if curReg.arraysize > 0:
            row_headers = [x[0] for x in curReg.description]
            rv = curReg.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            for json_created in json_data:
                json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")
                if json_created['active'] == 0:
                    json_created['active'] = False
                else:
                    json_created['active'] = True
            return jsonify(json_data)
        else:
            abort(404, 'No registrations with requested legacy address and signature found!')
    else:
        abort(404, 'No User with that legacy address and signature found!')


# GET registrations
@app.server.route('/api/v1/user/<address>/fiat2crypto/<id>', methods=['GET'])
@cross_origin()
def getFiat2CryptoById(address, id):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    if isParameterSQL(id):
        abort(400, 'Invalid id')
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address=%s AND signature=%s"
    val = (address, signature)
    cur.execute(sql, val)
    if cur.arraysize > 0:
        conn.close()
        connReg = createDBConnection()
        curReg = connReg.cursor()
        sqlReg = "SELECT * FROM fiat2crypto WHERE address=%s AND id=%s"
        curReg.execute(sqlReg, (address, id))
        if curReg.arraysize > 0:
            row_headers = [x[0] for x in curReg.description]
            rv = curReg.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            for json_created in json_data:
                json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")
                if json_created['active'] == 0:
                    json_created['active'] = False
                else:
                    json_created['active'] = True
            return jsonify(json_data)
        else:
            abort(404, 'No registrations with requested legacy address and signature found!')
    else:
        abort(404, 'No User with that legacy address and signature found!')


# POST registrations
@app.server.route('/api/v1/user/<address>/fiat2crypto', methods=['POST'])
@cross_origin()
def addFiat2Crypto(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    badFormat = 0
    message = 'Following data are missing:'
    if not request.json:
        abort(400, 'Data is no JSON')
    if not 'iban' in request.json:
        message += ', iban '
        badFormat = 1
    if not 'asset' in request.json:
        message += ', asset '
        badFormat = 1
    if badFormat == 1:
        abort(400, message)
    checkAddressAndSignature(address, signature)
    hash = hashlib.sha256((address + signature + str(getAssetByKey(request.json["asset"]).json[0]['id']) + str(
        request.json["iban"])).encode('utf-8')).hexdigest()
    hash = hash.upper()
    hash = hash[0:4] + '-' + hash[4:8] + '-' + hash[8:12]
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address= %s AND signature= %s"
    val = (address, signature)
    cur.execute(sql, val)
    rv = cur.fetchall()
    if cur.arraysize > 0:
        sql = "INSERT INTO fiat2crypto (id, address, iban, asset, bank_usage) VALUES (%s, %s, %s, %s, %s)"
        val = (
        address + ":" + str(getAssetByKey(request.json["asset"]).json[0]['id']), address, request.json["iban"],
        getAssetByKey(request.json["asset"]).json[0]['id'], hash)
        cur.execute(sql, val)
        conn.commit()
    else:
        abort(404, 'No User with that legacy address and signature found!')
    conn.close()
    connReg = createDBConnection()
    curReg = connReg.cursor()
    sqlReg = "SELECT * FROM fiat2crypto WHERE id=%s"
    valReg = (address + ":" + str(getAssetByKey(request.json["asset"]).json[0]['id']),)
    curReg.execute(sqlReg, valReg)
    if curReg.arraysize > 0:
        row_headers = [x[0] for x in curReg.description]
        rv = curReg.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        for json_created in json_data:
            json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")
    return jsonify(json_data), 201

# PUT fiat2crypto
@app.server.route('/api/v1/user/<address>/fiat2crypto/<asset>', methods=['PUT'])
@cross_origin()
def updateFiat2Crypto(address,asset):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    badFormat = 0
    message = 'Following data are missing:'
    if not request.json:
        abort(400, 'Data is no JSON')
    if not 'active' in request.json:
        message += 'active'
        badFormat = 1
    if badFormat == 1:
        abort(400, message)
    conn = createDBConnection()
    cur = conn.cursor()
    if request.json['active']:
        sql = "UPDATE fiat2crypto SET active =1 WHERE id=%s"
    else:
        sql = "UPDATE fiat2crypto SET active =0 WHERE id=%s"
    val = (address+":"+asset,)
    cur.execute(sql, val)
    conn.commit()
    return jsonify(getFiat2CryptoById(address,address+":"+asset).json)

# GET crypto2fiat
@app.server.route('/api/v1/user/<address>/crypto2fiat', methods=['GET'])
@cross_origin()
def getCrypto2Fiat(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address=%s AND signature=%s"
    val = (address, signature)
    cur.execute(sql, val)

    if cur.arraysize > 0:
        conn.close()
        connReg = createDBConnection()
        curReg = connReg.cursor()
        sqlReg = "SELECT * FROM crypto2fiat WHERE address=%s"
        curReg.execute(sqlReg, (address,))

        if curReg.arraysize > 0:
            row_headers = [x[0] for x in curReg.description]
            rv = curReg.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            for json_created in json_data:
                json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")
                if json_created['active'] == 0:
                    json_created['active'] = False
                else:
                    json_created['active'] = True
                if 'deposit_id' in json_created:
                    if not json_created['deposit_id'] is None:
                        json_created['deposit_address'] = getDepositByKey(json_created['deposit_id'])[0].json[0][
                            'address']
                    del json_created['deposit_id']

            return jsonify(json_data)
        else:
            jsonify([]), 404, 'No crypto2fiat with requested legacy address and signature found!'
    else:
        abort(404, 'No User with that legacy address and signature found!')


# GET crypto2fiat by id
@app.server.route('/api/v1/user/<address>/crypto2fiat/<id>', methods=['GET'])
@cross_origin()
def getCrypto2FiatByID(address, id):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    if isParameterSQL(id):
        abort(400, 'Invalid id')
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address=%s AND signature=%s"
    val = (address, signature)
    cur.execute(sql, val)

    if cur.arraysize > 0:
        conn.close()
        connReg = createDBConnection()
        curReg = connReg.cursor()
        sqlReg = "SELECT * FROM crypto2fiat WHERE address=%s AND id=%s"
        curReg.execute(sqlReg, (address, id))

        if curReg.arraysize > 0:
            row_headers = [x[0] for x in curReg.description]
            rv = curReg.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            for json_created in json_data:
                json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")
                if json_created['active'] == 0:
                    json_created['active'] = False
                else:
                    json_created['active'] = True
                if 'deposit_id' in json_created:
                    if not json_created['deposit_id'] is None:
                        json_created['deposit_address'] = getDepositByKey(json_created['deposit_id']).json[0][
                            'address']
                    del json_created['deposit_id']
            return jsonify(json_data)
        else:
            jsonify([]), 404, 'No crypto2fiat with requested legacy address and signature found!'
    else:
        abort(404, 'No User with that legacy address and signature found!')


# GET crypto2fiat
@app.server.route('/api/v1/user/<address>/crypto2fiat', methods=['POST'])
@cross_origin()
def addCrypto2Fiat(address):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    badFormat = 0
    message = 'Following data are missing:'
    if not request.json:
        abort(400, 'Data is no JSON')
    if not 'iban' in request.json:
        message += 'iban'
        badFormat = 1
    if not 'fiat' in request.json:
        message += 'fiat'
        badFormat = 1
    if badFormat == 1:
        abort(400, message)
    checkAddressAndSignature(address, signature)
    if not getFiatByKey(request.json["fiat"]).json:
        abort(400, 'Fiat is not available')
    if getUserInternal(address,signature).json['firstname'] == "":
        abort(400, 'Firstname is missing')
    if getUserInternal(address,signature).json['surname'] == "":
        abort(400, 'Surname is missing')
    if getUserInternal(address,signature).json['street'] == "":
        abort(400, 'Street is missing')
    if getUserInternal(address,signature).json['location'] == "":
        abort(400, 'Location is missing')
    if getUserInternal(address,signature).json['zip'] == "":
        abort(400, 'ZIP is missing')
    if getUserInternal(address,signature).json['phone_number'] == "":
        abort(400, 'Phone number is missing')

    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address= %s AND signature= %s"
    val = (address, signature)
    cur.execute(sql, val)
    rv = cur.fetchall()
    if cur.arraysize > 0:

        sql = "SELECT * FROM deposit_address WHERE used= 0 ORDER BY id ASC LIMIT 1"
        cur.execute(sql)
        rv = cur.fetchall()
        row_headers = [x[0] for x in cur.description]
        json_deposit = []
        for result in rv:
            json_deposit.append(dict(zip(row_headers, result)))
        for json_created in json_deposit:
            del json_created['created']
        if json_deposit != []:
            sql = "INSERT INTO crypto2fiat (id, address, fiat,iban, deposit_id) VALUES (%s, %s, %s, %s, %s)"
            val = (request.json['iban'] + ":" + str(getFiatByKey(request.json['fiat']).json[0]['id']), address,
                   str(getFiatByKey(request.json['fiat']).json[0]['id']), request.json["iban"], json_deposit[0]['id'])
            cur.execute(sql, val)
            sql = "UPDATE deposit_address SET used =1 WHERE id=%s"
            val = (json_deposit[0]['id'],)
            cur.execute(sql, val)
            conn.commit()
        else:
            abort(400, 'Please contract support: No deposit address available')
    else:
        abort(404, 'No User with that legacy address and signature found!')

    return jsonify(getCrypto2FiatByID(address, request.json['iban'] + ":" + str(
        getFiatByKey(request.json['fiat']).json[0]['id'])).json), 201


# PUT crypto2fiat
@app.server.route('/api/v1/user/<address>/crypto2fiat/<id>', methods=['PUT'])
@cross_origin()
def updateCrypto2Fiat(address,id):
    signature = request.headers.get('signature').replace(" ", "+")
    checkAddressAndSignature(address, signature)
    badFormat = 0
    message = 'Following data are missing:'
    if not request.json:
        abort(400, 'Data is no JSON')
    if not 'active' in request.json:
        message += 'active'
        badFormat = 1
    if badFormat == 1:
        abort(400, message)
    conn = createDBConnection()
    cur = conn.cursor()
    if request.json['active']:
        sql = "UPDATE crypto2fiat SET active =1 WHERE id=%s"
    else:
        sql = "UPDATE crypto2fiat SET active =0 WHERE id=%s"
    val = (id,)
    cur.execute(sql, val)
    conn.commit()
    return jsonify(getCrypto2FiatByID(address,id).json)

# GET all assets
@app.server.route('/api/v1/asset', methods=['GET'])
@cross_origin()
def getAllAssets():
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM token_info"
    cur.execute(executeString)
    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_assets = []
        for result in rv:
            json_assets.append(dict(zip(row_headers, result)))
        for json_created in json_assets:
            del json_created['created']
            if json_created['buyable'] == 0:
                json_created['buyable'] = False
            else:
                json_created['buyable'] = True
            if json_created['sellable'] == 0:
                json_created['sellable'] = False
            else:
                json_created['sellable'] = True
        return jsonify(json_assets), 201


# GET asset with key
@app.server.route('/api/v1/asset/<key>', methods=['GET'])
@cross_origin()
def getAssetByKey(key):
    if key is None or isParameterSQL(key):
        abort(400, 'Invalid key')
    conn = createDBConnection()
    cur = conn.cursor(buffered=True)
    if isInt(key):
        sql = "SELECT * FROM token_info WHERE id= %s"
    else:
        sql = "SELECT * FROM token_info WHERE name= %s"
    val = (key,)
    cur.execute(sql, val)
    conn.commit()
    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_assets = []
        for result in rv:
            json_assets.append(dict(zip(row_headers, result)))
        for json_created in json_assets:
            del json_created['created']
            if json_created['buyable'] == 0:
                json_created['buyable'] = False
            else:
                json_created['buyable'] = True
            if json_created['sellable'] == 0:
                json_created['sellable'] = False
            else:
                json_created['sellable'] = True
        return jsonify(json_assets), 201


# GET all assets
@app.server.route('/api/v1/fiat', methods=['GET'])
@cross_origin()
def getAllFiat():
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM fiat_info"
    cur.execute(executeString)
    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_assets = []
        for result in rv:
            json_assets.append(dict(zip(row_headers, result)))
        for json_created in json_assets:
            del json_created['created']
            if json_created['enable'] == 0:
                json_created['enable'] = False
            else:
                json_created['enable'] = True
        return jsonify(json_assets), 201


# GET fiat with key
@app.server.route('/api/v1/fiat/<key>', methods=['GET'])
@cross_origin()
def getFiatByKey(key):
    if key is None or isParameterSQL(key):
        abort(400, 'Invalid key')
    conn = createDBConnection()
    cur = conn.cursor(buffered=True)

    if isInt(key):
        sql = "SELECT * FROM fiat_info WHERE id= %s"
    else:
        sql = "SELECT * FROM fiat_info WHERE name= %s"
    val = (key,)
    cur.execute(sql, val)
    conn.commit()
    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_fiat = []
        for result in rv:
            json_fiat.append(dict(zip(row_headers, result)))
        for json_created in json_fiat:
            del json_created['created']
            if json_created['enable'] == 0:
                json_created['enable'] = False
            else:
                json_created['enable'] = True
        return jsonify(json_fiat)

#ADMIN

# Get all data
@app.server.route('/api/v1/allData', methods=['GET'])
@cross_origin()
def getAllData():
    query_parameters = request.args
    auth = query_parameters.get('oAuth')

    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
        if json_admin[0]['oAuth'] == auth:
            executeString = "SELECT * FROM fiat2crypto"
            cur.execute(executeString)

            if cur.arraysize > 0:
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_fiat2crypto = []
                for result in rv:
                    json_fiat2crypto.append(dict(zip(row_headers, result)))
                for json_created in json_fiat2crypto:
                    if json_created['active'] == 0:
                        json_created['active'] = False
                    else:
                        json_created['active'] = True
                    json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")


            executeString = "SELECT * FROM crypto2fiat"
            cur.execute(executeString)

            if cur.arraysize > 0:
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_crypto2fiat = []
                for result in rv:
                    json_crypto2fiat.append(dict(zip(row_headers, result)))
                for json_created in json_crypto2fiat:
                    if json_created['active'] == 0:
                        json_created['active'] = False
                    else:
                        json_created['active'] = True
                    json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")

            executeString = "SELECT * FROM users"
            cur.execute(executeString)

            if cur.arraysize > 0:
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_users = []
                for result in rv:
                    json_users.append(dict(zip(row_headers, result)))
                for json_created in json_users:
                    json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")

            executeString = "SELECT * FROM wallets"
            cur.execute(executeString)

            if cur.arraysize > 0:
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_wallets = []
                for result in rv:
                    json_wallets.append(dict(zip(row_headers, result)))
                for json_created in json_wallets:
                    json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")

            executeString = "SELECT * FROM transactions"
            cur.execute(executeString)

            if cur.arraysize > 0:
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_transactions = []
                for result in rv:
                    json_transactions.append(dict(zip(row_headers, result)))
                for json_created in json_transactions:
                    json_created['created'] = json_created['created'].strftime("%Y-%m-%dT%H:%M:%S")

            json_all = {"fiat2crypto": [], "crypto2fiat": [], "users": [], "wallets": [], "transactions": []}

            json_all['fiat2crypto'] = json_fiat2crypto
            json_all['crypto2fiat'] = json_crypto2fiat
            json_all['users'] = json_users
            json_all['wallets'] = json_wallets
            json_all['transactions'] = json_transactions
            return jsonify(json_all), 201
        else:
            abort(401, 'Unauthorized')


# Add Transaction
@app.server.route('/api/v1/transaction', methods=['POST'])
@cross_origin()
def addTransactiom():
    query_parameters = request.args
    auth = query_parameters.get('oAuth')
    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
        if json_admin[0]['oAuth'] == auth:
            badFormat = 0
            message = 'Following data are missing:'
            if not request.json:
                abort(400, 'Data is no JSON')
            if not 'bank_usage' in request.json:
                message += ', bank_usage'
                badFormat = 1
            if not 'fiat' in request.json:
                message += ', fiat'
                badFormat = 1
            if not 'asset' in request.json:
                message += ', asset'
                badFormat = 1
            if not 'amount' in request.json:
                message += ', amount'
                badFormat = 1
            if not 'fiat_timestamp' in request.json:
                message += ', fiat_timestamp'
                badFormat = 1
            if not 'asset_timestamp' in request.json:
                message += ', asset_timestamp'
                badFormat = 1
            if not 'txid' in request.json:
                message += ', txid'
                badFormat = 1
            if badFormat == 1:
                abort(400, message)
                return jsonify(""), 201
    else:
        abort(401, 'Invalid token')


# PUT asset
@app.server.route('/api/v1/asset', methods=['POST'])
@cross_origin()
def addAsset():
    query_parameters = request.args
    auth = query_parameters.get('oAuth')
    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
        if json_admin[0]['oAuth'] == auth:
            badFormat = 0
            message = 'Following data are missing:'
            if not request.json:
                abort(400, 'Data is no JSON')
            if not 'id' in request.json:
                message += ', id '
                badFormat = 1
            if not 'name' in request.json:
                message += ', name '
                badFormat = 1
            if not 'type' in request.json:
                message += ', type '
                badFormat = 1
            if not 'buyable' in request.json:
                message += ', buyable '
                badFormat = 1
            if not 'sellable' in request.json:
                message += ', sellable '
                badFormat = 1
            if badFormat == 1:
                abort(400, message)

            if getAssetByKey(request.json["id"]) != '[]':
                abort(400, 'Asset exists already')
            if request.json['type'] != 'Coin' and request.json['type'] != 'DAT' and request.json['type'] != 'DCT':
                abort(400, "Type must be 'Coin', 'DAT' or 'DCT'")
            if request.json['buyable'] != '0' and request.json['buyable'] != '1':
                abort(400, "Buyable must be '0' or '1'")
            if request.json['sellable'] != '0' and request.json['sellable'] != '1':
                abort(400, "Sellable must be '0' or '1'")

            sql = "INSERT INTO token_info (id, name, type, buyable, sellable) VALUES (%s, %s, %s, %s, %s)"
            val = (request.json['id'], request.json['name'], request.json['type'], request.json['buyable'],
                   request.json['sellable'])
            cur.execute(sql, val)
            conn.commit()
            return getAssetByKey(request.json["id"]), 201
        else:
            abort(401, 'Unauthorized')


# Change asset with key
@app.server.route('/api/v1/asset/<key>', methods=['PUT'])
@cross_origin()
def updateAsset(key):
    query_parameters = request.args
    auth = query_parameters.get('oAuth')

    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
            if json_admin[0]['oAuth'] == auth:
                if key is None or isParameterSQL(key):
                    abort(400, 'Invalid key')
                conn = createDBConnection()
                cur = conn.cursor(buffered=True)

                if 'id' in request.json:
                    if not isParameterSQL(request.json['id']):
                        changeID = False
                        if isInt(key):
                            sql = "UPDATE token_info SET id =%s WHERE id= %s"
                            changeID = True
                        else:
                            sql = "UPDATE token_info SET id =%s WHERE name= %s"
                        val = (request.json['id'], key)
                        cur.execute(sql, val)
                        conn.commit()
                        if changeID: key = request.json['id']
                if 'name' in request.json:
                    if not isParameterSQL(request.json['name']):
                        changeName = False
                        if isInt(key):
                            sql = "UPDATE token_info SET name =%s WHERE id= %s"
                        else:
                            sql = "UPDATE token_info SET name =%s WHERE name= %s"
                            changeName = True
                        val = (request.json['name'], key)
                        cur.execute(sql, val)
                        conn.commit()
                        if changeName: key = request.json['name']
                if 'type' in request.json:
                    if not isParameterSQL(request.json['type']):
                        if request.json['type'] == 'Coin' or request.json['type'] == 'DAT' or request.json['type'] == 'DCT':
                            if isInt(key):
                                sql = "UPDATE token_info SET type =%s WHERE id= %s"
                            else:
                                sql = "UPDATE token_info SET type =%s WHERE name= %s"
                            val = (request.json['type'], key)
                            cur.execute(sql, val)
                            conn.commit()
                if 'buyable' in request.json:
                    if not isParameterSQL(request.json['buyable']):
                        if type(request.json['buyable']) == bool:
                            if request.json['buyable']:
                                buyable = 1
                            else:
                                buyable = 0
                            if isInt(key):
                                sql = "UPDATE token_info SET buyable =%s WHERE id= %s"
                            else:
                                sql = "UPDATE token_info SET buyable =%s WHERE name= %s"
                            val = (buyable, key)
                            cur.execute(sql, val)
                            conn.commit()
                if 'sellable' in request.json:
                    if not isParameterSQL(request.json['sellable']):
                        if type(request.json['sellable']) == bool:
                            if request.json['sellable']:
                                sellable = 1
                            else:
                                sellable = 0
                            if isInt(key):
                                sql = "UPDATE token_info SET sellable =%s WHERE id= %s"
                            else:
                                sql = "UPDATE token_info SET sellable =%s WHERE name= %s"
                            val = (sellable, key)
                            cur.execute(sql, val)
                            conn.commit()
                return getAssetByKey(key), 201
            else:
                abort(401, 'Unauthorized')


# PUT asset
@app.server.route('/api/v1/fiat', methods=['POST'])
@cross_origin()
def addFiat():
    query_parameters = request.args
    auth = query_parameters.get('oAuth')
    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
        if json_admin[0]['oAuth'] == auth:
            badFormat = 0
            message = 'Following data are missing:'
            if not request.json:
                abort(400, 'Data is no JSON')
            if not 'id' in request.json:
                message += ', id '
                badFormat = 1
            if not 'name' in request.json:
                message += ', name '
                badFormat = 1
            if not 'enable' in request.json:
                message += ', enable '
                badFormat = 1
            if badFormat == 1:
                abort(400, message)

            if getFiatByKey(request.json["id"]).json != []:
                abort(400, 'Fiat already exists')
            if type(request.json['enable']) != bool:
                abort(400, "Enable must be boolean")

            if request.json['enable']:
                enable = 1
            else:
                enable = 0
            sql = "INSERT INTO fiat_info (id, name, enable) VALUES (%s, %s, %s)"
            val = (request.json['id'], request.json['name'],enable)
            cur.execute(sql, val)
            conn.commit()
            return jsonify(getFiatByKey(request.json["id"]).json), 201
        else:
            abort(401, 'Unauthorized')


# POST asset with key
@app.server.route('/api/v1/fiat/<key>', methods=['PUT'])
@cross_origin()
def updateFiat(key):
    query_parameters = request.args
    auth = query_parameters.get('oAuth')

    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
            if json_admin[0]['oAuth'] == auth:
                if key is None or isParameterSQL(key):
                    abort(400, 'Invalid key')
                conn = createDBConnection()
                cur = conn.cursor(buffered=True)
                if getFiatByKey(key).json == []:
                    abort(400, "ID is not available")

                if 'id' in request.json:
                    if not isParameterSQL(request.json['id']):
                        if key != request.json['id']:
                            if getFiatByKey(request.json['id']).json != []:
                                abort(400, "ID already exists")
                        changeID = False
                        if isInt(key):
                            sql = "UPDATE fiat_info SET id =%s WHERE id= %s"
                            changeID = True
                        else:
                            sql = "UPDATE fiat_info SET id =%s WHERE name= %s"
                        val = (request.json['id'], key)
                        cur.execute(sql, val)
                        conn.commit()
                        if changeID: key = request.json['id']
                if 'name' in request.json:
                    if not isParameterSQL(request.json['name']):
                        changeName = False
                        if isInt(key):
                            sql = "UPDATE fiat_info SET name =%s WHERE id= %s"
                        else:
                            sql = "UPDATE fiat_info SET name =%s WHERE name= %s"
                            changeName = True
                        val = (request.json['name'], key)
                        cur.execute(sql, val)
                        conn.commit()
                        if changeName: key = request.json['name']
                if 'enable' in request.json:
                    if not isParameterSQL(request.json['enable']):
                        if type(request.json['enable']) != bool:
                            abort(400, "Enable must be boolean")
                        if isInt(key):
                            sql = "UPDATE fiat_info SET enable =%s WHERE id= %s"
                        else:
                            sql = "UPDATE fiat_info SET enable =%s WHERE name= %s"

                        if request.json['enable']:
                            enable = 1
                        else:
                            enable = 0
                        val = (enable, key)
                        cur.execute(sql, val)
                        conn.commit()
                return jsonify(getFiatByKey(key).json)
            else:
                abort(401, 'Unauthorized')


# PUT asset
@app.server.route('/api/v1/deposit', methods=['POST'])
@cross_origin()
def addDeposit():
    query_parameters = request.args
    auth = query_parameters.get('oAuth')
    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
        if json_admin[0]['oAuth'] == auth:
            badFormat = 0
            message = 'Following data are missing:'
            if not request.json:
                abort(400, 'Data is no JSON')
            if not 'address' in request.json:
                message += ', address'
                badFormat = 1
            if badFormat == 1:
                abort(400, message)

            sql = "INSERT INTO deposit_address (address) VALUES (%s)"
            val = (request.json['address'],)
            cur.execute(sql, val)
            conn.commit()
            return jsonify(getDepositByKey(request.json["address"])[0].json), 201
        else:
            abort(401, 'Unauthorized')


# POST asset with key
@app.server.route('/api/v1/deposit/<key>', methods=['PUT'])
@cross_origin()
def updateDeposit(key):
    query_parameters = request.args
    auth = query_parameters.get('oAuth')

    if isParameterSQL(auth):
        abort(401, 'Invalid token')
    conn = createDBConnection()
    cur = conn.cursor()
    executeString = "SELECT * FROM admin"
    cur.execute(executeString)

    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_admin = []
        for result in rv:
            json_admin.append(dict(zip(row_headers, result)))
            if json_admin[0]['oAuth'] == auth:
                if key is None or isParameterSQL(key):
                    abort(400, 'Invalid key')
                conn = createDBConnection()
                cur = conn.cursor(buffered=True)
                if 'used' in request.json:
                    if not isParameterSQL(request.json['used']):
                        if type(request.json['used']) != bool:
                            abort(400, "Used must be boolean")
                        if isInt(key):
                            sql = "UPDATE deposit_address SET used =%s WHERE id= %s"
                        else:
                            sql = "UPDATE deposit_address SET used =%s WHERE address= %s"
                        if request.json['used']:
                            used = 1
                        else:
                            used = 0
                        val = (used, key)
                        cur.execute(sql, val)
                        conn.commit()
                return jsonify(getDepositByKey(key).json)
            else:
                abort(401, 'Unauthorized')


# Help functions

def createDBConnection():
    try:
        conn = mysql.connector.connect(
            user=config_file.user,
            password=config_file.password,
            host=config_file.host,
            port=config_file.port,
            database=config_file.database)
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def isParameterSQL(param):
    param = str(param).upper()
    if ('SELECT' in param or
            'FROM' in param or
            'WHERE' in param or
            'ORDER' in param or
            'BY' in param or
            'GROUP' in param or
            'INSERT' in param or
            'INTO' in param or
            'DELETE' in param or
            'UPDATE' in param or
            'CREATE' in param or
            'INDEX' in param or
            'VIEW' in param or
            'DROP' in param or
            'TABLE' in param or
            'ALTER' in param):
        return True
    else:
        return False


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def checkAddressAndSignature(address, signature):
    if address is None or isParameterSQL(address):
        abort(400, 'Legacy address is missing')
    if signature is None or isParameterSQL(signature):
        abort(400, "Signature not found")
    if not address.startswith('8') or not len(address) == 34:
        abort(400, 'Legacy address is wrong')
    if signature is None or isParameterSQL(signature):
        abort(400, 'Signature is missing')
    if not len(signature) == 88 or not signature.endswith('='):
        abort(400, 'Signature is wrong')
    return True


def getDepositByKey(key):
    if key is None or isParameterSQL(key):
        abort(400, 'Invalid key')
    conn = createDBConnection()
    cur = conn.cursor(buffered=True)

    if isInt(key):
        sql = "SELECT * FROM deposit_address WHERE id= %s"
    else:
        sql = "SELECT * FROM deposit_address WHERE address= %s"
    val = (key,)
    cur.execute(sql, val)
    conn.commit()
    if cur.arraysize > 0:
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_deposit = []
        for result in rv:
            json_deposit.append(dict(zip(row_headers, result)))
        for json_created in json_deposit:
            del json_created['created']
        return jsonify(json_deposit)


def getUserInternal(address, internal_signature):
    signature = internal_signature
    checkAddressAndSignature(address, signature)
    conn = createDBConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM users WHERE address = %s AND signature = %s"
    val = (address, signature)
    cur.execute(sql, val)
    rv = cur.fetchall()
    if len(rv) > 0:
        row_headers = [x[0] for x in cur.description]
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        json_data[0]['created'] = json_data[0]['created'].strftime("%Y-%m-%dT%H:%M:%S")
        json_data[0]['ref'] = str(json_data[0]['ref']).zfill(6)[0:3] + '-' + str(json_data[0]['ref']).zfill(6)[3:7]
        json_data[0]['used_ref'] = str(json_data[0]['used_ref']).zfill(6)[0:3] + '-' + str(
            json_data[0]['used_ref']).zfill(6)[3:7]
        return jsonify(json_data[0])
    else:
        abort(404, 'No User with that legacy address and signature found!')
