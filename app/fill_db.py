import numpy as np
from app import db
from app.models import Data


def test_db():
    """
    func will restart current db and recreate test data

    Returns:
        str: "all done", when complite
    """
    db.drop_all()
    db.create_all()
    # Generate train data
    rng = np.random.RandomState(42)
    X = 0.3 * rng.randn(100, 5)
    X_train = np.r_[X + 2, X - 2]
    feature_1, feature_2, feature_3, feature_4, feature_5 = zip(*X_train)
    for i in range(len(X_train)):
        data = Data(
            feature_1=feature_1[i],
            feature_2=feature_2[i],
            feature_3=feature_3[i],
            feature_4=feature_4[i],
            feature_5=feature_5[i],
        )
        # fill database with test data
        db.session.add(data)
    db.session.commit()
    return "all done"
