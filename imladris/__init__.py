from imladris.imladris_config import ImladrisConfig
from imladris.imladrisdb import ImladrisDatabase
from imladris.cmc import CMCApi
from imladris.nomics import NomicsApi
from imladris.twitter import TwitterApi
from imladris.twilio import TwilioApi


Config = ImladrisConfig("../imladris_config.json")

db = ImladrisDatabase(
    Config.DATABASE_HOST,
    Config.DATABASE_USER,
    Config.DATABASE_PASS,
    Config.DATABASE_NAME)

cmc_api = CMCApi(Config.CMC_API_KEY)

nom_api = NomicsApi(Config.NOMICS_API_KEY)

twit_api = TwitterApi(
    Config.TWITTER_API_KEY,
    Config.TWITTER_API_KEY_SECRET,
    Config.TWITTER_ACCESS_TOKEN,
    Config.TWITTER_ACCESS_TOKEN_SECRET)

twilio_api = TwilioApi(
    Config.TWILIO_ACCOUNT_SID,
    Config.TWILIO_AUTH_TOKEN,
    Config.TWILIO_PHONE_NUMBER,
    Config.SQUOG_PHONE_NUMBER)
