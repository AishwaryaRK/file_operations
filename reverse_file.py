import os


def reverse(file_name: str, output_file_name: str):
    with open(file_name, 'r') as fd, open(output_file_name, "a") as output_fd:
        fd.seek(0, os.SEEK_END)
        file_size = fd.tell()
        offset = 50  # 1024
        to_read = 0
        file_read = False
        i = 1
        while not file_read:
            buffer_size = offset if file_size - offset * i >= 0 else file_size - offset * (i - 1)
            seek_offset = file_size - buffer_size * i if file_size - offset * i >= 0 else 0
            if to_read:
                buffer_size += to_read
                to_read = 0
            if seek_offset == 0:
                file_read = True
            fd.seek(seek_offset, os.SEEK_SET)
            buffer = fd.read(buffer_size)
            lines = buffer.splitlines()
            lines = [line + "\n" for line in lines]
            first_line = lines[0]
            if not file_read:
                lines = lines[1:]
                to_read = len(first_line.encode("utf-8"))
            lines.reverse()
            output_fd.writelines(lines)
            output_fd.flush()
            i += 1


reverse("test_file.txt", "reversed_file.txt")
