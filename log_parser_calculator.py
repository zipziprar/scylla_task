import statistics
from collections import namedtuple

aggregated_summary = namedtuple('aggregated_summary', ('latency_mean_avg', 'latency_99th_percentile_avg',
                                                       'latency_max_stddev', 'op_rate_sum'))


class LogCalculator:
    def __init__(self):
        self.op_rate_sum = 0
        self.latency_mean_values = []
        self.latency_99th_percentile_values = []
        self.latency_max_values = []

    def process_lines(self, line):
        if line.startswith('Latency max'):
            name, rest = line.split(' : ', 1)
            value = rest.split(' ')[0]
            self.latency_max_values.append(float(value.replace(',', '')))
        if line.startswith('Latency 99th percentile'):
            name, rest = line.split(' : ', 1)
            value = float(rest.split(' ')[0])
            self.latency_99th_percentile_values.append(value)
        if line.startswith('Latency mean'):
            name, rest = line.split(' : ', 1)
            value = float(rest.split(' ')[0])
            self.latency_mean_values.append(value)
        if line.startswith('Op rate'):
            name, rest = line.split(' : ', 1)
            value = rest.split(' ')[0]
            self.op_rate_sum += float(value.replace(',', ''))

    def calc_latency_mean_avg(self):
        if self.latency_mean_values:
            return sum(self.latency_mean_values) / len(self.latency_mean_values)
        else:
            return 0

    def calc_latency_99th_percentile_avg(self):
        return sum(self.latency_99th_percentile_values) / len(self.latency_99th_percentile_values)

    def get_latency_max_stddev(self):
        return statistics.stdev(self.latency_max_values)

    def calculate_aggregations(self):
        latency_mean_avg = self.calc_latency_mean_avg()
        latency_99th_percentile_avg = self.calc_latency_99th_percentile_avg()
        latency_max_stddev = statistics.stdev(self.latency_max_values)
        return aggregated_summary(latency_mean_avg, latency_99th_percentile_avg, latency_max_stddev, self.op_rate_sum)
