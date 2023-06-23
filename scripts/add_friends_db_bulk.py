from imladris import db, twit_api
from imladris.utilities import save_pickle, load_pickle



def main():

    # min_id = 1
    # max_id = 959
    #
    # cryptos = db.get_cryptos(fields=["crypto_id", "twitter_username"], dictionary=True)
    #
    # valid_crypto = lambda c: c["twitter_username"] is not None and (c["crypto_id"] >= min_id and c["crypto_id"] <= max_id)
    # cryptos = list(filter(valid_crypto, cryptos))
    #
    # twitter_usernames = [crypto["twitter_username"] for crypto in cryptos]
    # users = twit_api.get_users(twitter_usernames)

    cryptos, users = load_pickle("cryptos_users.pickle")

    cryptoids_usernames = [(c["crypto_id"], c["twitter_username"].lower()) for c in cryptos]

    friends_cryptos_ids = []
    for user in users:
        if user.following:
            sn_lower = user.screen_name.lower()
            for crypto_id, username in cryptoids_usernames:
                if sn_lower == username:
                    friends_cryptos_ids.append(crypto_id)

    # save_pickle(friends_cryptos_ids, "friends_cryptos_ids.pickle")

    # with db.open_connection() as con:
    #     query = "UPDATE Crypto SET twitter_following = (%s) WHERE crypto_id = (%s)"
    #     cur = con.cursor()
    #     for crypto_id in friends_cryptos_ids:
    #         cur.execute(query, (True, crypto_id))
    #     con.commit()
    #     cur.close()







if __name__ == "__main__":
    main()
