#!/usr/bin/env python3
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)
CORS(app)
table_path = "table.csv"


class table_class:
    def __init__(self, table_path):
        '''column[0] port
        column[1] id
        columns[2] name #any column_name
        column[-2] threshold #any column_name
        column[-1] value #any column_name'''
        

        self.table_path = table_path
        table_df = pd.read_csv(self.table_path)
        self.id_name = "id"
        self.threshold_name = list(table_df.columns)[-2]
        self.dict_column_names = [self.id_name, "port"]
        self.send_column_names = list(table_df.columns)[1:]
        self.id_port_dict = table_df[["id", "port"]].set_index('id').to_dict("index")
    
    def send_df(self):
        df = pd.read_csv(self.table_path)
        return df[self.send_column_names]

    def update_table(self, id, column_name, value):
        df = pd.read_csv(self.table_path)
        index = df[df[self.id_name] == id].index[0]
        df.loc[index, column_name] = value
        df.to_csv(table_path, index = None)

table = table_class(table_path)


@app.route("/", methods = ["GET"])
def index():
    return render_template("page.html", dataframe=table.send_df())



@app.route("/<id>", methods = ["GET", "POST"])
def return_values(id):
    if request.method == 'GET':
        data = {"data":100} 
        return jsonify(data)

    elif request.method =="POST":
        data = request.json
        print(data)
        column_name = data["column"]
        value = data["value"]
        table.update_table(id, column_name, value)
        return jsonify({"status":200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
