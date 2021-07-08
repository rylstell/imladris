

class Evaluator:

    def __init__(self, name):
        self.name = name

    def evaluate(cryptos):
        return cryptos






# class E3434(Evaluator):
#
#     def __init__(self):
#         super().__init__("e3434")
#
#     def evaluate(self, cryptos):
#
#         chunk_sizes = [1, 6, 12]
#
#         for crypto in cryptos.values():
#
#             stored_price = [0] * len(chunk_sizes)
#             stored_volume = [0] * len(chunk_sizes)
#             stored_follower = [0] * len(chunk_sizes)
#
#             score_price = [0] * len(chunk_sizes)
#             score_volume = [0] * len(chunk_sizes)
#             score_followers = [0] * len(chunk_sizes)
#
#             interval_size = len(crypto["interval_data"]["price"])
#             for i in range(1, interval_size):
#
#                 data = crypto["interval_data"]
#                 price = data["price"][i]
#                 volume = data["volume"][i]
#                 followers = data["twitter_followers"][i]
#
#                 iweight = (i + 1) / interval_size
#
#                 for j, chunk_size in enumerate(chunk_sizes):
#                     if i % chunk_size == 0:
#                         score_price[j] += (price - stored_price[j]) / stored_price[j] * iweight
#                         score_volume[j] += (price - stored_volume[j]) / stored_volume[j] * iweight
#
#
#
#
#
#             crypto[self.name] = 100
#         return cryptos





class E3434(Evaluator):

    def __init__(self):
        super().__init__("e3434")

    def evaluate(self, cryptos):

        chunk_sizes = [1, 6, 12]

        for crypto in cryptos.values():

            score_price = [0] * len(chunk_sizes)
            score_volume = [0] * len(chunk_sizes)
            score_followers = [0] * len(chunk_sizes)

            for chunk_i, chunk_size in enumerate(chunk_sizes):

                first_chunk = True

                total_volume = 0

                prev_volume = 0
                prev_price = 0
                prev_followers = 0

                num_intervals = len(crypto["interval_data"]["price"])
                for i in range(num_intervals):

                    data = crypto["interval_data"]
                    price = data["price"][i]
                    volume = data["volume"][i]
                    followers = data["twitter_followers"][i]

                    if (i+1) % chunk_size == 0:

                        volume_change = (total_volume - prev_volume) / prev_volume
                        price_change = (price - prev_price) / prev_price
                        followers_change = (followers - prev_followers) / prev_followers

                        prev_volume = total_volume
                        prev_price = price
                        prev_followers = followers

                        total_volume = 0



                    total_volume += volume



    # def evaluate(self, cryptos):
    #
    #     chunk_sizes = [1, 6, 12]
    #
    #     for crypto in cryptos.values():
    #
    #         stored_price = [0] * len(chunk_sizes)
    #         stored_volume = [0] * len(chunk_sizes)
    #         stored_follower = [0] * len(chunk_sizes)
    #
    #         score_price = [0] * len(chunk_sizes)
    #         score_volume = [0] * len(chunk_sizes)
    #         score_followers = [0] * len(chunk_sizes)
    #
    #         interval_size = len(crypto["interval_data"]["price"])
    #         for i in range(1, interval_size):
    #
    #             data = crypto["interval_data"]
    #             price = data["price"][i]
    #             volume = data["volume"][i]
    #             followers = data["twitter_followers"][i]
    #
    #             iweight = (i + 1) / interval_size
    #
    #             for j, chunk_size in enumerate(chunk_sizes):
    #                 if i % chunk_size == 0:
    #                     score_price[j] += (price - stored_price[j]) / stored_price[j] * iweight
    #                     score_volume[j] += (price - stored_volume[j]) / stored_volume[j] * iweight
    #
    #         crypto[self.name] = 100
    #     return cryptos


    def evaluate(self, cryptos):

        chunk_size = 4

        for crypto in cryptos.values():

            data = crypto["interval_data"]

            score_price = 0
            score_volume = 0
            score_followers = 0

            prev_price = data["price"][chunk_size-1]
            prev_volume = sum(data["volume"][:chunk_size])
            prev_followers = data["twitter_followers"][chunk_size-1]

            num_intervals = len(data["price"])
            num_chunks = num_intervals / chunk_size

            for i in range(chunk_size*2-1, num_intervals, chunk_size):

                price = data["price"][i]
                volume = data["volume"][i-chunk_size+1:i+1]
                followers = data["twitter_followers"][i]

                weight = (i + 1) / num_chunks

                score_price += weight * ((price - prev_price) / prev_price)
                score_volume += weight * ((volume - prev_volume) / prev_volume)
                score_followers += weight * ((followers - prev_followers) / prev_followers)

                prev_volume = volume
                prev_price = price
                prev_followers = followers











# blank_space
