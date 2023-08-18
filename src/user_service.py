from csv_file_handler import CSVFileHandler
import os


class UserService:
    """
        Service which respond for all communications between users
        storing users, retrieving and so on.
    """
    def __init__(self, handler):
        pass

    def check_user_exist(self):
        pass

    def get_user_by_id(self, id: int):
        pass

    def add_user(self, id: int, username: str, first_name: str, last_name: str, user_type: str) -> None:
        csv_handler = CSVFileHandler(os.getenv("PATH_TO_DB"))
        csv_handler.write_row({'id': id,
                               'username': username,
                               'first_name': first_name,
                               'last_name': last_name,
                               'user_type': user_type
                               })
