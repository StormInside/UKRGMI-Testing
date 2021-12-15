from flask import Flask, jsonify, request, abort
import sqlite3

database_name = 'sqlite_python.db'
connection = sqlite3.connect(database_name, check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

get_cities_code = '''SELECT name FROM sqlite_schema
                    WHERE type ='table' AND name NOT LIKE 'sqlite_%';'''


@app.route('/cities')
def return_cities():
    cursor.execute(get_cities_code)

    cities = []
    for city in cursor.fetchall():
        cities.append(city[0])

    return jsonify(cities)


@app.route('/mean')
def return_mean():
    value_type = request.args.get('value_type')
    city = request.args.get('city')

    if value_type == 'temp': value_type = 'w_temp'

    try:
        cursor.execute(f'SELECT AVG({value_type}) FROM {city}')
    except sqlite3.OperationalError:
        abort(404, description=f"Wrong parameters")
    
    data = []
    for war in cursor.fetchall():
        data.append(war[0])
    
    return jsonify(data)


@app.route('/records')
def return_records():
    start_dt = request.args.get('start_dt')
    end_dt = request.args.get('end_dt')
    city = request.args.get('city')

    try:
        cursor.execute(f"SELECT * FROM {city} where w_date >= '{start_dt}' and w_date <= '{end_dt}';")
    except sqlite3.OperationalError:
        abort(404, description=f"Wrong parameters")
    
    columns = [column[0] for column in cursor.description]

    data = []
    for war in cursor.fetchall():
        data.append(dict(zip(columns, war)))

    return jsonify(data)


@app.route('/moving_mean')
def return_moving_mean():
    value_type = request.args.get('value_type')
    city = request.args.get('city')

    if value_type == 'temp': value_type = 'w_temp'

    try:
        cursor.execute(f'SELECT {value_type} FROM {city}')
    except sqlite3.OperationalError:
        abort(404, description=f"Wrong parameters")

    data = []
    for row in cursor.fetchall():
        data.append(row[0])

    moving_avg = moving_averange(data, 7)

    return jsonify(moving_avg)
    

def moving_averange(data, window):
    i=0
    result = []
    while i<len(data) - window+1:
        i_window = data[i:i+window]
        window_avg = sum(i_window) / window
        result.append(window_avg)
        i+=1
    
    return result


@app.errorhandler(404)
def page_not_found(error):
   return jsonify(error=str(error)), 404
