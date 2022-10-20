from flask import Blueprint, jsonify

#setting up Breakfast class
class Breakfast():
    def __init__(self, id, name, rating, prep_time):
        self.id = id
        self.name = name
        self.rating = rating
        self.prep_time = prep_time

#instantiating Breakfasts
breakfast_items = [
    Breakfast(1, "omelette", 4, 10),
    Breakfast(2, "french toast", 3, 15),
    Breakfast(3, "cereal", 1, 1),
    Breakfast(4, "oatmeal", 3, 10)
]

#we're making a decision in the code below- all of the endpoints for this Blueprint will
#start with "/breakfast" and will have potentially other things after it
#Blueprint keeps track of all our endpoints (it's like a bucket we're putting the routes into)
breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast")

# FIRST ROUTE
#decorator: takes whatever function after it, and wraps it into the breakfast blueprint route
#When we try to run this route in Flask, it'll run this route
@breakfast_bp.route('', methods=['GET'])
def get_all_breakfasts():
    #we can't turn classes into JSON but you can turn lists and dicts into JSON
    #this function will turn data into JSON
    result = []  # adding a dictionary of breakfast items into a list
    for item in breakfast_items:
        item_dict = {"id": item.id, "name": item.name, 
                    "rating":item.rating,"prep_time": item.prep_time}
        result.append(item_dict)

    return jsonify(result), 200 # return the data as JSON
