from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Tea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    water_temp = db.Column(db.Integer)  # In Ceilcus
    water_time = db.Column(db.Integer)  # In minutes

    def __repr__(self):
        return f'<Tea {self.name}>'


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    tea = db.relationship('Tea', backref='provenance', lazy='dynamic')

    def get_reg_list():
        regions = Region.query.all()
        list_region = []
        for region in regions:
            list_region.append({"id": region.id, "name": region.name})
        return list_region

    def reg_list_to_tupple():
        list_region = Region.get_reg_list()
        list_tuple_region = []
        for region in list_region:
            my_tuple = (str(region["id"]), region['name'])
            list_tuple_region.append(my_tuple)
        return list_tuple_region

    def __repr__(self):
        return f'<Region {self.name}>'

# Type of tea should have only 9 rows at the beginning: (Green tea, Balck, Matcha, infusion , Rooibos, white tea, oolong, MAté,Pu erh)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), index=True, unique=True)
    tea = db.relationship('Tea', backref='type of tea', lazy='dynamic')

    def get_type_list():
        types = Type.query.all()
        list_types = []
        for type in types:
            list_types.append({"id": type.id, "type": type.type})
        return list_types

    def type_list_to_tupple():
        list_types = Type.get_type_list()
        list_tuple_types = []
        for type in list_types:
            my_tuple = (str(type["id"]), type['type'])
            list_tuple_types.append(my_tuple)
        return list_tuple_types

    def __repr__(self):
        return f'<Type {self.type}>'

#! Backref and lazy


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
