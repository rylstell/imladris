from imladris import db
from random import shuffle




def main():

    min_id = 1
    max_id = 3935

    crypto_ids = db.get_cryptos(fields=["crypto_id"])
    valid = lambda crypto_id: crypto_id >= min_id and crypto_id <= max_id
    crypto_ids = list(filter(valid, crypto_ids))
    shuffle(crypto_ids)

    crypto_ids = crypto_ids[:100]

    with db.open_connection() as con:
        query = "UPDATE Crypto SET test_crypto = 1 WHERE crypto_id = (%s);"
        cur = con.cursor()
        for crypto_id in crypto_ids:
            cur.execute(query, (crypto_id,))
        con.commit()
        cur.close()






if __name__ == "__main__":
    main()
