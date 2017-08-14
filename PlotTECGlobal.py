#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Using PEP 8 -- Style Guide for Python Code
# https://www.python.org/dev/peps/pep-0008/
# Main dev.: Guilherme Hollweg - Electrical Engineer
# Last Modified on 25/07/2017

from __future__ import unicode_literals

import os, os.path, sys
import datetime, time
import struct
import numpy as np
import cartopy
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import math
import gmplot

'''
####             Developed for National Institute for Space Research   		 ####"
####                            by Guilherme Hollweg                         ####"
####                             v1.0       08/2017
'''

print "\n                       TEC-MAP Builder                    \n \
       \r                  Generate TEC MAP for Globe              \n \
       \r    Developed for National Institute for Space Research   \n \
       \r                    by Guilherme Hollweg                  \n \
       \r                      v1.0     08/2017                    \n \n"


dataFile = ''
descriptors = list()

# Additional variables to read data file
size = 1

# Lists to store file data
# coords - initial coordinates on file ; latCoord, lonCoord, and altCoord - All Coordinates present on file ;
# neighVal - nearest coordinate values (user input - file present)
coords = []
latCoord = []
lonCoord = []
altCoord = []
neighVal = []
matrixLon = []
matrixLat = []
matrixTec = []

# dir ---> path of all desc. files
dir = '.'

# lsVar - Variables present on file (ex.: TIMEDIFF, TEC, NE) ;
# vars - number of Variables present on file ;
lsVar = []
vars = 0
count = 0
gridSize = 0


# Function to read all files into desired folder and put all 'descriptors' into a list
def read_files():
    global descriptors
    filesonFolder = next(os.walk(dir))[2]
    for name in filesonFolder:
        if 'descriptor' in name and name[-1] == 'h':
            descriptors.append(name)
    descriptors.sort()


# Function to format numbers according to IONEX format (ex.: '09' instead of '9')
def check_for_zero(num):
    if int(num) < 10:
        num = '0%s' %(num)
    return num


# Function to calculate grid size
def calc_grid(lon, lat, alt):
    return lon*lat*alt


# Function to join data from coordinates list values
def join_coordinates(coordList):
    coordList = filter(lambda a: a != '\n', coordList)
    coordList = ''.join(coordList).split(' ')
    return coordList


# Function to read file for important data and acquire LON/LAT/ALT values, levels and
# Estimate the data block on dat file containing all the important data
def opt_scavenge_file(descfile):
    global readValue, coords, latCoord, lonCoord, altCoord, size, count, gridSize, vars, lsVar, dataFile, dir
    count = 0
    xdef, ydef, zdef = 0, 0, 0
    coordVals = []
    countCoord = 0
    inputFile = open(descfile, 'rb')
    countLines = 0
    dataFile = ''
    character = ''

    for line in inputFile:
        if xdef == 1:
            if 'ydef' in line:
                lonCoord = coordVals[:]
                coordVals = []
            else:
                for i in range(0, len(line)):
                    coordVals.append(line[i])
        elif ydef == 1:
            if 'zdef' in line:
                latCoord = coordVals[:]
                coordVals = []
            else:
                for i in range(0, len(line)):
                    coordVals.append(line[i])
        elif zdef == 1:
            if 'tdef' in line:
                altCoord = coordVals[:]
                coordVals = []
            else:
                for i in range(0, len(line)):
                    coordVals.append(line[i])

        if 'dset' in line:
            for i in range(6, len(line)):
                dataFile = dataFile + line[i]

        elif 'xdef' in line:
            coords.append(line[5] + line[6] + line[7])
            for i in range(15, len(line)):
                coordVals.append(line[i])
            xdef = 1

        elif 'ydef' in line:
            coords.append(line[5] + line[6] + line[7])
            for i in range(15, len(line)):
                coordVals.append(line[i])
            xdef = 0
            ydef = 1

        elif 'zdef' in line:
            coords.append(line[5] + line[6] + line[7])
            for i in range(15, len(line)):
                coordVals.append(line[i])
            ydef = 0
            zdef = 1

        elif 'tdef' in line:
            zdef = 0

    dataFile = dataFile.strip()
    lonCoord = join_coordinates(lonCoord)
    latCoord = join_coordinates(latCoord)
    altCoord = join_coordinates(altCoord)

    # Calculates gridsize
    gridSize = calc_grid(int(coords[0]), int(coords[1]), int(coords[2]))

    inputFile.close()
    return dataFile


# Calcs the equation for the desired data position on .dat file
def calc_pos_ne(lon, lat, alt, posVar, posLon, posLat, posAlt):
    return ((lon*lat*alt)*posVar + (lon*lat)*posAlt + lon*posLat + posLon)*4


# Function to acquire all TEC values for lat and lons on descriptor file
# Altitude is not needed because TEC is equal on altitude values
def find_tec_values(posVar):
    global lonCoord, latCoord, coords, matrixLon, matrixLat, matrixTec

    matrixLon = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]
    matrixLat = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]
    matrixTec = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]

    binFile = open(dir + dataFile, 'rb')

    for i in range(0, int(coords[0])):              # Longitude  ---- 361 iterations
        for j in range(0, int(coords[1])):          # Latitude   ---- 121 iterations
            funVal = calc_pos_ne(int(coords[0]),
                                 int(coords[1]),
                                 int(coords[2]),
                                 int(posVar),
                                 i,
                                 j,
                                 0
                                 )
            binFile.read(funVal)
            finalVal = struct.unpack('f', binFile.read(4))
            finalVal = str(finalVal).replace(",", "").replace("(", "").replace(")", "")

            # Build de map to perform the contourn plot on the future
            # 86x66 LAT/LON
            matrixLon[j][i] = lonCoord[i]
            matrixLat[j][i] = latCoord[j]
            matrixTec[j][i] = float(finalVal)

            binFile.seek(0)
    binFile.close()


# Plotting TEC using Cartopy
def plot_tec_cartopy(descfile):
    global matrixLon, matrixLat, matrixTec

    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    
    v = np.linspace(0, 80, 46, endpoint=True)
    cp = plt.contourf(matrixLon, matrixLat, matrixTec, v, cmap=plt.cm.rainbow)

    plt.clim(0, 80)
    plt.colorbar(cp)

    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.set_extent([-180, 180, -90, 90])
    
    # Setting X and Y labels using LON/LAT format
    ax.set_xticks([-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])
    ax.set_yticks([-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90])
    lon_formatter = LongitudeFormatter(number_format='.0f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.0f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    plt.title('Conteúdo Eletrônico Total', style='normal', fontsize='13')
 
    # Acquiring Date
    year, julianday = check_for_zero(descfile.split('.')[2]), descfile.split('.')[3]
    hour, minute = descfile.split('.')[4], descfile.split('.')[5].replace('h','')
    date = datetime.datetime(int(year), 1, 1, int(hour), int(minute)) + datetime.timedelta(int(julianday)-1)
    month = date.month
    day = date.day
    
    # Set common labels
    ax.text(1.09, 1.231, 'TEC', style='normal',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=11)
    ax.text(1, 0.005, 'EMBRACE/INPE', style='italic',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=11)
    ax.text(1, 0.995, str(date) + ' UT', style='italic',
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes,
        color='black', fontsize=11)
    ax.text(0.5, -0.1, 'Copyright \N{COPYRIGHT SIGN} 2017 INPE - Instituto Nacional de',
        style='oblique', transform=ax.transAxes,
        verticalalignment='bottom', horizontalalignment='center',
        color='black', fontsize=10)
    ax.text(0.5, -0.128, 'Pesquisas Espacias. Todos direitos reservados',
        style='oblique', transform=ax.transAxes,
        verticalalignment='bottom', horizontalalignment='center',
        color='black', fontsize=10)
    figName = 'tec.map' + '.' + str(year) + '.' + str(julianday) + '.' + str(hour) + '.' + str(minute) + 'h.png' 

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.savefig(figName, dpi = 300)

    plt.show()
    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    plt.savefig(figName, dpi=1000)
    plt.clf()




# Function to read descriptor file, acquire all important information, calculates the position to find
# the desired data and save all things on an output file named GradsOut.txt
def scavenge_output_map():
    global coords, descriptors

    read_files()
    for i in range(0, len(descriptors)):
        descfile = str(descriptors[i])
        print 'Generating TEC MAP for file %s...' %(descfile)
        opt_scavenge_file(descfile)
        funVal = calc_pos_ne(int(coords[0]),
                            int(coords[1]),
                            int(coords[2]),
                            int(2),
                            0,
                            0,
                            0
                            )
        find_tec_values(2)
        plot_tec_cartopy(descfile)
        print 'Done. \n'


# receiving terminal parameters
dir = str(sys.argv[1])

'''Call this function to insert values, calculate (NE, TEC, TIMEDIFF), generate a file containing all gathered data    \
   and printing a TEC MAP of the corresponding file '''
scavenge_output_map()





