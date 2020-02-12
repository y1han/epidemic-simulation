import numpy as np
from scipy.spatial import cKDTree

dic = {'x':0, 'y':1, 'status':2, 'bed':3, 'infected_time':4, 'confirmed_time':5, 'hospitalized_time':6, 'immuned_time':7}
x = dic['x']
y = dic['y']
status = dic['status']
bed = dic['bed']
infected_time = dic['infected_time']
confirmed_time = dic['confirmed_time']
hospitalized_time = dic['hospitalized_time']
immuned_time = dic['immuned_time']

class PeoplePool:
	def __init__(self, num, city, SCALE, BROAD_RATE, PROTECTION_RATE, DEATH_RATE, EXPOSED_TIME, IMMUNED_TIME, \
			HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST, u, FLUCTUATION, can_exposed_infect, recovered_included):
		self.num = num
		self.peoples = np.empty(shape=(0, len(dic)), dtype=int)
		self.BROAD_RATE = BROAD_RATE
		self.PROTECTION_RATE = PROTECTION_RATE
		self.DEATH_RATE = DEATH_RATE
		self.EXPOSED_TIME = EXPOSED_TIME
		self.HOSPITAL_RECEIVE_TIME = HOSPITAL_RECEIVE_TIME
		self.CURE_TIME = CURE_TIME
		self.IMMUNED_TIME = IMMUNED_TIME
		self.SAFETY_DIST = SAFETY_DIST
		self.FLUCTUATION = FLUCTUATION
		self.SCALE = SCALE
		self.u = np.exp(u)
		self.can_exposed_infect = can_exposed_infect
		self.recovered_included = recovered_included
		self.Tg = []
		self.Te = []
		self.Ti = []
		self.in_touch = 0
		self.can_infect_status = [1, 2] if can_exposed_infect == True else [2] 
		for i in range(num):
			x_init = self.SCALE*np.random.normal(0, 1) + city[0]
			y_init = self.SCALE*np.random.normal(0, 1) + city[1]
			#[0]x, [1]y, [2]status, [3]bed, [4]infected_time, [5]confirmed_time, [6]hospitalized_time, [7]immuned_time
			people = [[x_init, y_init, 0, None, None, None, None, None]]
			self.peoples = np.r_[self.peoples, people]
	
	def getX(self, included=False):
		if not included:
			return self.peoples[(self.peoples[:,2] != 3) & (self.peoples[:,2] != 5)][:, x]
		else:
			return self.peoples[:, x]
	
	def getY(self, included=False):
		if not included:
			return self.peoples[(self.peoples[:,2] != 3) & (self.peoples[:,2] != 5)][:, y]
		else:
			return self.peoples[:, y]

	def getStatus(self, included=False):
		if not included:
			return self.peoples[(self.peoples[:,2] != 3) & (self.peoples[:,2] != 5)][:, status]
		else:
			return self.peoples[:, status]

	def getCoordinates(self, included=False, only=None):
		if not included:
			return self.peoples[(self.peoples[:,2] != 3) & (self.peoples[:,2] != 5)][:, [0, 1]]
		elif only == 23:
			if self.can_infect_status == [1, 2]:
				return self.peoples[(self.peoples[:,2] == 1) | (self.peoples[:,2] == 2)][:, [0, 1]]
			else:
				return self.peoples[self.peoples[:,2] == 2][:, [0, 1]]
		elif only == 1:
			return self.peoples[self.peoples[:,2] == 0][:, [0, 1]]
		else:
			return self.peoples[:, [0, 1]]
		

	def update(self, time, hospital, cond):
		cond.acquire()
		cond.wait()
		protection_factor = np.exp(-self.PROTECTION_RATE)
		self.BROAD_RATE *= protection_factor
		self.u *= protection_factor
		self.DEATH_RATE *= protection_factor
		exposed_time = np.random.normal(self.EXPOSED_TIME, self.FLUCTUATION, size=(self.num, 1))
		hospital_receive_time = np.random.normal(self.HOSPITAL_RECEIVE_TIME, self.FLUCTUATION, size=(self.num, 1))
		cure_time = np.random.normal(self.CURE_TIME, self.FLUCTUATION, size=(self.num, 1))
		immune_time = np.random.normal(self.IMMUNED_TIME, self.FLUCTUATION, size=(self.num, 1))
		peoples = self.peoples
		coord = self.getCoordinates()
		coord_susceptible = self.getCoordinates(True, 1)
		coord_contagious = self.getCoordinates(True, 23)
		tree = cKDTree(coord)
		tree_susceptible = cKDTree(coord_susceptible)
		tree_contagious = cKDTree(coord_contagious)
		self.in_touch = tree_susceptible.count_neighbors(tree_contagious, r=self.SAFETY_DIST)
		for idx, people in enumerate(peoples):
			if people[status] == 0:
				for index in tree.query_ball_point(people[0:2], self.SAFETY_DIST):
					if peoples[index][status] in self.can_infect_status:
							if np.random.rand() < self.BROAD_RATE:
								people[infected_time] = time
								people[status] = 1
								break
			elif people[status] == 1:
				if (time - people[infected_time]) > exposed_time[idx][0]:
					people[confirmed_time] = time
					people[status] = 2
					self.Te.append(time-people[infected_time])
			elif people[status] == 2:
				if np.random.rand() < self.DEATH_RATE:
					people[status] = 5
				elif (time - people[confirmed_time]) > hospital_receive_time[idx][0]:
					tmp = hospital.pickBed()
					if len(tmp) == 0: 
						print(f"Time={time:<6}无隔离病房床位")
					else:
						people[bed] = tmp
						people[status] = 3
						people[hospitalized_time] = time
						self.Ti.append(time-people[confirmed_time])
						self.Tg.append(time-people[infected_time])
			elif people[status] == 3:
				if np.random.rand() < self.DEATH_RATE / 10:
					people[status] = 5
					people[bed][2] = False
					people[bed] = None
				elif (time - people[hospitalized_time]) > cure_time[idx][0]:
					if self.recovered_included:
						people[status] = 4
						people[immuned_time] = time
					else:
						people[status] = 0
					people[bed][2] = False
					people[bed] = None
					people[hospitalized_time] = None
					people[confirmed_time] = None
					people[infected_time] = None
			elif people[status] == 4:
				if (time - people[immuned_time]) > immune_time[idx][0]:
					people[immuned_time] = None
					people[status] = 0
			elif people[status] == 5:
				continue
		peoples[:, [0, 1]] += self.u*self.SCALE/50*np.random.randn(self.num, 2)
		cond.notify()
		cond.release()