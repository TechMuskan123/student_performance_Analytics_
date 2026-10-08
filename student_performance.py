import numpy as np
import pandas as pd

DATA_FILE = "students.csv"
MARK_COLUMNS = ["Python", "Database", "Mathematics", "Communication", "AI"]


def assign_grade(average):
    """Return a grade based on the student's average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def calculate_student_result(row):
    """Calculate total, average, grade and result for one student."""
    marks = row[MARK_COLUMNS].to_numpy(dtype=float)

    # NumPy is used for numerical calculations.
    total = np.sum(marks)
    average = np.mean(marks)

    # A student must score at least 40 in every subject
    # and maintain at least 75% attendance.
    passed = np.all(marks >= 40) and row["Attendance"] >= 75

    return total, average, assign_grade(average), "Pass" if passed else "Fail"


def add_result_columns(data):
    """Add calculated result columns using a reusable function and loop."""
    totals = []
    averages = []
    grades = []
    results = []

    for _, student in data.iterrows():
        total, average, grade, result = calculate_student_result(student)
        totals.append(total)
        averages.append(round(average, 2))
        grades.append(grade)
        results.append(result)

    data = data.copy()
    data["Total_Marks"] = totals
    data["Average_Marks"] = averages
    data["Grade"] = grades
    data["Result"] = results
    return data


def show_summary(data):
    """Display the main performance summary."""
    print("\n========== STUDENT PERFORMANCE SUMMARY ==========")
    print(f"Students analysed : {len(data)}")
    print(f"Class average     : {data['Average_Marks'].mean():.2f}")
    print(f"Highest average   : {data['Average_Marks'].max():.2f}")
    print(f"Lowest average    : {data['Average_Marks'].min():.2f}")
    print(f"Passed students   : {(data['Result'] == 'Pass').sum()}")
    print(f"Failed students   : {(data['Result'] == 'Fail').sum()}")


def show_top_performers(data, count=5):
    """Show the top performers according to average marks."""
    top = data.nlargest(count, "Average_Marks")
    print("\n========== TOP PERFORMERS ==========")
    print(top[["Student_ID", "Name", "Department",
               "Average_Marks", "Grade"]].to_string(index=False))


def show_subject_analysis(data):
    """Display subject-wise averages and the best-performing subject."""
    subject_averages = data[MARK_COLUMNS].mean().sort_values(ascending=False)

    print("\n========== SUBJECT-WISE AVERAGE ==========")
    for subject, average in subject_averages.items():
        print(f"{subject:15} : {average:.2f}")

    print(f"\nBest average subject: {subject_averages.index[0]}")


def show_department_analysis(data):
    """Compare average performance across departments."""
    department_avg = data.groupby("Department")["Average_Marks"].mean()
    print("\n========== DEPARTMENT ANALYSIS ==========")
    for department, average in department_avg.sort_values(ascending=False).items():
        print(f"{department:8} : {average:.2f}")


def main():
    try:
        data = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} was not found.")
        print("Keep students.csv in the same folder as this Python file.")
        return

    print("Student Performance Analytics System")
    print("------------------------------------")

    result_data = add_result_columns(data)

    print("\nFirst five analysed records:")
    print(
        result_data[
            ["Student_ID", "Name", "Department",
             "Total_Marks", "Average_Marks", "Grade", "Result"]
        ].head().to_string(index=False)
    )

    show_summary(result_data)
    show_top_performers(result_data)
    show_subject_analysis(result_data)
    show_department_analysis(result_data)


if __name__ == "__main__":
    main()
