#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os
import random
import time
import dotenv


# Load dotenv
python_env = os.getenv('PYTHON_ENV') or 'development'
dotenv_path = os.path.join(
    os.path.dirname(__file__),
    '.env.' + python_env
)
dotenv.load_dotenv(dotenv_path)


from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


# NOTE: Initial elastic apm
# https://www.elastic.co/guide/en/apm/agent/python/2.x/flask-support.html
# https://www.elastic.co/guide/en/apm/agent/python/2.x/configuration.html
from elasticapm.contrib.flask import ElasticAPM
apm = ElasticAPM()
apm.init_app(app,
             server_url=os.environ.get('APM_SERVER_URL'),
             service_name=os.environ.get('APM_SEVICE_NAME'),
             secret_token=os.environ.get('APM_SECRET_TOKEN'),
             capture_body='all', # Just for demo
             )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/signup", methods=['POST'])
def signup():
    """Signup user.
    """
    # NOTE: Sleep random seconds
    time.sleep(random.random())
    body = json.loads(request.data or b'{}')
    record = User(**body)
    db.session.add(record)
    db.session.commit()
    result = {
        'id': record.id,
        'username': record.username,
        'email': record.email,
    }
    return jsonify(result), 201


@app.route("/users/<username>")
def show_user(username):
    """Show user filter by username.
    """
    # NOTE: Sleep random seconds
    time.sleep(random.random())
    record = User.query.filter_by(username=username).first()
    if not record:
        result = {
            'status': 404,
            'errmsg': 'User with username={} not found'.format(username),
        }
        return jsonify(result), result['status']
    result = {
        'id': record.id,
        'username': record.username,
        'email': record.email,
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run()
