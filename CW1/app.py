from flask import Flask
from blueprints.budgets.budgets import budgets_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.auth.auth import auth_bp


app = Flask(__name__)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(budgets_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)