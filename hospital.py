import numpy as np

class Hospital:
	def __init__(self, bed_counts):
		self.bed_counts = bed_counts

		self.width = int(bed_counts / 20)
		self.column = int(bed_counts / self.width)
		if not bed_counts % self.width == 0:
			self.column += 1
		
		self.beds = np.empty(shape=(0, 3), dtype=int)
		for i in range(self.column):
			for j in range(self.width):
				bed = [[i, j, 0]]
				self.beds = np.r_[self.beds, bed]

	def pickBed(self):
		try:
			tmp = np.where(self.beds[:, 2] == False)[0][0]
			self.beds[tmp, 2] = 1
			return self.beds[tmp]
		except:
			return np.array([])

	def getX(self):
		return self.beds[:, 0]

	def getY(self):
		return self.beds[:, 1]

	def getStatus(self):
		return self.beds[:, 2]