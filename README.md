# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?

A: The constraint propagation technique is a method to reduce the search space of a problem. Sudoku constraint is that every unit (row, column, square) must contain every digit and just once; propagating this constraint we obtain that if in the unit A two cells, x and y, contain the same 2 values, m and n, therefore all the other cells of A could not contain m and n.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: The diagonal Sudoku introduces a constraint to the standard Sudoku: every diagonal should contain every number and just once. This constraint propagates in a way similar to the constraint of the other unit (row, column, square), therefore all the methods developed could be applied to this unit type in order to reduce the possible numbers of the diagonal cells (eg. if a diagonal cell contains only a number, this number must be removed from all the other diagonal cells of the unit).

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
