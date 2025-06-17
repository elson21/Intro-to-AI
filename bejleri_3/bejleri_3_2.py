#! /usr/bin/env python

import timeit
import heapq

"""
8-tile puzzle solved with A* for 2 different heuristics, Manhattan Distance (MD)
and Out Of Place tiles (OOP).

The A* search algorithm is a weighted algorithm used for finding the optimal path
from point A to point 
The A* search uses a heuristic function (h(n)) to estimate the cost from the current
not to the final node and a cost function (g(n)) to calculate the actual cost of 
going from point A to point B.
A* combines these two functions into an evaluation function (f(n)) and calculates
the estimated total cost of a path.
*f(n) = g(n) + h(n)

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

def get_valid_moves(state: list) -> list:
    """
    Get the next valid move depending on the current state

    Args:
        state (list): Current state of the board

    Returns:
        list: A list with the valid moves
    """
    
    blank_tile = state.index(0) # returns the index of 0
    moves = []

    if blank_tile % 3 != 2:
        moves.append('L')
    if blank_tile % 3 != 0:
        moves.append('R')
    if blank_tile >= 3:
        moves.append('D')
    if blank_tile <= 5:
        moves.append('U')
    
    return moves
    


def move_tile(state: list, action: str) -> list | None:
    """
    Swap the blank tile (0) with a legal tile depending on the action

    Args:
        state (list): A list with the current state of the board
        action (str): A string with the action to apply

    Returns:
        list: A list with the new state of the board after the tiles have been moved
        None: if there are no valid moves
    """

    new_state = state.copy()    # create a copy of the current state so that you can alter it
    blank_tile = state.index(0)

    if action == 'L':
        tile = blank_tile + 1
    elif action == 'R':
        tile = blank_tile - 1
    elif action == 'D':
        tile = blank_tile - 3
    elif action == 'U':
        tile = blank_tile +3
    else: return None

    # swap the blank tile with the tile
    (new_state[tile], new_state[blank_tile]) = (new_state[blank_tile], new_state[tile])

    return new_state


def manhattan_distance(state: list, goal: list) -> int:
    """
    Implementation of the Manhattan distance to find the minimum
    number of times I have to slide a tile to reach the goal state

    Args:
        state (list): The current configuration of the board
        goal (list): The goal configuration of the board

    Returns:
        int: An integer that represents the distance
    """
    distance = 0

    for num in range(1, 9): #excludes 0
        index_state = state.index(num)  # extract the index of each tile in the tcurrent configuration
        goal_state = goal.index(num)    # extract the index of each tile in the goal configuration

        x1, y1 = divmod(index_state, 3) # find the cartesian location of each tile in the current configuration
        x2, y2 = divmod(goal_state, 3)  # find the cartesian location of each tile in the goal configuration

        distance += abs(x1 - x2) + abs(y1 - y2) # MD formula

    return distance


def out_of_place_tiles(state: list, goal: list) -> int:
    """
    Finds and returns the number of tiles that are not
    in their correct place (ecluding the blank tile)

    Args:
        state (list): A list with the current configuration of the board
        goal (list): A list with the final configuration of the board

    Returns:
        int: An int with the amount of out of place tiles
    """
    
    oop_tiles = sum(
        1 # 3. increment by 1
        for state_tile, goal_tile in zip(state, goal)   # 1. Iterate state and goal lists 
        if state_tile != goal_tile and state_tile != 0
        ) # 2. if the tiles are not the same and if the tile of the current board confg is not zero

    return oop_tiles


def moves_taken(origin: dict, current_state: tuple) -> list:
    """
    Function that returns the moves taken once the goal configuration is reached

    Args:
        origin (dict): a dictionary that holds the path
        current_state (tuple): the current configuration of the board

    Returns:
        list: A list with the moves taken
    """
    moves = []  # store the moves taken

    # start iterating until you reach the root
    while current_state in origin:
        previous_state, move = origin[current_state]   # extract the previous state and the moves
        moves.append(move)  # put the move in the list
        current_state = previous_state  # update the current state

    return list(reversed(moves)) # return the path in reverse


def a_star(initial_state: list, goal_state: list, heuristic) -> list | None:
    """
    Implementation of the A* search.
    *f(n) = g(n) + h(n)
    
    h(n) = amount of out of place tiles
    g(n) = amount of moves so far

    Args:
        initial_state (list): The initial configuration of the board
        goal_state (list): The goal configuration of the board

    Returns:
        list: A list with the moves applied to reach the 
    """
    start = tuple(initial_state)
    goal = tuple(goal_state)

    closed = set()  # visited states
    g_score = {start: 0}
    frontier = []   # states waiting to be explored
    origin = {} # dictionary to store the path

    h = heuristic(start, goal)
    g = 0   # starts with 0 moves
    f = g + h

    # start the heapmin
    heapq.heappush(frontier, (f, g, start)) # put (f, g, state) in the heapmin

    while frontier:
        f, g, current_state = heapq.heappop(frontier)

        if current_state == goal:
            return moves_taken(origin, current_state)
        
        closed.add(current_state)    

        for move in get_valid_moves(list(current_state)):
            new_state = tuple(move_tile(list(current_state), move))
            temp_g = g + 1
            
            if new_state in closed:
                continue

            if new_state not in g_score or temp_g < g_score[new_state]:
                g_score[new_state] = temp_g
                f = temp_g + heuristic(new_state, goal)
                heapq.heappush(frontier, (f, temp_g, new_state))

                origin[new_state] = (current_state, move)

        


def user_input(prompt: str) -> list:
    """
    Receives user input and cleans it up by removing delimiters and whitespaces

    Args:
        prompt (str): Prompt given to user

    Returns:
        list: A list of unique integers between 0 and 9
    """
    while True:
        try:
            raw = input(prompt)
            state = list(map(int, raw.replace(",", " ").split()))

            # make sure the ensure enters 6 integers exactly
            if len(state) != 9:
                raise ValueError("Enter 9 integers exactly.")
            # make sure there are no duplicates from 0-9
            if set(state) != set(range(9)):
                raise ValueError("Enter integers between 0 and 9, no duplicates allowed.")
            return state
        except ValueError as e:
            print(f"Invalid input: {e}")


def main() -> None:
    
    initial_state = user_input("Enter the 8-puzzle start state: (e.g. 4,1,0,2,5,3,6,8,7):")
    goal_state = user_input("Enter the 8-puzzle goal state (e.g. 1,2,3,4,5,,6,7,8,0):")

    while True:
        print("\nMenu:")
        print("[1] MD")
        print("[2] OOP")
        print("[3] New start state")
        print("[4] New goal state")
        print("[5] Exit")

        choice = input("\nChoose an option: ")

        # MD
        if choice == "1":
            starttime = timeit.default_timer()
            print("============================================")
            print("The start time is :",starttime)

            result = a_star(initial_state, goal_state, manhattan_distance)
            
            if result == None:
                print("No solution")
            else:
                print("Sequence of moves (MD):", end=" ")
                print(*result)
                print(f"No. of steps: {len(result)}\n")
            
            print("Time taken:", timeit.default_timer() - starttime)
            print("============================================")

        # OOP
        elif choice == "2":
            starttime = timeit.default_timer()
            print("============================================")
            # print("The start time is :",starttime)            
            result = a_star(initial_state, goal_state, out_of_place_tiles)

            if result is None:
                print("No solution.")
            else:
                print("Sequence of moves (OOP):", end=" ")
                print(*result)
                print(f"No. of steps: {len(result)}\n")

            print("Time taken:", timeit.default_timer() - starttime)   
            print("============================================")             

        # New initial state
        elif choice == "3":
            initial_state =  user_input("Enter the state of the board (e.g. 4,1,0,2,5,3,6,8,7):")

        # New goal state
        elif choice == "4":
            goal_state = user_input("Enter the goal state (e.g. 1,2,3,4,5,6,7,8,0):")

        # Exit
        elif choice == "5":
            print("Bye Bye")
            break

        else:
            print("Invalid choice. Please choose between 1-5")


if __name__ == "__main__":
    main()
        
