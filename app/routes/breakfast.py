from flask import Blueprint, jsonify, request # request is an object that Flask creates for us. It'll populate with the request body.
from app import database # now we can interact with the database
from app.models.breakfast import Breakfast # now we have access to the model in this file


''' old hardcoded Breakfasts
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
'''
#we're making a decision in the code below which is that all of the endpoints for this Blueprint will
#start with "/breakfast" and will have potentially other things after it
#Blueprint keeps track of all our endpoints (it's like a bucket we're putting the routes into)
breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast") # initializing our Blueprint

# FIRST ROUTE
#decorator: takes whatever function after it, and wraps it into the breakfast blueprint route
#When we try to run this route in Flask, it'll run this route
@breakfast_bp.route('', methods=['GET'])
def get_all_breakfasts():
    #we can't turn classes into JSON but you can turn lists and dicts into JSON
    #this function will turn data into JSON
    result = []  # adding a dictionary of breakfast items into a list
    all_breakfasts = Breakfast.query.all() # we're essentiall running a SELECT * on the back end 
    for item in all_breakfasts: # this used to be hardcorded to the list "breakfast_items"
        item_dict = {"id": item.id, "name": item.name, # generate a dictionary
                    "rating":item.rating,"prep_time": item.prep_time}
        result.append(item_dict)

    return jsonify(result), 200 # return the data as JSON

# SECOND ROUTE 
@breakfast_bp.route('/<breakfast_id>', methods=['GET'])
#endpoint (breakfast_id) in decorator and parameter in the function have to be named exactly the same!
def get_one_breakfast(breakfast_id):
    #find the breakfast that matches the breakfast_id that was passed
    
    #try casting breakfast_id into an integer
    try:
        breakfast_id = int(breakfast_id)
    # if the casting doesn't work, send the user a message
    except ValueError:
        return jsonify({"msg": f"invalid data type:{breakfast_id}"}), 400
    
    chosen_breakfast = None
    breakfast_id = int(breakfast_id)
    for breakfast in breakfast_items:
        if breakfast.id == breakfast_id:
            chosen_breakfast = breakfast
    # check if chosen_breakfast is still None before we construct our dictionary message
    if chosen_breakfast is None:
        return jsonify({"msg": f"Could not find breakfast item with id: {breakfast_id}"}), 404
    
    #create a dictionary with the found breakfast
    return_breakfast = {
        "id": chosen_breakfast.id,
        "name": chosen_breakfast.name,
        "rating": chosen_breakfast.rating,
        "prep_time": chosen_breakfast.prep_time
    }
    #technically you don't need to jsonify for a single breakfast item 
    # (you'd get the same output bc the dict is already in json format)
    #the reason we're using it is to be consistent bc we're using it elsewhere, this is coding best practice
    return jsonify(return_breakfast), 200 

#route after connecting to database
@breakfast_bp.route('', methods=['POST'])
def create_one_breakfast():
    request_body = request.get_json()

    new_breakfast = Breakfast(
        name=request_body['name'],
        rating=request_body['rating'],
        prep_time=request_body['prep_time']
    )

    database.session.add(new_breakfast)
    database.session.commit()

    return jsonify({"msg":f"Successfully created Breakfast with id={new_breakfast}"}), 201
