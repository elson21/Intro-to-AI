#!/usr/bin/env python

def file_rw(file1: str, file2: str, file3: str) -> None:
    
    file1_list = []
    file2_list = []
    
    with open(file1, "r") as file1, open(file2, "r") as file2:
        for line in file1:
            file1_list.append(line)

        for line in file2:
            file2_list.append(line)

    file1.close()
    file2.close()

    file3_list = list(zip(file1_list, file2_list))

    with open(file3, "w") as file3:
        for line in file3_list:
            lines = "".join(line)
            file3.write(lines)


def main() -> None:
    file1 = "file1.txt"
    file2 = "file2.txt"
    file3 = "output.txt"

    file_rw(file1, file2, file3)


if __name__ == "__main__":
    main()

