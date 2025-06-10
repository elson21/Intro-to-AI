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


def main() -> None:

    #TODO: Implement a menu for [1]BFS, [2]IDS, [3]New start state, [4]New goal state, [5]exit
    #TODO: Put this in a function called cleaner or something
    user_input_initial = input("Enter the state of the board (e.g. 4,1,0,2,5,3):")
    user_input_goal = input("Enter the goal state (e.g. 1,2,3,4,5,0):")

    cleaned_input_initial = user_input_initial.replace(",", " ").replace(".", " ")
    cleaned_input_goal = user_input_goal.replace(",", " ").replace(".", " ")

    initial_state = list(map(int, cleaned_input_initial.strip().split()))
    goal_state = list(map(int, cleaned_input_goal.strip().split()))
    result = bfs(initial_state, goal_state)

    count = 0

    if result == None:
        print("No solution")
    else:
        print("Sequence of moves (BFS):")
        for action in result:
            count += 1
            print(action, end=" ")

    print(f"\nNo. of steps: {count}\n")


if __name__ == "__main__":
    main()

