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
        self.max_missing_allowed = 10
        self.allowed_consecutive_misses = 3


    def get_intervals_needed(self):
        return self.chunk_sizes[-1] * self.num_chunks + self.max_missing_allowed


    def __validate_intervals(interval_counts, current_interval_count, total_intervals):
        if total_intervals - len(interval_counts) > self.max_missing_allowed:
            return False
        if sum(interval_counts[:5]) != sum(range(current_interval_count, current_interval_count-5, -1)):
            return False
        for i in range(len(interval_counts)-1):
            if interval_counts[i] - interval_counts[i+1] - 1 > self.allowed_consecutive_misses:
                return False
        return True


    def __evaluate_field(self, nums, chunk_size, num_chunks):
        chunks = segment_list(nums, chunk_size)
        first_chunk = next(chunks)
        cur_avg = sum(first_chunk) / len(first_chunk)
        tot = 0
        for i in range(num_chunks-1):
            chunk = next(chunks)
            prev_avg = sum(chunk) / len(chunk)
            change = (cur_avg - prev_avg) / prev_avg
            weight = 1 / (i + 1)
            tot += weight * change
            cur_avg = prev_avg
        score = tot / (num_chunks - 1)
        return score


    def evaluate(self, cryptos):
        current_interval_count = cryptos["end_interval_count"]
        total_intervals = self.get_intervals_needed()
        for crypto in cryptos["cryptos"]:
            valid_intervals = self.__validate_intervals(crypto["interval_data"]["interval_count"], current_interval_count, total_intervals)
            field_tot = 0
            for field in self.fields:
                chunk_tot = 0
                for chunk_size in self.chunk_sizes:
                    nums = crypto["interval_data"][field][:total_intervals]
                    chunk_tot += self.__evaluate_field(nums, chunk_size, self.num_chunks)
                field_tot += chunk_tot / len(chunk_sizes)
            crypto[self.name] = field_tot / len(fields)























# blank_space
