import mysql.connector
from contextlib import contextmanager
from datetime import datetime




class ImladrisDatabase:

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.tables_metadata = {}
        self.__update_tables_metadata()


    def __update_tables_metadata(self):
        self.tables_metadata.clear()
        with self.open_connection() as con:
            cur = con.cursor(dictionary=True)
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            for table in tables:
                table_name = table[f"Tables_in_{self.db_name}"]
                cur.execute(f"DESCRIBE {table_name};")
                self.tables_metadata[table_name] = cur.fetchall()
            cur.close()


    @contextmanager
    def open_connection(self):
        try:
            con = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.db_name)
            yield con
        finally:
            con.close()


    def get_int_value(self, name):
        with self.open_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT value FROM IntValue WHERE int_value_id = (%s);", (name,))
            value = cur.fetchone()[0]
            cur.close()
            return value


    def get_cryptos(self, crypto_ids=[], cmc_ids=[], nomics_ids=[], fields=[], dictionary=False):
        where_clause = ""
        if crypto_ids or cmc_ids or nomics_ids:
            where_clause = f'''
WHERE
    crypto_id IN ({",".join([str(id) for id in crypto_ids]) if crypto_ids else "-1"})
OR
    cmc_id IN ({",".join([str(id) for id in cmc_ids]) if cmc_ids else "-1"})
OR
    nomics_id IN ({",".join(nomics_ids) if nomics_ids else "-1"})'''
        str_fields = ",".join(fields) if fields else "*"
        with self.open_connection() as con:
            cur = con.cursor(dictionary=dictionary)
            cur.execute(f"SELECT {str_fields} from Crypto {where_clause};")
            cryptos = cur.fetchall()
            cur.close()
            if len(fields) == 1 and not dictionary:
                return [c[0] for c in cryptos]
            return cryptos


    def get_mapping(self, from_id, to_fields=[]):
        if to_fields: fields = [from_id] + to_fields
        else: fields = [field["Field"] for field in self.tables_metadata["Crypto"]]
        cryptos = self.get_cryptos(fields=fields, dictionary=True)
        mapping = {}
        for crypto in cryptos:
            mapping[crypto[from_id]] = crypto
        if None in mapping: del mapping[None]
        return mapping


    def get_intervals(self, start_interval_count, end_interval_count):
        query = '''
SELECT * FROM Interval_1hr
WHERE interval_count >= (%s) AND interval_count <= (%s) AND (crypto_id = 29 OR crypto_id = 2467 OR crypto_id = 4124)
ORDER BY interval_count DESC;'''
        with self.open_connection() as con:
            cur = con.cursor(dictionary=True)
            cur.execute(query, (start_interval_count, end_interval_count))
            intervals = cur.fetchall()
            cur.close()
            return intervals


    def add_cmc_cryptos(self, cmc_meta):
        datetime_now = datetime.now()
        query = '''
INSERT INTO Crypto (
    crypto_id,
    cmc_id,
    nomics_id,
    name,
    symbol,
    category,
    description,
    slug,
    logo,
    subreddit,
    website,
    platform_id,
    twitter_username,
    twitter_following,
    source,
    date_added
) VALUES (DEFAULT, (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s));'''
        with self.open_connection() as con:
            cur = con.cursor()
            for crypto in cmc_meta:
                cur.execute(query, (
                    crypto["id"],
                    crypto["nomics_id"] if "nomics_id" in crypto else None,
                    crypto["name"],
                    crypto["symbol"],
                    crypto["category"],
                    crypto["description"],
                    crypto["slug"],
                    crypto["logo"],
                    crypto["subreddit"],
                    crypto["urls"]["website"][0] if crypto["urls"]["website"] else None,
                    crypto["platform"]["id"] if crypto["platform"] else None,
                    crypto["twitter_username"] if crypto["twitter_username"] else None,
                    crypto["twitter_following"],
                    "cmc",
                    datetime_now
                ))
            con.commit()
            cur.close()


    def add_intervals(self, intervals):
        query = '''
INSERT INTO Interval_1hr (interval_id, crypto_id, price, volume, circulating_supply, twitter_followers, interval_count, timestamp)
VALUES (DEFAULT, (%s), (%s), (%s), (%s), (%s), (%s), (%s));'''
        with self.open_connection() as con:
            cur = con.cursor()
            for interval in intervals:
                cur.execute(query, (
                    interval["crypto_id"],
                    interval["price"],
                    interval["volume"],
                    interval["circulating_supply"],
                    interval["twitter_followers"],
                    interval["interval_count"],
                    interval["timestamp"]
                ))
            con.commit()
            cur.close()


    def update_int_value(self, name, value):
        with self.open_connection() as con:
            cur = con.cursor()
            cur.execute("UPDATE IntValue SET value = (%s) WHERE int_value_id = (%s);", (value, name))
            con.commit()
            cur.close()


    def update_cmc_cryptos(self, cmc_meta):
        query = '''
UPDATE
	Crypto
SET
	name = (%s),
	symbol = (%s),
	category = (%s),
	description = (%s),
	slug = (%s),
	logo = (%s),
	subreddit = (%s),
	website = (%s),
	platform_id = (%s),
	twitter_username = (%s)
WHERE
	cmc_id = (%s);'''
        with self.open_connection() as con:
            cur = con.cursor()
            for crypto in cmc_meta:
                cur.execute(query, (
                    crypto["name"],
                    crypto["symbol"],
                    crypto["category"],
                    crypto["description"],
                    crypto["slug"],
                    crypto["logo"],
                    crypto["subreddit"],
                    crypto["urls"]["website"][0] if crypto["urls"]["website"] else None,
                    crypto["platform"]["id"] if crypto["platform"] else None,
                    crypto["twitter_username"],
                    crypto["id"]
                ))
            con.commit()
            cur.close()


    def update_interval_scores(self, interval_scores):
        set_fields = ", ".join([f"{name} = (%s)" for name in interval_scores[0][1]])
        query = "UPDATE Interval_1hr SET " + set_fields + " WHERE interval_id = (%s);"
        with self.open_connection() as con:
            cur = con.cursor()
            for interval_id, evaluator_scores in interval_scores:
                scores = evaluator_scores.values()
                scores = tuple(scores)
                values = scores + (interval_id,)
                cur.execute(query, values)
            con.commit()
            cur.close()
