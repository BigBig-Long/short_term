from ..db import database

class Trading(database.Model):
    __tablename__ = 'trading'
    id = database.Column(database.Integer, primary_key=True)
    community_name = database.Column(database.String(255), nullable=True)
    district = database.Column(database.String(255), nullable=True)
    area = database.Column(database.String(255), nullable=True)
    house_type = database.Column(database.String(255), nullable=True)
    building_area = database.Column(database.Float, nullable=True)
    transaction_price = database.Column(database.Float, nullable=True)
    listing_price = database.Column(database.Float, nullable=True)
    unit_price = database.Column(database.Integer, nullable=True)
    transaction_period = database.Column(database.Integer, nullable=True)
    transaction_date = database.Column(database.Date, nullable=True)
    transaction_channel = database.Column(database.String(255), nullable=True)
    orientation = database.Column(database.String(255), nullable=True)
    decoration = database.Column(database.String(255), nullable=True)
    elevator = database.Column(database.String(255), nullable=True)
    floor_level = database.Column(database.String(255), nullable=True)
    total_floors = database.Column(database.Integer, nullable=True)
    construction_year = database.Column(database.Integer, nullable=True)
    building_structure = database.Column(database.String(255), nullable=True)
    full_two_five = database.Column(database.String(255), nullable=True)
