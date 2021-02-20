"""
scoring.py

Created on 2021-01-24
Updated on 2021-02-20

Copyright © Ryan Kan

Description: Scoring functions.
"""

# IMPORTS
import math

from Quaestiones.settings import CUTOFF_SOLVER, EQUAL_SCORE_FOR_ALL_SOLVERS


# FUNCTIONS
def scoring_function_normal(nth_player_to_solve, question_points):
    """The normal scoring function."""
    return math.floor(
        question_points * math.log2(CUTOFF_SOLVER - nth_player_to_solve + 2) / math.log2(CUTOFF_SOLVER + 1))


def scoring_function_equal(nth_player_to_solve, question_points):
    """The scoring function for the case that everyone gets the same score."""
    _ = nth_player_to_solve  # Remove the value from memory
    return question_points


def scoring_function(solver_num, points):
    """
    The overarching scoring function.

    Args:
        solver_num (int):
            The number of the solver (e.g. 1st solver, 10th solver, 31st solver etc).

        points (int):
            How many points the question is worth.

    Returns:
        int:
            The score.
    """

    if EQUAL_SCORE_FOR_ALL_SOLVERS:
        return scoring_function_equal(solver_num, points)

    return scoring_function_normal(solver_num, points)


# DEBUG CODE
if __name__ == "__main__":
    print(scoring_function(1, 100))
    print(scoring_function(CUTOFF_SOLVER, 100))
    print(scoring_function(CUTOFF_SOLVER // 2, 100))
