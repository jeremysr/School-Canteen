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

#new item success page
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

#sell item page
@route('/sell-item/<food_id>')
@view('sell-item')
def sell_item(food_id):
    food_id = int(food_id)
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
    data = dict (fooditem = found_food)
    return data

#sell-item-success page
@route('/sell-item-success/<food_id>', method = "POST")
@view('sell-item-success')
def sell_item_success(food_id):
    food_id = int(food_id)
    sell_amount = request.forms.get('inp_sell_item')
    
    #to prevent an error if the user inputs something other than an int
    try:
        sell_amount = int(sell_amount)
    except ValueError:
        sell_amount = 0   #sets to zero if a ValueError occurs 
    
    #finds food item with same ID
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
        
    max_able_to_sell = found_food.stock #max able to sell is calculated before stock is reduced, used later on if needed.
    found_food.stock = found_food.stock - sell_amount #reduces stock buy amount sold
    
    
    #If statment put in place to detect if user attempted to sell more stock than existed
    if found_food.stock < 0:
        found_food.stock = 0
        found_food.sold = found_food.sold + max_able_to_sell #If so it only counts the stock that was sold
        display_message = True #displays warning message that number they entered was to large
    else:
        found_food.sold = found_food.sold + sell_amount #works as normal
        display_message = False
    data = dict (fooditem = [found_food, display_message, max_able_to_sell])
    return data

#stats page
@route('/stats')
@view('stats')
def stats():
    #placeholder's for if stats page is checked before any sales
    total_profit = 0
    total_sold = 0
    most_popular_sold = 0
    most_popular = "N/A"
    
    for food_objects in food:
        total_profit = total_profit + food_objects.sold * food_objects.price #total profit
        total_sold = total_sold + food_objects.sold #total sold
        if food_objects.sold > most_popular_sold: #most sold item
            most_popular_sold = food_objects.sold
            most_popular = food_objects.food_item
    data = dict (food_stats = [total_profit, total_sold, most_popular, most_popular_sold])
    return data


    

    


run(host='0.0.0.0', port = 8080, reloader = True, debug = True)
