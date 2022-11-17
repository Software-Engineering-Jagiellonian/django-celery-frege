class DownloadDirectoryFullException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DownloadQueueTooBigException(Exception):
    def __init__(self, count: int):
        super().__init__(f"Download queue too big, reserved tasks = {count}")
