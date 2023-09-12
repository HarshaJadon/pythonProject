from flask import Flask
from flask_cors import CORS, cross_origin
import requests
from flask import request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=['GET'])
def welcome():
    return "Hello world!"


@app.route("/v1/looker", methods=['POST'])
def get_looker_data_v1():
    request_json = request.get_json()
    AUTH_URL = "https://industowersnonprod.cloud.looker.com/api/4.0/login?client_id=KnDNV2vPhBFf693Mst56&client_secret=yzY7WxbYYmxBb2QB86r9cnwB"

    if request_json and 'id' in request_json:
        look_id = request_json['id']

        response = requests.post(AUTH_URL, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            token = response.json()['access_token']
        else:
            return "Error in fetching token"
    else:
        return "Attributes missing"

    print("look_id:", look_id)
    url = f'https://industowersnonprod.cloud.looker.com/api/4.0/looks/{look_id}/run/json'
    l_header = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=l_header)

    if response.status_code == 200:
        return (response.json()[0], 200)
    else:

        return ("Error fetching Look Data", 500)



if __name__ == '__main__':
    app.run(debug=True)
