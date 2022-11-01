from flask import Blueprint, jsonify, request, abort, make_response # request is an object that Flask creates for us. It'll populate with the request body.
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
#we're making a decision in the "breakfast_bp" line below which is that all of the endpoints for this Blueprint will
#start with "/breakfast" and will have potentially other things after it
#Blueprint keeps track of all our endpoints (it's like a bucket we're putting the routes into)
breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast") # initializing our Blueprint

# FIRST ROUTE
#decorator: takes whatever function after it, and wraps it into the breakfast blueprint route
#When we try to run this route in Flask, it'll run this route
@breakfast_bp.route('', methods=['GET']) #this function will turn data into JSON, we can't turn classes into JSON but you can turn lists and dicts into JSON
def get_all_breakfasts():
    rating_query_value = request.args.get("rating") #pass in the key, whatever the key happens to be. Has to be a string. 
    # "args" is a dictionary and .get() is a method. using .get() will give us NONE if there's no rating
    if rating_query_value is not None: # if there's a rating, make a query with that rating
        breakfasts = Breakfast.query.filter_by(rating=rating_query_value) 
    else:
        breakfasts = Breakfast.query.all() #if there's no rating, get all breakfasts. we're essentially running a SELECT * on the back end 

    result = []  # adding a dictionary of breakfast items into a list
    
    for item in breakfasts: # this used to be hardcorded to the list "breakfast_items"
        # item_dict = {"id": item.id, "name": item.name, # generate a dictionary
        #             "rating":item.rating,"prep_time": item.prep_time}
        result.append(item.to_dict()) # use our method 'to_dict()'

    return jsonify(result), 200 # return the data as JSON

# SECOND ROUTE 
@breakfast_bp.route('/<breakfast_id>', methods=['GET'])
#endpoint (breakfast_id) in decorator and parameter in the function have to be named exactly the same!
def get_one_breakfast(breakfast_id):
    #find the breakfast that matches the breakfast_id that was passed  
   
    '''
    #try casting breakfast_id into an integer
    try:
        breakfast_id = int(breakfast_id)
    # if the casting doesn't work, send the user a message
    except ValueError:
        return jsonify({"msg": f"invalid data type:{breakfast_id}"}), 400
    
    chosen_breakfast = None
    # breakfast_id = int(breakfast_id)
    # for breakfast in breakfast_items:
    #     if breakfast.id == breakfast_id:
    #         chosen_breakfast = breakfast

    # instead of querying "all", we use "get" which is a "SELECT * WHERE id ="
    chosen_breakfast = Breakfast.query.get(breakfast_id) 

    # check if chosen_breakfast is still None before we construct our dictionary message
    if chosen_breakfast is None:
        return jsonify({"msg": f"Could not find breakfast item with id: {breakfast_id}"}), 404
    
    #don't need this code that makes a dictionary because now I can use "to_dict" in the return line
    # #create a dictionary with the found breakfast
    # return_breakfast = {
    #     "id": chosen_breakfast.id,
    #     "name": chosen_breakfast.name,
    #     "rating": chosen_breakfast.rating,
    #     "prep_time": chosen_breakfast.prep_time
    # }
    #technically you don't need to jsonify for a single breakfast item 
    # (you'd get the same output bc the dict is already in json format)
    #the reason we're using it is to be consistent bc we're using it elsewhere, this is coding best practice
    '''
    chosen_breakfast = get_breakfast_from_id(breakfast_id) # all of the old code above has been turned into a helper function
    return jsonify(chosen_breakfast.to_dict()), 200 

#THIRD route after connecting to database
@breakfast_bp.route('', methods=['POST'])
def create_one_breakfast():
    request_body = request.get_json()

    new_breakfast = Breakfast(
        name=request_body['name'],
        rating=request_body['rating'],
        prep_time=request_body['prep_time']
    )

    database.session.add(new_breakfast) # .add because it's new data that is being added
    database.session.commit()

    return jsonify({"msg":f"Successfully created Breakfast with id={new_breakfast}"}), 201

#needs a breakfast_id because we need to know which one to update
@breakfast_bp.route('/<breakfast_id>', methods=['PUT']) # using PUT because we're requiring all of the fields from the user
def update_one_breakfast(breakfast_id):
    # there's a function already that gets one breakfast and we could theoretically just copy and paste that code from above
    # but, whenever we copy and paste, that's a sign that we can use a helper function!
    update_breakfast = get_breakfast_from_id(breakfast_id)
    
    request_body = request.get_json() # changing the json in request body into something Python can read

    try:
        update_breakfast.name = request_body["name"]
        update_breakfast.rating = request_body["rating"]
        update_breakfast.prep_time = request_body["prep_time"]
    except KeyError:
        return jsonify({"msg": "Missing required data"}), 400
    
    database.session.commit() # only "commit" because the data already exists

    return jsonify({"msg": f"Successfully updated breakfast with id {update_breakfast.id}"}), 200

@breakfast_bp.route('/<breakfast_id>', methods=['DELETE'])
def delete_one_breakfast(breakfast_id):
    breakfast_to_delete = get_breakfast_from_id(breakfast_id)

    database.session.delete(breakfast_to_delete)
    database.session.commit()

    return jsonify({"msg": f"Successfully deleted breakfast with id {breakfast_to_delete}"}), 200

#helper function 
def get_breakfast_from_id(breakfast_id):
    try:
        breakfast_id = int(breakfast_id)
    except ValueError:
        # 'abort' needs 'make_response' so both have to be imported at the top of the file
        # this makes sure our helper function returns a breakfast instead of just a response that also needs to be returned
        return abort(make_response({"msg": f"invalid data type:{breakfast_id}"}, 400)) 

    chosen_breakfast = Breakfast.query.get(breakfast_id) 

    if chosen_breakfast is None:
        return abort(make_response({"msg": f"Could not find breakfast item with id: {breakfast_id}"}, 404))
    
    return chosen_breakfast

