#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get("/restaurants")
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [r.to_dict(rules= ['-restaurant_pizzas']) for r in restaurants], 200

@app.get("/restaurants/<int:id>")
def get_rest_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if not restaurant:
        return {"error": "Restaurant not found"}, 404
    else: 
        return restaurant.to_dict(), 200
    
@app.delete("/restaurants/<int:id>")
def delete_rest(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if not restaurant:
        return {"error": "Restaurant not found"}, 404
    db.session.delete(restaurant)
    db.session.commit()
    return {}, 204

@app.get("/pizzas")
def get_pizzas():
    pizzas = Pizza.query.all()
    return [p.to_dict(rules= ['-restaurant_pizzas']) for p in pizzas], 200

@app.post("/restaurant_pizzas")
def post_pizza():
    json_data = request.get_json()

    try:
        new_pizza = RestaurantPizza(
            price = json_data.get('price'),
            pizza_id = json_data.get('pizza_id'),
            restaurant_id = json_data.get('restaurant_id')
        )
    except ValueError as e:
        return {"errors": ["validation errors"]}, 400
    
    db.session.add(new_pizza)
    db.session.commit()

    return new_pizza.to_dict(), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)