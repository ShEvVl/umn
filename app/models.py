from app import db


class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    with open("app/feature_names.txt", "r") as f:
        num_features = len(f.readlines())

    for i in range(num_features):
        exec(f"feature_{i+1} = db.Column(db.Float, nullable=False)")

    def __init__(self, *features):
        for i, feature in enumerate(features, start=1):
            setattr(self, f"feature_{i}", db.Column(db.Float, nullable=False))
            setattr(self, f"feature_{i}", feature)

    def __repr__(self):
        return f"<Data {self.id}>"
