import json


class ImladrisConfig:

    def __init__(self, config_filename):
        self.load(config_filename)

    def load(self, config_filename):

        config = None
        with open(config_filename, "r") as config_file:
            config = json.load(config_file)

        self.CMC_API_KEY = config.get("CMC_API_KEY")
        self.NOMICS_API_KEY = config.get("NOMICS_API_KEY")
        self.TWITTER_API_KEY = config.get("TWITTER_API_KEY")
        self.TWITTER_API_KEY_SECRET = config.get("TWITTER_API_KEY_SECRET")
        self.TWITTER_ACCESS_TOKEN = config.get("TWITTER_ACCESS_TOKEN")
        self.TWITTER_ACCESS_TOKEN_SECRET = config.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.TWILIO_ACCOUNT_SID = config.get("TWILIO_ACCOUNT_SID")
        self.TWILIO_AUTH_TOKEN = config.get("TWILIO_AUTH_TOKEN")
        self.TWILIO_PHONE_NUMBER = config.get("TWILIO_PHONE_NUMBER")
        self.SQUOG_PHONE_NUMBER = config.get("SQUOG_PHONE_NUMBER")
        self.DATABASE_HOST = config.get("DATABASE_HOST")
        self.DATABASE_USER = config.get("DATABASE_USER")
        self.DATABASE_PASS = config.get("DATABASE_PASS")
        self.DATABASE_NAME = config.get("DATABASE_NAME")
        self.RUN_EVALUATION = config.get("RUN_EVALUATION")
