"""
quaestiones.py

Created on 2021-01-25
Updated on 2021-01-25

Copyright © Ryan Kan

Description: Settings for Quaestiones modules.
"""

# Account Deletion
DAYS_INACTIVE_BEFORE_DELETE = 3

# Leaderboard's Scoring
EQUAL_SCORE_FOR_ALL_SOLVERS = False  # Should all users who solve the question gett he same score?
CUTOFF_SOLVER = 10  # After this solver, all the rest of the solvers would get a 0 if the above variable is `False`.
SCORE_FOR_FIRST_SOLVER = 100  # Ensure that this is at least the value of `math.floor(math.log2(CUTOFF_SOLVER + 1))`
