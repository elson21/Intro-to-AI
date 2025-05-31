#!/usr/bin/env python

def is_palindrome(num: int) -> bool:
    """Returns True if num is a palindrome, else False"""

    # check if num is positive
    if num < 0 or (num % 10 == 0 and num != 0):
        return False

    reversed_number = 0
    original_num = num

    while num > reversed_number:
        last_digit = num % 10   # grabs the last digit
        reversed_number = reversed_number * 10 + last_digit # reverses the number
        num = num // 10 # returns int

    return reversed_number == original_num  or original_num == reversed_number // 10


def main() -> None:
    """Main function"""

    num = int(input("Enter a positive integer: "))

    if is_palindrome(num):
        print(f"{num} is a palindrome.")
    else:
        print(f"{num} is a not palindrome.")

if __name__ == '__main__':
    main()


