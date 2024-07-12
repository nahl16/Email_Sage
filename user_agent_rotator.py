import random
from fake_useragent import UserAgent

class UserAgentRotator:
    def __init__(self):
        self.ua = UserAgent()

    def get_random_user_agent(self):
        return self.ua.random

    def rotate_user_agent(self):
        return {'User-Agent': self.get_random_user_agent()}