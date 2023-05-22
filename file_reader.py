

class LogReader:
    def __init__(self, file_path=None, page_size=1024):
        self.file_path = file_path
        self.page_size = page_size

    def _get_current_file(self):
        return self.file_path

    def get_values(self, filename=None, chunk_size=10):
        filename = filename if filename else self._get_current_file()
        with open(filename, 'r') as file:
            chunk = ''
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                chunk += data
                lines = chunk.split('\n')

                if not data.endswith('\n'):
                    chunk = lines.pop()
                else:
                    chunk = ''

                for line in lines:
                    yield line
