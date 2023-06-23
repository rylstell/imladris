from imladris import db
from imladris.utilities import save_pickle



def main():

    interval_counts = None
    with db.open_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT interval_count FROM Interval_1hr WHERE crypto_id = 29 ORDER BY interval_count DESC;")
        interval_counts = cur.fetchall()

    if not interval_counts: raise Exception("interval counts not retrieved from db")

    interval_counts = [count[0] for count in interval_counts]
    interval_counts.reverse()

    max_interval_count = interval_counts[-1]

    missed_intervals = []

    count = 0
    while count <= max_interval_count:
        if count != interval_counts[count-len(missed_intervals)]:
            missed_intervals.append(count)
        count += 1

    save_pickle(missed_intervals, "missed_intervals.pickle")




if __name__ == "__main__":
    main()
