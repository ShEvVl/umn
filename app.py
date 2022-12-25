import os
import numpy as np
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sklearn.ensemble import IsolationForest


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app)


@app.route("/api/add", methods=["POST"])
def pst():
    """_summary_

    Returns:
        _type_: _description_
    """
    if not request.json:
        abort(400)
    feature_1 = request.json["feature_1"]
    feature_2 = request.json["feature_2"]
    feature_3 = request.json["feature_3"]
    feature_4 = request.json["feature_4"]
    feature_5 = request.json["feature_5"]
    data = Data(
        feature_1=feature_1,
        feature_2=feature_2,
        feature_3=feature_3,
        feature_4=feature_4,
        feature_5=feature_5,
    )
    # import data to database
    db.session.add(data)
    db.session.commit()
    last = db.session.query(Data).order_by(Data.id.desc()).first()
    dic = {x: y for x, y in list(vars(last).items())[1:]}
    return jsonify(dic)


@app.route("/check", methods=["GET"])
def gt():
    """_summary_

    Returns:
        _type_: _description_
    """
    data = Data.query.all()
    # serialized data from database
    dic = {
        i + 1: {x: y for x, y in sorted(list(vars(v).items()))[1:-1]}
        for i, v in enumerate(data)
    }
    return jsonify(dic)


@app.route("/api/fit", methods=["POST"])
def model():
    """_summary_

    Returns:
        _type_: _description_
    """
    with app.app_context():
        # collect data from database
        X_train = np.array(
            [
                [
                    data.feature_1,
                    data.feature_2,
                    data.feature_3,
                    data.feature_4,
                    data.feature_5,
                ]
                for data in db.session.query(Data).all()
            ]
        )

    # fit the model
    rng = np.random.RandomState(42)
    global clf
    clf = IsolationForest(max_samples=100, random_state=rng)
    clf.fit(X_train)
    return jsonify({"Model learned": str(clf)})


@app.route("/api/predict", methods=["POST"])
def prdct():
    """_summary_

    Returns:
        _type_: _description_
    """
    feature_1 = request.json["feature_1"]
    feature_2 = request.json["feature_2"]
    feature_3 = request.json["feature_3"]
    feature_4 = request.json["feature_4"]
    feature_5 = request.json["feature_5"]
    data = np.array(
        [
            [
                feature_1,
                feature_2,
                feature_3,
                feature_4,
                feature_5,
            ]
        ]
    )
    ans = func(clf.estimators_, data)
    for i in list(ans["ans"].keys()):
        ans["ans"][sorted(list(vars(db.session.query(Data).first())))[1:-1][i]] = ans[
            "ans"
        ].pop(i)
    if clf.predict(data) == -1:
        anomaly = "anomaly(-1)"
    elif clf.predict(data) == 1:
        anomaly = "normal(1)"
    return jsonify({"predicted class": anomaly, "features importances": ans["ans"]})


def func(ens, X):
    """_summary_

    Args:
        ens (_type_): _description_
        X (_type_): _description_

    Returns:
        _type_: _description_
    """
    dic = {}
    dic["ans"] = {}
    dic["count"] = {}
    dic["hist"] = {}

    try:
        X.shape[1]
    except (TypeError, IndexError):
        X = np.array([X])
    else:
        pass

    for a in range(X.shape[1]):
        dic["ans"][a] = 0

    for i, clf in enumerate(ens):
        node_indicator = clf.decision_path(X)
        leaf_id = clf.apply(X)
        feature = clf.tree_.feature
        threshold = clf.tree_.threshold

        dic["count"][i] = {}
        for j in range(X.shape[1]):
            dic["count"][i][j] = 0
        dic["hist"][i] = {}
        for sample_id in range(len(X)):
            hist = []
            # obtain ids of the nodes 'sample_id goes through, i.e., row 'sample_id'
            node_index = node_indicator.indices[
                node_indicator.indptr[sample_id] : node_indicator.indptr[sample_id + 1]
            ]
            for node_id in node_index:
                # continue to the next node if is a leaf node
                if leaf_id[sample_id] == node_id:
                    continue

                # check if value of the split feature for sample 0 is below threshold
                if X[sample_id, feature[node_id]] <= threshold[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"

                for k in range(X.shape[1]):
                    if k == feature[node_id]:
                        dic["count"][i][k] += 1
                        dic["ans"][k] += 1

                hist.append(
                    f"node {node_id}: (X[{sample_id}, {feature[node_id]}] = {X[sample_id, feature[node_id]]:.4f}) {threshold_sign} {threshold[node_id]:.4f}"
                )
                dic["hist"][i][sample_id] = hist
    dic["ans"] = {
        k: v
        for k, v in sorted(dic["ans"].items(), key=lambda item: item[1], reverse=True)
    }
    return dic


def restart_db():
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


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature_1 = db.Column(db.Float)
    feature_2 = db.Column(db.Float)
    feature_3 = db.Column(db.Float)
    feature_4 = db.Column(db.Float)
    feature_5 = db.Column(db.Float)

    def __repr__(self):
        return f"<Data {self.id}>"


if __name__ == "__main__":
    app.run(debug=True)
