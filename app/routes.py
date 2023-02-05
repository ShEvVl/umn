import numpy as np
from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Data
from app.algorithm import func
from sklearn.ensemble import IsolationForest


routes = Blueprint("routes", __name__)


@routes.route("/")
def hello():
    return {"hello": "world"}


@routes.route("/api/data", methods=["POST", "GET"])
def handle_data():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_data = Data(
                feature_1=data["feature_1"],
                feature_2=data["feature_2"],
                feature_3=data["feature_3"],
                feature_4=data["feature_4"],
                feature_5=data["feature_5"],
            )
            db.session.add(new_data)
            db.session.commit()
            return {"message": f"data {new_data.id} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == "GET":
        datas = Data.query.all()
        results = [
            {
                "feature_1": value.feature_1,
                "feature_2": value.feature_2,
                "feature_3": value.feature_3,
                "feature_4": value.feature_4,
                "feature_5": value.feature_5,
            }
            for value in datas
        ]

        return {"count": len(results), "data": results}


@routes.route("/api/add", methods=["POST"])
def pst():
    """
    1st api is adding data to db

    Returns:
        json(dict): added string of data in db
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


@routes.route("/check", methods=["GET"])
def gt():
    """
    function to view what inside db right now

    Returns:
        json(dict): dict with all datas in db
    """
    data = Data.query.all()
    # serialized data from database
    dic = {
        i + 1: {x: y for x, y in sorted(list(vars(v).items()))[1:-1]}
        for i, v in enumerate(data)
    }
    return jsonify(dic)


@routes.route("/api/fit", methods=["POST"])
def ft():
    """
    2nd api is fitting model with all available data in db

    Returns:
        json(dict): "Model learned": info about fitting model
    """

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


@routes.route("/api/predict", methods=["POST"])
def prdct():
    """
    3rd api is predicting result of model with feature importances

    Returns:
        json(dict): get "anomaly(-1)" or "normal(1)" and descending features with amount
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
