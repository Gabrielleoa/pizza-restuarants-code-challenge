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
    restaurant = Restaurant.query.filter(Restaurant.id==id).first()

    restaurant_dict= restaurant.to_dict()

    response = make_response(
        restaurant_dict,
        200
    )
    return response
    