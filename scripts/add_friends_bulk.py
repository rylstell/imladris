from imladris import db, twit_api
import traceback
import sys
import time
from datetime import datetime
import pickler




# last friendship crypto_id: 5542
# start time: 2021-07-02 19:01:15.908966
# end time:   2021-07-02 19:23:46.556313



def main():

    UP_TO_CRYPTO_ID = 5542

    cryptos = db.get_cryptos(fields=["crypto_id", "twitter_username"], dictionary=True)
    valid = lambda crypto: crypto["twitter_username"] != None and crypto["crypto_id"] > UP_TO_CRYPTO_ID
    cryptos = list(filter(valid, cryptos))

    num_cryptos = len(cryptos)
    total_friendships = 399

    crypto_count = 0
    friendship_count = 0
    friends_cryptos_ids = []

    start_time = datetime.now()
    print("start time:", str(start_time))

    while friendship_count < total_friendships and crypto_count < num_cryptos:
        crypto = cryptos[crypto_count]
        print("crypto id", crypto["crypto_id"], end=", ")
        try:
            twit_api.create_friendship(crypto["twitter_username"])
            friends_cryptos_ids.append(crypto["crypto_id"])
            friendship_count += 1
            print(f"friendship count {friendship_count}, crypto count {crypto_count}, ** friendship created **")
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print(end="error:  ", flush=True)
            traceback.print_exc()
        crypto_count += 1
        time.sleep(5)

    print("start time:", str(start_time))
    print("end time:", str(datetime.now()))
    print(f"# {friendship_count} friendships created")

    pickler.dump(friends_cryptos_ids, "friends_cryptos_ids_3.pickle")

    with db.open_connection() as con:
        query = "UPDATE Crypto SET twitter_following = (%s) WHERE crypto_id = (%s)"
        cur = con.cursor()
        for crypto_id in friends_cryptos_ids:
            cur.execute(query, (True, crypto_id))
        con.commit()
        cur.close()

    print("imladrisdb updated")
    print("done")






if __name__ == "__main__":
    main()
