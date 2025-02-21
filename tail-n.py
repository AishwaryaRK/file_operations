import os
from typing import List


def tail_n(file_name: str, n: int) -> List[str]:
    with open(file_name, 'r') as fd:
        fd.seek(0, os.SEEK_END)
        file_size = position = fd.tell()
        num_lines = 0
        offset = 50  # 1024
        i = 1
        text = ""
        while num_lines <= n and position > 0:
            buffer_size = offset if file_size - offset * i >= 0 else file_size - offset * (i - 1)
            seek_offset = file_size - buffer_size * i if file_size - offset * i >= 0 else 0
            fd.seek(seek_offset, os.SEEK_SET)
            buffer = fd.read(buffer_size)
            # buffer = buffer.decode("utf-8") #for binary mode using -ve offset with SEEK_END
            num_lines += buffer.count("\n")
            text = buffer + text
            i += 1
            position = seek_offset + buffer_size
        # lines.reverse()
        lines = text.splitlines()
        return lines[-n:]


print(tail_n("test_file.txt", 5))
