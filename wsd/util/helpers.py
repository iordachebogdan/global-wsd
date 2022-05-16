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
