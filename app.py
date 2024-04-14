from flask import Flask, jsonify, request
from config import Config
from models import db, Toilet
from flask_migrate import Migrate

app = Flask(__name__)

# Database
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "Test"

@app.route('/toilets', methods=['GET'])
def get_toilets():
    print("before query")
    toilets = Toilet.query.all()
    print(f"toilets: {toilets}")
    return jsonify([toilet.to_dict() for toilet in toilets])

@app.route('/toilets', methods=['POST'])
def add_toilet():
    toilet_data = request.json
    toilet = Toilet(
        name=toilet_data['name'],
        latitude=toilet_data['latitude'],
        longitude=toilet_data['longitude'],
        accessibility=toilet_data.get('accessibility', ''),
        description=toilet_data.get('description', '')
    )
    db.session.add(toilet)
    db.session.commit()
    return jsonify(toilet.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)









# GET API request
@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Mike",
        "email": "mike.mock@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

# POST API request
@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data), 201