import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from bed import Bed
from city import City
from hospital import Hospital
from people import People
from peoplepool import PeoplePool
from threading import Thread, Condition
# import time as tm

line = ['l', 'line']

def graph(city, pool, hos, mode=line[0]):
	#0未感染, 1潜伏期, 2确诊, 3住院(在地图上无), 4免疫期, 5病死, 6总体得病(仅包含确诊), 7总存活人数, 8传染源, 
	colors_people = ['white', 'yellow', 'red', 'black', 'green', 'black', 'purple', 'grey', 'blue'] 
	colors_bed = ['red', 'black'] #0有人，1无人
	colors_statics = ['white'] #1 R0
	PERSON_COUNT = pool.num
	BED_COUNT = hos.bed_counts

	fig = plt.figure(figsize=(20, 10))
	plt.style.use('dark_background')
	fig.patch.set_facecolor('black')
	grid = plt.GridSpec(3, 5, wspace=0.5, hspace=0.3)
	ax1 = plt.subplot(grid[0:3, 0:3])
	ax2 = plt.subplot(grid[0:2, 3])

	ax3 = plt.subplot(grid[0, 4])
	ax4 = plt.subplot(grid[1, 4])
	ax5 = plt.subplot(grid[2, 4])
	ax6 = plt.subplot(grid[2, 3])

	if mode in line:
		ax3_susceptible_data = [0, 0]
		ax3_total_data = [0, 0]
		ax3_recover_data = [0, 0]
		ax4_exposed_data = [0, 0]
		ax4_contagious_data = [0, 0]
		ax5_infective_data = [0, 0]
		ax5_diagnosed_data = [0, 0]
		ax6_r0_data = [0, 0]

	hosX = hos.getX()
	hosY = hos.getY()

	ax1background = fig.canvas.copy_from_bbox(ax1.bbox)
	ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
	ax3background = fig.canvas.copy_from_bbox(ax3.bbox)
	ax4background = fig.canvas.copy_from_bbox(ax4.bbox)
	ax5background = fig.canvas.copy_from_bbox(ax5.bbox)
	ax6background = fig.canvas.copy_from_bbox(ax6.bbox)

	def init():
		pass

	def multi_process(time):
		cond = Condition()
		# start = tm.time()
		animate_thread = Thread(target=animate, args=(time, cond), name='animate')
		update_thread = Thread(target=pool.update, args=(time, hos, cond), name='update')
		update_thread.start()
		animate_thread.start()
		update_thread.join()
		# end = tm.time()
		# print(f'Time={time:<6}运行用时{(end-start):.2f}秒')
		return 0

	def animate(time, cond):
		cond.acquire()
		cond.notify()
		boundry = 5 * pool.SCALE
		status = pool.getStatus()
		status_hos = hos.getStatus()
		susceptible = np.sum(status == 0)
		exposed = np.sum(status == 1)
		infective = np.sum(status == 2)
		recovered = np.sum(status == 4)
		hospitalized = np.sum(status_hos == False)
		diagnosed = infective + hospitalized # 仅包含确诊
		contagious = exposed + infective # 能传染给他人的
		total = susceptible + exposed + diagnosed + recovered # SEIR
		
		if time > 0 and sum(pool.Ti) != 0:
			Ti = sum(pool.Ti)/len(pool.Ti)
			Tg = sum(pool.Tg)/len(pool.Tg)
			Te = sum(pool.Te)/len(pool.Te)
			if pool.can_exposed_infect:
				k = pool.in_touch / contagious if contagious != 0 else 0
				R0 = k * pool.BROAD_RATE * (Ti + Te) 
				# R0 = k*b*D (Lipsitch M，Cohen T, Cooper B, et al. TransmissionDynamics and Control of Severe Acute Respiratory Syndrome. Science, 2003,300(5627): 1966-1970.)
			else:
				k = pool.in_touch / infective if infective != 0 else 0
				R0 = k * pool.BROAD_RATE * Ti
		else:
			R0 = np.nan
			Ti = np.nan
			Tg = np.nan
			Te = np.nan

		if mode in line:
			ax3_susceptible_data[1] = susceptible
			ax3_total_data[1] = total
			ax3_recover_data[1] = recovered
			ax4_exposed_data[1] = exposed
			ax4_contagious_data[1] = contagious
			ax5_infective_data[1] = infective
			ax5_diagnosed_data[1] = diagnosed
			ax6_r0_data[1] = R0

		fig.canvas.restore_region(ax1background)
		fig.canvas.restore_region(ax2background)
		fig.canvas.restore_region(ax3background)
		fig.canvas.restore_region(ax4background)
		fig.canvas.restore_region(ax5background)
		fig.canvas.restore_region(ax6background)

		ax1.clear()
		ax1.scatter(pool.getX(), pool.getY(), c = [colors_people[j] for j in status], marker = '.', \
					alpha = 0.6, s = 10)
		ax1.set_title(f'Te:{Te:<10.2f}Ti:{Ti:<10.2f}Tg:{Tg:<10.2f}R0:{R0:.2f}\nTime:{time:<10}Susceptible:{susceptible:<10}Exposed:{exposed:<10}Infective:{infective:<10}Recovered:{recovered}')
		ax1.set_xticks([])
		ax1.set_yticks([])
		ax1.set_xlim(-boundry, boundry)
		ax1.set_ylim(-boundry, boundry)

		ax2.clear()
		ax2.scatter(hosX, hosY, c = [colors_bed[j] for j in status_hos], marker = '.', \
					alpha = 1, s = 10)
		ax2.set_title(f'death:{PERSON_COUNT-total}\nhospitalized:{hospitalized}/{BED_COUNT}')
		ax2.set_xticks([])
		ax2.set_yticks([])

		cond.wait()
		cond.release()

		color_total = colors_people[7]
		color_contagious = colors_people[8]
		color_diagnosed = colors_people[6]
		color_susceptible = colors_people[0]
		color_exposed = colors_people[1]
		color_infective = colors_people[2]
		color_recovered = colors_people[4]
		color_R0 = colors_statics[0]

		if mode in line:
			if (time >= 1):
				ax3.plot([time-1, time], ax3_susceptible_data, color = color_susceptible)
				ax3.plot([time-1, time], ax3_total_data, color = color_total)
				ax3.plot([time-1, time], ax5_infective_data, color = color_infective)
				ax3.plot([time-1, time], ax4_exposed_data, color = color_exposed)
				ax3.plot([time-1, time], ax3_recover_data, color = color_recovered) if pool.recovered_included == True else None
				ax4.plot([time-1, time], ax4_exposed_data, color = color_exposed)
				ax4.plot([time-1, time], ax4_contagious_data, color = color_contagious)
				ax5.plot([time-1, time], ax5_infective_data, color = color_infective)
				ax5.plot([time-1, time], ax5_diagnosed_data, color = color_diagnosed)
				ax6.plot([time-1, time], ax6_r0_data, color = color_R0)
		else:
			ax3.bar(time, total, color = color_total, width=1)
			ax3.bar(time, susceptible, color = color_susceptible, width=1)
			ax3.bar(time, exposed, color = color_exposed, width=1)
			ax3.bar(time, infective, color = color_infective, width=1)
			ax3.bar(time, recovered, color = color_recovered, width=1) if pool.recovered_included == True else None
			ax4.bar(time, contagious, color = color_contagious, width=1)
			ax4.bar(time, exposed, color = color_exposed, width=1)
			ax5.bar(time, diagnosed, color = color_diagnosed, width=1)
			ax5.bar(time, infective, color = color_infective, width=1)
			ax6.bar(time, R0, color = color_R0, width=1)

		ax3.set_title(f'total({color_total}):{total}\nsusceptible({color_susceptible}):{susceptible}\nrecovered({color_recovered}):{recovered}\nexposed({color_exposed}):{exposed}\ninfective({color_infective}):{infective}')
		ax4.set_title(f'contagious({color_contagious}):{contagious}\nexposed({color_exposed}):{exposed}')
		ax5.set_title(f'diagnosed({color_diagnosed}):{diagnosed}\ninfective({color_infective}):{infective}')
		ax6.set_title(f'R0({color_R0}):{R0:.2f}\nBROAD_RATE:{pool.BROAD_RATE:.2f}\nu:{pool.u:.2f}')

		if mode in line:
			ax3_susceptible_data[0] = susceptible
			ax3_total_data[0] = total
			ax3_recover_data[0] = recovered
			ax4_exposed_data[0] = exposed
			ax4_contagious_data[0] = contagious
			ax5_infective_data[0] = infective
			ax5_diagnosed_data[0] = diagnosed
			ax6_r0_data[0] = R0

	ani = animation.FuncAnimation(fig=fig, init_func=init, interval=1, func=multi_process, repeat=False)
	plt.show()
