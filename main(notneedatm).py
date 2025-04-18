from DataManagingClasses import user_data, menu_data

data = user_data.load()
course_of_study_name = data.get("Course of Study")
course_of_study_data = menu_data.load().get(course_of_study_name)
exam_type_list = course_of_study_data.get("exam_type")
