import csv
import io
from datetime import datetime
from flask import Flask, jsonify, request
from config import Config
from utility import standard_response
from models import db, Toilet
from flask_migrate import Migrate

app = Flask(__name__)

# Database
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return "Welcome to the Toilet API!"

@app.route('/toiletList', methods=['GET'])
def get_toilets():
    toilets = Toilet.query.all()
    toilets_data = [toilet.to_dict() for toilet in toilets]
    return standard_response(toilets_data, 200, "success")

@app.route('/importToiletsCSV', methods=['POST'])
def import_csv():
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
    return standard_response(status="CSV data imported successfully")
@app.route('/addToilet', methods=['POST'])
def add_toilet():
    toilet_data = request.json
    required_fields = ['name', 'status', 'longitude', 'latitude']
    missing_fields = [field for field in required_fields if field not in toilet_data]

    if missing_fields:
        return standard_response(code=404, status=f"{missing_fields} not found")

    try:
        last_uploaded = datetime.strptime(toilet_data.get('lastUploaded'), '%Y-%m-%d %H:%M:%S') \
            if 'lastUploaded' in toilet_data and toilet_data['lastUploaded'] else datetime.now()

        toilet = Toilet(
            name=toilet_data['name'],
            status=toilet_data['status'],
            timeOfDay=toilet_data.get('timeOfDay'),  # Optional field
            openingHours=toilet_data.get('openingHours'),  # Optional field
            buildingNumber=toilet_data.get('buildingNumber'),  # Optional field
            street=toilet_data.get('street'),  # Optional field
            postcode=toilet_data.get('postcode'),  # Optional field
            longitude=float(toilet_data['longitude']),
            latitude=float(toilet_data['latitude']),
            lastUploaded=last_uploaded
        )
        db.session.add(toilet)
        db.session.commit()
        return standard_response(toilet.to_dict(), 201, "success")
    except Exception as e:
        return standard_response({"error": str(e)}, 500, "error")

if __name__ == "__main__":
    app.run(debug=True)