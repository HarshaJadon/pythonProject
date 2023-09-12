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


@app.route("/v1/delete_rules", methods=['POST'])
def get_delete_rules_v1():
    request_json = request.get_json()
    if request_json and 'id' in request_json:
        row_id = request_json['id']
    else:
        return "Attributes missing"

    PROJECT_ID = 'snmp-poc-indus'

    BQ_DATASET = 'indus_poc'

    BQ_TABLE = 'indus_rules'

    table = BQ.get_table(f'{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}')

    # row = {u"SiteId": siteid, u"Parameter": param, u"Operator": operator, u"Value": value, u"EmailId": emailid, u"SetParameter": setparam, u"SetValue": setvalue, u"CreationTime": creationtime}
    print("Rowids:", row_id)

    if len(row_id) == 1:
        delete_query = f"delete from `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}` where id in ({int(row_id[0])})"
    else:
        delete_query = f"delete from `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}` where id in {tuple(int(item) for item in row_id)}"
    print("delete query: ", delete_query)
    query_job = BQ.query(delete_query)  # retry=retry.Retry(deadline=30))
    # result = query_job.result()

    if query_job.errors:
        print("Errors occurred during the deletion:")
        for error in query_job.errors:
            print("Error statement:", error)
        return 'false'
    else:
        print("Row successfully deleted from BigQuery table.")
        return 'true'


if __name__ == '__main__':
    app.run(debug=True)
