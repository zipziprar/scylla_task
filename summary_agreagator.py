from file_reader import LogReader
from log_parser_calculator import LogCalculator


class SummaryAggregator:
    def __init__(self, file_path=None, page_size=1024):
        self.file_reader = LogReader(file_path=file_path, page_size=page_size)
        self.calculator = LogCalculator()
        self.summary = None

    def do_calculate_summary(self):
        return self.calculator.calculate_aggregations()

    def get_summary(self):
        for line in self.file_reader.get_values():
            self.calculator.process_lines(line)
        return self.do_calculate_summary()

    def print_summary(self):
        self.summary = self.get_summary()
        print(f'Op rate: {self.summary.op_rate_sum}, Latency mean: {self.summary.latency_mean_avg}, Latency 99th percentile: '
              f'{self.summary.latency_99th_percentile_avg}, Latency max: {self.summary.latency_max_stddev}')
