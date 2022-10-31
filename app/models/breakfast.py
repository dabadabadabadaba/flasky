from app import database

#create a class for our model
#it'll inherit from a class from the database object
class Breakfast(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String)
    rating = database.Column(database.Float)
    prep_time = database.Column(database.Integer)

    #this will produce a dictionary and help refactor our code
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "prep_time": self.prep_time
        }
