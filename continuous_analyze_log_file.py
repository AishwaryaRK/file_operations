import datetime
import time
from enum import Enum
import heapq


class LogType(Enum):
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"


class MedianFinder:
    def __init__(self):
        self.max_heap = []
        self.min_heap = []
        self.max_heap_len = 0
        self.min_heap_len = 0

    def addNum(self, num: int) -> None:
        if self.max_heap_len == 0:
            heapq.heappush(self.max_heap, -num)
            self.max_heap_len += 1
            return
        left_num = -self.max_heap[0]
        if num <= left_num:
            heapq.heappush(self.max_heap, -num)
            self.max_heap_len += 1
        else:
            heapq.heappush(self.min_heap, num)
            self.min_heap_len += 1
        if abs(self.max_heap_len - self.min_heap_len) > 1:
            if self.max_heap_len > self.min_heap_len:
                n = -heapq.heappop(self.max_heap)
                self.max_heap_len -= 1
                heapq.heappush(self.min_heap, n)
                self.min_heap_len += 1
            else:
                n = heapq.heappop(self.min_heap)
                self.min_heap_len -= 1
                heapq.heappush(self.max_heap, -n)
                self.max_heap_len += 1

    def findMedian(self) -> float:
        if not self.max_heap and not self.min_heap:
            return 0
        if (self.max_heap_len + self.min_heap_len) % 2 == 0:
            return (-self.max_heap[0] + self.min_heap[0]) / 2

        return -self.max_heap[0] if self.max_heap_len > self.min_heap_len else self.min_heap[0]


class LogMonitor:

    def __init__(self, median_finder: MedianFinder):
        self.median_finder = median_finder

    def __write_error_file(self, log, fd):
        fd.write(log)
        fd.flush()

    def __process_log(self, log: str, error_fd):
        print(log)
        log_parts = log.strip().split("]", 1)
        timestamp_str = log_parts[0].strip("[").strip()
        log_timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        log_parts = log_parts[1].strip().split(":", 1)
        log_type = log_parts[0].strip()
        log_msg = log_parts[1].strip()
        if log_type == LogType.ERROR.value:
            self.__write_error_file(log, error_fd)
        elif log_type == LogType.INFO.value:
            self.median_finder.addNum(int(log_msg)) # error handling for int
        print("median-----", self.median_finder.findMedian())

    def continuous_monitor_logs(self, file_name: str):
        with open(file_name, "r") as log_fd, open("error.log", "a") as error_fd:
            for log in log_fd:
                self.__process_log(log, error_fd)

            while True:
                log = log_fd.readline()
                if not log:
                    time.sleep(1)
                else:
                    self.__process_log(log, error_fd)


LogMonitor(MedianFinder()).continuous_monitor_logs("server.log")
