import time


# dummy predictor that does nothing and returns dummy prediction object
def tss_predictor(file_path):
    # simulate work
    time.sleep(10)
    return {"TSS Sites": [{"start": 1, "end": 11, "confidence": 0.5}, {"start": 11, "end": 12, "confidence": 0.1}]}
