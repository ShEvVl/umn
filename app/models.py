from app import db


class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    feature_1 = db.Column(db.Float)
    feature_2 = db.Column(db.Float)
    feature_3 = db.Column(db.Float)
    feature_4 = db.Column(db.Float)
    feature_5 = db.Column(db.Float)

    def __init__(self, feature_1, feature_2, feature_3, feature_4, feature_5):
        self.feature_1 = feature_1
        self.feature_2 = feature_2
        self.feature_3 = feature_3
        self.feature_4 = feature_4
        self.feature_5 = feature_5

    def __repr__(self):
        return f"<Data {self.id}>"
