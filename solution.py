import numpy as np
from collections import Counter

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Found the boxes where there are only 2 possibilities
        twins_boxes = [box for box in unit if len(values[box]) == 2]
        # extract the possible values
        twins_values = [values[box] for box in twins_boxes]
        # detect the naked twins.
        naked_twins_values = [naked_twins_value for naked_twins_value,v in Counter(twins_values).items() if v == 2]
        # remove values from the other boxes in the unit
        for box in unit:
            if values[box] not in naked_twins_values:
                for nt in naked_twins_values:
                    for v in nt:
                        assign_value(values, box, values[box].replace(v,''))
                        #values[box] = values[box].replace(v,'')
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Set diagonal_flag to True for solve diagonal sudoku
diagonal_flag = True

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Build the diagonal boxes labels
diagonal_units = [[(rows[k]+cols[k]) for k in range(9)],[(rows[k]+cols[8-k]) for k in range(9)]]
# Add the diagonal boxes labels to units if diagonal_flag is True
if (diagonal):
    unitlist = row_units + column_units + square_units + diagonal_units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    dict_grid = dict(zip(boxes, grid))
    for box in boxes:
        if dict_grid[box] == '.':
            dict_grid[box] = '123456789'
    return dict_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(values[box],''))
            #values[peer] = values[peer].replace(values[box],'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after take only choice.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice and naked_twins();

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary:
        - the solution if the sudoku is solved;
        - False if the possibilities of a box go to zero
        - a sudoku if after an iteration the sudoku board remain the same.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    First, reduce the puzzle using reduce_puzzle().
    Using depth-first search and propagation, create a search tree and solve the sudoku.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        values: Sudoku in dictionary form, False if solution does not exist.
    """

    values = reduce_puzzle(values)
    if values == False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes  = [box for box in values.keys() if len(values[box]) > 1]
    number = [len(values[box]) for box in values.keys() if len(values[box]) > 1]

    if len(unsolved_boxes) > 0:
        box = unsolved_boxes[np.argmin(number)]
        # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        for pos in values[box]:
            sudoku_copy = values.copy()
            sudoku_copy[box] = pos
            output = search(sudoku_copy)
            if output:
                return output
    else:
        return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
