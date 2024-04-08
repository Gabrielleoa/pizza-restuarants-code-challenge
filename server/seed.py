from random import choice as rc
from faker import Faker


from app import app
from models import db, Restaurant, RestaurantPizza, Pizza

with app.app_context():

    fake = Faker()

    Restaurant.query.delete()

    restaurants = []

    name = ['Dominion Pizza','Pizza Hut'] 
    address= ['Westgate Mall, Mwanzi Road, Nrb 100','Good Italian, Ngong Road, 5th Avenue']

    for i in range(2):
        restaurant = Restaurant(name=rc(name), address=rc(address))
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()
