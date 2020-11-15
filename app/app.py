from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'heightsAndWeightsData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def retrieve_all_heights_and_weights():
    user = {'username': 'Josh'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightsAndWeights')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, heightsAndWeights=result)


@app.route('/view/<int:height_and_weight_id>', methods=['GET'])
def record_view(height_and_weight_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightsAndWeights WHERE id=%s', height_and_weight_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', heightAndWeight=result[0])


@app.route('/edit/<int:height_and_weight_id>', methods=['GET'])
def form_edit_get(height_and_weight_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightsAndWeights WHERE id=%s', height_and_weight_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', heightAndWeight=result[0])


@app.route('/edit/<int:height_and_weight_id>', methods=['POST'])
def form_update_post(height_and_weight_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('heightInches'), request.form.get('weightPounds'), height_and_weight_id)
    sql_update_query = """UPDATE tableHeightsAndWeights t SET t.heightInches = %s, t.weightPounds = %s  WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/heightsAndWeights/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Height and Weight Form')


@app.route('/heightsAndWeights/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('heightInches'), request.form.get('weightPounds'))
    sql_insert_query = """INSERT INTO tableHeightsAndWeights (heightInches, weightPounds) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:height_and_weight_id>', methods=['POST'])
def form_delete_post(height_and_weight_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tableHeightsAndWeights WHERE id = %s """
    cursor.execute(sql_delete_query, height_and_weight_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/heightsAndWeights', methods=['GET'])
def retrieve_full_json() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tableHeightsAndWeights')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    return Response(json_result, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
