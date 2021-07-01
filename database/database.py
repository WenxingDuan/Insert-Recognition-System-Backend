import os
import csv

from flask import request, make_response, Flask
from flask_sqlalchemy import SQLAlchemy

baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    baseDir, 'inserts.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.create_all()


class Insert(db.Model):
    __tablename__ = 'inserts'
    order = db.Column(db.String, primary_key=True)
    family = db.Column(db.String, primary_key=True)
    family_code = db.Column(db.String, primary_key=True)
    genus = db.Column(db.String, primary_key=True)
    genus_code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    pest_code = db.Column(db.String, primary_key=True)
    latin_name = db.Column(db.String(collation='NOCASE'), primary_key=True)
    plant = db.Column(db.String, primary_key=True)
    area = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, primary_key=True)
    link = db.Column(db.String, primary_key=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
            return dict

    def __repr__(self):
        return self.latin_name


# order, family, family_code, genus, genus_code, name, pest_code, latin_name, plant, area, description
# i["order"], i["family"], i["family_code"], i["genus"], i["genus_code"], i["name"], i["pest_code"], i["latin_name"], i["plant"], i["area"], i["description"]

# @app.route('/search', methods=['GET'])
# def bug():
#     bug = insert.query.filter_by(name='bug').first()
#     return bug.description
