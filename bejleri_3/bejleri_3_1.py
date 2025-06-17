#! /usr/bin/env python

from collections import deque
import timeit
import time
import sys

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

    visited = set() # holds the visisted nodes
    fringe = deque()    # holds the nodes to be explored
    fringe.append((initial_state, []))   # (initial configuration, path so far). Path so far starts empty
    visited.add(tuple(initial_state))

    while fringe:
        # save the current state and path
        current_state, path = fringe.popleft()

        # check if goal is reached
        if current_state == goal_state:
            return path
        
        # # if current state has been repeated, keep going
        # if tuple(current_state) in visited:
        #     continue

        # check the valid moves for each action and put them in a new_state
        for action in get_valid_move(current_state):
            new_state = move_tile(current_state, action)
            key = tuple(new_state)
            if tuple(new_state) not in visited:
                # visited.update(new_state)
                visited.add(key)
                fringe.append((new_state, path + [action]))

    return None

def progress_bar():
        for i in range(0, 101, 10):
            sys.stdout.write(f"\rShutting down... [{i}%]")
            sys.stdout.flush()
            time.sleep(0.3)
        print()

        messages = [
        "Exiting very gracefully...",
        "I'm trying...",
        "Let me ask Google...",
        "I know, I'll ask ChatGPT...",
        "Hmm... Let me get the hammer 🔨"
        "That worked! Bye!"
    ]
        
        for msg in messages:
            print(msg)
            time.sleep(2)


def dfs(initial_state: list, goal_state: list, depth_limit: int) -> list | None:
    """
    Implementation of the DFS helper for IDS. Takes the initial and goal configuration
    of the board and find the best way to reach it.

    Args:
        initial_state (list): The initial configuration of the board
        goal_state (list): The goal configuration of the board
        depth_limit (int): The depth limit as incremented by the IDS

    Returns:
        list: Returns the path if the goal state is found, else None
    """

    stack = deque() # holds the node to be explored (fringe in BFS, but I like the name stack more)
    visited = set() # holds the visited nodes

    stack.append((initial_state, [], 0))    # [(current state, path, current depth)]

    # loop until you find the goal state
    while stack:
        current_state, path, depth = stack.pop()  

        # check if goal is found
        if current_state == goal_state:
            return path
        
        if depth < depth_limit:
            visited.add(tuple(current_state))
            for action in get_valid_move(current_state):
                new_state = move_tile(current_state, action)
                if tuple(new_state) not in visited:
                    stack.append((new_state, path + [action], depth + 1))

    return None

    
def ids(initial_state: list, goal_state: list, max_depth = 20) -> list | None:
    """
    Implementation of the IDS. Takes the initial and goal configuratios
    of the board and starts check each level and increases the depth
    until the goal configuration is found. Then it returns the path.

    Args:
        initial_state (list): The inigial configration of the voard
        goal_state (list): The goal configuration of the board
        max_depth (int): The maximum depth limit that it can go to

    Returns:
        list: Return the path if goal is found, else None
    """

    depth_limit = 0 # start with the root (depth 0)

    # keep calling DFS until goal is met
    for depth_limit in range(max_depth + 1):
        result = dfs(initial_state, goal_state, depth_limit)
        if result is not None:
            return result
        
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

    initial_state = user_input("Enter the state of the board (e.g. 4,1,0,2,5,3):")
    goal_state = user_input("Enter the goal state (e.g. 1,2,3,4,5,0):")

    # # check if there is a solution
    # if not is_solution(initial_state):

    while True:
        print("\nMenu:")
        print("[1] BFS")
        print("[2] IDS")
        print("[3] New initial state")
        print("[4] New goal state")
        print("[5] Exit")

        choice = input("\nChoose an option: ")

        # BFS
        if choice == "1":
            starttime = timeit.default_timer()
            print("============================================")
            # print("The start time is :",starttime)

            result = bfs(initial_state, goal_state)
            
            if result == None:
                print("No solution")
            else:
                print("Sequence of moves (BFS):", end=" ")
                print(*result)
                print(f"No. of steps (BFS): {len(result)}\n")
            
            print("Time taken:", timeit.default_timer() - starttime)
            print("============================================")

        # IDS
        elif choice == "2":
            starttime = timeit.default_timer()
            print("============================================")
            # print("The start time is :",starttime)            
            result = ids(initial_state, goal_state)

            if result is None:
                print("No solution.")
            else:
                print("Sequence of moves (IDS):", end=" ")
                print(*result)
                print(f"No. of steps (IDS): {len(result)}\n")

            print("Time taken:", timeit.default_timer() - starttime)   
            print("============================================")             
        
        # New start state
        elif choice == "3":
            initial_state =  user_input("Enter the state of the board (e.g. 4,1,0,2,5,3):")
        
        # New goal state
        elif choice == "4":
            goal_state = user_input("Enter the goal state (e.g. 1,2,3,4,5,0):")

        # Exit
        elif choice == "5":
            progress_bar()
            break

        else:
            print("Invalid choice. Please choose between 1-5")


if __name__ == "__main__":
    main()

