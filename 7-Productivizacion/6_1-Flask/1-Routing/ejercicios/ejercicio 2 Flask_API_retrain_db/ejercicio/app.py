from copyreg import pickle
from turtle import pd
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import csv, sqlite3, json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.config["DEBUG"] = True

'''
La petición sería:
http://127.0.0.1:5000/api/v1/adv/create_db
'''

@app.route('/api/v1/adv/create_db', methods = ['GET'])
def createdb():

    con = sqlite3.connect(r'C:\Users\Admin\Documents\GitHub\ds-nov23-thebridge\7-Productivizacion\6_1-Flask\1-Routing\ejercicios\ejercicio 2 Flask_API_retrain_db\ejercicio\advertising.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS t;")
    cur.execute("CREATE TABLE t (TV, radio, newspaper, sales);")

    with open('C:\Users\Admin\Documents\GitHub\ds-nov23-thebridge\7-Productivizacion\6_1-Flask\1-Routing\ejercicios\ejercicio 2 Flask_API_retrain_db\ejercicio\Advertising.csv', 'r') as fin:
        dr = csv.DictReader(fin) # la coma es el separador por defecto
        to_db = [(i['TV'], i['radio'], i['newspaper'], i['sales']) for i in dr]
        cur.executemany("INSERT INTO t (TV, radio, newspaper, sales) VALUES (?,?,?,?);", to_db)

    con.commit()
    con.close()

    return jsonify(list({'TV': i[0], 'radio': i[1], 'newspaper': i[2], 'sales': i[3]} for i in to_db))

"""
La petición sería:
http://127.0.0.1:5000/api/v1/adv_model/predict?TV=180&radio=15&newspaper=60
"""
@app.route('/api/v1/adv_model/predict', methods = ['GET'])
def predict():
    args = request.args
    if 'TV' in args and 'radio' in args and 'newspaper' in args:
        with open('C:\Users\Admin\Documents\GitHub\ds-nov23-thebridge\7-Productivizacion\6_1-Flask\1-Routing\ejercicios\ejercicio 2 Flask_API_retrain_db\ejercicio\advertising.model', 'rb') as archivo_entrada:
            model = pickle.load(archivo_entrada)
        
        tv = args.get('TV', None)
        radio = args.get('radio', None)
        newspaper = args.get('newspaper', None)

        if tv is None or radio is None or newspaper is None:
            return "Error. Args empty"
        else:
            predictions = model.predict([[float(tv), float(radio), float(newspaper)]])
            return jsonify({"predictions": list(predictions)})
    else:
        return "Error in args"









app.run()