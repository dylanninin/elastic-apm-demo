#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_script import Manager
from app import app
from app import db


manager = Manager(app)


@manager.command
def init_db():
    db.create_all()


if __name__ == '__main__':
    manager.run()
