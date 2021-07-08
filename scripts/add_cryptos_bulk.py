from imladris import cmc_api, nom_api, db
import pickler




def main():

    cmc_meta = pickler.load("bbblah1.pickle")
    # cmc_ids = [crypto["id"] for crypto in cmc_api.mapping()]
    # cmc_meta = cmc_api.metadata(cmc_ids)
    # pickler.dump(cmc_meta, "bbblah1.pickle")
    print("cmc received")

    # nomics_metadata = pickler.load("bbblah1.pickle")
    # nomics_ids = set([crypto["id"] for crypto in nomics_metadata])
    nomics_ids = set([crypto["id"] for crypto in nom_api.metadata()])
    pickler.dump(cmc_meta, "bbblah2.pickle")
    print("nomics received")

    db_cmc_ids = set(db.get_cryptos(fields=["cmc_id"], dictionary=False))
    print("db cmc received")

    valid = lambda c: c["id"] not in db_cmc_ids
    cmc_meta = filter(valid, cmc_meta)
    print("cmc filtered")

    for crypto in cmc_meta:
        crypto["nomics_id"] = crypto["symbol"] if crypto["symbol"] in nomics_ids else None
        crypto["twitter_following"] = False

    print("data added to cryptos")

    db.add_cmc_cryptos(cmc_meta)
    print("db updated")






if __name__ == "__main__":
    main()
