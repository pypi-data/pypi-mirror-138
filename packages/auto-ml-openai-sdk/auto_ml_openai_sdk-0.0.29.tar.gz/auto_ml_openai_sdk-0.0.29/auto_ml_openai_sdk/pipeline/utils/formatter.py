import nltk
from nltk import tokenize

nltk.download("punkt")


def clean_generation_prediction(generation: str) -> str:
    """Clean the generation.

    Parameters
    ----------
    generation : str
        the raw generation

    Returns
    -------
    str
        cleaned generation

    """
    generation_cleaned = ".".join(generation.split(".")[:-1]) + "."

    sentences = tokenize.sent_tokenize(generation_cleaned)

    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.replace("\xa0", "").replace("->", "")
        cleaned_sentences.append(sentence.split("\n")[-1])
    generation_cleaned = " ".join(cleaned_sentences)

    generation_cleaned = (
        generation_cleaned[2:] if generation_cleaned[:2] == "->" else generation_cleaned
    )
    return generation_cleaned
