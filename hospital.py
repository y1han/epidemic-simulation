from bed import Bed
import numpy as np

class Hospital:
	def __init__(self, bed_counts):
		self.bed_counts = bed_counts

		self.width = int(bed_counts / 20)
		self.column = int(bed_counts / self.width)
		if not bed_counts % self.width == 0:
			self.column += 1
		
		self.beds = np.array([])
		for i in range(self.column):
			for j in range(self.width):
				bed = Bed(True, i, j)
				self.beds = np.append(self.beds, bed)

	def pickBed(self):
		for bed in self.beds:
			if bed.isEmpty:
				bed.isEmpty = False
				return bed
		return None

	def getX(self):
		return np.array([bed.x for bed in self.beds])

	def getY(self):
		return np.array([bed.y for bed in self.beds])

	def getStatus(self):
		return np.array([bed.isEmpty for bed in self.beds])