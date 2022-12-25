from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature_1 = db.Column(db.Float)
    feature_2 = db.Column(db.Float)
    feature_3 = db.Column(db.Float)
    feature_4 = db.Column(db.Float)
    feature_5 = db.Column(db.Float)

    def __repr__(self):
        return f"<Data {self.id}>"
