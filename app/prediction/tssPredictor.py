import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os

dirname = os.path.dirname(__file__)

classifier_path = os.path.join(dirname, 'RandomForestClassifierTSSFiltered.pkl')

with open(classifier_path, 'rb') as f:
    classifier_sklearn = pickle.load(f)


def tss_predictor_sklearn(data_frame):

    y = classifier_sklearn.predict(data_frame)

    tss = np.where(y == 1)[0]

    probabilities = classifier_sklearn.predict_proba(data_frame)[tss][:, 1]

    tss_list = []

    for index, site in enumerate(tss):
        tss_list.append({"start": int(site), "end": int(site), "confidence": float(probabilities[index])})

    return {"TSS Sites": tss_list}
