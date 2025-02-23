import matplotlib.pyplot as plt


fig,ax = plt.subplots()
total_weeks_semester = 26
#Total weeks = 70% des Pie-Charts
remaining_weeks_semester = 5
remaining_converting_for_pie_chart = 70/26*remaining_weeks_semester
passed_weeks_semester = total_weeks_semester - remaining_weeks_semester
passed_converting_for_pie_chart = 70-remaining_converting_for_pie_chart
#total_weeks, remaining_weels müssen entsprechend geupdatet werden, das sie die richtigen Daten bekommen von JSON-File

size = 0.3
vals_o = [15,3,10,57,15]
vals_i = [15,remaining_converting_for_pie_chart,passed_converting_for_pie_chart,15]
# passed_weeks_semester + remaining_weeks_semester = 70%

outer_colors = ["none","yellow","red","#003B00","none"]
inner_colors = ["none","0.2", "#003B00","none"]

ax.pie(vals_o, radius=1, colors=outer_colors,wedgeprops=dict(width=0.05, edgecolor='none'),
       startangle=270,)
ax.pie(vals_i, radius=0.92, colors=inner_colors,wedgeprops=dict(width=size, edgecolor='none'),
       startangle=270)

fig.patch.set_alpha(0)
ax.set_facecolor("none")
ax.set(aspect="equal")

