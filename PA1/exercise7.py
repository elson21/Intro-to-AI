#!/usr/bin/env python

def file_rw(file1: str, file2: str, file3: str) -> None:
    """
    Reads 2 text files and writes each line of both files in
    an output text file
    """
    
    with open(file1, "r") as f1, open(file2, "r") as f2, open(file3, "w") as f3:
        for line1, line2 in zip(f1, f2):
            f3.write(line1.strip("\n") + " " + line2)


def main() -> None:
    file1 = "file1.txt"
    file2 = "file2.txt"
    file3 = "output.txt"

    file_rw(file1, file2, file3)


if __name__ == "__main__":
    main()