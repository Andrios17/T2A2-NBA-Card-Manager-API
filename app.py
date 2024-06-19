from init import app
from blueprints.cli_bp import db_commands
from blueprints.user_bp import users_bp
from blueprints.card_bp import card_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(card_bp)

if __name__ == '__main__':
    app.run(debug=True)