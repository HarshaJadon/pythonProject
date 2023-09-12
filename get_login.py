from flask import Flask
from flask_cors import CORS, cross_origin
import requests
from flask import request
#from google.cloud import bigquery
import google.cloud.bigquery
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=['GET'])
def welcome():
    return "Hello world!"


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\harsha_jadon\Downloads\snmp-poc-indus-3d039bda581d.json"
BQ = google.cloud.bigquery.Client()
#GOOGLE_APPLICATION_CREDENTIAL = r"C:\Users\harsha_jadon\Downloads\snmp-poc-indus-e5c1cb3b5358.json"


@app.route("/v1/login", methods=['POST'])
def get_login_v1():

    request_json = request.get_json()
    if request_json and 'username' in request_json:
        username = request_json['username']
    else:
        return ("Attribute username missing", 422, headers)

    print("username:", username)

    PROJECT_ID = 'snmp-poc-indus'

    BQ_DATASET = 'indus_poc'

    BQ_TABLE = 'indus_login'

    table = BQ.get_table(f'{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}')

    query_string = f'SELECT password FROM `{table}` where username = "{username}"'
    print("Query String:", query_string)

    resultset = BQ.query(query_string)
    # df = resultset.to_dataframe()

    for row in resultset:
        # Row values can be accessed by field name or index.
        result = row["password"]

    # data = json.loads(df.to_json())
    # return data
    data = [{"password": str(result)}]
    print("data:", data)
    return (data)
    # print("Result:", str(result))
    # return (str(result))


if __name__ == '__main__':
    app.run(debug=True)
