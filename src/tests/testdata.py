import os


def read(file_name):
    """
    Reads test data responses from test_responses folder.
    """
    test_path = os.path.dirname(__file__)
    file_path = os.path.join(test_path, "test_responses", file_name)
    with open(file_path, 'r', encoding='utf8') as data_file:
        return data_file.read()
