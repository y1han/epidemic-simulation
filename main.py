import numpy as np
from city import City
from hospital import Hospital
from peoplepool import PeoplePool
from graph import graph

def init():
	ORIGINAL_COUNT = 50 #初始感染数量
	BROAD_RATE = 0.8 #被传染概率
	PROTECTION_RATE = 0.001 # 保护措施增长率
	EXPOSED_TIME = 5 #平均潜伏时间
	HOSPITAL_RECEIVE_TIME = 3 #平均医院收治时间
	CURE_TIME = 10 #平均治疗时间
	IMMUNED_TIME = 30 #平均免疫期时间
	DEATH_RATE = 0.01/(CURE_TIME+10*HOSPITAL_RECEIVE_TIME) #每日死亡概率
	BED_COUNT = 1000 #医院床位
	SAFETY_DIST = 50 #安全距离
	FLUCTUATION = 4 #各参数与平均值之间的波动
	u = 1 #流动意向
	PERSON_COUNT = 10000 #城市内人数
	can_exposed_infect = False # 潜伏期能否感染他人
	recovered_included = True # 是否有免疫期

	city = City(0, 0)
	pool = PeoplePool(PERSON_COUNT, city, BROAD_RATE, PROTECTION_RATE, DEATH_RATE, EXPOSED_TIME, IMMUNED_TIME, \
					  HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST, u, FLUCTUATION, \
					  can_exposed_infect, recovered_included)
	hos = Hospital(BED_COUNT)

	for i in range(ORIGINAL_COUNT):
		idx = np.random.randint(0, PERSON_COUNT)
		pool.peoples[idx].status = 1
		pool.peoples[idx].infected_time = 0

	return city, pool, hos

def choose(city, pool, hos, mode='bar'): # mode='l'或者'line'时为折线图(line)，否则为柱状图(bar)
	graph(city, pool, hos, mode)
	
if '__main__' == __name__:
	city, pool, hos = init()
	choose(city, pool, hos, 'l')
