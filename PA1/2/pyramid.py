#!/usr/bin/env python

def pyramid(num: int) -> None:
    """
    Calculates and prints the integers between 1 and N (inclusive)
    with one integer on line 1, 2 on line 2 and so on.

    *Example:
    N=15
    *Output
    1
    2 3
    4 5 6
    7 8 9 10
    11 12 13 14 15
    """
    
    row_length = 1
    current_num = 1

    while current_num <= num:
        
        for i in range(row_length):
            if current_num <= num:
                print(current_num, end=' ')
                current_num += 1
        print()
        row_length += 1

def main() -> None:
    """Main function"""

    N = int(input("Enter a positive integer: "))

    if N < 0: print("Enter a positive integer.")

    pyramid(N)


if __name__ == "__main__":
    main()