from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def restaurants(id):
    restaurants = Restaurant.query.all()

    restaurants_list = [restaurant.to_dict() for restaurant in restaurants]
    return jsonify(restaurants_list), 200
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": []
    }

    for pizza in restaurant.pizzas:
        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        restaurant_data["pizzas"].append(pizza_data)

    return jsonify(restaurant_data), 200

    