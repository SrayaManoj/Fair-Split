import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

st.title("Fair Split")

# Step 1: Input students
students_input = st.text_area("Enter students (comma separated)", "")
students = [s.strip() for s in students_input.split(",") if s.strip()]

# Step 2: Input tasks
tasks_input = st.text_area("Enter tasks (comma separated)", "")
tasks = [t.strip() for t in tasks_input.split(",") if t.strip()]

# Step 3: Show editable skill matrix ONLY if students & tasks are provided
if students and tasks:
    st.subheader("Enter Skill Ratings (1–10)")

    # Initialize a blank DataFrame (all 0s initially)
    skill_df = pd.DataFrame(0, index=students, columns=tasks)

    # Editable grid for entering ratings
    skill_df = st.data_editor(skill_df, key="skills_editor")

    # Step 4: Assign tasks when button is clicked
    if st.button("Assign Tasks"):
        skills = skill_df.to_numpy()

        if np.all(skills == 0):
            st.warning("⚠️ Please enter skill ratings before assigning tasks.")
        else:
            max_skill = np.max(skills)
            cost_matrix = max_skill - skills
            row_ind, col_ind = linear_sum_assignment(cost_matrix)

            # Display results
            st.subheader("Optimal Task Assignment:")
            for i in range(len(row_ind)):
                st.write(f"{students[row_ind[i]]} → {tasks[col_ind[i]]}")
else:
    st.info("👆 Enter students and tasks to start building the skill matrix.")
