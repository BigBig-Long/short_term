from short_term.db import database
class User(database.Model):
    __tablename__ = 'user'
    user_id = database.Column(database.Integer, primary_key=True,autoincrement=True)
    user_name = database.Column(database.String(255), nullable=True,unique=True)
    user_password = database.Column(database.String(255), nullable=True)
    histories = database.relationship('History',backref="user",lazy=True)
