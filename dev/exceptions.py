class AdminNotFound(Exception):
    def __init__(self, login):
        self.login = login

    def __str__(self):
        return f"Admin with login '{self.login}' not found"