import matplotlib.pyplot as plt

labels = "Done", "In Progress", "Open"
#Hier müssen dann variablen hin bei der Klasse
sizes = [10, 20, 70]
fig, ax = plt.subplots()
#Hintergrund transparent
fig.patch.set_alpha(0)
ax.set_facecolor("none")

ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#008F11", "#92e5a1", "#A5FFFF"], pctdistance=0.4, labeldistance=0.6,
       explode=(0.1, 0,0), shadow=True, startangle=90, radius=1.2, textprops={'fontsize': 8})

plt.show()