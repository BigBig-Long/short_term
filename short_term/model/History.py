from .. db import database


class History(database.Model):
    __tablename__='history'
    id=database.Column(database.Integer,primary_key=True,autoincrement=True)
    city=database.Column(database.String(255),nullable=False)
    price=database.Column(database.String(255),nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.user_id'), nullable=False)