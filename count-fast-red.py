#!/usr/bin/env python

import os
from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.measure import ResultsTable, Measurements
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager
from ij.gui import GenericDialog, WaitForUserDialog, Roi
from ij.io import DirectoryChooser

binary_threshold = 180
part_min = 500
part_max = 10000

def get_jpglist():
    imagedir = DirectoryChooser("Choose your image directory").getDirectory()
    files = os.listdir(imagedir)
    jpgs = [imagedir + i for i in files if "jpg" in i.lower()]
    return(jpgs)

def roi_select():
    rm = RoiManager.getInstance()
    if not rm:
        rm = RoiManager()
    rm.reset()
    WaitForUserDialog("Please add ROI if any").show()
    nroi = rm.getCount()
    return(nroi)

def analyze_image(path):
    img = IJ.openImage(path)
    img.show()
    nroi = roi_select()
    IJ.run(img, "Colour Deconvolution", "vectors=[FastRed FastBlue DAB]")
    windows = WindowManager.getImageTitles()
    redwindow = [s for s in windows if "Colour_1" in s]
    IJ.selectWindow(redwindow[0])
    red = WindowManager.getCurrentImage()
    IJ.setThreshold(red, 0, binary_threshold)
    IJ.run(red, "Convert to Mask", "")
    if nroi > 0:
        rm = RoiManager.getInstance()
        rm.select(0)
    table = ResultsTable()
    pa = ParticleAnalyzer(ParticleAnalyzer.DISPLAY_SUMMARY|ParticleAnalyzer.SHOW_OVERLAY_MASKS, Measurements.AREA, table, part_min, part_max, 0.0, 1.0)
    pa.analyze(red)

def close_windows():
    WaitForUserDialog("Please inspect the result").show()
    allw = WindowManager.getImageTitles()
    ni = WindowManager.getNonImageTitles()
    imagew = [i for i in allw if i not in ni]
    for w in imagew:
        IJ.selectWindow(w)
        IJ.run("Close")
    
def main():
    jpgs = get_jpglist()
    for i in jpgs:
        analyze_image(i)
        close_windows()

if __name__ in ['__builtin__', '__main__']:
    main()
