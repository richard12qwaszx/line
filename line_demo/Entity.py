from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bjyewxfavmmuiz:c15c1c5b08518b8f0714d7018b0091aaf2e11c16e30292a9de781c335a68b9f7@ec2-107-22-33-173.compute-1.amazonaws.com:5432/dbaej41dd77jbp'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class PictureDate(db.Model):
    __tablename__ = 'PictureDate'

    Id = db.Column(db.Integer, primary_key=True)
    Uuid = db.Column(db.String(64), unique=True)
    Title = db.Column(db.String(64))
    Description = db.Column(db.String(128))

if __name__ == '__main__':
    manager.run()