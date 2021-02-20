"""
quaestiones.py

Created on 2021-01-25
Updated on 2021-02-20

Copyright © Ryan Kan

Description: Settings for Quaestiones modules.
"""

# Account Deletion
DAYS_INACTIVE_BEFORE_DELETE = 3

# Statistics Settings
ENABLE_SOLVE_STATISTICS = True  # Should the number of solves for each question be displayed?

# Leaderboard's Settings
ENABLE_LEADERBOARD = True
NUM_USERS_TO_SHOW = 50  # Number of users to show on the leaderboard

# Scoring Settings
EQUAL_SCORE_FOR_ALL_SOLVERS = False  # Should all users who solve the question get he same score?
CUTOFF_SOLVER = 10  # After this solver, all the rest of the solvers would get a 0 if the above variable is `False`.
