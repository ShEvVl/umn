import pickle
import numpy as np
from flask import Blueprint, jsonify, request
from app import db
from app.models import Data
from app.utils import algorithm
from app.config import clf_model_name
from sklearn.ensemble import IsolationForest


routes = Blueprint("routes", __name__)


@routes.route("/")
def hello():
    return {
        "Greetings": [
            "This is the anomaly detection server",
            "If you see this message, the server is up",
        ]
    }


@routes.route("/api/data", methods=["POST", "GET"])
def data_endpoint():
    if request.method == "POST":
        # Read the number of features from the file
        with open("app/feature_names.txt", "r") as f:
            num_features = len(f.readlines())

        # Get the values from the request
        values = request.get_json()
        # Check if the number of values matches the number of features
        if len(values) != num_features:
            return (
                jsonify(
                    {
                        "error": "The number of values does not match the number of features"
                    }
                ),
                400,
            )

        # Create a new data object and add it to the database
        data = Data(*values)
        print(vars(data))
        db.session.add(data)
        db.session.commit()

        return jsonify({"message": "Data created successfully"}), 201

    if request.method == "GET":
        # Read the number of features from the file
        with open("app/feature_names.txt", "r") as f:
            num_features = len(f.readlines())

        # Get all the data from the database
        data = Data.query.all()

        # Convert the data to a list of dictionaries
        data = [
            {
                f"feature_{i}": getattr(d, f"feature_{i}")
                for i in range(1, num_features + 1)
            }
            for d in data
        ]

        return jsonify({"count": len(data), "data": data}), 200


@routes.route("/api/fit", methods=["POST"])
def ft():
    """
    2nd api is fitting model with all available data in db

    Returns:
        json(dict): "Model learned": info about fitting model
    """
    with open("app/feature_names.txt", "r") as f:
        num_features = len(f.readlines())

    # collect data from database
    X_train = np.array(
        [
            [getattr(data, f"feature_{i}") for i in range(1, num_features + 1)]
            for data in db.session.query(Data).all()
        ]
    )

    # fit the model
    clf = IsolationForest(max_samples=100)
    clf.fit(X_train)
    pickle.dump(clf, open(clf_model_name, "wb"))
    clf = pickle.load(open(clf_model_name, "rb"))
    return jsonify({"Model learned": str(clf)})


@routes.route("/api/predict", methods=["POST"])
def predict():
    """
    API endpoint for making predictions

    Returns:
        json(dict): returns the predicted class as "anomaly(-1)" or "normal(1)" and the feature importances in descending order.
    """
    with open("app/feature_names.txt", "r") as f:
        features = f.read().strip().split("\n")
    with open("app/feature_names.txt", "r") as f:
        num_features = len(f.readlines())

    # Recieve request
    data = np.array([request.get_json()])

    # Check if the number of values matches the number of features
    if data.shape[1] != num_features:
        return (
            jsonify(
                {
                    "error": f"The number of values ({data.shape[1]}) does not match the number of features ({num_features})"
                }
            ),
            400,
        )

    # Load the classifier model
    clf = pickle.load(open(clf_model_name, "rb"))

    # Prepare the data for prediction
    ans = algorithm(clf.estimators_, data)
    # Make the prediction
    ans["ans"] = {features[n]: v for n, v in ans["ans"].items()}
    display = dict(list(ans["ans"].items())[:15])
    if clf.predict(data) == -1:
        anomaly = "anomaly(-1)"
    elif clf.predict(data) == 1:
        anomaly = "normal(1)"
    return jsonify({"predicted class": anomaly, "features importances": display})
