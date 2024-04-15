from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Toilet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    timeOfDay = db.Column(db.String(128), nullable=True)
    openingHours = db.Column(db.String(128), nullable=True)
    buildingNumber = db.Column(db.String(128), nullable=True)
    street = db.Column(db.String(128), nullable=True)
    postcode = db.Column(db.String(128), nullable=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    lastUploaded = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'timeOfDay': self.timeOfDay,
            'openingHours': self.openingHours,
            'buildingNumber': self.buildingNumber,
            'street': self.street,
            'postcode': self.postcode,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'lastUploaded': self.lastUploaded.strftime('%Y-%m-%d %H:%M:%S') if self.lastUploaded else None
        }