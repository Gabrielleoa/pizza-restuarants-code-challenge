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
@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_or_delete_restaurant(id):
    if request.method == 'GET':
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

    elif request.method == 'DELETE':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return jsonify({"error": "Restaurant not found"}), 404

        
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()

        
        db.session.delete(restaurant)
        db.session.commit()

        return '', 204
    @app.route('/pizzas', methods=['GET'])
    def pizzas():
        pizzas = Pizza.query.all()
        pizza_list=[]
        for pizza in pizzas:
            pizza_info={
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients            
                }
            pizza_list.append(pizza_info)
        return jsonify(pizza_list)
    
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.json

        
        pizza = Pizza.query.get(data['pizza_id'])
        restaurant = Restaurant.query.get(data['restaurant_id'])
        if pizza is None or restaurant is None:
            return jsonify({"errors": ["validation errors"]}), 400

        
        new_restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201


    