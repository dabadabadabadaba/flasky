from app import db

#class Menu that has many breakfast items
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_name = db.Column(db.String)
    meal = db.Column(db.String)
    #creating the relationship between menu and breakfast, this will be a list of breakfasts
    breakfast_items = db.relationship('Breakfast', back_populates='menu')

    def to_dict(self):
        # all of this code is now in the line ""breakfast_items": self.get_breakfast_list"
        # #update menu so it has a list of all the breakfast items associated with it
        # list_of_breakfasts = []
        # for item in self.breakfast_items:
        #     list_of_breakfasts.append(item.to_dict())# this calls to_dict on breakfast NOT on menu

        return {
            "id": self.id,
            "restaurant_name": self.restaurant_name,
            "meal": self.meal,
            "breakfast_items": self.get_breakfast_list()
        }
    # function to list all the breakfast items associated with the menu
    def get_breakfast_list(self):
        list_of_breakfasts = []
        for item in self.breakfast_items:
            list_of_breakfasts.append(item.to_dict()) #convert an instance of the class so I can jsonify it
        return list_of_breakfasts