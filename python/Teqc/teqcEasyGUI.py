from tkinter import *
import tkinter.messagebox
import subprocess
import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import scrolledtext
from tkinter import ttk
import fileinput
import webbrowser
import matplotlib.pyplot as plt
import numpy as np

import sys
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# The teqcplot.py web site is http://www.westernexplorers.us/teqcplot/
# This file is online at      http://www.westernexplorers.us/teqcplot/teqcplot.py
# See also the document at    http://www.westernexplorers.us/teqcplot/Teqcplot_Documentation.txt.

# Version: 11 Sep. 2015

# Copyright (c) 2015 Stuart K. Wier

#         ============  to save plots automatically as PNG files ===============
# As supplied teqcplot is an interactive program, that makes one plot image in a window on your screen.
#     You can save that image with a click on the disc icon in the window lower margin.
# To automatically make and save the plot image as a PNG file, do these code changes in this teqcplot.py file:
# 1. Uncomment the line  #mptl.use('Agg')   below, i.e. remove the #, and preserving the indentation level
# 2. Comment out the line  plt.show() ;           i.e. start the line with #,  preserving the indentation level
# 3. Uncomment the line # plt.savefig(filename) ; i.e. remove the # , preserving the indentation level

# To see debug statements, set the value noprint=0 in the noprint= line below.


import os
import sys
import string
import datetime
import numpy as np
import matplotlib as mptl
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# new 10 Sep 2015
# the next line is used ONLY to save figures as PNG files (see also lines around 'savefig' below):
# mptl.use('Agg') # uncomment when needed to save figures as PNG files.

from numpy import *
from datetime import timedelta
from datetime import datetime
from matplotlib.pyplot import grid, figure, plot, savefig
from time import gmtime, strftime
# import teqcplot

import os
import sys
import string
import datetime
import numpy as np
import matplotlib as mptl
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# new 10 Sep 2015
# the next line is used ONLY to save figures as PNG files (see also lines around 'savefig' below):
# mptl.use('Agg') # uncomment when needed to save figures as PNG files.

from numpy import *
from datetime import timedelta
from datetime import datetime
from matplotlib.pyplot import grid, figure, plot, savefig
from time import gmtime, strftime

Copyright_and_License_Notice = """
 * Copyright 2014, 2015 Stuart K. Wier
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License (GNU GPL v3),
 * or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
 * General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the 
 * Free Software Foundation, Inc., 
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 """

helptext = """

How to Use teqcplot

Preparation 

To install and run teqcplot, first verify your system requirements, and download the teqcplot.py file, as described 
in teqcplot's Wiki Installation page, http://code.google.com/p/teqcplot/wiki/Installation.
You need Python, and the Python libraries numpy version 1.5 and matplotlib version 1.3.

Teqcplot plots data from the UNAVCO "teqc" program for analysing GNSS observations.
About teqc, see http://www.unavco.org/software/data-processing/teqc/teqc.html.
Teqcplot uses teqc's "plot files" in teqc's COMPACT3 format, made with teqc released versions after December 1, 2013.

To adapt teqcplot.py to read data from files in formats other than teqc's COMPACT3, 
you will need to change the method read_input_files() below. 
Note the Python data objects used in plotting, and fill those from your data.

For automatic scripting of teqcplot image file generation:
As supplied teqcplot is an interactive program, that makes one plot image in a window on your screen. 
To automatically make and save the plot image as a PNG file, do these code changes in this teqcplot.py file:
 1. Uncomment the line  # mptl.use('Agg') ;      i.e. remove the # , preserving the indentation level
 2. Comment out the line  plt.show() ;           i.e. start the line with #,  preserving the indentation level
 3. Uncomment the line # plt.savefig(filename) ; i.e. remove the # , preserving the indentation level


Use 

Teqcplot uses command line commands, with data filenames and options. Each run of teqcplot.py makes one plot on your screen. 
To stop the program click on the 'x' in the upper right corner of the window which pops up. 
Spaces " " are not allowed in options. Option order should not matter. 

Examples of teqcplot commands:

To run teqcplot.py, you use the command teqcplot.py in the working directory where that file is, 
or use ./teqcplot.py if that directory is not in your Linux PATH.  These examples use teqcplot.py.

Entering the command teqcplot.py shows this help message.


To make skyplots (polar plots):

   teqcplot.py +skyplot jplv1200.azi jplv1200.ele

This creates a skyplot of tracks of SVs, with data from teqc COMPACT3 plot files "jplv1200.azi" and "jplv1200.ele"


To make azimuth-elevation plots (azimuth on x axis; elevation on y axis):

   teqcplot.py +azelplot jplv1200.azi jplv1200.ele

This shows an azimuth-elevation plot of tracks of SVs, with data from teqc COMPACT3 plot files "jplv1200.azi" and "jplv1200.ele"


To make plots with time of day on the x axis and elevation on the y axis 

   teqcplot.py +timeelplot jplv1200.azi jplv1200.ele


Options may added to the command, for example using the option -R means do not plot any GLONASS SVs. 

   teqcplot.py +skyplot jplv1200.azi jplv1200.ele -R

This makes a skyplot of tracks of SVs, but with no GLONASS SVs shown. 

Likewise use -G for no GPS SVs, -E for no Galileo, -J for no QZSS, -C for no Beidou, and -S for no SBAS.

To save an image file of the display, click on the "Save the figure" button on the bottom of the window which pops up.
To change the plot image file size (pixels) use the options +pw and +pd described next.

SVs are selected to plot from the data files, in the order the SVs appear in the data file.  If you choose to plot
10 tracks and the first 5 are GPS and the next five are GLONASS in the file, those are the ones plotted, unless 
options change SV selection. 


Other options:

+tcl=n 
n, an integer, is the maximum number of how many tracks to show (lines in plot). Default is 6.

+msize=f.f
f.f is a float number denoting point marker size, for line width or thickness.  Default is 2.5.

+legend 
to show a legend of colors identifying each SV next to the figure. Default is no legend. This is for plots
where each SV data has one color.

-tracklabels 
do not show the SV id (like G12) on each track (line on plot). Default is to show the SV labels.

+pw=f.f 
f.f, a float number, sets the width of plot in centimeters. Default value is 20.0 cm. 

+pd=nn 
nn, an integer, is the pixel density, how many pixels per centimeter (* 2.54 is "dots per inch"). Default is 50. 
For printing illustrations, you can adjust the quality of the figure image file by changing pw and/or pd.  For example:

    teqcplot.py  +skyplot  +tcl=8  jplv0970.azi jplv0970.ele +pw=25.0 +pd=80 

+GNN, +GNN-MM, +RNN, +RNN-MM, +J01, etc.  Select SVs to plot by constellation and a single number or number range.

    +G12 to plot only data from GPS G12; likewise +R20 for GLONASS; +J01 for QZSS 

    +G12-20 to plot only data from GPS SVs included in the list from G12 through G20; likewise +R20-24 for GLONASS from R20 through R24

    +G12,23,24,25 to plot only data from G12, G23, G24 and G25; likewise +R15,20,22 to plot these three GLONASS SVs 

     With the +G, +R, etc. options you may to also include a +tcl=N option.

  Example:

    teqcplot.py +skyplot mal20970.azi mal20970.ele +R15,20,22,23,25 +G12,23,24,25  +tcl=9


+color=orange 
sets this one color for all tracks (lines in plot). Use standard HTML color names. 
Has no effect on plot lines colored by parameter values as described below.


+minHour=8.0, +maxHour=16.5
  You can limit the time range shown in time plots with options +minHour, +maxHour:

    teqcplot.py +timeparmplot p2301220.azi p2301220.ele p2301220.m12 +G22 +minHour=8 +maxHour=16


To Color Tracks by Parameter Value

To make plots like the above, and also color the SV tracks by data values, including signal to noise ratios, multipath values, or by ionosphere values, from the corresponding teqc plot files, use an additional teqc QC plot file name in the command, such as jplv1200.sn1

    teqcplot.py  +skyplot  jplv0970.azi jplv0970.ele  jplv1200.sn1

    teqcplot.py  +timeelplot  jplv0970.azi jplv0970.ele  jplv1200.m12  

    teqcplot.py  +axelplot  jplv0970.azi jplv0970.ele  jplv1200.i12

Color ranges used depend on the parameter type, each of which has a preset range of values, 
to enable equal comparion of several plots, and to not stretch the color scale to cover a 
few extreme high and low values.    

The default limits for colors of values are:

signal to noise:              20.0 to 60.0
multipath:                    -1.5 to  1.5
ionspheric delay:            -30.0 to 40.0
ionspheric delay derivative:  -0.5 to  0.5

You can change these with either or both of the options +colorMax and +colorMin, for example

    teqcplot.py +bandplot IRID1380.azi IRID1380.ele IRID1380.sn1  +colorMax=50  +colorMin=10

The default color map is the Python matplotlib's "hsv." By experience this is the most distinct color map for many uses. 
You can change the Python code to change the color map used to any other matplotlib color map name.  
You can, if you wish, change the color map name in the line cmap=mptl.cm.hsv.

Another colored plot is the Band Plot.  To make GNSS band plots, with a horizontal line for each SV, versus time, 
  use the plot type option +bandplot:

    teqcplot.py  +bandplot  jplv0970.azi jplv0970.ele  jplv1200.sn1


Time-Parameter Plots. To make plots with time of day on the x axis and the parameter on the y axis.  Not colored.

    teqcplot.py +timeparmplot jplv1200.azi jplv1200.ele   jplv1200.m12  +G23

  Usually this is done with data from one SV, with an option like +G23.

  You can limit the time range shown with options +minHour, +maxHour:

    teqcplot.py +timeparmplot p2301220.azi p2301220.ele p2301220.m12 +G22 +minHour=8 +maxHour=16


Visibility Plot 

  Bandplots without a 3rd (parameter values) file make a "Visibility" plot:

    teqcplot.py  +bandplot  jplv0970.azi jplv0970.ele 

Spaces " " are not allowed in options. Option order should not matter.


                                               Copyright (C) 2014, 2015 Stuart K. Wier

  Teqcplot.py is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License.
  You must retain the original and complete Copyright and License Notice in all cases.

    """

global mycanvas
global mybutton
global mytoolbar

def my_destory():
    global canvas
    global button
    print("hello")
    canvas.get_tk_widget().destroy();
    button.destroy()

def read_input_files():
    global noprint
    global asciiStartTime
    # open the azi file
    datapath1 = os.path.dirname(azifile)
    filename1 = os.path.basename(azifile)
    fileext = filename1.split(".")
    file1 = open(azifile)
    # open the elevation file
    datapath2 = os.path.dirname(elefile)
    filename2 = os.path.basename(elefile)
    fileext = filename2.split(".")
    file2 = open(elefile)
    # handle the parm file, if any
    if len(parmfile) > 5:
        datapathp = os.path.dirname(parmfile)
        pfilename = os.path.basename(
            parmfile)  # debug if plottype != "Time-parameter plot": #   if noprint!=1 : print "  Color by value the "+parmtype+" data from "+pfilename
        pfile = open(parmfile)
    # count lines in input files
    allLines = file1.readlines()
    file1linecount = len(allLines)
    file1.seek(0)
    # check ele file
    allLines = file2.readlines()
    if len(allLines) != file1linecount:
        print(
            "  Problem: the input '.azi' and '.ele' files have differing count of lines; should be the same. \n  Exit. \n")
        sys.exit(1)
    file2.seek(0)
    if len(parmfile) > 5:
        allLines = pfile.readlines()
        if len(allLines) != file1linecount:
            print(
                "  Problem: the input .azi and parm files have differing count of lines; should be the same. \n  Exit. \n")
            sys.exit(1)
        pfile.seek(0)
    epoch = None
    gotepoch = False

    # step through each line in 2 files; or in 3 files if doParmPlot
    for ln in range(file1linecount):
        # read equivalent lines from 2 or 3 files, at index ln (line number); 0 base
        line = file1.readline()
        file2line = file2.readline()
        if doParmPlot:
            pfileline = pfile.readline()

        # this code assumes that the azi and ele file structures are identical in structure,
        # except for the values in the the value lines after the epoch-sv lines.
        # the epoch-sv lines must be identical in azi and ele files.

        # if first line is not COMPACT3, break

        if ln == 0:
            if line[0:8] != "COMPACT3":
                print("  Problem: input file " + file1 + " is not COMPACT3 format. Exit.\n")
                sys.exit(1)
            if file2line[0:8] != "COMPACT3":
                print("  Problem: input file " + file2 + " is not COMPACT3 format. Exit.\n")
                sys.exit(1)
            if doParmPlot and pfileline[0:8] != "COMPACT3":
                print("  Problem: input file " + pfile + " is not COMPACT3 format. Exit.\n")
                sys.exit(1)
        # make sure start time, in line index 1, is same for all files; get the start time as a datetime
        if ln == 1:
            if line[0:-1] != file2line[0:-1]:
                print("  Problem: azi file, line 2 (start time) does not match ele line 2.\n Exit \n")
                sys.exit(1)
            if doParmPlot and line[0:-1] != pfileline[0:-1]:
                print("  Problem: azi file start time does not match parm file start time.\n  Exit \n")
                sys.exit()
            # get start epoch time from azi file, line index 1
            st1 = line[15:-1]
            st1 = st1[0:19]
            # make python DateTime object:
            starttimeDT = datetime.strptime(st1, '%Y %m %d %H %M %S')
            # make time strings:
            asciiStartTime = starttimeDT.strftime('%Y %m %d %H:%M:%S')
            gotepoch = False

            # read the next values line (in 2 or 3 files) which correspond to a just-read epoch-sv line (next code block)
        if gotepoch:
            gotepoch = False
            azis = line[:-1]
            azis = azis.replace("    ", " ")
            azis = azis.replace("   ", " ")
            azis = azis.replace("  ", " ")
            azis = azis[1:-1]
            azislist = azis.split(" ")
            # if debug: print "  there are "+`len(azislist)`+" azis"
            # the List azislist for this line must correspond to the List of SVS svslist
            if len(azislist) != len(svslist):
                print("  Problem:  number of SVs does not match number of azimuths at line " + ln + " \n  Exit")
                sys.exit()
            # for this epoch, make a List 'eles' of the elevation values at each SV in the List svslist
            # if debug: print " elevations line is _"+file2line[0:-1]
            eles = file2line[:-1]
            eles = eles.replace("    ", " ")
            eles = eles.replace("   ", " ")
            eles = eles.replace("  ", " ")
            eles = eles[1:-1]
            eleslist = eles.split(" ")  # split on whitespace; makes a List
            # the List eleslist for this line should correspond to the List of SVS svslist
            if len(eleslist) != len(svslist):
                print(
                    "  Problem:  number of SVs does not match number of elevations in file2 at line " + ln + " \n Exit")
                sys.exit()
            if not doParmPlot:
                # compose the tuples for the Lists of values to use in making plots
                for ist in range(len(svslist)):
                    posituple = (svslist[ist], epoch, azislist[ist], eleslist[ist])
                    SVpositionList.append(posituple)
            elif doParmPlot:
                if debug: print("  parm line " + ln + " is at epoch or seconds offset =" + dt + "_")
                if debug: print("       line " + ln + " parm data line is _" + pfileline[0:-1])
                parms = pfileline[:-1]
                parms = parms.replace("    ", " ")
                parms = parms.replace("   ", " ")
                parms = parms.replace("  ", " ")
                parms = parms[1:-1]
                parmslist = parms.split(" ")  # split on whitespace; makes a List
                # the List parmslist for this line should correspond to the List of SVS parmsvslist  nnn
                # print '      the lines parm List is  ' + ', '.join(parmslist)
                if len(parmslist) != len(parmsvslist):
                    print(
                        "  Problem:  number of parm SVs does not match number of parm values in parm file at line " + ln + " \n")
                    sys.exit()
                for ist in range(len(parmsvslist)):
                    psv = parmsvslist[ist]
                    if psv in svslist:
                        for i, obj in enumerate(svslist):
                            if obj == psv:
                                svindex = i
                                break
                        # got the index of that SV in the azi and ele files; ist != svindex usually
                        # make one of these tuples with ONE value of SV, time, azi, ele, parm-value.
                        posituple = (psv, epoch, azislist[svindex], eleslist[svindex], parmslist[ist])
                        SVpositionList.append(posituple)
                    # if debug: print "     parm SV "+psv+"  epoch="+`dt`+"   azi , ele="+`azislist[svindex]`+"  "+`eleslist[svindex]`
        # read the next epoch-sv line; 1. get time of line; 2. get lists of SVS on line; one for az-ele data; one for the parms
        if ln > 1 and ln % 2 == 0:
            # print " epoch line "+`ln`+" is ="+line+"_"
            # print " epoch line key is ="+line[12:14]+"_"
            if line[0:-1] != file2line[0:-1]:
                print("  Problem: ele file epoch does not match azi file epoch line.\n")
                sys.exit()
            # if debug: print "\n  next epoch-SV line is _"+line[0:-1]
            offset = line[0:11]
            dt = float(offset)
            if doParmPlot:
                poffset = pfileline[0:11]
                pdt = float(offset)
                if pdt != dt:
                    pass
                    # to use dt time offset from start of file, in seconds, in epoch varible:
            epoch = dt
            # LOOK convert epoch in seconds since start to hours since start time
            epoch = epoch / 3600.0
            # get lists of SVs
            # if epoch-sv line has -1 in line[12:13], use previous svslist
            if line[12:14] == "-1":
                pass  # use previous svslist
            else:
                svs = line[15:-1]
                svslist = svs.split(" ")
            if doParmPlot:
                if pfileline[12:14] == "-1":
                    pass  # use previous parmsvslist
                else:
                    parmsvs = pfileline[15:-1]
                    if debug: print("  parm svs =" + parmsvs + "_")
                    parmsvslist = parmsvs.split(" ")  # split on whitespace; makes a List

            gotepoch = True
    # end function read_input_files()


def makePlot(master):
    # f = Figure(figsize=(4, 4), dpi=100)


    global noprint
    global asciiStartTime
    global maxT
    global minT
    global lineSize
    maxPV = -999.0
    minPV = 9999.0
    svid = ""
    allToPlot = {}
    maxT = -100000.0  # float hours
    minT = 100000.0  # float hours
    numberplotted = 0
    for svid in SVidList:
        times = []
        azis = []
        eles = []
        parms = []
        slipcount = 0
        for aRow in SVpositionList:
            if svid == aRow[0]:
                if plottype == "Skyplot":
                    times.append(aRow[1])
                    azv = float(aRow[2])
                    azis.append(azv * (np.pi / 180))
                    anele = float(aRow[3])
                    eles.append(90.00 - anele)
                else:
                    t = float(aRow[1])
                    if t > maxT: maxT = t
                    if t < minT: minT = t
                    times.append(aRow[1])
                    azv = float(aRow[2])
                    azis.append(azv)
                    anele = float(aRow[3])
                    eles.append(anele)
                if doParmPlot:
                    pv = aRow[4]
                    if pv[-1:] == "S":
                        pv = pv[:-1]
                    pv = float(pv)
                    if pv > maxPV: maxPV = pv
                    if pv < minPV: minPV = pv
                    parms.append(pv)
        if doParmPlot:
            plotDataArrays = (times, azis, eles, parms)
        else:
            plotDataArrays = (times, azis, eles)
        allToPlot[svid] = plotDataArrays

    if noprint != 1: print("  " + parmtype + " data values span " + minPV + " to " + maxPV)
    if noprint != 1: print("  Done reading data to plot.  The figure is being created.")

    starttime_t1 = datetime.now()
    bgcolor = "#FFFFff"
    if plottype == "Skyplot":
        # fig = figure(figsize=(widthDistance, widthDistance), dpi=pixeldensity, facecolor=bgcolor, edgecolor='k')
        fig = Figure(figsize=(widthDistance, widthDistance), dpi=pixeldensity, facecolor=bgcolor, edgecolor='k')
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar', facecolor=bgcolor)
    else:
        # fig = figure(figsize=(1.6 * widthDistance, 1.2 * widthDistance / 1.62), dpi=pixeldensity, facecolor=bgcolor,
                     # edgecolor='k')
        fig = Figure(figsize=(1.6 * widthDistance, 1.2 * widthDistance / 1.62), dpi=pixeldensity, facecolor=bgcolor,edgecolor='k')
        ax = fig.add_axes([0.1, 0.13, 0.8, 0.8], facecolor=bgcolor)
    # a = fig.add_subplot(111)


    if showLegend:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    numberColors = 30
    size = 0.3
    svPRNIndex = 0
    plotlist = []
    svlist = []
    trackcount = 1
    bandindex = 0
    mplot = None
    pvtop = -9999
    pvbot = 9999
    numberplotted = 0
    for svid in sorted(allToPlot.keys()):
        bandindex += 1
        # do not plot unwanted SVs:
        if svid[0:1] == "R" and doglonass != True: continue
        if svid[0:1] == "G" and dogps != True: continue
        if svid[0:1] == "E" and dogalileo != True: continue
        if svid[0:1] == "S" and dosbas != True: continue
        if svid[0:1] == "J" and doqzss != True: continue
        if svid[0:1] == "C" and dobeidou != True: continue
        if len(doShowSVslist) > 0:
            if svid not in doShowSVslist:
                continue;
        if trackcount > trackCountLimit: continue
        trackcount += 1
        svPRNIndex = int(svid[1:])
        if svid[0:1] == "R": svPRNIndex += 32
        plotDataArrays = allToPlot[svid]
        times = plotDataArrays[0]
        azis = plotDataArrays[1]
        eles = plotDataArrays[2]
        if parmtype == "Multipath combination":
            minPV = -1.5
            maxPV = 1.5
        elif parmtype == "Signal to Noise":
            minPV = 20.0
            maxPV = 60.0
        elif parmtype == "Ionspheric Delay (m)":
            minPV = -30.0
            maxPV = 40.0
        elif parmtype == "Ionspheric Delay Derivative (m/min)":
            minPV = -0.5
            maxPV = 0.5
        if colorMax != 1.234567:
            maxPV = colorMax
        if colorMin != 1.234567:
            minPV = colorMin
        # else use minPV maxPV values already found from the data

        if plottype == "Skyplot" or plottype == "Azimuth-elevation plot":
            if True == doParmPlot:
                parms = plotDataArrays[3]
                colmap = mptl.cm.hsv
                prange = maxPV - minPV
                pvtop = -999993.0
                pvbot = 999993.0
                for pi in range(0, len(parms)):
                    pnew = parms[pi]
                    if pnew > maxPV: pnew = maxPV;
                    if pnew < minPV: pnew = minPV;
                    pnew = (pnew - minPV) / prange
                    parms[pi] = pnew
                    if parms[pi] > pvtop: pvtop = parms[pi]
                    if parms[pi] < pvbot: pvbot = parms[pi]
                    # if debug: print "        pvbot, pvtop= "+`pvbot`+" to "+`pvtop`+"     min max PV="+`minPV`+" to "+`maxPV` +"\n"
                norm = mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                mplot = ax.scatter(azis, eles, c=parms, norm=norm, s=lineSize, cmap=mptl.cm.hsv, lw=0)
                # mplot = plt.scatter(azis, eles, c=parms, norm=norm, s=lineSize, cmap=mptl.cm.hsv, lw=0)
                numberplotted += 1
            else:
                if colorname == "":
                    mplot = ax.scatter(azis, eles, s=size, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                    # mplot = plt.scatter(azis, eles, s=size, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                    numberplotted += 1
                else:
                    mplot = ax.scatter(azis, eles, s=size, color=colorname)
                    # mplot = plt.scatter(azis, eles, s=size, color=colorname)
                    numberplotted += 1
        elif plottype == "Time-elevation plot":
            if True == doParmPlot:
                parms = plotDataArrays[3]
                colmap = mptl.cm.hsv
                # print "  parameter allowed range ="+`maxPV`+" to "+`minPV`
                prange = maxPV - minPV
                pvtop = -999993.0
                pvbot = 999993.0
                for pi in range(0, len(parms)):
                    pnew = parms[pi]
                    if pnew > maxPV: pnew = maxPV;
                    if pnew < minPV: pnew = minPV;
                    pnew = (pnew - minPV) / prange
                    parms[pi] = pnew
                    if parms[pi] > pvtop: pvtop = parms[pi]
                    if parms[pi] < pvbot: pvbot = parms[pi]
                norm = mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                mplot = ax.scatter(times, eles, c=parms, norm=norm, s=lineSize, cmap=mptl.cm.hsv, lw=0)
                # mplot = plt.scatter(times, eles, c=parms, norm=norm, s=lineSize, cmap=mptl.cm.hsv, lw=0)
                numberplotted += 1
            else:
                if colorname == "":
                    mplot = ax.scatter(times, eles, s=lineSize, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                    # mplot = plt.scatter(times, eles, s=lineSize, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                    numberplotted += 1
                else:
                    mplot = ax.scatter(times, eles, s=lineSize, color=colorname)
                    # mplot = plt.scatter(times, eles, s=lineSize, color=colorname)
                    numberplotted += 1
        elif plottype == "Time-parameter plot":  # ppp
            if True == doParmPlot:
                parms = plotDataArrays[3]
                yvals = []
                for pi in range(0, len(parms)):
                    yvals.append(parms[pi])
                colmap = mptl.cm.hsv
                prange = maxPV - minPV
                # to set color legend and color of points correctly, need this:
                pvtop = -999993.0
                pvbot = 999993.0
                for pi in range(0, len(parms)):
                    pnew = parms[pi]
                    if pnew > maxPV: pnew = maxPV;
                    if pnew < minPV: pnew = minPV;
                    pnew = (pnew - minPV) / prange  # shoves parm values into 0 to 1 range
                    parms[pi] = pnew
                    if parms[pi] > pvtop: pvtop = parms[pi]
                    if parms[pi] < pvbot: pvbot = parms[pi]
                norm = mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                # plt.plot line style: in plt.plot function: k- means a connected black line;
                # see matplotlib.org/api/pyplot_api.html
                # ko black circle point markers.  g green, b blue , etc.

                mplot=ax.plot(times, yvals, 'ko', markersize=1.5)
                # mplot = plt.plot(times, yvals, 'ko', markersize=1.5)
                numberplotted += 1
            else:
                print("\n   Your teqcplot command needs a parameter input filename, to make a time-parameter plot.\n")
                sys.exit(1)
        elif "GNSS_Band_Plot" == plottype:
            for yi in range(0, len(eles)):
                eles[yi] = bandindex * 1.0
            if True == doParmPlot:
                parms = plotDataArrays[3]
                colmap = mptl.cm.hsv
                prange = maxPV - minPV
                pvtop = -999993.0
                pvbot = 999993.0
                for pi in range(0, len(parms)):
                    pnew = parms[pi]
                    if pnew > maxPV: pnew = maxPV;
                    if pnew < minPV: pnew = minPV;
                    pnew = (pnew - minPV) / prange
                    parms[pi] = pnew
                    if parms[pi] > pvtop: pvtop = parms[pi]
                    if parms[pi] < pvbot: pvbot = parms[pi]
                norm = mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                mplot = ax.scatter(times, eles, c=parms, norm=norm, s=lineSize, marker='s', cmap=mptl.cm.hsv, lw=0)
                # mplot = plt.scatter(times, eles, c=parms, norm=norm, s=lineSize, marker='s', cmap=mptl.cm.hsv, lw=0)
                numberplotted += 1
            else:
                mplot = ax.scatter(times, eles, s=lineSize, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                # mplot = plt.scatter(times, eles, s=lineSize, color=cm.gist_ncar(1.0 * svPRNIndex / numberColors))
                numberplotted += 1
        else:
            print("  NOTE: plot type=_" + plottype + "_ is not recognized.  Exit. \n")
            sys.exit()
        if showLabel:
            if plottype == "Skyplot" or plottype == "Azimuth-elevation plot":
                lenaz = len(azis)
                ax.annotate(svid, (azis[int(lenaz / 3)], eles[int(lenaz / 3)]))
            elif plottype == "Time-elevation plot" or "GNSS_Band_Plot" == plottype:
                lenaz = len(times)
                ax.annotate(svid, (times[int(lenaz / 3)], eles[int(lenaz / 3)]))
            elif plottype == "Time-parameter plot":  # ppp lll
                svnumb = 5 * (int(svid[1:]))  # for an offset from start point
                ax.annotate(svid, (times[svnumb], parms[svnumb]))
                # print "      put svid label at time=" + `times[0]` + "    y="+ `eles[0]`
        plotlist.append(mplot)
        svlist.append(svid)
    if True == doParmPlot and mplot != None and plottype != "Time-parameter plot":
        pvtop = 1.0000
        pvbot = 0.0
        dran = (pvtop - pvbot) / 4
        m1 = pvbot
        m2 = m1 + dran
        m3 = m1 + 2 * dran
        m4 = m1 + 3 * dran
        m5 = pvtop
        lran = (maxPV - minPV) / 4
        l1 = minPV
        l2 = l1 + lran
        l3 = l1 + 2 * lran
        l4 = l1 + 3 * lran
        l5 = maxPV
        print("before")
        print(mplot)
        # colorbar = ax.colorbar(cax=mplot, shrink=0.85, pad=0.075)
        colorbar = fig.colorbar(mplot, ax=ax)
        print("end")


        # colorbar = plt.colorbar(mplot, shrink=0.85, pad=0.075)
        colorbar.set_ticks([m1, m2, m3, m4, m5])
        colorbar.set_ticklabels([l1, l2, l3, l4, l5])
        # print "  Colors limited to values "+`minPV`+" to "+`maxPV`
    ax.grid(True)
    if plottype == "Skyplot":
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rmax(90.0)
        ax.set_yticks(range(0, 90, 10))  # (min int, max int, increment)
        ax.set_yticklabels(map(str, range(90, 0, -10)))
    if plottype == "Azimuth-elevation plot":
        ax.set_xticks(range(-360, 405, 45))
        ax.set_xticklabels(map(str, range(-360, 405, 45)))
        ax.set_yticks(range(0, 100, 10))
        ax.set_yticklabels(map(str, range(0, 100, 10)))
    if plottype == "Time-elevation plot":
        ax.set_xticks(range(0, 25, 3))
        ax.set_yticks(range(0, 100, 10))
        ax.set_yticklabels(map(str, range(0, 100, 10)))
    if plottype == "Time-parameter plot":  # ppp
        ax.set_xticks(range(0, 25, 3))
        spacing = int((maxPV - minPV) / 5.0)
        if 1 > spacing: spacing = 1
        ax.set_yticks(range(int(minPV), int(maxPV + 1.0), spacing))
        ax.set_yticklabels(map(str, range(int(minPV), int(maxPV + 1.0), spacing)))
    if plottype == "GNSS_Band_Plot":
        ax.set_xticks(range(0, 25, 3))
        plt.setp(ax.get_yticklabels(), visible=False)
    if showLegend:
        print("showLegend")
        plots = tuple(plotlist)
        svs = tuple(svlist)
        ax.legend(plots, svs, scatterpoints=1, ncol=1, fontsize=10, markerscale=5.0, loc=2, bbox_to_anchor=(1.05, 1))
    title1 = plottype + " for station " + azifile[-12:-8]
    if "" != parmtype:
        title1 = title1 + ".   " + parmtype + " from " + parmfile
    elif "" == parmtype and plottype == "GNSS_Band_Plot":
        title1 = "   Visibility for station " + azifile[-12:-8]
    if plottype == "Skyplot":
        fig.suptitle(title1, y=0.90, fontsize=11)
    else:

        fig.suptitle(title1, fontsize=11)
    doyear = azifile[-8:-5]
    if len(doyear) < 3: doyear = ""
    if plottype == "Azimuth-elevation plot":
        title2 = " \n Azimuth, degrees \n Data starts " + asciiStartTime + ".  Day of year " + doyear
    elif plottype == "Time-elevation plot" or plottype == "Time-parameter plot" or "GNSS_Band_Plot" == plottype:
        title2 = " \n Time, hours of day \n Data starts " + asciiStartTime + ".  Day of year " + doyear
    else:
        title2 = "Data starts " + asciiStartTime + ".  Day of year " + doyear
    if plottype == "Skyplot":
        if True == doParmPlot:
            ax.set_title(title2, y=-0.15, fontsize=11)
        else:
            ax.set_title(title2, y=-0.11, fontsize=11)
    else:
        ax.set_title(title2, y=-0.15, fontsize=11)
    if plottype == "Azimuth-elevation plot" or plottype == "Time-elevation plot":
        ax.set_ylim(-2.0, 92.0)
        ax.set_ylabel('Elevation, degrees', fontsize=10)
    if plottype == "Azimuth-elevation plot":
        ax.set_xlim(-370.0, 370.0)
    if plottype == "Time-elevation plot" or plottype == "Time-parameter plot":
        # sett
        if minHour > -998.0:
            minT = minHour
        if maxHour > -998.0:
            maxT = maxHour
        ax.set_xlim(minT - 1, maxT + 1)
    if plottype == "Time-parameter plot":  # ppp
        ax.set_ylim((minPV), (maxPV))
    if "GNSS_Band_Plot" == plottype:
        ax.set_ylim(-1.0, trackCountLimit + 1.0)
        ax.set_xlim(minT - 1, maxT + 1)
        ax.set_ylabel('SVs', fontsize=10)
    elapsedtime = (datetime.now() - starttime_t1)
    if noprint != 1: print("  Plotted " + numberplotted + " tracks in " + (elapsedtime.total_seconds()) + " seconds.")
    filestarttime = strftime('%Y%m%d_%H:%M:%S', gmtime())
    filename = svid + "_" + plottype[:10] + "_" + filestarttime + ".png"

    # 把绘制的图形显示到tkinter窗口上
    global mycanvas
    global mybutton
    global mytoolbar

    mycanvas = FigureCanvasTkAgg(fig, master=master)
    mycanvas.draw()
    # toolbar = NavigationToolbar2Tk(canvas, self)
    mycanvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
    mycanvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=1)

    mytoolbar = NavigationToolbar2Tk(mycanvas, master)
    # mytoolbar.update()
    # mycanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    mybutton = Button(master=master, text='Quit', command=sys.exit)
    mybutton = Button(master=master, text='Quit', command=my_destory)
    mybutton.pack(side=TOP)


    # ============       To show the new plot in a pop-up window in the screen:
    # plt.show()  # Note: process pauses here until user clicks on something.
    # ============   end To show the new plot in a pop-up window in the screen.

    # OR do this:

    # ============      To automatically make and save plot in a PNG file ===============
    # Comment out the line plt.show() four lines above, i.e. #plt.show(), and uncomment this next line (remove the #):
    # plt.savefig(filename)
    #   For more arguments to savefig(), see the section "matplotlib.pyplot.savefig(*args, **kwargs)"
    #                                    in http://matplotlib.org/api/pyplot_api.html
    # ============      end to automatically save plot in a PNG file ===============

    # end function makePlot


def teqcplot(argv,master):
    global widthDistance
    global pixeldensity
    widthDistance = 7.3  # for width of plot;  inches is units of distance in matplotlib;
    pixeldensity = 100
    global asciiStartTime
    global maxT
    global minT
    global noprint

    global plottype
    global colorname
    global showLegend
    global showLabel
    global doParmPlot
    global svs
    global svslist
    global parmsvslist
    global options
    global files
    global SVpositionList
    global SVparmList
    global SVidList
    global SVparmidList
    global doShowSVslist
    global doNotShowSVslist

    colorname = ""
    showLegend = False
    showLabel = True
    doParmPlot = False
    svs = []
    svslist = []
    parmsvslist = []
    options = []
    files = []
    SVpositionList = []
    SVparmList = []
    SVidList = []
    SVparmidList = []
    doShowSVslist = []
    doNotShowSVslist = []

    global azifile
    global elefile
    global parmfile
    global parmtype
    global debug
    global dogps
    global doglonass
    global dogalileo
    global dosbas
    global dobeidou
    global doqzss
    global trackCountLimit
    global colorMax
    global colorMin
    global maxHour
    global minHour

    azifile = ""
    elefile = ""
    parmfile = ""
    parmtype = ""
    debug = False
    dogps = True
    doglonass = True
    dogalileo = True
    dosbas = True
    dobeidou = True
    doqzss = True
    trackCountLimit = 6
    colorMax = 1.234567
    colorMin = 1.234567
    maxHour = -999.0
    minHour = -999.0

    # def Main program:
    print("parmtype_start1: {}".format(parmtype))
    argv = argv.strip('\n').split(' ')
    print("wp")
    print(argv)
    global maxT
    global minT
    global asciiStartTime
    global lineSize
    global noprint

    lineSize = 2.5
    noprint = 1  # 1 means do not print debug statements to the screen.
    print(" teqcplot.py 20Jan2019")
    args = argv
    print(len(args))
    print(args)
    lenargs = len(args)
    if lenargs == 1:
        print(helptext)
        sys.exit()
    if lenargs == 2:
        print("\n   Your teqcplot command is missing either a teqcplot command option or an input filename.  ")
        print("   Please read the help:")
        print(helptext)
        sys.exit(1)
    plottype = " "
    for arg in args:
        print(arg)
        if arg == "+skyplot":
            plottype = "Skyplot"
        if arg == "+azelplot":
            plottype = "Azimuth-elevation plot"
        if arg == "+timeelplot":
            plottype = "Time-elevation plot"
        if arg == "+timeparmplot":
            plottype = "Time-parameter plot"
        if arg == "+bandplot":
            plottype = "GNSS_Band_Plot"
        if arg == "-R" and len(arg) == 2:
            doglonass = False
        if arg == "-G" and len(arg) == 2:
            dogps = False
        if arg == "-E" and len(arg) == 2:
            dogalileo = False
        if arg == "-S" and len(arg) == 2:
            dosbas = False
        if arg == "-J" and len(arg) == 2:
            doqzss = False
        if arg == "-C" and len(arg) == 2:
            dobeidou = False
        if arg[0:4] == '+pw=' and len(arg) >= 5:  # set plot width in cm; matplotlib uses inches so / 2.54
            widthDistance = float(arg[4:]) / 2.54
        if arg[0:4] == '+pd=' and len(arg) >= 5:  # set pixel density per cm (matplotlib uses dpi or dots per inch)
            pixeldensity = int(2.54 * int(arg[4:]))
        if arg[0:5] == '+tcl=' and len(arg) >= 6:
            trackCountLimit = int(arg[5:])
        if arg[0:10] == '+colorMax=' and len(arg) >= 11:
            colorMax = float(arg[10:])
        if arg[0:10] == '+colorMin=' and len(arg) >= 11:
            colorMin = float(arg[10:])
        if arg[0:9] == '+minHour=' and len(arg) >= 10:
            minHour = float(arg[9:])
        if arg[0:9] == '+maxHour=' and len(arg) >= 10:
            maxHour = float(arg[9:])
        if arg[0:7] == '+msize=' and len(arg) >= 8:
            lineSize = float(arg[7:])
        if arg[0:7] == '+color=' and len(arg) >= 9:
            colorname = arg[7:]
        if arg == "+legend":
            showLegend = True
        if arg == "-tracklabels":
            showLabel = False
        if arg[0:2] == "+G" and len(arg) > 2:
            liststr = arg[2:]
            if "," in liststr:
                svnumbers = liststr.split(",")
                for svn in svnumbers:
                    doShowSVslist.append("G" + svn)
            elif "-" in liststr:
                numbers = liststr.split("-")
                i1 = int(numbers[0])
                i2 = int(numbers[1])
                for numb in range(i1, (i2 + 1)):
                    svn = "" + numb
                    if len(svn) == 1: svn = "0" + svn
                    doShowSVslist.append("G" + svn)
            else:
                doShowSVslist.append("G" + liststr)
        if arg[0:2] == "+R" and len(arg) > 2:
            liststr = arg[2:]
            if "," in liststr:
                numbers = liststr.split(",")
                for svn in numbers:
                    doShowSVslist.append("R" + svn)
            elif "-" in liststr:
                numbers = liststr.split("-")
                i1 = int(numbers[0])
                i2 = int(numbers[1])
                for svn in range(i1, (i2 + 1)):
                    doShowSVslist.append("R" + svn)
            else:
                doShowSVslist.append("R" + liststr)
        if arg[0:2] == "+J" and len(arg) > 2:
            liststr = arg[2:]
            if "," in liststr:
                numbers = liststr.split(",")
                for svn in numbers:
                    doShowSVslist.append("J" + svn)
            elif "-" in liststr:
                numbers = liststr.split("-")
                i1 = int(numbers[0])
                i2 = int(numbers[1])
                for svn in range(i1, (i2 + 1)):
                    doShowSVslist.append("J" + svn)
            else:
                doShowSVslist.append("J" + liststr)
        print("parmtype: {}".format(parmtype))
        if len(arg) > 5 and arg[-4] == ".":
            files.append(arg)
            if arg[-4:] == ".azi":
                azifile = arg
            if arg[-4:] == ".ele":
                elefile = arg
            if arg[-4:-2] == ".i":
                parmfile = arg
                parmtype = "Ionspheric Delay (m)"
            if arg[-4:-2] == ".d":
                parmfile = arg
                parmtype = "Ionspheric Delay Derivative (m/min)"
            if arg[-4:-1] == ".sn":
                parmfile = arg
                parmtype = "Signal to Noise"
            if arg[-4:-2] == ".m":
                parmfile = arg
                parmtype = "Multipath combination"
            if parmtype != "":
                doParmPlot = True
    if plottype == "GNSS_Band_Plot":
        lineSize *= 10.0
    elif (plottype == "Skyplot" or plottype == "Azimuth-elevation plot") and doParmPlot:
        lineSize *= 2
    elif (plottype == "Time-elevation plot") and doParmPlot:
        lineSize *= 3
    elif (plottype == "Time-parameter plot") and doParmPlot:
        lineSize *= 3

    if noprint != 1: print(
        "  Teqcplot: do " + plottype + " with azimuth and elevation files " + azifile + " and " + elefile)

    read_input_files()

    for tuples in SVpositionList:
        svid = tuples[0]
        if svid not in SVidList:
            SVidList.append(svid)
    SVidList.sort()

    # debug print    "  There are "+`len(SVidList)`+" SVs with plottable data, and " \
    #    +`len(SVpositionList)`+" sets of SV, time, azimuth, and elevation."
    # debug print "  The SVs with data of this parameter are: " + ', '.join(SVidList)

    noplot = ""
    if doglonass != True: noplot += " GLONASS"
    if dogps != True: noplot += " GPS"
    if dogalileo != True: noplot += " Galileo"
    if dosbas != True: noplot += " SBAS"
    if doqzss != True: noplot += " QZSS"
    if dobeidou != True: noplot += " Beidou"
    if "" != noplot: print("  Will not plot SVs from" + noplot)
    if doParmPlot:
        if len(SVparmidList) > 0:
            if noprint != 1: print("  There are " + len(SVparmidList) + " SVs with parm values, and " + len(
                SVparmList) + " sets of SV parm values.")

    makePlot(master)

    # end main


def mydraw(master):
    # 设置图形尺寸与质量
    f = Figure(figsize=(4, 4), dpi=100)
    a = f.add_subplot(111)
    t = arange(0.0, 3, 0.01)
    s = sin(2 * pi * t)
    # 绘制图形
    a.plot(t, s)


    # 把绘制的图形显示到tkinter窗口上
    canvas = FigureCanvasTkAgg(f, master=master)
    canvas.draw()
    # toolbar = NavigationToolbar2Tk(canvas, self)
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)
    canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上

class Application(Tk):

    
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.title('Teqc EasyGUI')


    def create_widgets(self):
        # MENU
        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.subMenu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Open file', command=self.chooseFile)
        self.subMenu.add_separator()
        self.subMenu.add_command(label='File version check', command=self.czyRinex)

        self.aboutMenu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='About', menu=self.aboutMenu)
        self.aboutMenu.add_command(label='About application', command=self.about_program)

        self.helpMenu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='Help', command=self.help)


        # TABS
        self.tab_control = ttk.Notebook(self)
        self.tab_edit = ttk.Frame(self.tab_control)
        self.tab_analyze = ttk.Frame(self.tab_control)
        self.tab_draw = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_edit, text = 'Edit')
        self.tab_control.add(self.tab_analyze, text = 'Analyze')
        self.tab_control.add(self.tab_draw, text = 'Visualize')
        self.tab_control.pack(expand = 1, fill = BOTH, side=TOP)

        # EDIT TOOLBAR
        self.toolbar = Frame(self.tab_edit, bg='#749da8')

        self.e_text_com =[('Convert into RINEX obs file', self.convert),
        ('Convert into RINEX obs and RINEX nav files', self.convert_with_nav),
        ('Merge multiple RINEX files', self.splice_data)]

        for i in self.e_text_com:
            self.e_button = Button(self.toolbar, text=i[0], command=i[1])
            self.e_button.pack(side=LEFT, padx=2, pady=2)


        self.button6 = Button(self.toolbar, text='Clear textbox', command=self.clear)
        self.button6.pack(side=RIGHT, padx=2, pady=2)

        self.toolbar.pack(side=TOP, fill=X)

        # STATUSBAR
        self.statusbar = Label(self, text='Waiting for input...', bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=BOTH)


        # LEFT EDIT FRAME
        self.left_edit_frame = Frame(self.tab_edit)

        # ANTENNA HEIGHT INSERT
        self.left_e_frame1 = Frame(self.left_edit_frame)

        self.ins_time_label = Label(self.left_e_frame1, text='Insert start time [hh:mm:ss]')
        self.ins_time_label.pack(side=LEFT, pady = 10)
        self.ins_time_entry = Entry(self.left_e_frame1)
        self.ins_time_entry.pack(side=LEFT, padx=2)

        self.left_e_frame1.pack()

        self.left_e_frame1 = Frame(self.left_edit_frame)

        self.time_per_label = Label(self.left_e_frame1, text='Insert time period\nin minutes')
        self.time_per_label.pack(side=LEFT)
        self.time_per_entry = Entry(self.left_e_frame1)
        self.time_per_entry.pack(side=LEFT, padx=2)
        self.time_per_button = Button(self.left_e_frame1, text='Insert', command=self.time_windowing)
        self.time_per_button.pack(side=LEFT, padx=2)

        self.left_e_frame1.pack()

        self.left_e_frame1 = Frame(self.left_edit_frame)

        self.interval_label = Label(self.left_e_frame1, text='Interval [s]')
        self.interval_label.pack(side=LEFT, pady = 15)
        self.interval_entry = Entry(self.left_e_frame1)
        self.interval_entry.pack(side=LEFT, padx=2)
        self.interval_button = Button(self.left_e_frame1, text='Insert', command=self.decimate_data)
        self.interval_button.pack(side=LEFT, padx=2)

        self.left_e_frame1.pack()


        self.entry2 = Label(self.left_edit_frame, text='------ RINEX header modify ------')
        self.entry2.pack(side=TOP, pady = 10, padx = 10)

        # RINEX HEADER MODIFICATION
        self.left_e_frame1 = Frame(self.left_edit_frame)

        self.antenna_label = Label(self.left_e_frame1, text='Satellite system')
        self.antenna_label.pack(side=LEFT, pady = 5)
        self.satellite_system_entry = ttk.Combobox(self.left_e_frame1, values=('G (GPS)', 'R (GLONASS)', 'S (SBAS)', 'E (Galileo)', 'C (Beidou)', 'J (QZSS)'), width=17)
        self.satellite_system_entry.pack(side=RIGHT, padx=2)
        self.left_e_frame1.pack(fill=X)

        self.username_entry = StringVar()
        self.observer_entry = StringVar()
        self.agency_entry = StringVar()
        self.monument_entry = StringVar()
        self.monumentnumber_entry = StringVar()
        self.recievernumber_entry = StringVar()
        self.recievertype_entry = StringVar()
        self.software_entry = StringVar()
        self.antennanumber_entry = StringVar()
        self.antennatype_entry = StringVar()

        header_mod_list = [('Username', self.username_entry),
        ('Observer', self.observer_entry),
        ('Agency name', self.agency_entry),
        ('Monument name', self.monument_entry),
        ('Monument number', self.monumentnumber_entry),
        ('Reciever number', self.recievernumber_entry),
        ('Reciever type', self.recievertype_entry),
        ('Software version', self.software_entry),
        ('Antenna number', self.antennanumber_entry),
        ('Antenna type', self.antennatype_entry)]

        for i in header_mod_list:

            self.left_e_frame1 = Frame(self.left_edit_frame)
            self.left_frame_label = Label(self.left_e_frame1, text=i[0])
            self.left_frame_label.pack(side=LEFT, pady = 5)
            self.left_frame_entry = Entry(self.left_e_frame1, textvariable=i[1])
            self.left_frame_entry.pack(side=RIGHT, padx=2)
            self.left_e_frame1.pack(fill=X)

        self.left_e_frame1 = Frame(self.left_edit_frame)
        self_antenna_label = Label(self.left_e_frame1, text='Approximate position X/Y/Z')
        self_antenna_label.pack(side=LEFT, pady = 5)
        self.appposx_entry = Entry(self.left_e_frame1, width=10)
        self.appposx_entry.pack(side=RIGHT, padx=2)
        self.appposy_entry = Entry(self.left_e_frame1, width=10)
        self.appposy_entry.pack(side=RIGHT, padx=2)
        self.appposz_entry = Entry(self.left_e_frame1, width=10)
        self.appposz_entry.pack(side=RIGHT, padx=2)
        self.left_e_frame1.pack(fill=X)

        self.left_e_frame1 = Frame(self.left_edit_frame)
        self_antenna_label = Label(self.left_e_frame1, text='Antenna delta H/E/N')
        self_antenna_label.pack(side=LEFT, pady = 5)
        self.antennadh_entry = Entry(self.left_e_frame1, width=10)
        self.antennadh_entry.pack(side=RIGHT, padx=2)
        self.antennade_entry = Entry(self.left_e_frame1, width=10)
        self.antennade_entry.pack(side=RIGHT, padx=2)
        self.antennadn_entry = Entry(self.left_e_frame1, width=10)
        self.antennadn_entry.pack(side=RIGHT, padx=2)
        self.left_e_frame1.pack(fill=X)

        self.left_e_frame1 = Frame(self.left_edit_frame)
        self_comment_label = Label(self.left_e_frame1, text='Add comment')
        self_comment_label.pack(side=LEFT, pady = 5)
        self.comment_entry = Entry(self.left_e_frame1, width=40)
        self.comment_entry.pack(side=RIGHT, padx=2)
        self.left_e_frame1.pack(fill=X)

        self.left_e_frame1 = Frame(self.left_edit_frame)
        self_antenna_button = Button(self.left_e_frame1, text='Modify', command=self.rinex_header_modify)
        self_antenna_button.pack(pady = 5, fill=X)
        self.left_e_frame1.pack(fill=X)



        self.left_edit_frame.pack(side=LEFT, fill=BOTH, expand=1)


        # ANALYZE TOOLBAR
        self.analyze_toolbar = Frame(self.tab_analyze, bg='#c5e0dc')

        self.a_text_com =[('Show metadata', self.show_metadata),
        ('Format check', self.format_check),
        ('Quality check', self.qC),
        ('Summary', self.ile)]

        for i in self.a_text_com:
            self.a_button = Button(self.analyze_toolbar, text=i[0], command=i[1])
            self.a_button.pack(side=LEFT, padx=2, pady=2)

        self.a_button = Button(self.analyze_toolbar, text='Clear textbox', command=self.a_clear)
        self.a_button.pack(side=RIGHT, padx=2, pady=2)

        self.analyze_toolbar.pack(side=TOP, fill=X)

        # LEFT ANALYZE FRAME
        self.left_analyze_frame = Frame(self.tab_analyze)
        self.a_label1 = Label(self.left_analyze_frame, text ='Choose satellite systems to analyze', pady=10)
        self.a_label1.pack()

        self.gps_check = IntVar()
        self.glonass_check = IntVar()
        self.sbas_check = IntVar()
        self.galileo_check = IntVar()
        self.beidou_check = IntVar()
        self.qzss_check = IntVar()

        self.left_checkframe = Frame(self.left_analyze_frame)

        self.checklist = [('GPS', self.gps_check),
        ('GLONASS', self.glonass_check),
        ('SBAS', self.sbas_check),
        ('Galileo', self.galileo_check),
        ('Beidou', self.beidou_check),
        ('QZSS', self.qzss_check)]

        for i in self.checklist:
            self.checkbutton = Checkbutton(self.left_checkframe, text=i[0], variable=i[1])
            self.checkbutton.select()
            self.checkbutton.pack(side=LEFT, padx=2, pady=2)
        self.left_checkframe.pack()

        self.left_analyze_frame.pack(side=LEFT, fill=BOTH, expand=1)


        # DRAW

        # LEFT DRAW FRAME
        self.left_draw_frame = Frame(self.tab_draw)

        self.left_d_frame1 = Frame(self.left_draw_frame)
        self.svn_label = Label(self.left_d_frame1, text='Insert maximum number of SVs to visualize')
        self.svn_label.pack(side=LEFT, pady = 10)
        self.svn_entry = Entry(self.left_d_frame1)
        self.svn_entry.pack(side=LEFT, padx=2)
        self.left_d_frame1.pack()

        self.left_d_frame1 = Frame(self.left_draw_frame)
        self.file_label = Label(self.left_d_frame1, text='Choose file for additional visualisation')
        self.file_label.pack(side=LEFT)
        self.file_entry = Button(self.left_d_frame1, text='Choose', command=self.load_drawfile)
        self.file_entry.pack(side=RIGHT, padx=2)
        self.left_d_frame1.pack(pady=30)

        self.left_d_frame1 = Frame(self.left_draw_frame)
        self.skyplot_button = Button(self.left_d_frame1, text='Draw skyplot', command=self.draw_skyplot)
        self.skyplot_button.pack(side=LEFT, expand=1, fill=BOTH)
        self.aziele_button = Button(self.left_d_frame1, text='Draw azimuth-elevation plot', command=self.draw_azelplot)
        self.aziele_button.pack(side=LEFT, expand=1, fill=BOTH)
        self.left_d_frame1.pack(fill=X)

        self.left_d_frame1 = Frame(self.left_draw_frame)
        self.bandplot_button = Button(self.left_d_frame1, text='Draw bandplot', command=self.draw_bandplot)
        self.bandplot_button.pack(side=LEFT, expand=1, fill=BOTH)
        self.timeelplot_button = Button(self.left_d_frame1, text='Draw time-elevation plot', command=self.draw_timeelplot)
        self.timeelplot_button.pack(side=LEFT, expand=1, fill=BOTH)
        self.left_d_frame1.pack(fill=X)

        self.display_map_button = Button(self.left_draw_frame, text='Display position on map', command=self.map_display)
        self.display_map_button.pack(side=TOP, pady=30, fill=X)

        self.left_draw_frame.pack(side=LEFT, fill=BOTH, expand=1)


        #EDIT SCROLLED TEXT
        self.scrltxt = scrolledtext.ScrolledText(self.tab_edit, width = 100, height = 40, wrap=WORD, bg='beige')
        self.scrltxt.pack(side=RIGHT)

        #ANALYZE SCROLLED TEXT
        self.scrltxt2 = scrolledtext.ScrolledText(self.tab_analyze, width = 100, height = 40, wrap=WORD)
        self.scrltxt2.pack(side=RIGHT)


        self.scrltxt3 = scrolledtext.ScrolledText(self.tab_draw, width=100, height=60, wrap=WORD)
        self.scrltxt3.pack(side=RIGHT, anchor=SE)




    def show_metadata(self):
        try:
            print("wp")
            a = subprocess.run('teqc +meta ' + self.filename, capture_output=True, encoding='utf-8')
            self.scrltxt2.insert(INSERT, a.stdout)
        except AttributeError:
            self.attribute_error()
        
    def clear(self):
        self.scrltxt.delete(1.0, END)
    
    def a_clear(self):
        self.scrltxt2.delete(1.0, END)
        
    def d_clear(self):
        self.scrltxt3.delete(1.0, END)
        
    def qC(self):
        try:
            com_list = []
            var_list = [('-G ', self.gps_check.get()),
            ('-R ', self.glonass_check.get()),
            ('-S ', self.sbas_check.get()),
            ('-E ', self.galileo_check.get()),
            ('-C ', self.beidou_check.get()),
            ('-J ', self.qzss_check.get())]
            
            for i in var_list:
                if not i[1]:
                    com_list.append(i[0])
            qc = subprocess.run('teqc +qc +plot ' + ' '.join(com_list) + self.filename, capture_output=True, encoding='utf-8')
            self.scrltxt2.insert(INSERT, qc.stdout)
        except AttributeError:
            self.attribute_error()
            
    def qc_full(self):
        try:
            obs_file = self.filename
            nav_file = self.chooseFile()
            com_list = []
            var_list = [('-G ', self.gps_check.get()),
            ('-R ', self.glonass_check.get()),
            ('-S ', self.sbas_check.get()),
            ('-E ', self.galileo_check.get()),
            ('-C ', self.beidou_check.get()),
            ('-J ', self.qzss_check.get())]
            
            for i in var_list:
                if not i[1]:
                    com_list.append(i[0])
                    
            qc_f = subprocess.run('teqc +qc +plot -nav ' + ' '.join(com_list) + nav_file + ' ' + obs_file, capture_output=True, encoding='utf-8')
            self.scrltxt2.insert(INSERT, qc_f.stderr)
            self.scrltxt2.insert(INSERT, qc_f.stdout)
        except AttributeError:
            self.attribute_error()
            
    def czyRinex(self):
        try:
            b = subprocess.run('teqc +v ' + self.filename, capture_output=True, encoding='utf-8')
            self.scrltxt.insert(INSERT, b.stderr)
        except AttributeError:
            self.attribute_error()
        
    def attribute_error(self):
        print('wykryto błąd!')
        tkinter.messagebox.showerror('Warning', 'Please open file first')
        
    def chooseFile(self):
        self.filename = askopenfilename()
        self.filename = self.filename.replace('/', '\\')
        print(self.filename)
        check = subprocess.run('teqc ' + self.filename, capture_output=True, encoding='utf-8')
        while check.stdout == '':
            if self.filename == '':
                break
            else:
                self.scrltxt.insert(INSERT, check.stderr)
                tkinter.messagebox.showerror('Warning', 'File not selected or selected in incorrect format')
                self.filename = askopenfilename()
                check = subprocess.run('teqc ' + self.filename, capture_output=True, encoding='utf-8')
        if self.filename != '':
            self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
            
        print(self.filename)
        return(self.filename)
        
    def convert(self):
        try:
            self.saved_filename = asksaveasfilename()
            print('teqc ' + self.filename + ' > ' + self.saved_filename)
            conv = subprocess.run('teqc ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
            print(conv.stderr)
            self.scrltxt.insert(INSERT, conv.stdout)
            self.scrltxt.insert(INSERT, 'Conversion ended with success.\n')
            self.filename = self.saved_filename
            self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
        except AttributeError:
            self.attribute_error()
        except FileNotFoundError:
            self.attribute_error()
            
    def convert_with_nav(self):
        try:
            input_file = self.filename
            obs_file = asksaveasfilename(title = "Select observation file name")
            nav_file = asksaveasfilename(title = "Select navigation file name")
            subprocess.run('teqc +nav ' + nav_file + ' ' + input_file + ' > ' + obs_file, capture_output=True, encoding='utf-8', shell = True)
            self.scrltxt.insert(INSERT, 'Conversion ended with success.\n')
            self.filename = obs_file
            self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
        except AttributeError:
            self.attribute_error()
        
    def format_check(self):
        try:
            format_check = subprocess.run('teqc +mdf ' + self.filename, capture_output=True, encoding='utf-8')
            self.scrltxt2.insert(INSERT, format_check.stdout)
            print(format_check.stdout.split()[-1])
        except AttributeError:
            self.attribute_error()
        except UnboundLocalError:
            self.attribute_error()
        return(format_check.stdout)
            
    def about_program(self):
        tkinter.messagebox.showinfo('About', 'An application for satellite data edit and analyze based on existing open-source application teqc and plotting script teqcplot.py.\nDeveloped by Maciej Miliszewski\nWarsaw University of Technology\nPoland')
    
    def help(self):
        tkinter.messagebox.showinfo('Help', 'For help with usage of application please check file README.md in source folder')
    
    def rinex_header_modify(self):
        try:
            self.saved_filename = asksaveasfilename()
            com_list = []
            sat_list = {'-G', '-R', '-E', '-C', '-S', '-J'}
            var_list = [('-O.s ', self.satellite_system_entry.get()),
            ('-O.r ', self.username_entry.get()),
            ('-O.o ', self.observer_entry.get()),
            ('-O.ag ', self.agency_entry.get()),
            ('-O.mo ', self.monument_entry.get()),
            ('-O.mn ', self.monumentnumber_entry.get()),
            ('-O.rn ', self.recievernumber_entry.get()),
            ('-O.rt ', self.recievertype_entry.get()),
            ('-O.rv ', self.software_entry.get()),
            ('-O.an ', self.antennanumber_entry.get()),
            ('-O.at ', self.antennatype_entry.get()),
            ('-O.px[WGS84xyz,m] ', self.appposx_entry.get(), self.appposy_entry.get(), self.appposz_entry.get()),
            ('-O.pe[hEN,m] ', self.antennadh_entry.get(), self.antennade_entry.get(), self.antennadn_entry.get()),
            ('-O.c ', self.comment_entry.get())]
            
            if not self.filename:
                raise AttributeError
                
            for i in var_list:
                if i[1]:
                    if i[0] == '-O.s ':
                        com_list.append(i[0] + '"{}"'.format(i[1]))
                        sat_list.remove('-' + i[1].split()[0])
                        com_list.append(' '.join(sat_list))
                    elif i[0] == '-O.px[WGS84xyz,m] ' or i[0] == '-O.pe[hEN,m] ':
                        com_list.append(i[0] + ' '.join(i[1:4]))
                    else:
                        com_list.append(i[0] + '"{}"'.format(i[1]))

            subprocess.run('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
            print('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename)
            self.scrltxt.insert(INSERT, 'Header modification ended with success.\n')
        except AttributeError:
            self.attribute_error()
    
    def compare(self):
        try:
            file1 = self.filename
            file2 = self.chooseFile()
            compare_variable = subprocess.run('diff ' + file1 + ' ' + file2, capture_output=True, encoding='utf-8', shell = True)
            self.scrltxt2.insert(INSERT, compare_variable.stderr)
            self.scrltxt2.insert(INSERT, compare_variable.stdout)
        except AttributeError:
            self.attribute_error()
        
    def decimate_data(self):
        try:
            if len(self.interval_entry.get()) > 0 and type(int(self.interval_entry.get())): 
                self.saved_filename = asksaveasfilename()
                subprocess.run('teqc -O.dec ' + str(int(self.interval_entry.get())) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
                self.scrltxt.insert(INSERT, 'Decimation ended with success.\n')
        except AttributeError:
            self.attribute_error()
        except ValueError:
            self.scrltxt.insert(INSERT, 'Cannot decimate data. Inserted value has to be an integer number.\n')
        
    def time_windowing(self):
        try:
            self.saved_filename = asksaveasfilename()
            com_list = []
            var_list = [('-st ', self.ins_time_entry.get()),
            ('-dm ', self.time_per_entry.get())]
            
            if not self.filename:
                raise AttributeError
                
            for i in var_list:
                if i[1]:
                    com_list.append(i[0] + i[1])

            subprocess.run('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
            self.scrltxt.insert(INSERT, 'Time windowing ended with success.\n')
        except AttributeError:
            self.attribute_error()
        except ValueError:
            self.scrltxt.insert(INSERT, 'Cannot decimate data. Inserted value has to be an integer number.\n')
        
        
    def splice_data(self):
        try:
            filename_list = [self.filename]
            while(len(self.filename) > 0):
                self.filename = askopenfilename()
                filename_list.append(self.filename)
            self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' opened successfully'
            tkinter.messagebox.showinfo('', 'Choose output filename now.')
            saved = asksaveasfilename()
            subprocess.run('teqc ' + ' '.join(filename_list) + ' > ' + saved, encoding='utf-8', shell=True)
            self.scrltxt.insert(INSERT, 'Splicing ended with success.\n')
        except AttributeError:
            self.attribute_error()

    def ile(self):
        try:
            com_list = []
            var_list = [('-G ', self.gps_check.get()),
            ('-R ', self.glonass_check.get()),
            ('-S ', self.sbas_check.get()),
            ('-E ', self.galileo_check.get()),
            ('-C ', self.beidou_check.get()),
            ('-J ', self.qzss_check.get())]
            
            for i in var_list:
                if not i[1]:
                    com_list.append(i[0])
                    
            ile = subprocess.run('teqc -O.sum . ' + ' '.join(com_list) + self.filename, encoding='utf-8', capture_output = True, shell=True)
            self.scrltxt2.insert(INSERT, ile.stdout)
        except AttributeError:
            self.attribute_error()

    def map_display(self):
        try:
            file = self.filename[:-1] + 'S'
            map_var = 0
            for i in fileinput.input(files = file):
                if 'antenna WGS 84 (geo)  :  ' in i and float(i.split()[7]) < 180:
                    webbrowser.open('http://www.google.com/maps/place/{},{}'.format(i.split()[5], i.split()[7]))
                    map_var = 1
                elif 'antenna WGS 84 (geo)  :  ' in i and float(i.split()[7]) > 180:
                    webbrowser.open('http://www.google.com/maps/place/{},{}'.format(i.split()[5], i.split()[10]))
                    map_var = 1
            if not map_var:
                self.scrltxt3.insert(INSERT, 'Cannot display map, unable to find coordinates in quality check report file.\n')
        except FileNotFoundError:
            self.scrltxt3.insert(INSERT, 'Cannot display map, unable to find quality check report file.\n')
        except AttributeError:
            self.attribute_error()
            
    def load_drawfile(self):
        self.drawfile = askopenfilename()

    global mycanvas
    global mybutton
    global mytoolbar
    def draw_skyplot(self):
        try:
            elevation_file = self.filename[:-3] + 'ele'
            azimuth_file = self.filename[:-3] + 'azi'
            print(self.svn_entry.get())
            if int(self.svn_entry.get()):
                # DRAW SCROLLED TEXT
                # self.scrltxt3.destroy()
                # self.scrltxt3 = scrolledtext.ScrolledText(self.tab_draw, width=100, height=60, wrap=WORD)
                # self.scrltxt3.pack(side=RIGHT, anchor=SE)

                print("hello")
                try:
                    mycanvas.get_tk_widget().destroy();
                    mybutton.destroy()
                    mytoolbar.destroy()
                except:
                    pass

                teqcplot("teqcplot.py +skyplot +tcl="+ self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile,self.scrltxt3)
                # draw = subprocess.run('python teqcplot.py +skyplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
                # self.scrltxt3.insert(INSERT, draw.stdout)
        except FileNotFoundError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
        except ValueError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
        except AttributeError:
            self.attribute_error()

    def draw_bandplot(self):
        try:
            elevation_file = self.filename[:-3] + 'ele'
            azimuth_file = self.filename[:-3] + 'azi'
            print(self.svn_entry.get())
            if int(self.svn_entry.get()):
                try:
                    mycanvas.get_tk_widget().destroy();
                    mybutton.destroy()
                    mytoolbar.destroy()
                except:
                    pass
                # print('python teqcplot.py +bandplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile)

                teqcplot('teqcplot.py +bandplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile,self.scrltxt3)
                # draw = subprocess.run('python teqcplot.py +bandplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
                # self.scrltxt3.insert(INSERT, draw.stdout)
        except FileNotFoundError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
        except ValueError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
        except AttributeError:
            self.attribute_error()

    def draw_azelplot(self):
        try:
            elevation_file = self.filename[:-3] + 'ele'
            azimuth_file = self.filename[:-3] + 'azi'
            print(self.svn_entry.get())
            if int(self.svn_entry.get()):
                try:
                    mycanvas.get_tk_widget().destroy();
                    mybutton.destroy()
                    mytoolbar.destroy()
                except:
                    pass
                # self.scrltxt3.destroy();
                teqcplot('teqcplot.py +azelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile,self.scrltxt3)
                # draw = subprocess.run('python teqcplot.py +azelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
                # self.scrltxt3.insert(INSERT, draw.stdout)
        except FileNotFoundError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
        except ValueError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
        except AttributeError:
            self.attribute_error()
        
    def draw_timeelplot(self):
        try:
            elevation_file = self.filename[:-3] + 'ele'
            azimuth_file = self.filename[:-3] + 'azi'
            print(self.svn_entry.get())
            if int(self.svn_entry.get()):
                try:
                    mycanvas.get_tk_widget().destroy();
                    mybutton.destroy()
                    mytoolbar.destroy()
                except:
                    pass
                teqcplot('teqcplot.py +timeelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile,self.scrltxt3)
                # draw = subprocess.run('python teqcplot.py +timeelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
                # self.scrltxt3.insert(INSERT, draw.stdout)
        except FileNotFoundError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
        except ValueError:
            self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
        except AttributeError:
            self.attribute_error()
        
    
if __name__ == "__main__":        
    print('Starting...')        
    app = Application()
    app.mainloop()
    print('Done!')