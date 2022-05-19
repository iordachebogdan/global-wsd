import json
from sys import argv

path_to_predictions = argv[1]

with open(path_to_predictions) as f:
    predictions: dict = json.load(f)
    ok, not_ok = 0, 0
    for item in predictions.values():
        local_ok, local_not_ok = 0, 0
        for pred_syn in item["predicted"]:
            if pred_syn in item["correct"]:
                local_ok += 1
            else:
                local_not_ok += 1
        ok += local_ok / len(item["predicted"])
        not_ok += local_not_ok / len(item["predicted"])

    precision = ok / (ok + not_ok)
    recall = ok / (len(predictions))
    f1 = 0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

    print(f"{precision=}, {recall=}, {f1=}")
