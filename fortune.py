import collections
import logging
import os
import random


class Fortune:
    def __init__(self, fortune_filename):
        self.fortune_filename = fortune_filename
        self.fortune_index_filename = self.__index_fortune_file()
        logging.basicConfig(filename="fortune.log", level=logging.ERROR,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    def __index_fortune_file(self) -> str:
        fortune_index_filename = "fortune_index"
        try:
            with open(self.fortune_filename, "r") as fd:
                count = 0
                indices = collections.deque([0])

                while True:
                    line = fd.readline()
                    if line:
                        if line == "%\n":
                            offset = fd.tell()
                            indices.append(offset)
                            count += 1
                    else:
                        break
                # fd.seek(0,os.SEEK_END)
                offset = fd.tell()
                indices.append(offset)
                count += 1
            indices.appendleft(count)
            print(indices)
            print(count)
            with open(fortune_index_filename, "wb") as index_fd:
                for index in indices:
                    index_fd.write(index.to_bytes(4, byteorder="big"))

        except FileNotFoundError as e:
            logging.error("error: file not found %s", e)
        except ValueError as e:
            logging.error("error: invalid file content %s", e)
        except Exception as e:
            logging.error("error: %s", e)
        else:
            return fortune_index_filename

    def fortune(self) -> str:
        start_offset = end_offset = 0
        with open(self.fortune_index_filename, "rb") as index_fd:
            count_b = index_fd.read(4)
            count = int.from_bytes(count_b, byteorder="big")
            offset = random.randint(1, count)
            seek_offset = offset * 4
            index_fd.seek(seek_offset, os.SEEK_SET)
            start_offset_b = index_fd.read(4)
            end_offset_b = index_fd.read(4)
            start_offset = int.from_bytes(start_offset_b, byteorder="big")
            end_offset = int.from_bytes(end_offset_b, byteorder="big")
        with open(self.fortune_filename, "r") as fd:
            fd.seek(start_offset, os.SEEK_SET)
            fortune = fd.read(end_offset - start_offset - 4)
            return fortune



fortune = Fortune("fortune.txt")
print(fortune.fortune())
