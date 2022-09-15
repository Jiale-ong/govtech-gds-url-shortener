import os

from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from sqlalchemy import null
from sqlalchemy.sql import func

import traceback

basedir = os.path.abspath(os.path.dirname(__file__))

# Proper DB URI: mysql://username:password@host:port/database_name
DB_URI = "mysql+mysqlconnector://root:@127.0.0.1:3306/govtech_url"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# url table mapping
class Url(db.Model):
    __tablename__ = 'govtech_url'

    id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    short_url = db.Column(db.String(150), nullable=False)
    original_url = db.Column(db.String(500), nullable=False)
    creator = db.Column(db.String(150), nullable=True)
    click_count = db.Column(db.Integer, nullable=False)

    # def __init__(self, id, short_url, original_url, creator, click_count):
    #     self.id = id
    #     self.short_url = short_url
    #     self.original_url = original_url
    #     self.creator = creator
    #     self.click_count = click_count

    def json(self):
        return {
            "id": self.id,
            "short_url": self.short_url,
            "original_url": self.original_url,
            "creator": self.creator,
            "click_count": self.click_count
        }

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "url.py is callable!"
        }
    ), 200

# retrieve specific url details
@app.route("/db/<short_url>")
def find_by_short_url(short_url):
    try:
        url = Url.query.filter_by(short_url=short_url).first()
        if url:
            url_json = url.json()

            return jsonify({
                "code": 200,
                "message" : "success",
                "data": url_json
            })
        else:
            return jsonify({
                "code": 404,
                "message" : "No url ending with {} found".format(short_url),
                "data" : {}
            })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# retrieve all url
@app.route("/all")
def get_all():
    try:
        url_list = Url.query.all()
        output_list = [] 

        for url in url_list:
            output_list.append(url.json())

        return jsonify({
            "code": 200,
            "message" : "success",
            "data": output_list
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# add new url to db
@app.route("/new", methods=["POST"])
def add_new():
    try:
        sent_json = request.get_json(force=True)

        if "creator" not in sent_json:
            sent_json["creator"] = ""
        
        new_url = Url(
            short_url = sent_json["short_url"],
            original_url = sent_json["original_url"],
            creator = sent_json["creator"],
            click_count = 0
        )

        db.session.add(new_url)
        db.session.commit()

        to_return = {"id": new_url.id}

        return jsonify({
            "code": 200,
            "message" : "success",
            "data": to_return
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

# delete existing url from db
@app.route("/delete", methods=["DELETE"])
def remove_existing():
    try:
        sent_json = request.get_json(force=True)

        existing_url = Url.query.filter_by(
            short_url = sent_json["short_url"],
            original_url = sent_json["original_url"]
        ).first()

        db.session.delete(existing_url)
        db.session.commit()

        return jsonify({
            "code": 200,
            "message" : "success"
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "code" : 500,
            "message": "Server error, error message: " + str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)