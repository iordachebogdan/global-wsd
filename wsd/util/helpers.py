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


def xml_to_wn_pos(tag: str) -> None | str:
    tag = tag.lower()
    if tag == "noun":
        return "n"
    if tag == "adj":
        return "a"
    if tag == "verb":
        return "v"
    if tag == "adv":
        return "r"
    return None


def translate_to_wn_relations(relation: str) -> list[str]:
    if relation == "holonyms":
        return ["substance_holonyms", "part_holonyms", "member_holonyms"]
    elif relation == "meronyms":
        return ["substance_meronyms", "part_meronyms", "member_meronyms"]
    else:
        return [relation]


def discrete_random_variable(weights: list[float]) -> int:
    """Sample discrete random variable.

    Args:
        weights: N - 1 probability weights, the Nth weight is 1 - sum of the others

    Returns:
        the sampled value between 0 and N - 1
    """
    rand = random.uniform(0, 1)
    sum_weights: float = 0
    for i, weight in enumerate(weights):
        sum_weights += weight
        if rand < sum_weights:
            return i
    return len(weights)


def normalize(
    array: list[int | float], tol: float = 1e-7, ensure_distribution: bool = False
) -> list[float]:
    """Normalize array values.

    Args:
        array: the array to normalize
        tol: tolerance for 0-sum arrays
        ensure_distribution: if 0-sum array return uniform discrete distribution

    Returns:
        normalized array
    """
    sum_array = sum(array)
    if sum_array < tol:
        sum_array = 1
        if ensure_distribution:
            return [1 / len(array)] * len(array)
    return [x / sum_array for x in array]
