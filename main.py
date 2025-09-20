import json
import numpy as np
from scipy.optimize import linear_sum_assignment

# Load data
tasks = json.load(open("data/tasks.json"))
students = json.load(open("data/students.json"))

# Create cost matrix (lower = better match)
cost_matrix = []
for task in tasks:
    row = []
    for student in students:
        if task["skill"] in student["skills"]:
            cost = abs(student["hours"] - task["difficulty"])  # balance by availability
        else:
            cost = 100  # large penalty if skills don’t match
        row.append(cost)
    cost_matrix.append(row)

# Solve assignment problem
cost_matrix = np.array(cost_matrix)
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Print results
assignments = {}
for task_idx, student_idx in zip(row_ind, col_ind):
    student = students[student_idx]["name"]
    task = tasks[task_idx]["task"]
    assignments.setdefault(student, []).append(task)

print(assignments)
