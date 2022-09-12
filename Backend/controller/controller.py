import os
from os import environ
import traceback

from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import requests

import json
import random
import string

# url microservice is hosted at port 5001
url_base = environ.get('url_api') or "http://localhost:5001"

app = Flask(__name__)
CORS(app)

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "controller.py is callable!"
        }
    ), 200

# Given a short url, get the long url
# Also possible to update the click count
@app.route("/url/<short_url>")
def fetch_by_short_url(short_url):
    try:
        if short_url:
            url_api = url_base + "/db/" + short_url
            json_response = call_api(url=url_api, method="GET")
            print(json_response)
            original_url = "http://" + json_response["data"]["original_url"]

            return redirect(original_url, code=302)
        else:
            return jsonify({
                "code": 404,
                "message" : "Invalid URL, url given: ${short_url}",
                "data" : {}
            })
    
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# On loading the web page at the start, fetch all the urls and shortened URLs
@app.route("/all")
def get_all():
    try:
        url_api = url_base + "/all"
        json_response = call_api(url=url_api, method="GET")
        return json_response
    
    except Exception as e:
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# When user enters a new url and shortened URL, invoke url to store in the database
@app.route("/new", methods=["POST"])
def add_new():
    try:
        if not request.is_json:
            return jsonify({
                "code": 400,
                "message": "Invalid request body: " + str(request.get_data())
            }), 400

        new_url_data = request.get_json()

        # If user does not give a shortened url, generate random string of 6 digits
        if "short_url" not in new_url_data:
            new_url_data["short_url"] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        # check for spaces in short or long url
        if " " in new_url_data["short_url"] or " " in new_url_data["original_url"]:
            return jsonify({
                "code": 400,
                "message": "Invalid request body, either shortened url or original url includes spaces: " + str(request.get_data())
            }), 400

        # Check if shortened url exists
        check_url_api = url_base + "/db/" + new_url_data["short_url"]
        json_response = call_api(url=check_url_api, method="GET")
        if json_response["code"] == 200 and json_response["data"]["original_url"]:
            return jsonify({
                "code": 400,
                "message": "Invalid request body, shortened url already exists in database, use different shortened url: " + str(request.get_data())
            }), 400
    
        # Add url to db, calling url microservice
        add_url_api = url_base + "/new"
        json_response = call_api(url=add_url_api, method="POST", req_body=new_url_data)
        if json_response["code"] == 200:
            return jsonify({
                "code": 200,
                "message": "Successfully added short url: {} with original url: {} to database".format(new_url_data["short_url"], new_url_data["original_url"]),
                "data" : new_url_data
            }), 200

        # Failed to add
        return jsonify({
            "code": 500,
            "message": "Failed to add url to the database",
            "data" : json_response
        }), 500
    
    except Exception as e:
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# When user wants to delete, invoke url to delete url entry in database
@app.route("/delete", methods=["DELETE"])
def remove_existing():
    try:
        delete_url_data = request.get_json()

        # Check if delete body has both shortened and original url
        if ("short_url" not in delete_url_data) or ("original_url" not in delete_url_data):
            return jsonify({
                "code": 400,
                "message": "Invalid request body, missing short url or original url, request data:" + str(request.get_data())
            }), 400

        # Check if shortened url exists
        check_url_api = url_base + "/db/" + delete_url_data["short_url"]
        json_response = call_api(url=check_url_api, method="GET")
        if json_response["code"] == 404 or json_response["data"] == {}:
            return jsonify({
                "code": 400,
                "message": "Invalid request body, shortened url does not exists in database, request data:" + str(request.get_data())
            }), 400

        # original url given by delete request, and the original url from database based on the short url mismatch
        # Will not delete
        if json_response["data"]["original_url"] != delete_url_data["original_url"]:
            return jsonify({
                "code": 400,
                "message": "Invalid request body, requested original url and database original url do not match, database original url: {}, request data: {}".format( json_response["data"]["original_url"], str(request.get_data()) )
            }), 400

        # shortened url exists and original url matches, can delete
        delete_url_api = url_base + "/delete"
        json_response = call_api(url=delete_url_api, method="DELETE", req_body=delete_url_data)

        return jsonify({
            "code": 200,
            "message" : "success"
        })

    except Exception as e:
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

def call_api(url, method="GET", req_body=None):
    # Method to call other microservices
    try:
        print("Attempting to call " + url)
        req = requests.request(method=method, url=url, json = req_body)
    except Exception as e:
        print(traceback.format_exc())
        result = {
            "code": 500,
            "message": "Failed to call microservice at {}, error message: ".format(url, str(e)) 
        }
        return result
    
    try:
        if len(req.content) > 0:
            result = req.json() 
        else:
            result = {}
    
    except Exception as e:
        print(traceback.format_exc())
        result = {
            "code": 500,
            "message": "Invalid return data from microservice at {}, error message: ".format(url, str(e)) 
        }
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)