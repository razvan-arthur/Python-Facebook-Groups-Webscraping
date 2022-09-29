class Post:
    

    def __init__(self, url, user, cerere):
        self.url = url
        self.user = user
        self.cerere = cerere

    def __repr__(self):
        return "Post('{}', '{}', {})".format(self.url, self.user, self.cerere)
    def get_user(self):
        return self.user