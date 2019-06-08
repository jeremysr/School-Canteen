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

#re-stock-success page
@route('/re-stock-success/<food_id>', method = "POST")
@view('re-stock-success')
def re_stock_success(food_id):
    food_id = int(food_id)
    restock = request.forms.get('inp_re_stock')
    
    #to prevent an error if the user inputs something other than an int
    try:
        resto = int(restock) #atempts to convert to an int
    except ValueError:
        resto = 0   #sets to zero if a ValueError occurs 
        
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
        data = dict (fooditem = found_food)
    found_food.stock = found_food.stock + resto
    
    #added to prevent stock going into negitive values
    if found_food.stock < 0:
        found_food.stock = 0
    return data

#new item page
@route('/new-item')
@view('new-item')
def new_item():
    pass

#new item success page, notifys the user that the new addedd item was successful
@route('/new-item-success', method ="POST")
@view('new-item-success')
def new_item_success():
    
    #try/except ValueError to prevent internal server error from wrong input
    try:
        food_item = request.forms.get('food_item')
        stock = request.forms.get('stock')
        stock = int(stock)
        price = request.forms.get('price')
        price = int(price)
        sold = 0
        
        if stock < 0: #these are added to prevent negitive values.
            stock = 0
        if price < 0:
            price = 0
    
        new_item = FoodItem(food_item, stock, price, sold)
        food.append(new_item)
        
    except ValueError:
        pass
    


run(host='0.0.0.0', port = 8080, reloader = True, debug = True)
