from flask import Flask, Response, jsonify, request
import json
import MySQLdb

db = MySQLdb.connect(
    host = 'mysqldb',
    port = 3306,
    user = 'admin',
    password = 'admin',
    db = 'Meteo'
)

cursor = db.cursor()

app = Flask(__name__)

@app.route('/api/countries', methods=['POST'])
def post_countries():
    # get body
    payload = request.get_json(silent=True)

    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine 3 intrari returnam 400
    if (payload is None or 'nume' not in payload.keys() or
        'lat' not in payload.keys() or 'lon' not in payload.keys() or
        len(payload) != 3):
        return Response(status=400)

    # daca am deja am numele tarii in bd se intoarce 409
    cursor.execute("SELECT * FROM Tari where nume_tara = %s", [payload['nume']])
    query_result = cursor.fetchone()
    
    if (query_result is not None):
        return Response(status=409)

    # daca intrarea este noua, inseram valorile in tabela
    sql = "INSERT INTO Tari (nume_tara, latitudine, longitudine) \
        VALUES (%s, %s, %s)"
    val = (payload['nume'], payload['lat'], payload['lon'])
    cursor.execute(sql, val)

    db.commit()

    # intorc randul daca exista tara in baza de date
    cursor.execute("SELECT * FROM Tari WHERE nume_tara = %s", [payload['nume']])
    query_result = cursor.fetchone()

    # return 201 si un obiect json cu id (cu ajutorul json.dumbs)
    return Response(status=201, response=json.dumps({'id': int(query_result[0])}), mimetype='application/json')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    # extragere randuri
    cursor.execute("SELECT * FROM Tari")
    query_result = cursor.fetchall()

    # adaugare in lista de dictionare valoarile de pe fiecare rand
    json_lst = []
    for row in query_result:
        row_dict = {}
        row_dict['id'] = row[0]
        row_dict['nume'] = row[1]
        row_dict['lat'] = row[2]
        row_dict['lon'] = row[3]
        json_lst.append(row_dict)

    # returnare 200 si lista de obiecte
    return Response(status=200, response=json.dumps(json_lst), mimetype='application/json')

@app.route('/api/countries/<int:given_id>', methods=['PUT'])
def put_countries(given_id):

    payload = request.get_json(silent=True)

    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine 4 intrari returnam 400
    if (payload is None or 'id' not in payload.keys() or
        'nume' not in payload.keys() or 'lat' not in payload.keys() or 
        'lon' not in payload.keys() or len(payload) != 4):
        return Response(status=400)
    
    # daca tara din payload deja exista in baza de date, la un id diferit,
    # in caz ca incercam sa facem un update, vom avea duplicate entry
    sql = "SELECT * FROM Tari where nume_tara = %s and id != %s"
    val = (payload['nume'], str(given_id))
    cursor.execute(sql, val)
    query_result = cursor.fetchone()

    if (query_result is not None):
        return Response(status=400)

    # query pentru a scoate randul cu tara care are id-ul dat
    cursor.execute("SELECT * FROM Tari where id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)
    
    # daca query-ul a gasit intrare actualizez id-ul
    sql = "UPDATE Tari SET nume_tara = %s, latitudine = %s, longitudine = %s \
        WHERE id = %s"
    val = (payload['nume'], payload['lat'], payload['lon'], str(given_id))
    cursor.execute(sql, val)

    db.commit()

    return Response(status=200)

@app.route('/api/countries/<int:given_id>', methods=['DELETE'])
def delete_countries(given_id):
    # daca avem un id care nu este integer
    if (isinstance(given_id, int)) is not True:
        return Response(status=400)
    
    # query pentru a scoate randul cu tara care are id-ul dat
    cursor.execute("SELECT * FROM Tari where id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    cursor.execute("DELETE FROM Tari where id = %s", [str(given_id)])

    db.commit()

    return Response(status=200)

@app.route('/api/cities', methods=['POST'])
def post_cities():
    # get body
    payload = request.get_json(silent=True)

    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine 4 intrari returnam 400
    if (payload is None or 'idTara' not in payload.keys() or
        'nume' not in payload.keys() or 'lat' not in payload.keys() or 
        'lon' not in payload.keys() or len(payload) != 4):
        return Response(status=400)

    # daca am deja numele orasului in bd se intoarce 409
    cursor.execute("SELECT * FROM Orase where nume_oras = %s", [payload['nume']])
    query_result = cursor.fetchone()

    if (query_result is not None):
        return Response(status=409)

    # daca intrarea este noua, inseram valorile in tabela
    sql = "INSERT INTO Orase (id_tara, nume_oras, latitudine, longitudine) \
        VALUES (%s, %s, %s, %s)"
    val = (payload["idTara"], payload['nume'], payload['lat'], payload['lon'])
    cursor.execute(sql, val)

    db.commit()

    # intorc randul daca exista orasul in baza de date
    cursor.execute("SELECT * FROM Orase WHERE nume_oras = %s", [payload['nume']])
    query_result = cursor.fetchone()

    # return 201 si un obiect json cu id (cu ajutorul json.dumbs)
    return Response(status=201, response=json.dumps({'id': int(query_result[0])}), mimetype='application/json')

@app.route('/api/cities', methods=['GET'])
def get_cities():
    # extragere randuri
    cursor.execute("SELECT * FROM Orase")
    query_result = cursor.fetchall()

    # adaugare in lista de dictionare valoarile de pe fiecare rand
    json_lst = []
    for row in query_result:
        row_dict = {}
        row_dict['id'] = row[0]
        row_dict['idTara'] = row[1]
        row_dict['nume'] = row[2]
        row_dict['lat'] = row[3]
        row_dict['lon'] = row[4]
        json_lst.append(row_dict)

    # returnare 200 si lista de obiecte
    return Response(status=200, response=json.dumps(json_lst), mimetype='application/json')

@app.route('/api/cities/country/<int:given_id>', methods=['GET'])
def get_cities_by_country_id(given_id):
    # extragere randuri
    cursor.execute("SELECT * FROM Orase WHERE id_tara = %s", [str(given_id)])
    query_result = cursor.fetchall()

    # adaugare in lista de dictionare valoarile de pe fiecare rand
    json_lst = []
    for row in query_result:
        row_dict = {}
        row_dict['id'] = row[0]
        row_dict['idTara'] = row[1]
        row_dict['nume'] = row[2]
        row_dict['lat'] = row[3]
        row_dict['lon'] = row[4]
        json_lst.append(row_dict)

    # returnare 200 si lista de obiecte
    return Response(status=200, response=json.dumps(json_lst), mimetype='application/json')

@app.route('/api/cities/<int:given_id>', methods=['PUT'])
def put_cities(given_id):

    payload = request.get_json(silent=True)

    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine 5 intrari returnam 400
    if (payload is None or 'id' not in payload.keys() or 'idTara' not in payload.keys() or
        'nume' not in payload.keys() or 'lat' not in payload.keys() or 
        'lon' not in payload.keys() or len(payload) != 5):
        return Response(status=400)
    
    # daca orasul din payload deja exista in baza de date, la un id diferit,
    # in caz ca incercam sa facem un update, vom avea duplicate entry
    sql = "SELECT * FROM Orase WHERE nume_oras = %s and id != %s"
    val = (payload['nume'], str(given_id))
    cursor.execute(sql, val)
    query_result = cursor.fetchone()

    if (query_result is not None):
        return Response(status=400)
    
    # query pentru a scoate randul cu tara care are id-ul dat
    cursor.execute("SELECT * FROM Tari WHERE id = %s", [payload['idTara']])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    # query pentru a scoate randul cu orasul care are id-ul dat
    cursor.execute("SELECT * FROM Orase WHERE id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)
    
    # daca query-ul a gasit intrare actualizez id-ul
    sql = "UPDATE Orase SET id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s \
        WHERE id = %s"
    val = (payload['idTara'], payload['nume'], payload['lat'], payload['lon'], str(given_id))
    cursor.execute(sql, val)

    db.commit()

    return Response(status=200)

@app.route('/api/cities/<int:given_id>', methods=['DELETE'])
def delete_cities(given_id):
    # daca avem un id care nu este integer
    if (isinstance(given_id, int)) is not True:
        return Response(status=400)
    
    # query pentru a scoate randul cu tara care are id-ul dat
    cursor.execute("SELECT * FROM Orase where id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    cursor.execute("DELETE FROM Orase where id = %s", [str(given_id)])

    db.commit()

    return Response(status=200)

@app.route('/api/temperatures', methods=['POST'])
def post_temperatures():
    payload = request.get_json(silent=True)
    
    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine de 2 intrari returnam 400
    if (payload is None or 'idOras' not in payload.keys() or
        'valoare' not in payload.keys() or len(payload) != 2):
        return Response(status=400)

    # daca orasul nu exista in tabela de orase se intoarce 409
    cursor.execute("SELECT * FROM Orase where id = %s", [payload['idOras']])
    query_result = cursor.fetchone()

    if (query_result is None):
        return Response(status=409)

    # daca am deja am id-ul orasului in bd se intoarce 409
    cursor.execute("SELECT * FROM Temperaturi where id_oras = %s", [payload['idOras']])
    query_result = cursor.fetchone()

    if (query_result is not None):
        return Response(status=409)

    # daca intrarea este noua, inseram valorile in tabela
    sql = "INSERT INTO Temperaturi (valoare, id_oras) \
        VALUES (%s, %s)"
    val = (payload["valoare"], payload['idOras'])
    cursor.execute(sql, val)

    db.commit()

    # intorc randul daca exista orasul in baza de date
    cursor.execute("SELECT * FROM Temperaturi WHERE id_oras = %s", [payload['idOras']])
    query_result = cursor.fetchone()

    # return 201 si un obiect json cu id (cu ajutorul json.dumbs)
    return Response(status=201, response=json.dumps({'id': int(query_result[0])}), mimetype='application/json')

@app.route('/api/temperatures/<int:given_id>', methods=['PUT'])
def put_temperatures(given_id):

    payload = request.get_json(silent=True)

    # daca body-ul este null sau daca una dintre chei este nula sau daca
    # body-ul nu contine 3 intrari returnam 400
    if (payload is None or 'id' not in payload.keys() or 'idOras' not in payload.keys() or
        'valoare' not in payload.keys() or len(payload) != 3):
        return Response(status=400)

    # daca orasul din payload deja exista in baza de date, la un id diferit,
    # in caz ca incercam sa facem un update, vom avea duplicate entry
    sql = "SELECT * FROM Temperaturi WHERE id_oras = %s and id != %s"
    val = (payload['idOras'], str(given_id))
    cursor.execute(sql, val)
    query_result = cursor.fetchone()

    if (query_result is not None):
        return Response(status=400)

    # query pentru a scoate randul cu orasul care are id-ul dat
    cursor.execute("SELECT * FROM Orase WHERE id = %s", [payload['idOras']])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    # query pentru a scoate randul cu temperatura care are id-ul dat
    cursor.execute("SELECT * FROM Temperaturi WHERE id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    # daca query-ul a gasit intrare actualizez id-ul
    sql = "UPDATE Temperaturi SET valoare = %s, id_oras = %s \
        WHERE id = %s"
    val = (payload['valoare'], payload['idOras'], str(given_id))
    cursor.execute(sql, val)

    db.commit()

    return Response(status=200)

@app.route('/api/temperatures/<int:given_id>', methods=['DELETE'])
def delete_temperatures(given_id):
    # daca avem un id care nu este integer
    if (isinstance(given_id, int)) is not True:
        return Response(status=400)
    
    # query pentru a scoate randul cu tara care are id-ul dat
    cursor.execute("SELECT * FROM Temperaturi where id = %s", [str(given_id)])
    query_result = cursor.fetchone()

    # daca query-ul nu a gasit nicio intrare, returnez 404
    if (query_result is None):
        return Response(status=404)

    cursor.execute("DELETE FROM Temperaturi where id = %s", [str(given_id)])

    db.commit()

    return Response(status=200)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
