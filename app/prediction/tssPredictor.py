import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os

dirname = os.path.dirname(__file__)

classifier_forward_path = os.path.join(dirname, 'RandomForestClassifierTSSFilteredForward.pkl')

classifier_reverse_path = os.path.join(dirname, 'RandomForestClassifierTSSFilteredReverse.pkl')

with open(classifier_forward_path, 'rb') as f:
    classifier_forward = pickle.load(f)

with open(classifier_reverse_path, 'rb') as f:
    classifier_reverse = pickle.load(f)


def tss_predictor_sklearn(data_frame, reverse = False):

    if(reverse):
        y = classifier_reverse.predict(data_frame)
        tss = np.where(y == 1)[0]
        probabilities = classifier_reverse.predict_proba(data_frame)[tss][:, 1]

    else:
        y = classifier_forward.predict(data_frame)
        tss = np.where(y == 1)[0]
        probabilities = classifier_forward.predict_proba(data_frame)[tss][:, 1]

    tss_list = []

    for index, site in enumerate(tss):
        tss_list.append({"start": int(site), "end": int(site), "confidence": float(probabilities[index])})

    return {"TSS Sites": tss_list}
