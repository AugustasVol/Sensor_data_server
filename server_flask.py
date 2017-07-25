#!/usr/bin/env python3
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from random import randrange
import helper
import os
app = Flask(__name__)
CORS(app)



table_path = "table.csv"
lang = helper.language()
table = helper.table_class(table_path, table_column_names=lang.table_column_names)
sensors = helper.sensor_data()




@app.route("/", methods = ["GET"])
def index():
    return render_template("page.html", dataframe=table.send_df(), heading=lang.lang_pack["heading"], change_name=lang.lang_pack["change_name"], refresh_name = lang.lang_pack["refresh_name"])



@app.route("/<id>", methods = ["GET", "POST"])
def return_values(id):
    if request.method == 'GET':

        data = { "data" : sensors.get(id) } 
        
        return jsonify(data)

    elif request.method =="POST":
        data = request.json
        print(data)
        column_number = data["column"]
        value = data["value"]
        table.update_table(id, column_number, value)
        return jsonify({"status":200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
