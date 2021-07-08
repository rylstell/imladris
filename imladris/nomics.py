import requests
import logging


class NomicsApi:

    def __init__(self, api_key):
        self.base_url = "https://api.nomics.com/v1"
        self.api_key = api_key

    def get_request(self, url, **kwargs):
        try:
            kwargs["key"] = self.api_key
            res = requests.get(url, params=kwargs)
            if res.status_code == 200:
                return res.json()
        except:
            logging.warning(f"unable to make nomics request\nurl={url}\nkwargs={kwargs}\n")
        return None

    def metadata(self, **kwargs):
        url = self.base_url + "/currencies"
        return self.get_request(url, **kwargs)

    def tickers(self, status="active", **kwargs):
        kwargs["status"] = status
        url = self.base_url + "/currencies/ticker"
        return self.get_request(url, **kwargs)

    def interval(self, **kwargs):
        url = self.base_url + "currencies/interval"
        return self.get_request(url, **kwargs)
