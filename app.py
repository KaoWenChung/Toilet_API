import csv
import io
from datetime import datetime
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

@app.route('/import-csv', methods=['POST'])
def import_csv():
    print("got the file")
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    next(csv_input, None)  # Skip the header row if present

    for row in csv_input:
        new_toilet = Toilet(
            name=row[0],
            status=row[1],
            timeOfDay=row[2],
            openingHours=row[3],
            buildingNumber=row[4],
            street=row[5],
            postcode=row[6],
            longitude=float(row[7]),
            latitude=float(row[8]),
            lastUploaded=datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S') if row[9] else None
        )
        db.session.add(new_toilet)

    db.session.commit()
    return jsonify({"message": "CSV data imported successfully"}), 200
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