from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ostap:11111111@localhost:3306/studentdb'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    brand = db.Column(db.String(10))
    origin_country = db.Column(db.String(10))
    category = db.Column(db.String(10))
    producer = db.Column(db.String(10))

    def __init__(self, price, brand, origin_country, category, producer):
        self.price = price
        self.brand = brand
        self.origin_country = origin_country
        self.category = category
        self.producer = producer


class DevicesSchema(ma.Schema):
    class Meta:
        fields = ('price', 'brand', 'origin_country', 'category', 'producer')


device_schema = DevicesSchema()
devices_schema = DevicesSchema(many=True)


@app.route("/devices", methods=["GET"])
def get_devices():
    devices = Devices.query.all()
    result = devices_schema.dump(devices)

    return jsonify(result)


@app.route("/devices/<id>", methods=["GET"])
def get_device(id):
    device = Devices.query.get(id)

    if device is None:
        abort(404)

    return device_schema.jsonify(device)


@app.route("/devices", methods=["POST"])
def add_device():
    data = DevicesSchema().load(request.json)
    new_device = Devices(**data)

    db.session.add(new_device)
    db.session.commit()

    return device_schema.jsonify(new_device)


@app.route("/devices/<id>", methods=["PUT"])
def update_device(id):
    device = Devices.query.get(id)
    if device is None:
        abort(404)

    data = DevicesSchema().load(request.json)
    for i in data:
        setattr(device, i, request.json[i])

    db.session.commit()
    return device_schema.jsonify(device)


@app.route("/devices/<id>", methods=["DELETE"])
def delete_device(id):
    device = Devices.query.get(id)

    if device is None:
        abort(404)

    db.session.delete(device)
    db.session.commit()

    return device_schema.jsonify(device)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)