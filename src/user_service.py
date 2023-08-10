from csv_file_handler import CSVFileHandler


class UserService:
    """
        Service which respond for all communications between users
        storing users, retrieving and so on.
    """
    def __init__(self, handler: CSVFileHandler):
        self.csv_file_handler = handler

    def check_user_exist(self, id: int):
        pass

    def get_user_by_id(self, id: int):
        users = self.csv_file_handler.read_all_rows()
        for user in users:
            print(f"Checking user id: {user['id']}")
            if user['id'] == id:
                return user
            return None
