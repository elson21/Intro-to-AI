#!/usr/bin/env python

def main() -> None:

    file = "file3.txt"
    word_count = 0
    replace_deli = " "

    with open(file, "r") as file:
        f = file.read()
        f = f.replace(" ", replace_deli)\
             .replace("!", replace_deli)\
             .replace(",", replace_deli)\
             .replace(".", replace_deli)\
             .replace(";", replace_deli)\
             .replace("-", replace_deli)\
             .replace("\n", replace_deli)\
             .replace(" ", replace_deli)\
             .split()
        
        print(f)

        for word in f:
            word_count += 1

    print(f"The file has {word_count} words")

if __name__ == "__main__":
    main()
        