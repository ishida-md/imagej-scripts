## Little snippet that runs "Measure" on all ROIs

from ij import IJ
from ij.plugin.frame import RoiManager
from ij.measure import Measurements
from ij.plugin.filter import ParticleAnalyzer

def measure_rois():
	roim = RoiManager().getInstance()
	n_roi = roim.getCount()
	for i in range(n_roi):
		roim.select(i)
		roim.runCommand('Measure')

def main():
	measure_rois()

if __name__ in ['__builtin__', '__main__']:
	main()
