#! /usr/bin/env python

from collections import deque

"""
5-tile puzzle with BFS and IDS

This code solves a puzzle of a 5-tile board and a blank.
At each step, one of the tiles can be moved into the blank space.
The problem starts at a given initial configuration and the objective is to find a sequence
of moves so that the tiles are in the goal configuration.

Both the initial state and goal configuration are provided by user input as
*initial configuration = initial_state
*goal configuration = goal_state

There are 4 possible actions:
*Up = U
*Down = D
*Left = L
*Right = R
"""


def get_valid_move(state: list) -> list:
    """
    Get the next valid move depending on the current state.

    Args:
        state (list): Current state of the board

    Returns:
        list: A list with the 
    """

    blank_tile = state.index(0)
    moves = []

    if blank_tile + 3 < 6:
        moves.append('U')
    if blank_tile - 3 >= 0:
        moves.append('D')
    if blank_tile % 3 != 2:
        moves.append('L')
    if blank_tile % 3 != 0:
        moves.append('R')

    return moves


def move_tile(state: list, action: str) -> list | None:
    """
    Swap the black tile (0) with a legal tile depending on the action

    Args:
        state (list): Current state of the board
        action (str): Action to apply

    Returns:
        list: New board state after the move or None if no valid moves found
    """

    blank_tile = state.index(0)
    new_state = state.copy()    # create a copy so as to keep the current state the same

    if action == 'U':
        tile = blank_tile + 3
    elif action == 'D':
        tile = blank_tile - 3
    elif action == 'L':
        tile = blank_tile + 1
    elif action == 'R':
        tile = blank_tile - 1
    else:
        return None 
    
    # swap the blank tile with a normal tile
    (new_state[tile], new_state[blank_tile]) = (new_state[blank_tile], new_state[tile])

    return new_state



def bfs(initial_state: list, goal_state: list) -> list | None:
    """
    Implementation of BFS. Takes the initial and the goal configuration
    of the board and finds the best way to reach the goal configuration.

    Args:
        initial_state (list): The initial configuration of the board
        goal_state (list): The goal configuration of the board

    Returns:
        list: The shortest path from the initial configuration to the
              goal configuration as a list or None if no solution is found
    """

    visited = set()
    fringe = deque()
    fringe.append((initial_state, []))   # (initial configuration, path so far). Path so far starts empty

    while fringe:
        # save the current state and path
        current_state, path = fringe.popleft()

        # check if goal is reached
        if current_state == goal_state:
            return path
        
        # if current state has been repeated, keep going
        if tuple(current_state) in visited:
            continue

        visited.add(tuple(current_state))

        # check the valid moves for each action and put them in a new_state
        for action in get_valid_move(current_state):
            new_state = move_tile(current_state, action)
            if tuple(new_state) not in visited:
                fringe.append((new_state, path + [action]))

    return None


def user_input(prompt: str) -> list:
    """
    Receives user input and cleans away all delimiters and whitespaces

    Args:
        prompt (str): Input from user, like "4, 1, 0, 2, 5, 3"

    Returns:
        list: A list of unique integers like between 0 and 5
    """

    while True:
        try:
            raw = input(prompt)
            state = list(map(int, raw.replace(",", " ").split()))

            # make sure the ensure enters 6 integers exactly
            if len(state) != 6:
                raise ValueError("Enter 6 integers exactly.")
            # make sure there are no duplicates from 0-5
            if set(state) != set(range(6)):
                raise ValueError("Enter integers between 0 and 5, no duplicates allowed.")
            return state
        except ValueError as e:
            print(f"Invalid input: {e}")


def main() -> None:

    #TODO: Implement a menu for [1]BFS, [2]IDS, [3]New start state, [4]New goal state, [5]exit


    initial_state = user_input("Enter the state of the board (e.g. 4,1,0,2,5,3):")
    goal_state = user_input("Enter the goal state (e.g. 1,2,3,4,5,0):")

    while True:
        print("\nMenu:")
        print("[1] BFS")
        print("[2] IDS")
        print("[3] New initial state")
        print("[4] New goal state")
        print("[5] Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            result = bfs(initial_state, goal_state)
            
            if result == None:
                print("No solution")
            else:
                print("\nSequence of moves (BFS):", end=" ")
                print(*result)
                print(f"No. of steps: {len(result)}\n")

        elif choice == "2":
            # TODO: implement IDS
            pass

        elif choice == "3":
            initial_state =  user_input("Enter the state of the board (e.g. 4,1,0,2,5,3):")

        elif choice == "4":
            goal_state = user_input("Enter the goal state (e.g. 1,2,3,4,5,0):")

        elif choice == "5":
            print("Exiting very gracefully...")
            break

        else:
            print("Invalid choice. Please choose between 1-5")


if __name__ == "__main__":
    main()

