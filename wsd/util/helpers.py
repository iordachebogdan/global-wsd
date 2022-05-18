import random


def penntreebank_to_wn(tag: str) -> None | str:
    tag = tag.lower()
    if tag.startswith("nn"):  # noun
        return "n"
    if tag.startswith("vb"):  # verb
        return "v"
    if tag.startswith("rb") or tag == "wrb":  # adverb
        return "r"
    if tag.startswith("jj"):  # adjective
        return "a"
    return None


def translate_to_wn_relations(relation: str) -> list[str]:
    if relation == "holonyms":
        return ["substance_holonyms", "part_holonyms", "member_holonyms"]
    elif relation == "meronyms":
        return ["substance_meronyms", "part_meronyms", "member_meronyms"]
    else:
        return [relation]


def discrete_random_variable(weights: list[float]) -> int:
    rand = random.uniform(0, 1)
    sum_weights: float = 0
    for i, weight in enumerate(weights):
        sum_weights += weight
        if rand < sum_weights:
            return i
    return len(weights)


def normalize(array: list[int | float], tol: float = 1e-7) -> list[float]:
    sum_array = sum(array)
    if sum_array < tol:
        sum_array = 1
    return [x / sum_array for x in array]
