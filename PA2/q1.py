#!/usr/bin/env python

"""
This script is used to solve a variation of the Missionaries and Cannibals puzzle.
It finds a valid way to transport 3 Timid Thalassians and 3 Vile Voridians from their
imploding planet Xylophus to the safer planet Zenithia, without violating the safety
constratints of the Voridians never outnumbering the Thalassians on either side.
"""

from collections import deque


def is_valid(thal_left: int, vors_left: int) -> bool:
    """
    Checks whether a state is valid.

    Args:
        thal_left (int): Number of Thalassians on Xylophus
        vors_left (int): Number of Voridians on Xylophus

    Returns:
        bool: True if the state is valid, else False
    """

    thal_right = 3 - thal_left
    vors_right = 3 - vors_left

    # if (0 <= thal_left <= 3 and 0 <= vors_left <= 3):
    #     return True

    if not (0 <= thal_left <= 3 and 0 <= vors_left <= 3):
        return False
    if not (0 <= thal_right <= 3 and 0 <= vors_right <= 3):
        return False
    
    if thal_left > 0 and thal_left < vors_left:
        return False
    if thal_right > 0 and thal_right < vors_right:
        return False

    return True


def valid_moves(state: tuple) -> list:
    """
    Takes a starting state as argument and returns
    the next state of the people and location of the
    spaceship

    Args:
        state (tuple): Current state in the format (thal_left, vors_left, spaceship_location)

    returns:
        list: A list of a valid next state
    """

    # valid passengers
    valid_passengers = [
        (1, 0), # 1 Thalasian
        (0, 1), # 1 Voridian
        (2, 0), # 2 Thalasians
        (0, 2), # 2 Voridians
        (1, 1)  # 1 of each
    ]

    # original positions
    thal_left, vors_left, ss_loc = state

    next_states = []    # Store the possible states

    
    if ss_loc == 'L':
        for thal_in_ss, vors_in_ss in valid_passengers:
            # check that there are valid moves
            if thal_left >= thal_in_ss and vors_left >= vors_in_ss:

                # make new variables to keep the original state
                new_thal_left = thal_left - thal_in_ss
                new_vors_left = vors_left - vors_in_ss


                # validate the move
                if is_valid(new_thal_left, new_vors_left):
                    # move the spaceship
                    new_ss_loc = 'R'

                    # move people to the right
                    new_state = (new_thal_left, new_vors_left, new_ss_loc)

                    # add new state to the states
                    next_states.append(new_state)

    # if spaceship is on Zenithia
    if ss_loc == 'R':
        thal_right = 3 - thal_left
        vors_right = 3 - vors_left

        for thal_in_ss, vors_in_ss in valid_passengers:
            # check if there are valid moves
            if thal_right >= thal_in_ss\
            and vors_right >= vors_in_ss:
                
                # make new variables to keep the original state
                new_thal_left = thal_left + thal_in_ss
                new_vors_left = vors_left + vors_in_ss

                # validate the move
                if is_valid(new_thal_left, new_vors_left):
                    # move the spaceship
                    new_ss_loc = 'L'

                    # move people to the right
                    new_state = (new_thal_left, new_vors_left, new_ss_loc)

                    # add new state to the states
                    next_states.append(new_state)

    return next_states


def bfs(start_state: tuple, goal_state: tuple) -> list | None:
    """
    Breadth First Search algorithm
    Takes the start state and goal and finds the best way
    to transprot all 6 people to the new planet.

    Args:
        start_state (tuple): The starting state of the system
        goal_state (tuple): The target state

    Return:
        list: The shortest path from the starting state to the goal state
              as a list or None if no solution is found
    """

    visited = set()
    fringe = deque()
    fringe.append((start_state, [start_state])) # fringe(starting state, path so far)

    while fringe:
        # save the current state and the path so far
        current_state, path = fringe.popleft()

        # check if we're done
        if current_state == goal_state:
            return path
        
        # if we've done the same transport again, keep going
        if current_state in visited:
            continue

        visited.add(current_state)

        for next_state in valid_moves(current_state):
            if next_state not in visited:
                fringe.append((next_state, path+[next_state]))

    return None


def main() -> None:

    result = bfs((3, 3, 'L'), (0, 0, 'R'))

    if result == None:
        print("No solutions")
    else:    
        for step in result:
            print(step)


if __name__ == "__main__":
    main()
            