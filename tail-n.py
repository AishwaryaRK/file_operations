import logging
import os
from typing import List


# def tail_n(file_name: str, n: int) -> List[str]:
#     with open(file_name, 'r') as fd:
#         fd.seek(0, os.SEEK_END)
#         file_size = position = fd.tell()
#         num_lines = 0
#         offset = 50  # 1024
#         i = 1
#         text = ""
#         while num_lines <= n and position > 0:
#             buffer_size = offset if file_size - offset * i >= 0 else file_size - offset * (i - 1)
#             seek_offset = file_size - buffer_size * i if file_size - offset * i >= 0 else 0
#             fd.seek(seek_offset, os.SEEK_SET)
#             buffer = fd.read(buffer_size)
#             # buffer = buffer.decode("utf-8") #for binary mode using -ve offset with SEEK_END
#             num_lines += buffer.count("\n")
#             text = buffer + text
#             i += 1
#             position = seek_offset + buffer_size
#         # lines.reverse()
#         lines = text.splitlines()
#         return lines[-n:]


def tail_n_lines(file_name: str, n: int) -> List[str]:
    if n==0:
        return []
    try:
        with open(file_name, "r") as fd:
            fd.seek(0, os.SEEK_END)
            file_size = fd.tell()
            offset = 50
            position = file_size
            n_lines = []
            partial_line = ""
            while len(n_lines) <= n and position > 0:
                buffer_size = min(offset, position)
                position -= buffer_size
                fd.seek(position, os.SEEK_SET)
                buffer = fd.read(buffer_size)
                buffer = buffer + partial_line
                lines = buffer.splitlines()
                partial_line = lines[0]
                n_lines = lines[1:] + n_lines
            if partial_line:
                n_lines = [partial_line] + n_lines
        return n_lines[-n:]
    except FileNotFoundError as e:
        logging.error("Error: file not found %s", e)
    except Exception as e:
        logging.error("Error: %s", e)


print(tail_n_lines("test_file.txt", 90))
