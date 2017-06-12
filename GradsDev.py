#!/usr/bin/env python

# Using PEP 8 -- Style Guide for Python Code
# https://www.python.org/dev/peps/pep-0008/
# Main dev.: Guilherme Hollweg - Electrical Engineer
# Last Modified on 18/04/2017

import struct
import numpy as np
import matplotlib.pyplot as plt
import math

'''
####             Developed for National Institute for Space Research   		 ####"
####                    by Guilherme Hollweg and Felipe Maia                 ####"
####                             v1.0       04/2017
'''

print "\n                  Grads TEC Manipulator                   \n \
       \r    Developed for National Institute for Space Research   \n \
       \r          by Guilherme Hollweg and Felipe Maia v0.1       \n \
       \r                    v1.0     04/2017                         "

# Open file and writes the header
inputFile = open('descriptor.ctl.2017.90.0.0h', 'rb')
outputFile = open('GradsOut.txt', 'w+b')
outputFile.write("\n                  Grads TEC Manipulator                   \n \
                  \r    Developed for National Institute for Space Research   \n \
                  \r           by Guilherme Hollweg and Felipe Maia v0.1      \n \
                  \r                  v1.0        04/2017                     \n \n \n")
dataFile = ''

# Additional variables to read data file
size = 1
readVal = inputFile.read(size)

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

# lsVar - Variables present on file (ex.: TIMEDIFF, TEC, NE) ;
# vars - number of Variables present on file ; posCoord - VarPosition of LON,LAT,ALT to calc the equation
lsVar = []
vars = 0
posCoord  = []
count = 0
gridSize = 0


# Function to calculate grid size
def calc_grid(lon, lat, alt):
    return lon*lat*alt


# Function to search for user LON/LAT/ALT similar values into file
def calc_neighbors(value, coordList):
    res = 10000000
    desired = 0
    count = -1
    # Check for equal value
    for i in range(0, len(coordList)):
        if value == float(coordList[i]):
            posCoord.append(i)
            return coordList[i]

    # if same value was not found, try for the first next value
    for i in range(0, len(coordList)):
        if res > abs((float(value) - float(coordList[i]))):
            res = (float(value) - float(coordList[i]))
            desired = float(coordList[i])
            count += 1
    posCoord.append(count)
    print posCoord
    return desired


# Function to join data from coordinates list values
def join_coordinates(coordList):
    coordList = filter(lambda a: a != '\n', coordList)
    coordList = ''.join(coordList).split(' ')
    return coordList


# Function to read file for important data and acquire LON/LAT/ALT values, levels and
# Estimate the data block on dat file containing all the important data
def opt_scavenge_file():
    global readValue, coords, latCoord, lonCoord, altCoord, size, count, gridSize, vars, lsVar, dataFile
    count = 0
    coordVals = []
    countCoord = 0
    inputFile = open('descriptor.ctl.2017.90.0.0h', 'rb')
    countLines = 0
    dataFile = ''
    character = ''

    for line in inputFile:
        if 'dset' in line:
            for i in range(6, len(line)):
                dataFile = dataFile + line[i]
        elif 'xdef' in line or 'ydef' in line or 'zdef' in line:
            coords.append(line[5] + line[6])
            for i in range(15, len(line)):
                coordVals.append(line[i])
            countLines = 0
            countCoord += 1

        elif countCoord == 1 and countLines < 4:
            if countLines == 0:
                lonCoord = coordVals[:]
            for i in range(0, len(line)):
                lonCoord.append(line[i])
            countLines += 1
            coordVals = []

        elif countCoord == 2 and countLines < 6:
            if countLines == 0:
                latCoord = coordVals[:]
            for i in range(0, len(line)):
                latCoord.append(line[i])
            countLines += 1
            coordVals = []

        elif countCoord == 3 and countLines < 6:
            if countLines == 0:
                altCoord = coordVals[:]
            for i in range(0, len(line)):
                altCoord.append(line[i])
            countLines += 1
            coordVals = []

        elif 'Vars' in line:
            vars = line[5]

        elif vars != 0 and int(vars) > count:
            for char in line:
                character = character + char
                if char == ' ':
                    break
            character = character.strip()
            lsVar.append(character)
            count += 1
        character = ''

    dataFile = dataFile.strip()
    lonCoord = join_coordinates(lonCoord)
    latCoord = join_coordinates(latCoord)
    altCoord = join_coordinates(altCoord)

    outputFile.write('The corresponding DATA file name is: ')
    outputFile.write('%s' % dataFile)
    outputFile.write('\nThe file coordinate levels are (LON LAT ALT): ')

    # Calculates gridsize
    gridSize = calc_grid(int(coords[0]), int(coords[1]), int(coords[2]))
    outputFile.write('\nThe corresponding Grid size is ')
    outputFile.write('%s.' % gridSize)

    inputFile.close()
    return dataFile


# Function to compare the Variable in observation (NE, TEC, TIMEDIFF)
# from user input with Vars available on the file
def comp_var():
    global lsVar, neighVal
    posVar = []
    outputFile = open('GradsOut.txt', 'a')
    for i in range(0, len(lsVar)):
        if str(lsVar[i]) == str(neighVal[3]):
            outputFile.write('\nThe desired data is present on .dat file. ')
            posVar.append(lsVar[i])
            posVar.append(i)
    outputFile.close()
    return posVar


# Function to print LON/LAT/ALT file values
def print_coordinates():
    print '\n\nThe file Coordinates (LON, LAT, ALT) are: %s' % coords
    print 'The Longitude data are: %s' % lonCoord
    print 'The Latitude data are: %s' % latCoord
    print 'The Altitude data are: %s' % altCoord


# Function to user insert parameters and calculates neighbors
def user_data():
    global neighVal
    userVal = []

    print '\n\nInsert the corresponding values: \n'
    userLon = float(raw_input('Type the Longitude: '))
    userLat = float(raw_input('Type the Latitude: '))
    userAlt = float(raw_input('Type the Altitude: '))
    userVar = raw_input('Type the Desired Variable to look for: ').upper()

    userVal.append(userLon)
    userVal.append(userLat)
    userVal.append(userAlt)

    neighVal.append(calc_neighbors(userLon, lonCoord))
    neighVal.append(calc_neighbors(userLat, latCoord))
    neighVal.append(calc_neighbors(userAlt, altCoord))
    neighVal.append(userVar)

    outputFile.write('\n\nLongitude data on the file: \n')
    outputFile.write('%s' % lonCoord)
    outputFile.write('\n\nLatitude data on the file: \n')
    outputFile.write('%s' % latCoord)
    outputFile.write('\n\nAltitude data on the file: \n')
    outputFile.write('%s' % altCoord)
    outputFile.write('\n\nThe user input coordinates are ')
    outputFile.write('%s.' % userVal)
    outputFile.write('\nThe closest coordinates on .dat file are ')
    outputFile.write('%s.' % neighVal)
    outputFile.write('\nThe user desired observed data is ')
    outputFile.write('%s.' % userVar)
    outputFile.close()


def find_binary_value_ionex(funVal):
    global dataFile
    binFile = open(dataFile, 'rb')

    binFile.read(funVal)
    finalVal = struct.unpack('f', binFile.read(4))
    return finalVal
    binFile.close()


# Calcs the equation for the desired data position on .dat file
def calc_pos_ne(lon, lat, alt, posVar, posLon, posLat, posAlt):
    return ((lon*lat*alt)*posVar + (lon*lat)*posAlt + lon*posLat + posLon)*4


# Open the binary value and find the desired value according with user input,
# calculating the size that needs to be jumped and acquiring the immediate next value
def find_binary_value(funVal, var):
    binFile = open(dataFile, 'rb')
    outputFile = open('GradsOut.txt', 'a')

    binFile.read(funVal)
    finalVal = struct.unpack('f', binFile.read(4))
    print 'The desired found value is %s' % finalVal
    outputFile.write('\n\nThe desired value for %s on selected coordinates is: ' % var)
    outputFile.write('%s.' % finalVal)

    binFile.close()
    outputFile.close()


# Function to acquire all TEC values for lat and lons on descriptor file
# Altitude is not needed because TEC is equal on altitude values
def find_tec_values(posVar):
    global lonCoord, latCoord, posCoord, coords, matrixLon, matrixLat, matrixTec

    matrixLon = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]
    matrixLat = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]
    matrixTec = [[0 for x in range(int(coords[0]))] for y in range(int(coords[1]))]

    binFile = open(dataFile, 'rb')

    for i in range(0, int(coords[0])):              # Longitude  ---- 66 iteracoes
        for j in range(0, int(coords[1])):          # Latitude   ---- 86 iteracoes
            funVal = calc_pos_ne(int(coords[0]),
                                 int(coords[1]),
                                 int(coords[2]),
                                 int(posVar),
                                 i,
                                 j,
                                 posCoord[2]
                                 )
            binFile.read(funVal)
            finalVal = struct.unpack('f', binFile.read(4))
            finalVal = str(finalVal).replace(",", "").replace("(", "").replace(")", "")

            # Build de map to perform the contourn plot on the future
            # 86x66 LAT/LON
            matrixLon[j][i] = lonCoord[i]
            matrixLat[j][i] = latCoord[j]
            matrixTec[j][i] = finalVal

            binFile.seek(0)
    binFile.close()


# Example plot function using matplotlib
def plot_example():

    xlist = np.linspace(-3.0, 3.0, 7)
    ylist = np.linspace(-3.0, 3.0, 7)

    X, Y = np.meshgrid(xlist, ylist)
    Z = (X ** 2 + Y ** 2)

    #plt.style.use('ggplot')
    #plt.style.use('seaborn-dark-palette')


    plt.figure()
    cp = plt.contourf(X, Y, Z)

    plt.set_cmap('Blues')
    plt.colorbar(cp)
    plt.title('Filled Contours Plot')
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.show()


# Example plot function using matplotlib
def plot_tec():
    global matrixLon, matrixLat, matrixTec
    print plt.style.available

    plt.figure()
    v = np.linspace(0, 80, 25, endpoint=True)
    cp = plt.contourf(matrixLon, matrixLat, matrixTec, v, cmap=plt.cm.rainbow)

    axes = plt.gca()
    axes.set_xlim([-85, -30])
    axes.set_ylim([-60, 15])

    plt.clim(0, 80)
    plt.colorbar(cp)

    plt.title('TEC Map')
    plt.xlabel('latitude (deg)')
    plt.ylabel('longitude (deg)')
    plt.show()


# Function to read descriptor file, acquire all important information, calculates the position to find
# the desired data and save all things on an output file named GradsOut.txt
def scavenge_output_map():
    global posCoord, coords

    opt_scavenge_file()
    user_data()
    posVar = comp_var()
    #print posVar
    #print coords
    funVal = calc_pos_ne(int(coords[0]),
                         int(coords[1]),
                         int(coords[2]),
                         int(posVar[1]),
                         posCoord[0],
                         posCoord[1],
                         posCoord[2]
                         )
    find_binary_value(funVal, posVar[0])
    find_tec_values(posVar[1])
    plot_tec()


def scavenge_ouptut_ionex(lon, lat, lonCoord, latCoord, coords, filename):
    global dataFile
    dataFile = filename
    posCoord = []

    for i in range(0, len(lonCoord)):
        if str(lon) == str(lonCoord[i]):
            posCoord.append(i)
    for j in range(0, len(latCoord)):
        if str(lat) == str(latCoord[j]):
            posCoord.append(j)

    funVal = calc_pos_ne(int(coords[0]),
                         int(coords[1]),
                         int(coords[2]),
                         2,
                         posCoord[0],
                         posCoord[1],
                         0)
    tec = find_binary_value_ionex(funVal)
    tec = ",".join(str(tec)).replace(",", "").replace("(", "").replace(")", "")
    return tec


'''Call this function to insert values, calculate (NE, TEC, TIMEDIFF), generate a file containing all gathered data    \
   and printing a TEC MAP of the corresponding file '''
scavenge_output_map()






