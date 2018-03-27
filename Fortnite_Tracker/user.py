class User:
    name = ""
    username = ""
    url = ""
    number = ""
    total = None
    top25 = None
    top12 = None
    top6 = None

    def __init__(self, name, username, number):
        self.name = name
        self.username = username
        self.url = "https://api.fortnitetracker.com/v1/profile/psn/" + username
        self.number = number