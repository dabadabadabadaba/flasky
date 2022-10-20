from flask import Flask

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

# import inside the body of the function bc that's how it's done in Flask
    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app