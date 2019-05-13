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

#stock info page
@route('/stockinfo')
@view('stockinfo')
def stock_info():
    data = dict (stock_list = food)
    return data

#re-stock food item
@route('/re-stock-item/<food_id>')
@view('re-stock-item')
def re_stock_item(food_id):
    food_id = int(food_id)
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
    data = dict (fooditem = found_food)
    return data


run(host='0.0.0.0', port = 8080, reloader = True, debug = True)
