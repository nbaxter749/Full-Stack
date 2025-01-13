from flask import Flask
from flask_cors import CORS
from blueprints.businesses.businesses import businesses_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.auth.auth import auth_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(businesses_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)