from people import People
import numpy as np
from scipy.spatial.distance import cdist

class PeoplePool:
	def __init__(self, num, city, BROAD_RATE, PROTECTION_RATE, DEATH_RATE, EXPOSED_TIME, IMMUNED_TIME, \
			HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST, u, FLUCTUATION, can_exposed_infect, recovered_included):
		# self.city = city
		self.peoples = np.array([])
		self.BROAD_RATE = BROAD_RATE
		self.PROTECTION_RATE = PROTECTION_RATE
		self.DEATH_RATE = DEATH_RATE
		self.EXPOSED_TIME = EXPOSED_TIME
		self.HOSPITAL_RECEIVE_TIME = HOSPITAL_RECEIVE_TIME
		self.CURE_TIME = CURE_TIME
		self.IMMUNED_TIME = IMMUNED_TIME
		self.SAFETY_DIST = SAFETY_DIST
		self.FLUCTUATION = FLUCTUATION
		self.SCALE = 1000
		self.u = np.exp(u)
		self.can_exposed_infect = can_exposed_infect
		self.recovered_included = recovered_included
		self.Tg = []
		self.Te = []
		self.Ti = []
		self.in_touch = 0
		if can_exposed_infect == True:
			self.can_infect_status = [1, 2]
		else:
			self.can_infect_status = [2]
		for i in range(num):
			x = self.SCALE*np.random.normal(0, 1) + city.centerX
			y = self.SCALE*np.random.normal(0, 1) + city.centerY
			self.peoples = np.append(self.peoples, People(x, y))
	
	def getX(self, included=False):
		return np.array([people.x for people in self.peoples if not ((included == False) and (people.status == 3 or people.status == 5))])

	def getY(self, included=False):
		return np.array([people.y for people in self.peoples if not ((included == False) and (people.status == 3 or people.status == 5))])

	def getStatus(self, included=False):
		return np.array([people.status for people in self.peoples if not ((included == False) and (people.status == 3 or people.status == 5))])

	def getCoordinates(self):
		return np.array([(i.x, i.y) for i in self.peoples])

	def update(self, time, hospital):
		self.BROAD_RATE *= np.exp(-self.PROTECTION_RATE)
		self.in_touch = 0
		peoples = self.peoples
		coord = self.getCoordinates()
		dists = cdist(coord, coord)
		for idx, people in enumerate(peoples):
			if people.status == 0:
				index_neighbors = np.where(dists[idx] < self.SAFETY_DIST)[0]
				for index in index_neighbors:
					if peoples[index].status in self.can_infect_status:
							self.in_touch += 1
							if np.random.rand() < self.BROAD_RATE:
								people.infected_time = time
								people.status = 1
								# break
			elif people.status == 1:
				if (time - people.infected_time) > np.random.randint(self.EXPOSED_TIME-self.FLUCTUATION, self.EXPOSED_TIME+self.FLUCTUATION+1):
					people.confirmed_time = time
					people.status = 2
					self.Te.append(time-people.infected_time)
			elif people.status == 2:
				if np.random.rand() < self.DEATH_RATE:
					people.status = 5
				elif (time - people.confirmed_time) > np.random.randint(self.HOSPITAL_RECEIVE_TIME-self.FLUCTUATION, self.HOSPITAL_RECEIVE_TIME+self.FLUCTUATION+1):
					tmp = hospital.pickBed()
					if tmp == None:
						print(f"Time={time:<6}无隔离病房床位")
					else:
						people.bed = tmp
						people.status = 3
						people.hospitalized_time = time
						self.Ti.append(time-people.confirmed_time)
						self.Tg.append(time-people.infected_time)
			elif people.status == 3:
				if np.random.rand() < self.DEATH_RATE / 10:
					people.status = 5
					people.bed.isEmpty = True
					people.bed = None
				elif (time - people.hospitalized_time) > np.random.randint(self.CURE_TIME-self.FLUCTUATION, self.CURE_TIME+self.FLUCTUATION+1):
					if self.recovered_included:
						people.status = 4
						people.immuned_time = time
					else:
						people.status = 0
					people.bed.isEmpty = True
					people.bed = None
					people.hospitalized_time = None
					people.confirmed_time = None
					people.infected_time = None
			elif people.status == 4:
				if (time - people.immuned_time) > np.random.randint(self.IMMUNED_TIME-self.FLUCTUATION, self.IMMUNED_TIME+self.FLUCTUATION+1):
					people.immuned_time = None
					people.status = 0
			elif people.status == 5:
				continue
			people.move(self.u, self.SCALE)
		return self