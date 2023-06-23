from datetime import datetime, timedelta
import pytz
from imladris import db
from imladris.utilities import save_pickle


def main():

    print("CORRECTING INTERVAL COUNTS")
    # "2021-07-11 21:59:00"
    start_date = datetime(2021, 7, 11, hour=22, tzinfo=pytz.utc)

    utcnow = datetime.utcnow().replace(tzinfo=pytz.utc)

    hours_1 = timedelta(hours=1)

    print("creating correct_data")
    correct_data = []
    count = 0
    while start_date < utcnow:
        correct_data.append((count, start_date))
        count += 1
        start_date += hours_1


    print("retrieving doge_data")
    with db.open_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT interval_count, timestamp FROM Interval_1hr WHERE crypto_id = 29 ORDER BY interval_count ASC;")
        doge_data = cur.fetchall()
        cur.close()


    corrections = []

    di = 0
    ci = 0

    mins_10 = timedelta(minutes=10)

    print("creating corrections")
    while di < len(doge_data) and ci < len(correct_data):

        d_count, d_dt = doge_data[di]
        c_count, c_dt = correct_data[ci]

        d_dt = d_dt.replace(tzinfo=pytz.utc)

        diff = abs(c_dt - d_dt)

        if diff <= mins_10:
            corrections.append((d_count, c_count))
            di += 1
            ci += 1
        else:
            ci += 1

    save_pickle(corrections, "corrections.pickle")


    print("updating interval_count")
    print(f"{len(corrections)} corrections")
    with db.open_connection() as con:
        cur = con.cursor()
        query = "UPDATE Interval_1hr SET interval_count = (%s) WHERE interval_count = (%s);"
        ccount = 1
        for wrong, right in reversed(corrections):
            print(ccount, wrong, right)
            cur.execute(query, (right, wrong))
            ccount += 1
        con.commit()
        cur.close()


    print("done")





def main2():

    # 2021-07-29 15:59:00
    recent_interval_date = datetime(2021, 7, 29, hour=16, tzinfo=pytz.utc)
    int_date = int(recent_interval_date.timestamp())

    with db.open_connection() as con:
        cur = con.cursor()

        cur.execute("UPDATE IntValue SET value = 427 WHERE int_value_id = 'interval_count';")

        query = "INSERT INTO IntValue (int_value_id, value) VALUES ('previous_interval_datetime', (%s));"
        cur.execute(query, (int_date,))

        con.commit()
        cur.close()



def main3():

    corrections = [
        (429, 428),
        (430, 429)
    ]

    with db.open_connection() as con:
        cur = con.cursor()
        query = "UPDATE Interval_1hr SET interval_count = (%s) WHERE interval_count = (%s);"
        ccount = 1
        for wrong, right in corrections:
            print(ccount, wrong, right)
            cur.execute(query, (right, wrong))
            ccount += 1
        con.commit()
        cur.close()





if __name__ == "__main__":
    # main()
    # main2()
    main3()
