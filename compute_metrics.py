from collections import defaultdict
import json
from sys import argv

path_to_predictions = argv[1]

wn_to_pos = {
    "n": "NOUN",
    "a": "ADJ",
    "s": "ADJ",
    "v": "VERB",
    "r": "ADV",
}

with open(path_to_predictions) as f:
    predictions: dict = json.load(f)
    ok, not_ok, total = defaultdict(int), defaultdict(int), defaultdict(int)
    for item in predictions.values():
        local_ok, local_not_ok = 0, 0
        for pred_syn in item["predicted"]:
            if pred_syn in item["correct"]:
                local_ok += 1
            else:
                local_not_ok += 1
        add_ok = local_ok / len(item["predicted"])
        add_not_ok = local_not_ok / len(item["predicted"])
        ok["ALL"] += add_ok
        not_ok["ALL"] += add_not_ok
        total["ALL"] += 1
        pos = wn_to_pos[item["correct"][0].split(".")[1]]
        ok[pos] += add_ok
        not_ok[pos] += add_not_ok
        total[pos] += 1

    for tag in ok:
        precision = ok[tag] / (ok[tag] + not_ok[tag])
        recall = ok[tag] / total[tag]
        f1 = (
            0
            if precision + recall == 0
            else 2 * precision * recall / (precision + recall)
        )

        print(f"{tag}: {precision=}, {recall=}, {f1=}")
