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
