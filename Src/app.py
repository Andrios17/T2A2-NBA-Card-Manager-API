from marshmallow.exceptions import ValidationError
from init import app, jwt
from blueprints.cli_bp import db_commands
from blueprints.user_bp import users_bp
from blueprints.card_bp import card_bp
from blueprints.post_bp import posts_bp
from blueprints.auction_bp import auction_bp
from blueprints.pc_bp import pc_bp
from sqlalchemy.exc import DataError

# Registering blueprints to the app
app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(card_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(pc_bp)
app.register_blueprint(auction_bp)


# Running the Flask app with debug mode enabled
if __name__ == '__main__':
    app.run(debug=True)


# Custom error handlers for specific exceptions in the application
@app.errorhandler(ValidationError)
def invalid_request(err):
    return {'error': vars(err)['messages']}, 400

@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {'error': 'Not Found'}, 404

@app.errorhandler(DataError)
def data_error(err):
    return {'error': 'Invalid data. Please ensure you are using the correct data types'}, 400

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'Unauthorized'}, 401

@app.errorhandler(403)
def forbidden(err):
    return {"error": "You are not authorized to access this route"}, 403

@app.errorhandler(KeyError)
def missing_key(err):
    return {'error': f'{str(err)} is missing'}, 400

@jwt.invalid_token_loader
def invalid_token(err):
    return {"error": "Invalid token. Please log in again"}, 401

@jwt.expired_token_loader
def expired_token(err):
    return {"error": "Token has expired. Please log in again"}, 401

@jwt.unauthorized_loader
def missing_token(err):
    return {"error": "Please ensure you are logged in so you are able to access this route"}, 401