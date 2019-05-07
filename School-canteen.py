from bottle import run, route, view, get, post, request
from itertools import count


class FoodItem:
    _ids = count(0)

    def __init__(self, food_item, stock, price, sold):
        self.id = next(self._ids)
        self.food_item = food_item
        self.stock = stock
        self.price = price
        self.sold = sold

food = [
    FoodItem("Sushi roll Pack",5,7,0),
    FoodItem("Hot dog and chips",12,5,0),
    FoodItem("Ham and cheese sandwich",4,4,0),
]

#pages

#index page
@route('/')
@view('index')
def index():
    pass


run(host='0.0.0.0', port = 8080, reloader = True, debug = True)
