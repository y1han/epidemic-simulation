from people import People
import numpy as np
from scipy.spatial.distance import cdist
from math import sqrt

class PeoplePool:
	def __init__(self, num, city, BROAD_RATE, SHADOW_TIME, \
			HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST, u, FLUCTUATION):
		# self.city = city
		self.peoples = np.array([])
		self.BROAD_RATE = BROAD_RATE
		self.SHADOW_TIME = SHADOW_TIME
		self.HOSPITAL_RECEIVE_TIME = HOSPITAL_RECEIVE_TIME
		self.CURE_TIME = CURE_TIME
		self.SAFETY_DIST = SAFETY_DIST
		self.FLUCTUATION = FLUCTUATION
		self.u = u
		for i in range(num):
			x = 1000*np.random.normal(0, 1) + city.centerX
			y = 1000*np.random.normal(0, 1) + city.centerY
			self.peoples = np.append(self.peoples, People(x, y))
	
	def getX(self, hospitalized_included=False):
		return np.array([people.x for people in self.peoples if not ((hospitalized_included == False) and (people.status == 3))])

	def getY(self, hospitalized_included = False):
		return np.array([people.y for people in self.peoples if not ((hospitalized_included == False) and (people.status == 3))])

	def getStatus(self, hospitalized_included = False):
		return np.array([people.status for people in self.peoples if not ((hospitalized_included == False) and (people.status == 3))])

	def getCoordinates(self):
		return np.array([(i.x, i.y) for i in self.peoples])

	def update(self, time, hospital):
		peoples = self.peoples
		coord = self.getCoordinates()
		dists = cdist(coord, coord)
		for idx, people in enumerate(peoples):
			if people.status == 0:
				index_neighbors = np.where(dists[idx] < self.SAFETY_DIST)[0]
				for index in index_neighbors:
					if index != idx:
						if peoples[index].status == 1 or peoples[index].status == 2:
								if np.random.rand() < self.BROAD_RATE:
									people.infected_time = time
									people.status = 1
									break
				# for others in peoples[idx:]:
				# 	if others.status == 1 or others.status == 2:
				# 		if  sqrt((people.x - others.x) ** 2 + (people.y - others.y) ** 2) \
				# 					< self.SAFETY_DIST: #距离
				# 			if np.random.rand() < self.BROAD_RATE:
				# 				people.infected_time = time
				# 				people.status = 1
				# 				break
			elif people.status == 1:
				if (time - people.infected_time) > np.random.normal(self.SHADOW_TIME, self.FLUCTUATION):
					people.confirmed_time = time
					people.status = 2
			elif people.status == 2:
				if (time - people.confirmed_time) > np.random.normal(self.HOSPITAL_RECEIVE_TIME, self.FLUCTUATION):
					tmp = hospital.pickBed()
					if tmp == None:
						print(f"Time={time:<6}无隔离病房床位")
					else:
						people.bed = tmp
						people.status = 3
						people.hospitalized_time = time
			elif people.status == 3:
				if (time - people.hospitalized_time) > np.random.normal(self.CURE_TIME, self.FLUCTUATION):
					people.status = 0
					people.bed.isEmpty = True
					people.bed = None
					people.hospitalized_time = None
					people.confirmed_time = None
					people.infected_time = None

			people.move(self.u)
