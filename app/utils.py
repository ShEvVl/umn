import numpy as np
from app import db
from app.models import Data


def algorithm(ens, X):
    """
    function to create descending feature importances
    Args:
        ens (list): list of deciding trees
        X (numpy.ndarray): data to predict model

    Returns:
        dict: descending feature importances
    """
    dic = {"ans": {}}

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

        for sample_id in range(len(X)):
            # obtain ids of the nodes 'sample_id goes through, i.e., row 'sample_id'
            node_index = node_indicator.indices[
                node_indicator.indptr[sample_id] : node_indicator.indptr[sample_id + 1]
            ]
            for node_id in node_index:
                # continue to the next node if is a leaf node
                if leaf_id[sample_id] == node_id:
                    continue

                for k in range(X.shape[1]):
                    if k == feature[node_id]:
                        dic["ans"][k] += 1

    dic["ans"] = {
        k: v
        for k, v in sorted(dic["ans"].items(), key=lambda item: item[1], reverse=True)
    }
    return dic


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
