class Credential:
    def __init__(self):
        self.username = "root"
        self.password = ""

    @staticmethod
    def get_username(cred):
        return cred.username

    @staticmethod
    def get_password(cred):
        return cred.password
