from .. db import database

class Hourse_info(database.Model):
    __tablename__='hourse_info'
    id=database.Column(database.Integer,primary_key=True,autoincrement=True)
    title=database.Column(database.String(255),nullable=False)
    cover=database.Column(database.String(2555),nullable=False)
    city=database.Column(database.String(255),nullable=False)
    region=database.Column(database.String(255),nullable=False)
    address=database.Column(database.String(2555),nullable=False)
    rooms_desc=database.Column(database.String(255),nullable=False)
    area_range=database.Column(database.String(255),nullable=False)
    all_ready=database.Column(database.String(255),nullable=False)
    price=database.Column(database.String(255),nullable=False)
    hourseDecoration=database.Column(database.String(255),nullable=False)
    company=database.Column(database.String(255),nullable=False)
    hourseType=database.Column(database.String(255),nullable=False)
    on_time=database.Column(database.String(255),nullable=False)
    open_date=database.Column(database.String(255),nullable=False)
    tags=database.Column(database.String(255),nullable=False)
    totalPrice_range=database.Column(database.String(255),nullable=False)
    sale_status=database.Column(database.String(255),nullable=False)
    detail_url=database.Column(database.String(2555),nullable=False)
