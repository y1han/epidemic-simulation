import numpy as np
import matplotlib.pyplot as plt
from bed import Bed
from city import City
from hospital import Hospital
from people import People
from peoplepool import PeoplePool
from matplotlib import animation

line = ['l', 'line']

def graph(city, pool, hos, mode=line[0]):
	#0未感染, 1潜伏期, 2确诊, 3住院, 4病死, 5总体得病(仅包含确诊), 6总存活人数, 7传染源
	colors_people = ['white', 'yellow', 'red', 'black', 'black', 'purple', 'grey', 'blue'] 
	colors_bed = ['red', 'black'] #0有人，1无人

	fig = plt.figure(figsize=(20, 10))
	plt.style.use('dark_background')
	fig.patch.set_facecolor('black')
	grid = plt.GridSpec(3, 5, wspace=0.3, hspace=0.3)
	ax1 = plt.subplot(grid[0:3, 0:3])
	ax2 = plt.subplot(grid[0:3, 3])

	ax3 = plt.subplot(grid[0, 4])
	ax4 = plt.subplot(grid[1, 4])
	ax5 = plt.subplot(grid[2, 4])

	if mode in line:
		ax3_ydata = [0, 0]
		ax3_totdata = [0, 0]
		ax4_ydata = [0, 0]
		ax4_totdata = [0, 0]
		ax5_ydata = [0, 0]
		ax5_totdata = [0, 0]

	hosX = hos.getX()
	hosY = hos.getY()

	axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
	ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

	def animate(time):
		boundry = 5 * pool.SCALE
		status = pool.getStatus()
		status_hos = hos.getStatus()
		susceptible = np.sum(status == 0)
		incubated = np.sum(status == 1)
		exposed = np.sum(status == 2)
		hospitalized = np.sum(status_hos == False)
		illed = exposed + hospitalized # 仅包含确诊
		contagious = incubated + exposed # 能传染给他人的
		total = susceptible + incubated + illed

		if mode in line:
			ax3_ydata[1] = susceptible
			ax3_totdata[1] = total
			ax4_ydata[1] = incubated
			ax4_totdata[1] = contagious
			ax5_ydata[1] = exposed
			ax5_totdata[1] = illed

		fig.canvas.restore_region(axbackground)
		fig.canvas.restore_region(ax2background)

		ax1.clear()
		ax1.scatter(pool.getX(), pool.getY(), c = [colors_people[j] for j in status], marker = '.', \
					alpha = 0.6, s = 10)
		ax1.set_title(f'Time:{time:<10}Susceptible:{susceptible:<10}Incubated:{incubated:<10}Exposed:{exposed}')
		ax1.set_xticks([])
		ax1.set_yticks([])
		ax1.set_xlim(-boundry, boundry)
		ax1.set_ylim(-boundry, boundry)

		ax2.clear()
		ax2.scatter(hosX, hosY, c = [colors_bed[j] for j in status_hos], marker = '.', \
					alpha = 1, s = 10)
		ax2.set_title(f'Hospitalized:{hospitalized}/{hos.bed_counts}')
		ax2.set_xticks([])
		ax2.set_yticks([])

		if mode in line:
			if (time >= 1):
				ax3.plot([time-1, time], ax3_ydata, color = colors_people[0])
				ax3.plot([time-1, time], ax3_totdata, color = colors_people[6])
				ax4.plot([time-1, time], ax4_ydata, color = colors_people[1])
				ax4.plot([time-1, time], ax4_totdata, color = colors_people[7])
				ax5.plot([time-1, time], ax5_ydata, color = colors_people[2])
				ax5.plot([time-1, time], ax5_totdata, color = colors_people[5])
		else:
			ax3.bar(time, total, color = colors_people[6], width=1)
			ax3.bar(time, susceptible, color = colors_people[0], width=1)
			ax4.bar(time, contagious, color = colors_people[7], width=1)
			ax4.bar(time, incubated, color = colors_people[1], width=1)
			ax5.bar(time, illed, color = colors_people[5], width=1)
			ax5.bar(time, exposed, color = colors_people[2], width=1)

		ax3.set_title(f'total({colors_people[6]}):{total:<6}\nsusceptible({colors_people[0]}):{susceptible}')
		ax4.set_title(f'contagious({colors_people[7]}):{contagious:<6}\nincubated({colors_people[1]}):{incubated}')
		ax5.set_title(f'illed({colors_people[5]}):{illed:<6}\nexposed({colors_people[2]}):{exposed}')

		pool.update(time, hos)
		# plt.pause(0.00001)
		if mode in line:
			ax3_ydata[0] = susceptible
			ax3_totdata[0] = total
			ax4_ydata[0] = incubated
			ax4_totdata[0] = contagious
			ax5_ydata[0] = exposed
			ax5_totdata[0] = illed

		return 0

	# Writer = animation.writers['ffmpeg']
	# writer = Writer(fps=60, bitrate=256000)

	ani = animation.FuncAnimation(fig=fig, func=animate)
	# ani.save('infection.mp4', writer=writer)

	plt.show()
