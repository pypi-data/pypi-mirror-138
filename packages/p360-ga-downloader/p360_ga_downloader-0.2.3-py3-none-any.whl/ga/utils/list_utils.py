def split(data: list, chunk_size: int):
    """
    Evenly split list into lists of defined size

    :param data:
    :param chunk_size:
    :return:
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]
