from csv_file_handler import CSVFileHandler
import os


class UserService:
    """
        Service which respond for all communications between users
        storing users, retrieving and so on.
    """
    def __init__(self):
        self.csv_file_handler = CSVFileHandler('users.csv')

    def check_user_exist(self, id: int):
        pass

    def get_user_by_id(self, id: int):
        users = self.csv_file_handler.read_all_rows()
        for user in users:
            print(f"Checking user id: {user['id']}")
            if user['id'] == id:
                return user
            return None
        pass

    def add_user(self, id: int, username: str, first_name: str, last_name: str, user_type: str) -> None:
        csv_handler = CSVFileHandler(os.getenv("PATH_TO_DB"))
        csv_handler.write_row({'id': id,
                               'username': username,
                               'first_name': first_name,
                               'last_name': last_name,
                               'user_type': user_type
                               })
