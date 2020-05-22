import os
from app import models
from app import db
from app.models import Region


def put_db():
    with open("liste-tea-en.txt", "r") as d:
        data = d.read()
        data_list = data.splitlines()
        for country in data_list:
            r = Region(name=country)
            db.session.add(r)
            db.session.commit()

