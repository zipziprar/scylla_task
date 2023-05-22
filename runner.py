import argparse
import subprocess
import threading
from summary_agreagator import SummaryAggregator


class CommandRunner:
    def __init__(self, threads, duration, cassandra_threads=10):
        self.threads = threads
        self.duration = duration
        self.cassandra_threads = cassandra_threads
        self.summary_aggregator = SummaryAggregator()

    def _run_command(self, node_ip, thread_number, run_and_parse=True):
        command = f"docker exec some-scylla cassandra-stress write duration={self.duration}s -rate threads=" \
                  f"{self.cassandra_threads} -node {node_ip}"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        # store the thread result in file
        with open(f'{thread_number}_{node_ip}_output.txt', 'w') as file:
            # Iterate over the stdout
            for line in iter(process.stdout.readline, b''):
                file.write(line.decode('utf-8'))

        # actually this is not proper place for such logic but decided to simplify due to want to calculate summary
        # inplace
        process.wait()
        if run_and_parse:
            self.do_calculate_process_summary(f'{thread_number}_{node_ip}_output.txt')

    def do_calculate_process_summary(self, filename):
        self.summary_aggregator.file_reader.file_path = filename
        self.summary_aggregator.print_summary()

    def run_stress_test(self, node_ip, num_threads):
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=self._run_command, args=(node_ip, i + 1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


def main():
    parser = argparse.ArgumentParser(description="Run Cassandra Stress Test")
    parser.add_argument('--threads', type=int, required=True, help="Number of threads for the stress command")
    parser.add_argument('--duration', type=int, required=True, help="Duration for the stress command")
    parser.add_argument('--node_ip', type=str, required=True, help="Node IP to run stress command")
    args = parser.parse_args()

    runner = CommandRunner(args.threads, args.duration)

    runner.run_stress_test(args.node_ip, args.threads)
    print(runner.threads)


if __name__ == "__main__":
    main()
