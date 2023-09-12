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


@app.route("/v1/rules_log", methods=['POST'])
def get_rules_log_v1():

    request_json = request.get_json()
    if request_json and 'siteid' in request_json:
        siteid = request_json['siteid']
        record_count = request_json['recordcount']
    else:
        return ("Attributes <siteid> <recordcount> missing", 422, headers)

    print("siteid:", siteid, "record count:", record_count)

    PROJECT_ID = 'snmp-poc-indus'

    BQ_DATASET = 'indus_poc'

    BQ_TABLE = 'indus_rules_log'

    table = BQ.get_table(f'{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}')

    if siteid.upper() == 'ALL':
        query_string = f'SELECT SiteId, Parameter, Operator, Value, CurrentValue, EmailId, SetParameter, SetValue, RuleCondition, SetResult, EmailResult, FORMAT_DATE("%d-%m-%Y %H:%M:%S",DATETIME(ProcessTime, "Asia/Calcutta")) as ProcessTime FROM `{table}` order by ProcessTime desc LIMIT {record_count}'
    else:
        query_string = f'SELECT SiteId, Parameter, Operator, Value, CurrentValue, EmailId, SetParameter, SetValue, RuleCondition, SetResult, EmailResult, FORMAT_DATE("%d-%m-%Y %H:%M:%S",DATETIME(ProcessTime, "Asia/Calcutta")) as ProcessTime FROM `{table}` where siteid = "{siteid}" order by ProcessTime desc LIMIT {record_count}'
    print("Query String:", query_string)

    resultset = BQ.query(query_string)
    df = resultset.to_dataframe()

    # for row in resultset:
    #    # Row values can be accessed by field name or index.
    #    result = row["param_value"]
    # data = json.loads(df.to_json())
    # return data
    data = df.to_dict('records')
    print("Result:", data)
    return (data)

if __name__ == '__main__':
    app.run(debug=True)
