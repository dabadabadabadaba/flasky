from app import db

#create a class for our model
#it'll inherit from a class from the database object
class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    prep_time = db.Column(db.Integer)
    #adding the foreign key, "menu.id" needs to match whatever the primary key is in Menu
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id')) # menu can have many breakfasts
    #adding the relationship, our breakfast has one menu
    menu = db.relationship('Menu', back_populates='breakfast_items')

    #INSTANCE method: produces a dictionary and helps refactor our code. this dictionary representation is similiar to json
    #already have an instance, want a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "prep_time": self.prep_time,
            "menu_id": self.menu_id # added menu_id
        }

    #CLASS method: instead if "self", it takes in cls
    # class method instead of instance method because an instance requires
    # breakfast first before it can be used
    # cls will be populated with the Breakfast class, not one breakfast but the overall concept of Breakfast
    @classmethod
    def from_dict(cls, breakfast_dict):
        #using "cls" below instead of "Breakfast" allows for flexiblity if children
        # classes/subclasses are made in the future, won't need to rewrite this code
        return cls(
            name=breakfast_dict['name'],
            rating=breakfast_dict['rating'],
            prep_time=breakfast_dict['prep_time'],
            menu_id=breakfast_dict["menu_id"] # added menu_id
            )
