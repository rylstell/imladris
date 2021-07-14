from imladris.utilities import segment_list


class Evaluator:

    def __init__(self, name):
        self.name = name

    def get_intervals_needed(self):
        return 24

    def evaluate(self, cryptos):
        return cryptos




class E3434(Evaluator):

    def __init__(self):
        super().__init__("e3434")
        self.fields = ["price", "volume", "twitter_followers"]
        self.chunk_sizes = [1, 4, 12]
        self.num_chunks = 12

    def get_intervals_needed(self):
        return self.chunk_sizes[-1] * self.num_chunks

    def __evaluate_field(self, nums, chunk_size, num_chunks):
        segments = segment_list(nums, chunk_size)
        first_seg = next(segments)
        cur_avg = sum(first_seg) / len(first_seg)
        tot = 0
        for i in range(num_chunks-1):
            seg = next(segments)
            prev_avg = sum(seg) / len(seg)
            change = (cur_avg - prev_avg) / prev_avg
            weight = 1 / (i + 1)
            tot += weight * change
            cur_avg = prev_avg
        score = tot / (num_chunks - 1)
        return score

    def evaluate(self, cryptos):
        for crypto in cryptos:
            field_tot = 0
            for field in self.fields:
                chunk_tot = 0
                for chunk_size in self.chunk_sizes:
                    nums = crypto["interval_data"][field]
                    chunk_tot += self.__evaluate_field(nums, chunk_size, self.num_chunks)
                field_tot += chunk_tot / len(chunk_sizes)
            crypto[self.name] = field_tot / len(fields)










# blank_space
