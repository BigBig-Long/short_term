from db import db

class Trading(db.Model):
    __tablename__ = 'trading'
    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(255), nullable=True)
    district = db.Column(db.String(255), nullable=True)
    area = db.Column(db.String(255), nullable=True)
    house_type = db.Column(db.String(255), nullable=True)
    building_area = db.Column(db.Float, nullable=True)
    transaction_price = db.Column(db.Float, nullable=True)
    listing_price = db.Column(db.Float, nullable=True)
    unit_price = db.Column(db.Integer, nullable=True)
    transaction_period = db.Column(db.Integer, nullable=True)
    transaction_date = db.Column(db.Date, nullable=True)
    transaction_channel = db.Column(db.String(255), nullable=True)
    orientation = db.Column(db.String(255), nullable=True)
    decoration = db.Column(db.String(255), nullable=True)
    elevator = db.Column(db.String(255), nullable=True)
    floor_level = db.Column(db.String(255), nullable=True)
    total_floors = db.Column(db.Integer, nullable=True)
    construction_year = db.Column(db.Integer, nullable=True)
    building_structure = db.Column(db.String(255), nullable=True)
    full_two_five = db.Column(db.String(255), nullable=True)
