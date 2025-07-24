from app import app
from db import database

from model.User import User
from model.History import History
from model.Hourse_info import Hourse_info

app.app_context().push()
database.create_all()
