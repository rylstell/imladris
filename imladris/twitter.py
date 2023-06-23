import tweepy
from imladris.utilities import segment_list


class TwitterApi(tweepy.API):

    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        self.auth = tweepy.OAuthHandler(api_key, api_key_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        super().__init__(self.auth)

    def get_users(self, usernames):
        request_size = 100
        users = []
        for seg in segment_list(usernames, request_size):
            users += list(self.lookup_users(screen_names=seg))
        return users

