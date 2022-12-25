import numpy as np


def func(ens, X):
    """
    function to create descending feature importances
    Args:
        ens (list): list of deciding trees
        X (numpy.ndarray): data to predict model

    Returns:
        dict: descending feature importances
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
