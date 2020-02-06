import numpy as np
from city import City
from hospital import Hospital
from peoplepool import PeoplePool
from graph import graph

def init():
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
	pool = PeoplePool(PERSON_COUNT, city, BROAD_RATE, \
					  SHADOW_TIME, HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST, u)
	hos = Hospital(BED_COUNT)

	for i in range(ORIGINAL_COUNT):
		idx = np.random.randint(0, PERSON_COUNT)
		pool.peoples[idx].status = 1
		pool.peoples[idx].infected_time = 0

	return city, pool, hos

def choose(city, pool, hos, mode='bar'):#mode='l'或者'line'时为折线图(line)，否则为柱状图(bar)
	graph(city, pool, hos, mode)


if '__main__' == __name__:
	city, pool, hos = init()
	choose(city, pool, hos, 'l')
