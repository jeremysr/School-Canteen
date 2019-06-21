# importing the libraries needed, added ver1.0
from bottle import run, route, view, get, post, request, static_file
from itertools import count

"""
#README SUMMARY
VER1.0 - created class, data dictionary, and index page
VER2.0 - added stock info, page to display stock infomation
VER2.1 - add re-stock feature
VER2.3 - fixing bugs from VER2 and finalizing it
VER3.0 - added sell item feature
VER3.1 - added statistics page and calculations
VER3.2 - fixing bugs from VER3 and finalizing it
VER4.0 - added images to stok info page
"""


# Creating class called FoodItem, added ver1.0
class FoodItem:
    # gives ids to each food item
    _ids = count(0)

    def __init__(self, food_item, stock, price, sold, image):
        self.id = next(self._ids)
        self.food_item = food_item
        self.stock = stock
        self.price = price
        self.sold = sold
        self.image = image

# data dictionary called food, added Ver1.0
food = [
    # Items required to be on the menu
    FoodItem("Sushi roll Pack",5,7,0,"/Assets/sushi-photo.jpg"),
    FoodItem("Hot dog and chips",12,5,0,"/Assets/hotdog-photo.jpg"),
    FoodItem("Ham and cheese sandwich",4,4,0,"/Assets/sandwich-photo.jpg"),
]

# images added Ver4.0
@route('/Assets/<filename>')
def server_static(filename):
    # returns the image and tells the location
    return static_file(filename, root='./Assets')


# index page, Added Ver1.0
@route('/')
@view('index')
def index():
    # no info from python needed on page
    pass

# stock info page, Added Ver2.0
@route('/stockinfo')
@view('stockinfo')
# function that returns data to the html page
def stock_info():
    data = dict (stock_list = food)
    return data

# re-stock food item, Added Ver2.1
@route('/re-stock-item/<food_id>')
@view('re-stock-item')
def re_stock_item(food_id):
    # when the user clicks on an item it give an id, this for loop finds what fooditem has that id
    food_id = int(food_id)
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
    data = dict (fooditem = found_food)
    return data

# re-stock-success page, Added Ver2.1
@route('/re-stock-success/<food_id>', method = "POST")
@view('re-stock-success')
# function what adjust stock level by number inputed
def re_stock_success(food_id):
    food_id = int(food_id)
    restock = request.forms.get('inp_re_stock')
    
    # to prevent an error if the user inputs something other than an int
    try:
        resto = int(restock)
    except ValueError:
        resto = 0   # sets to zero if a ValueError occurs 
        
    # when the user clicks on an item it give an id, this for loop finds what fooditem has that id
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
        data = dict (fooditem = found_food)
    # once the item is found, adjust by inputed value
    found_food.stock = found_food.stock + resto
    
    # added to prevent stock going into negitive values
    if found_food.stock < 0:
        found_food.stock = 0
    return data

# new item page, Added Ver2.2
@route('/new-item')
@view('new-item')
def new_item():
    # no info from python needed on page
    pass

# new item success page, Added Ver2.2
@route('/new-item-success', method ="POST")
@view('new-item-success')
def new_item_success():
    
    # try/except ValueError to prevent internal server error from wrong input
    try:
        # Requesting Values that were inputed, then converting them to intergers
        food_item = request.forms.get('food_item')
        stock = request.forms.get('stock')
        stock = int(stock)
        price = request.forms.get('price')
        price = int(price)
        sold = 0
        image = "/Assets/placeholder.png"
        
        # these are added to prevent negitive values.
        if stock < 0:
            stock = 0
        if price < 0:
            price = 0
        
        # new_item is a list created with all varibles needed to add a new item
        new_item = FoodItem(food_item, stock, price, sold, image)
        # added to data dictionary
        food.append(new_item)
        
    except ValueError:
        pass

# sell item page, Added Ver3.0
@route('/sell-item/<food_id>')
@view('sell-item')
def sell_item(food_id):
    
    # when the user clicks on an item it give an id, this for loop finds what fooditem has that id
    food_id = int(food_id)
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
    data = dict (fooditem = found_food)
    return data

# sell-item-success page, Added Ver3.0
@route('/sell-item-success/<food_id>', method = "POST")
@view('sell-item-success')
# this function requests the sell amount and adjusts the stock by that much
def sell_item_success(food_id):
    food_id = int(food_id)
    sell_amount = request.forms.get('inp_sell_item')
    
    # to prevent an error if the user inputs something other than an int
    try:
        sell_amount = int(sell_amount)
    except ValueError:
        sell_amount = 0   # sets to zero if a ValueError occurs 
    
    # finds food item with same ID
    found_food = None
    for fooditem in food:
        if fooditem.id == food_id:
            found_food = fooditem
        
    max_able_to_sell = found_food.stock # max able to sell is calculated before stock is reduced, used later on if needed.
    found_food.stock = found_food.stock - sell_amount # reduces stock buy amount sold
    
    
    # If statment put in place to detect if user attempted to sell more stock than existed
    if found_food.stock < 0:
        found_food.stock = 0
        found_food.sold = found_food.sold + max_able_to_sell # If so it only counts the stock that was sold
        display_message = True # displays warning message that number they entered was to large
    else:
        found_food.sold = found_food.sold + sell_amount # works as normal
        display_message = False
    # returns data, also had tells html if it should display and error message.
    data = dict (fooditem = [found_food, display_message, max_able_to_sell])
    return data

# stats page, Added Ver3.1
@route('/stats')
@view('stats')
def stats():
    # placeholder's for if stats page is checked before any sales
    total_profit = 0
    total_sold = 0
    most_popular_sold = 0
    most_popular = "N/A"
    
    # for loop runs through each food item and calculates the total amounts
    for food_objects in food:
        total_profit = total_profit + food_objects.sold * food_objects.price #total profit
        total_sold = total_sold + food_objects.sold #total sold
        # if statment checks which fooditem has the largest sold amount
        if food_objects.sold > most_popular_sold:
            most_popular_sold = food_objects.sold
            most_popular = food_objects.food_item #most popular
    # returns data so page can display these stats
    data = dict (food_stats = [total_profit, total_sold, most_popular, most_popular_sold])
    return data


    
# bottle feature
run(host='0.0.0.0', port = 8080, reloader = True, debug = True)
