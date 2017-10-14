from time import sleep


def file_input(file_path, old_value, delay=3, force=False):
    """
    Renvoit le contenu d'un fichier tant qu'il est différent de old_value: str
    """
    assert isinstance(old_value, str)
    while True:
        with open(file_path, 'r') as f:
            data = f.read().split('\n')[0]
        if data != old_value or force:
            return data
        sleep(delay)


def print_into_file(file, message):
    assert isinstance(file, str)
    assert isinstance(message, str)
    with open(file, 'w') as f:
        f.write(message)
