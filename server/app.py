#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict())


class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return jsonify(plant.to_dict())



def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'image': self.image,
        'price': self.price
    }



Plant.to_dict = to_dict


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')


def ensure_test_plant_exists():
    with app.app_context():
        plant = Plant.query.get(1)
        if not plant:
            new_plant = Plant(name="Test Plant", image="test_image_url", price=19.99)
            db.session.add(new_plant)
            db.session.commit()

# Call the function to ensure the plant exists
ensure_test_plant_exists()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
