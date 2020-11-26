from flask_script import Command
from flask_blog import db


class InitDB(Command):
    "create database"  #コメントアウト?

    def run(self):
        db.create_all()
