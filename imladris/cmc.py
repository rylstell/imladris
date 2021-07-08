import requests
import logging




class CMCApi:

    def __init__(self, api_key):
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.api_key = api_key
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key
        }

    def get_request(self, url, **kwargs):
        try:
            res = requests.get(url, headers=self.headers, params=kwargs)
            if res.status_code == 200:
                return res.json()["data"]
        except:
            logging.warning(f"unable to make cmc request\nurl={url}\nkwargs={kwargs}\n")
        return None

    def mapping(self, **kwargs):
        url = self.base_url + "/cryptocurrency/map"
        return self.get_request(url, **kwargs)

    def metadata(self, ids, **kwargs):
        url = self.base_url + "/cryptocurrency/info"
        cryptos = []
        request_size = 500
        start = 0
        while start < len(ids):
            ids_slice = ids[start:start+request_size]
            kwargs["id"] = ",".join([str(id) for id in ids_slice])
            data = self.get_request(url, **kwargs)
            if data:
                cryptos += data.values()
            start += request_size
        return cryptos
