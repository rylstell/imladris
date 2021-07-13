import time
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
import traceback
import logging
import pickler
from imladris import db, cmc_api, nom_api, twit_api, twilio_api, Config
from imladris.evaluators import E3434
from imladris.utilities import datetime_from_rfc3339






def prep_intervals_for_eval(intervals, evaluators):

    logging.info("preping intervals for eval")

    eval_scores_dict = dict(zip([e.name for e in evaluators], [None] * len(evaluators)))
    eval_intervals_scores_dict = dict(zip([e.name for e in evaluators], [[] for e in evaluators]))

    def get_default_crypto_mapping(id):
        crypto = {
            "crypto_id": id,
            "interval_start": None,
            "interval_end": None,
            "interval_data": {
                "interval_id": [],
                "price": [],
                "volume": [],
                "twitter_followers": [],
                "circulating_supply": [],
                "interval_count": [],
                "timestamp": []
            }
        }
        crypto.update(eval_scores_dict)
        crypto["interval_data"].update(eval_intervals_scores_dict)
        return crypto

    mapped_intervals = {}
    for interval in intervals:
        crypto_id = interval["crypto_id"]
        if crypto_id not in mapped_intervals:
            mapped_intervals[crypto_id] = get_default_crypto_mapping(crypto_id)
        interval_data = mapped_intervals[crypto_id]["interval_data"]
        for key in interval_data:
            interval_data[key].append(interval[key])

    for crypto in mapped_intervals.values():
        crypto["interval_start"] = crypto["interval_data"]["timestamp"][0]
        crypto["interval_end"] = crypto["interval_data"]["timestamp"][-1]

    return mapped_intervals







def add_crypto_intervals(start_datetime):

    logging.info("adding crypto intervals")

    try:

        interval_count = db.get_int_value("interval_count")

        tickers = nom_api.tickers(interval="1h")

        if tickers is None:
            raise Exception("tickers not recevied. returning.")

        cryptos = db.get_mapping("nomics_id", ["crypto_id", "twitter_username, twitter_following"])

        timestamp_buffer_10min = timedelta(minutes=10)

        def is_valid_ticker(ticker):
            timestamp = datetime_from_rfc3339(ticker["price_timestamp"])
            valid_timestamp = start_datetime - timestamp <= timestamp_buffer_10min
            return valid_timestamp and "1h" in ticker and ticker["id"] in cryptos and cryptos[ticker["id"]]["twitter_following"]

        tickers = list(filter(is_valid_ticker, tickers))

        ticker_ids = set([ticker["id"] for ticker in tickers])

        def is_valid_crypto(crypto):
            return crypto[0] in ticker_ids

        cryptos = dict(filter(is_valid_crypto, cryptos.items()))

        twitter_friends = twit_api.get_users([crypto["twitter_username"] for crypto in cryptos.values()])

        follower_counts = {}
        for friend in twitter_friends:
            follower_counts[friend.screen_name.lower()] = friend.followers_count

        intervals = []
        for ticker in tickers:

            crypto = cryptos[ticker["id"]]

            twitter_username = crypto["twitter_username"].lower()
            if twitter_username not in follower_counts:
                continue

            intervals.append({
                "crypto_id": crypto["crypto_id"],
                "price": ticker["price"],
                "volume": ticker["1h"]["volume"],
                "circulating_supply": ticker["circulating_supply"] if "circulating_supply" in ticker else None,
                "twitter_followers": follower_counts[twitter_username],
                "interval_count": interval_count,
                "timestamp": datetime_from_rfc3339(ticker["price_timestamp"])
            })

        db.add_intervals(intervals)
        db.update_int_value("interval_count", interval_count + 1)

        logging.info(f"{len(intervals)} intervals added. interval count is {interval_count}.")

        return True

    except:
        db.update_int_value("interval_count", interval_count + 1)
        tb = traceback.format_exc()
        logging.warning(f"error when adding crypto intervals.\n{tb}")
        twilio_api.send_text_to_admin("error in add_crypto_intervals")
        return False








def evaluate_cryptos(end_date):

    logging.info("evaluating cryptos")

    try:

        evaluators = [E3434()]
        evaluator_names = [e.name for e in evaluators]

        days_14 = timedelta(days=14)
        start_date = end_date - days_14

        intervals = db.get_intervals(start_date, end_date)

        cryptos = prep_intervals_for_eval(intervals, evaluators)

        for evaluator in evaluators:
            evaluator.evaluate(cryptos)

        interval_scores = []
        for crypto in cryptos.values():
            interval_id = crypto["interval_data"]["interval_id"][-1]
            scores = [crypto[name] for name in evaluator_names]
            evaluator_scores = dict(zip(evaluator_names, scores))
            interval_scores.append((interval_id, evaluator_scores))

        db.update_interval_scores(interval_scores)

        logging.info(f"{len(cryptos)} evaluated using evaluators: {', '.join(evaluator_names)}.")

    except:
        tb = traceback.format_exc()
        logging.warning(f"error when evaluating cryptos.\n{tb}")
        twilio_api.send_text_to_admin("error in evaluate_cryptos")







def add_new_cryptos():

    logging.info("adding new cryptos")

    try:

        api_cmc_ids = [crypto["id"] for crypto in cmc_api.mapping()]
        db_cmc_ids = db.get_cryptos(fields=["cmc_id"])

        new_ids = list(set(api_cmc_ids) - set(db_cmc_ids))

        new_cmc_meta = cmc_api.metadata(new_ids)

        nomics_ids = set([crypto["id"] for crypto in nom_api.metadata()])

        with_nomics_id = 0

        for crypto in new_cmc_meta:

            if crypto["twitter_username"]:
                try:
                    twit_api.create_friendship(crypto["twitter_username"])
                    crypto["twitter_following"] = True
                except:
                    crypto["twitter_following"] = False

            if crypto["symbol"] in nomics_ids:
                with_nomics_id += 1
                crypto["nomics_id"] = crypto["symbol"]
            else: crypto["nomics_id"] = None

        db.add_cmc_cryptos(new_cmc_meta)

        logging.info(f"cryptos added. {len(new_cmc_meta)} total. {with_nomics_id} with nomics_id.")

    except:
        tb = traceback.format_exc()
        logging.warning(f"error when adding cryptos.\n{tb}")
        twilio_api.send_text_to_admin("error in add_new_cryptos")







#twitter friendship isn't updated if twitter_username changes
def update_all_cryptos():

    logging.info("updating all cryptos")

    try:
        cmc_ids = [crypto["id"] for crypto in cmc_api.mapping()]
        cmc_meta = cmc_api.metadata(cmc_ids)
        db.update_cmc_cryptos(cmc_meta)
        logging
    except:
        tb = traceback.format_exc()
        logging.warning(f"error when updating cryptos.\n{tb}")
        twilio_api.send_text_to_admin("error in update_all_cryptos")








def run_hourly_jobs():
    Config.load("imladris_config.json")
    utcnow = datetime.utcnow().replace(tzinfo=pytz.utc, minute=0, second=0, microsecond=0)
    success = add_crypto_intervals(utcnow)
    if success and Config.RUN_EVALUATION:
        evaluate_cryptos(utcnow)


def run_daily_jobs():
    add_new_cryptos()


def run_weekly_jobs():
    if Config.UPDATE_ALL_CRYPTOS:
        update_all_cryptos()








def main():

    master_start = datetime.utcnow()

    log_filename = str(master_start.replace(microsecond=0))
    logging.basicConfig(
        filename=f"log/{log_filename}.log",
        level=logging.DEBUG,
        format='%(levelname)s: %(asctime)s      %(message)s'
    )
    logging.getLogger("requests").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    hours_1 = timedelta(hours=1)
    days_1 = timedelta(days=1)
    days_7 = timedelta(days=7)
    mins_2 = timedelta(minutes=2)
    mins_5 = timedelta(minutes=5)

    base_start = master_start.replace(tzinfo=pytz.utc, minute=0, second=0, microsecond=0)
    hourly_jobs_start = base_start + hours_1
    daily_jobs_start = base_start + days_1 - mins_2
    weekly_jobs_start = base_start + days_7 - mins_5

    logging.info(f"beginning scheduled jobs. hourly_jobs_start={hourly_jobs_start}, daily_jobs_start={daily_jobs_start}, weekly_jobs_start{weekly_jobs_start}")

    scheduler = BlockingScheduler(timezone=pytz.utc)
    scheduler.add_job(run_hourly_jobs, "interval", hours=1, start_date=hourly_jobs_start)
    scheduler.add_job(run_daily_jobs, "interval", days=1, start_date=daily_jobs_start)
    scheduler.add_job(run_weekly_jobs, "interval", days=7, start_date=weekly_jobs_start)

    try:
        scheduler.start()
    except:
        tb = traceback.format_exc()
        logging.warning(f"error with scheduler?\n{tb}")







def test():
    pass

    # add_crypto_intervals()
    # evaluate_cryptos()
    # add_new_cryptos_2()

    # utc_now = datetime.utcnow()
    # t_11_48 = utc_now.replace(tzinfo=pytz.utc, minute=48, second=0, microsecond=0)
    # print(t_11_48)
    #
    # scheduler = BlockingScheduler(timezone=pytz.utc)
    # scheduler.add_job(run_hourly_tasks, "interval", hours=1, start_date=t_11_48, args=(t_11_48,))
    # scheduler.start()





if __name__ == "__main__":
    main()
    # test()
