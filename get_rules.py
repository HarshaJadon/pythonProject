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


@app.route("/v1/rules", methods=['POST'])
def get_rules_v1():

    request_json = request.get_json()
    AUTH_URL = "https://www.googleapis.com/auth/bigquery"

    if request_json and 'siteid' in request_json:
        siteid = request_json['siteid']
    else:
        return ("Attributes <siteid> missing", 422, headers)

    print("siteid:", siteid)

    PROJECT_ID = 'snmp-poc-indus'

    BQ_DATASET = 'indus_poc'

    BQ_TABLE = 'indus_rules'

    table = BQ.get_table(f'{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}')

    if siteid.upper() == 'ALL':
        query_string = f'SELECT CAST(Id as STRING) Id, SiteId, Parameter, Operator, value, EmailId, SetParameter, SetValue, FORMAT_DATE("%d-%m-%Y %H:%M:%S",DATETIME(CreationTime, "Asia/Calcutta")) as CreationTime FROM `{table}` order by CreationTime desc'
    else:
        query_string = f'SELECT CAST(Id as STRING) Id, SiteId, Parameter, Operator, value, EmailId, SetParameter, SetValue, FORMAT_DATE("%d-%m-%Y %H:%M:%S",DATETIME(CreationTime, "Asia/Calcutta")) as CreationTime FROM `{table}` where siteid = "{siteid}" order by CreationTime desc'
    print("Query String:", query_string)

    resultset = BQ.query(query_string)
    df = resultset.to_dataframe()

    # for row in resultset:
    #    # Row values can be accessed by field name or index.
    #    result = row["param_value"]
    # data = json.loads(df.to_json())
    # return data
    # df['IdStr'] = df['Id'].apply(lambda x: x.decode('latin1') if x is not None else '')
    # df['cleaned_Id'] = df['IdStr'].str.replace(r'[^\x00-\x7F]', '')
    # df = df.drop(["Id","IdStr"],axis=1)
    data = df.to_dict('records')
    print("Result:", data)
    return (data)


if __name__ == '__main__':
    app.run(debug=True)
