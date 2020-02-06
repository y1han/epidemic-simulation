import numpy as np
import matplotlib.pyplot as plt
from bed import Bed
from city import City
from hospital import Hospital
from people import People
from peoplepool import PeoplePool
from matplotlib import animation

ORIGINAL_COUNT = 50 #初始感染数量
BROAD_RATE = 0.7 #传播率
SHADOW_TIME = 14 #潜伏时间
HOSPITAL_RECEIVE_TIME = 3 #医院收治响应时间
CURE_TIME = 14 #治疗时间
BED_COUNT = 1000 #医院床位
SAFETY_DIST = 15 #安全距离
u = np.exp(0.99) #流动意向平均值
PERSON_COUNT = 5000 #城市内人数

city = City(0, 0)
pool = PeoplePool(PERSON_COUNT, city, BROAD_RATE, SHADOW_TIME, HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST)
hos = Hospital(BED_COUNT)
colors_people = ['white', 'yellow', 'red', 'black'] #0未感染，1潜伏期，2感染, 3住院
colors_bed = ['red', 'black'] #0有人，1无人

for i in range(ORIGINAL_COUNT):
	idx = np.random.randint(0, PERSON_COUNT)
	pool.peoples[idx].status = 1
	pool.peoples[idx].infected_time = 0

fig = plt.figure(figsize=(20, 10))
plt.style.use('dark_background')
fig.patch.set_facecolor('black')
grid = plt.GridSpec(3, 5, wspace=0.5, hspace=0.5)
ax1 = plt.subplot(grid[0:3, 0:3])
ax2 = plt.subplot(grid[0:3, 3])
ax3 = plt.subplot(grid[0, 4])
ax4 = plt.subplot(grid[1, 4])
ax5 = plt.subplot(grid[2, 4])

hosX = hos.getX()
hosY = hos.getY()

axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

def animate(time):
	status = pool.getStatus()
	status_hos = hos.getStatus()
	suspected = np.sum(status == 0)
	incubated = np.sum(status == 1)
	exposed = np.sum(status == 2)
	hospitalized = np.sum(status_hos == False)

	fig.canvas.restore_region(axbackground)
	fig.canvas.restore_region(ax2background)

	ax1.clear()
	ax1.scatter(pool.getX(), pool.getY(), c = [colors_people[j] for j in status], marker = '.', \
				alpha = 0.5, s = 10)
	ax1.set_title(f'Time:{time:<10}Suspected:{suspected:<10}Incubated:{incubated:<10}Exposed:{exposed}')
	ax1.set_xticks([])
	ax1.set_yticks([])
	ax1.set_xlim(-5000, 5000)
	ax1.set_ylim(-5000, 5000)

	ax2.clear()
	ax2.scatter(hosX, hosY, c = [colors_bed[j] for j in status_hos], marker = '.', \
				alpha = 1, s = 10)
	ax2.set_title(f'Hospitalized:{hospitalized}/{BED_COUNT}')
	ax2.set_xticks([])
	ax2.set_yticks([])

	ax3.bar(time, suspected, color = colors_people[0], width=1)
	ax3.set_title(f'Suspected:{suspected}')
	ax4.bar(time, incubated, color = colors_people[1], width=1)
	ax4.set_title(f'Incubated:{incubated}')
	ax5.bar(time, exposed, color = colors_people[2], width=1)
	ax5.set_title(f'Exposed:{exposed}')

	pool.update(time, hos, u)
	# plt.pause(0.00001)
	return 0

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=60, bitrate=256000)

ani = animation.FuncAnimation(fig=fig, func=animate)
# ani.save('infection.mp4', writer=writer)

plt.show()
