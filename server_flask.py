#!/usr/bin/env python3
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)
CORS(app)
table_path = "table.csv"

table_df = pd.read_csv(table_path)
head = list(table_df.columns)
print(head)
head_send = head[0:4] # no port


@app.route("/", methods = ["GET"])
def index():
        
    return render_template("page.html", dataframe=table_df[head_send])



@app.route('/<id>', methods = ['GET'])
def return_values(id):

    data = {"data":100}	
    return jsonify(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


  
