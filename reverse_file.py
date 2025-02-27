import os


def reverse(file_name: str, output_file_name: str):
    with open(file_name, 'r') as fd, open(output_file_name, "a") as output_fd:
        fd.seek(0, os.SEEK_END)
        file_size = fd.tell()
        offset = 50  # 1024
        position = file_size
        partial_line = ""
        while position > 0:
            buffer_size = min(offset, position)
            position -= buffer_size
            fd.seek(position, os.SEEK_SET)
            buffer = fd.read(buffer_size) + partial_line
            lines = buffer.splitlines()
            lines = [line + "\n" for line in lines]
            partial_line = lines[0]
            lines = lines[1:]
            lines.reverse()
            output_fd.writelines(lines)
            output_fd.flush()
        if partial_line:
            output_fd.writelines(partial_line)


reverse("test_file.txt", "reversed_file.txt")
