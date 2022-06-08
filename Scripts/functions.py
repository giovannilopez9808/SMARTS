from os import makedirs


def mkdir(path: str) -> None:
    makedirs(path,
             exist_ok=True)


def fill_number(number: int, fill: int) -> str:
    number_str = str(number)
    number_str = number_str.zfill(fill)
    return number_str
