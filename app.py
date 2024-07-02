from marshmallow.exceptions import ValidationError
from init import app
from blueprints.cli_bp import db_commands
from blueprints.user_bp import users_bp
from blueprints.card_bp import card_bp
from blueprints.post_bp import posts_bp
from blueprints.auction_bp import auction_bp
from blueprints.pc_bp import pc_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(card_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(pc_bp)
app.register_blueprint(auction_bp)

if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(ValidationError)
def invalid_request(err):
    return {'error': vars(err)['messages']}, 400

