from .meta import content_proper, initial_data, ponencia_slice, sanitized


def get_legacy_sc_data(text: str, idx: str) -> dict:
    """Use the supplied parameters to combine data dictionaries.

    Args:
        text (str): The unprocessed string representing the ponencia
        idx (str): The url identifier

    Returns:
        dict: A dictionary with keys acceptable to scrapy processing pipeline.
    """
    data = initial_data(text, idx)
    if data["ponencia"]:
        data |= content_proper(data["ponencia"])
        data["ponencia"] = ponencia_slice(data)
    data = sanitized(data)

    # data_complete["ponencia"] = transform(data_complete["ponencia"]) TODO: causes TypeError on BAD DATE
    return data
