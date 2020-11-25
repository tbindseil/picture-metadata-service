from project.server.log import INFO


class User():
    username = None
    admin = None

    def __init__(self, username, admin):
        self.username = username
        self.admin = admin
