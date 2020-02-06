import numpy as np

class People:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		# self.city = city
		self.status = 0 #0未感染，1潜伏期，2感染, 3住院, 4病死
		self.bed = None
		self.infected_time = None
		self.confirmed_time = None
		self.hospitalized_time = None

	def move(self, u, SCALE):
		self.x += u*SCALE/50*np.random.normal(0, 1)
		self.y += u*SCALE/50*np.random.normal(0, 1)