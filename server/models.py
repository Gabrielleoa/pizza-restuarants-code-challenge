from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules= ('-restaurant.pizzas',)

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= True,)
    address = db.Column(db.String)

class Pizza(db.Model, SerializerMixin):
    __tablename__='pizzas'

    serialize_rules=('-pizza.restaurants',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

class RestaurantPizza(db.Model, SerializerMixin): 
    __tablename__ = 'restuarantpizzas'

    serialize_rules= ('-restaurantpizza.pizza','-restaurantpizza.restaurant',)


    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)


    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))


    