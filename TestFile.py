from DashboardClasses import uni_data, student_data, semester_data, course_of_study_data
from DataManagingClasses import exam_data

uni_data.add_student(student_data)
#print(uni_data.students)
#print(type(semester_data.get_passed_weeks()))
#print(course_of_study_data.num_semesters)
#print(course_of_study_data.all_grades)
#print(course_of_study_data.current_avg_grade)

print(exam_data.load())