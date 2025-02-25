from DataManagingClasses import JSONFile
from DashboardClasses import University, Student
import json

iu = University("IU", "Flachsstarstraße 9", "Buchshausen", 72459)
print(iu.info())
bastian = Student("Bastian", 45934512)
iu.add_student(bastian)



testfile = JSONFile("test.json", "list")
testfile.new_file()
testfile.save(iu.students)
print(testfile.load())

