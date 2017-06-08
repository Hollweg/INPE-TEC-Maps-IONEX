#!/usr/bin/env python

# Using PEP 8 -- Style Guide for Python Code
# https://www.python.org/dev/peps/pep-0008/
# Main dev.: Guilherme Hollweg - Electrical Engineer
# Last Modified on 22/05/2017

import os, os.path, sys
import struct
import datetime, time
import math

print "\n                  IONEX Files Generator                   \n \
       \r    Developed for National Institute for Space Research   \n \
       \r                  by Guilherme Hollweg                    \n \
       \r                    v1.0     05/2017                         "

# Max, Min and Step of Coordinates --- used to generate IONEX maps (headers)
hgtMax, hgtMin, hgtStep = 0, 0, 0
latMax, latMin, latStep = 0, 0, 0
lonMax, lonMin, lonStep = 0, 0, 0

# Information about date used on Headers (First and last TEC map information)
# Time Interval calculated from descriptor files hour difference and baseRadius used
# on SUPIM simulation system
firstyear, firstjulianday, firstmonth, firstday, firsthour, firstminute, firstsecond = 0, 0, 0, 0, 0, 0, 0
lastyear, lastmonth, lastday, lasthour, lastminute, lastsecond = 0, 0, 0, 0, 0, 0
year, month, day, hour, minute, second = 0, 0, 0, 0, 0, 0
timeinterval = 0
baseradius = 6370
exponent = 0

# yearlist ---> List with all descriptor files years ; descriptors ---> all desc. files
# sortDescriptors ---> descriptors sorted by data ; coords ---> number of LAT/LON/ALT coordinates
yearlist = list()
descriptors = list()
sortDescriptors = list()
coords = list()

# dir ---> path of all desc. files
dir = '.'

# Generate current date information and declare strings used on IONEX headers
date = datetime.datetime.now()
dataFile = ''

today = time.strftime("%Y-%B-%d %H:%M")[2:]
email = 'adr.petry@inpe.br  '
personName = 'Adriano Petry'
binFile = ''


# Function to put day into correct format --- used on fileName
def format_day(day):
    if int(day) < 10:
        day = '00%s' %(day)
    elif int(day) < 100:
        day = '0%s' %(day)
    return day


# Function to read all files into desired folder and put all 'descriptors' into a list
def read_files():
    global descriptors
    filesonFolder = next(os.walk(dir))[2]
    for name in filesonFolder:
        if 'descriptor' in name and name[-1] == 'h':
            descriptors.append(name)
    descriptors.sort()


# Function to find MIN and MAX descriptor's years --- used on IONEX headers
def find_min_max_year(descfile):
    global yearlist
    for i in range(0, len(descfile)):
        yearlist.append(descfile[i].split('.')[2])
    yearlist = list(set(yearlist))
    maxyear, minyear = max(enumerate(yearlist))[1], min(enumerate(yearlist))[1]


# Function to format numbers according to IONEX format (ex.: '09' instead of '9')
def check_for_zero(num):
    if int(num) < 10:
        num = '0%s' %(num)
    return num


# Function to acquire descriptor date information --- it can store information about the first and last descriptor
# file (useful to use on Headers) --- it is also used to sort descriptor files
def julian_to_date(descfile, first, last):
    global firstyear, firstjulianday, firstmonth, firstday, firsthour, firstminute, firstsecond, lastyear, lastmonth, lastday, \
    lasthour, lastminute, lastsecond, year, month, day, hour, minute, second

    if first == 1:
        firstyear, julianday = check_for_zero(descfile.split('.')[2]), descfile.split('.')[3]
        firstjulianday = julianday
        firsthour, firstminute = check_for_zero(descfile.split('.')[4]), check_for_zero(descfile.split('.')[5].replace('h',''))
        date = datetime.datetime(int(firstyear), 1, 1, int(firsthour), int(firstminute)) + datetime.timedelta(int(julianday)-1)
        firstmonth = check_for_zero(date.month)
        firstday = check_for_zero(date.day)
        firstsecond = check_for_zero(firstsecond)
    elif last == 1:
        lastyear, julianday = check_for_zero(descfile.split('.')[2]), check_for_zero(descfile.split('.')[3])
        lasthour, lastminute = check_for_zero(descfile.split('.')[4]), check_for_zero(descfile.split('.')[5].replace('h',''))
        date = datetime.datetime(int(lastyear), 1, 1, int(lasthour), int(lastminute)) + datetime.timedelta(int(julianday)-1)
        lastmonth = check_for_zero(date.month)
        lastday = check_for_zero(date.day)
        lastsecond = check_for_zero(lastsecond)
    else:
        year, julianday = descfile.split('.')[2], descfile.split('.')[3]
        hour, minute = descfile.split('.')[4], descfile.split('.')[5].replace('h','')
        date = datetime.datetime(int(year), 1, 1, int(hour), int(minute)) + datetime.timedelta(int(julianday)-1)
        month = date.month
        day = date.day
        second = second


# Function to calculate time interval between files
def calculate_time_interval(descriptors):
    global timeinterval
    for i in range(0, len(descriptors)):
        descriptors[i] = descriptors[i][15:-1].split('.')
    try:
        return math.fabs(int(descriptors[0][2]) - int(descriptors[1][2])*3600)
    except:
        return 3600


# Function to sort descriptor files by year-month-day-hour
def ord_descriptors(descriptors):
    global yearlist, firstyear, firsthour, firstminute, lastyear, lasthour, lastminute
    ordDescript = list()

    for i in range(0, len(descriptors)):
        descriptors[i] = descriptors[i][15:-1].split('.')
        if int(descriptors[i][2]) < 10:
            descriptors[i][2] = '0%s'% (descriptors[i][2])
        if int(descriptors[i][3]) < 10:
            descriptors[i][3] = '0%s'% (descriptors[i][3])
    descriptors.sort()

    for i in range(0, len(descriptors)):
        if int(descriptors[i][2]) < 10:
            descriptors[i][2] = int(descriptors[i][2])
        if int(descriptors[i][3]) < 10:
            descriptors[i][3] = int(descriptors[i][3])
        ordDescript.append('descriptor.ctl.%s.%s.%s.%sh'% (descriptors[i][0], descriptors[i][1], descriptors[i][2], descriptors[i][3]))
    return ordDescript


# Function to calculate spaces according to header fields
def calc_spaces(num, form):
    if form == 5:
        num = int(float(num))
        length = len(str(num))
        spaces = 5 - int(length)
    elif form == 6:
        length = len(str(num))
        spaces = 6 - int(length)
    else:
        '%.1f'.format(num)
        length = len(str(num))
        spaces = 6 - int(length)

    if spaces == 1:
        num = ' %s' % (num)
    elif spaces == 2:
        num = '  %s' % (num)
    elif spaces == 3:
        num = '   %s' % (num)
    elif spaces == 4:
        num = '    %s' % (num)
    elif spaces == 5:
        num = '     %s' % (num)

    return num


# Function to calculate the equation for the desired data position on .dat file
def calc_pos_ne(lon, lat, alt, posVar, posLon, posLat, posAlt):
    return ((lon*lat*alt)*posVar + (lon*lat)*posAlt + lon*posLat + posLon)*4


# Function to find TEC value of a given point --- opens binary file and jump to the right position
def find_binary_value_ionex_optimized(funVal):
    global binFile

    binFile.read(funVal)
    finalVal = struct.unpack('f', binFile.read(4))
    return finalVal


# Function to mount all needed lists to find TEC value on binary file
def scavenge_ouptut_ionex(lon, lat, alt, lonCoord, latCoord, altCoord, coords, dimension, exponent):
    global hgtStep
    posCoord = []

    if int(dimension) == 2:
        # calculate current position of LON and LAT to put on the equation and find the amount to
        # jump and read binary file containing TEC
        for i in range(0, len(lonCoord)):
            if str(lon) == str(lonCoord[i]):
                posCoord.append(i)
        for j in range(0, len(latCoord)):
            if str(lat) == str(latCoord[j]):
                posCoord.append(j)

        # funVal ---> the number of positions to jump on binary file
        funVal = calc_pos_ne(int(coords[0]),
                             int(coords[1]),
                             int(coords[2]),
                             2,
                             posCoord[0],
                             posCoord[1],
                             0)
        tec = find_binary_value_ionex_optimized(funVal)
        tec = ",".join(str(tec)).replace(",", "").replace("(", "").replace(")", "")
        return tec

    elif int(dimension) == 3:
        # calculate current position of LON and LAT and ALT to put on the equation and find the amount to
        # jump and read binary file containing TEC
        for i in range(0, len(lonCoord)):
            if str(lon) == str(lonCoord[i]):
                posCoord.append(i)
        for j in range(0, len(latCoord)):
            if str(lat) == str(latCoord[j]):
                posCoord.append(j)
        for k in range(0, len(altCoord)):
            if str(alt) == str(altCoord[k]):
                posCoord.append(k)
        # funVal ---> the number of positions to jump on binary file
        funVal = calc_pos_ne(int(coords[0]),
                             int(coords[1]),
                             int(coords[2]),
                             1,
                             posCoord[0],
                             posCoord[1],
                             posCoord[2])
        ne = find_binary_value_ionex_optimized(funVal)
        ne = ",".join(str(ne)).replace(",", "").replace("(", "").replace(")", "")
        # ne = ne*DeltaHGT*1000 (km)/(TECU) ---> multiplicado por 10^-16 (transformado em TECU) e entao multiplicado por 10^-2 (expoente '-2' do IONEX)
        # para otimizacao ----> ne*hgtStep*10^-11
        ne = float(ne)*hgtStep*10**(-13 - int(exponent))
        return ne

# Function to write IONEX main header
def write_header(dimension):
    global outputFile, today, day, year, email, personName, yearlist, sortDescriptors, timeinterval, baseradius, \
    hgtMax, hgtMin, hgtStep, latMax, latMin, latStep, lonMax, lonMin, lonStep, exponent

    if int(dimension) == 2:
        hgtMax, hgtMin, hgtStep, exponent = 450000, 450000, 0, -1
    else:
        exponent = -2

    outputFile.write("     1.0            IONOSPHERE MAPS     GPS                 IONEX VERSION / TYPE\
\nSUPIM-INPE          EMBRACE/INPE        %s     PGM / RUN BY / DATE \
\nGlobal ionosphere map from Ionosphere Dynamics Prediction   DESCRIPTION         \
\nSystem developed for the Brazilian Space Weather Program.   DESCRIPTION         \
\nThe system is based on an enhanced version of Sheffield     DESCRIPTION         \
\nUniversity Plasmasphere-Ionosphere Model (SUPIM).           DESCRIPTION         \
\nThis file was developed for the collaboration between       COMMENT             \
\nNational Institute for Space Research (INPE) - Brazil       COMMENT             \
\nand German Aerospace Center (DLR) - Germany                 COMMENT             \
\nFile prepared by Dr. Adriano Petry - adriano.petry@inpe.br  COMMENT             \
\n%s%s%s%s%s%s                        EPOCH OF FIRST MAP  \
\n%s%s%s%s%s%s                        EPOCH OF LAST MAP   \
\n%s                                                      INTERVAL            \
\n%s                                                      # OF MAPS IN FILE   \
\n  NONE                                                      MAPPING FUNCTION    \
\n     0.0                                                    ELEVATION CUTOFF    \
\nSolar fluxes (EUV, F10.7 and F10.7A)                        OBSERVABLES USED    \
\n  %.1f                                                    BASE RADIUS         \
\n%s                                                      MAP DIMENSION       \
\n  %s%s%s                                        HGT1 / HGT2 / DHGT  \
\n  %s%s%s                                        LAT1 / LAT2 / DLAT  \
\n  %s%s%s                                        LON1 / LON2 / DLON  \
\n    %s                                                      EXPONENT            \
\n                                                            END OF HEADER       "
                     % (today, calc_spaces(firstyear, 6), calc_spaces(firstmonth, 6),
                        calc_spaces(firstday, 6), calc_spaces(firsthour, 6), calc_spaces(firstminute, 6),
                        calc_spaces(firstsecond, 6), calc_spaces(lastyear, 6), calc_spaces(lastmonth, 6),
                        calc_spaces(lastday, 6), calc_spaces(lasthour, 6), calc_spaces(lastminute, 6),
                        calc_spaces(lastsecond, 6), calc_spaces(int(timeinterval), 6),
                        calc_spaces(int(len(sortDescriptors)), 6), baseradius, calc_spaces(dimension, 6),
                        calc_spaces(float(hgtMin)/1000, 6.1), calc_spaces(float(hgtMax)/1000, 6.1),
                        calc_spaces(float(hgtStep), 6.1), calc_spaces(float(latMin), 6.1),
                        calc_spaces(float(latMax), 6.1), calc_spaces(float(latStep), 6.1),
                        calc_spaces(float(lonMin), 6.1), calc_spaces(float(lonMax), 6.1),
                        calc_spaces(float(lonStep), 6.1), exponent))


# Function to write mini-headers containing descriptor information and print all tec values
# into output file
def write_tec_map(dimension):
    global outputFile, sortDescriptors, year, month, day, hour, minute, second, latCoord, lonMax, lonMin, lonStep,     \
    altCoord, lonCoord, coords, dir, binFile, exponent
    dataFile = ''
    cont = 0
    dlon = lonStep
    
    for i in range(0, len(sortDescriptors)):
        # find all information about current descriptor file
        julian_to_date(sortDescriptors[i], 0, 0)

        # build binfile name to find TEC
        if cont == 0:
            inputFile = open(dir + sortDescriptors[i], 'rb')
            for line in inputFile:
                if 'dset' in line:
                    for n in range(6, len(line)):
                        dataFile = dataFile + line[n]
            dataFile = dataFile.rstrip()
            cont = 1
            inputFile.close()
            print '\n Generating map %s...' % str((int(i)+1))
        binFile = open(dir + dataFile, 'rb')
        outputFile.write("\n%s                                                      START OF TEC MAP    \
\n%s%s%s%s%s%s                        EPOCH OF CURRENT MAP"
                         % (calc_spaces((i+1), 6), calc_spaces(year, 6), calc_spaces(month, 6), calc_spaces(day, 6),
                            calc_spaces(hour, 6), calc_spaces(minute, 6), calc_spaces(second, 6)))
        
        if int(dimension) == 2:
            hgt = 450.0
            # for loops to print information on output file
            # mantaining LAT and read LON, generating TEC maps
            for j in range(0, len(latCoord)):
                outputFile.write("\n  %s%s%s%s%s                            LAT/LON1/LON2/DLON/H"
                                %(calc_spaces(float(latCoord[j]), 6.1), calc_spaces(float(lonMin), 6.1),
                                calc_spaces(float(lonMax), 6.1), calc_spaces(float(dlon), 6.1), calc_spaces(hgt, 6.1)))

            # find TEC value to desired position using scavenge_ouptut_ionex and passing all needed information
            # to calculate current jump number and find TEC for the desired LON/LAT/ALT
                for k in range(0, len(lonCoord)):
                    tec = scavenge_ouptut_ionex(lonCoord[k], latCoord[j], 0, lonCoord, latCoord, 0, coords, dimension, exponent)
                    binFile.seek(0)
                    tec = 10.0*float(tec)
                    if k == 0 or int(k) % 16 == 0:
                        outputFile.write("\n%s" %(calc_spaces(tec, 5)))
                    else:
                        outputFile.write("%s" % (calc_spaces(tec, 5)))
            print ' Map %s done...' % (i)
            binFile.close()
            outputFile.write("\n%s                                                      END OF TEC MAP      "
                            %(calc_spaces((i+1), 6)))

        elif int(dimension) == 3:
            # for loops to print information on output file
            # mantaining LAT and read LON, generating TEC maps
            for j in range(0, len(altCoord)):
                for k in range(0, len(latCoord)):
                    outputFile.write("\n  %s%s%s%s%s                            LAT/LON1/LON2/DLON/H"
                                   %(calc_spaces(float(latCoord[k]), 6.1), calc_spaces(float(lonMin), 6.1),
                                     calc_spaces(float(lonMax), 6.1), calc_spaces(float(dlon), 6.1), calc_spaces(float(altCoord[j])/1000, 6.1)))

                    # find TEC value to desired position using scavenge_ouptut_ionex and passing all needed information
                    # to calculate current jump number and find TEC for the desired LON/LAT/ALT
                    for l in range(0, len(lonCoord)):
                        ne = scavenge_ouptut_ionex(lonCoord[l], latCoord[k], altCoord[j], lonCoord, latCoord, altCoord, coords, dimension, exponent)
                        binFile.seek(0)
                        ne = float(ne)
                        if l == 0 or int(l) % 16 == 0:
                            outputFile.write("\n%s" %(calc_spaces(ne, 5)))
                        else:
                            outputFile.write("%s" %(calc_spaces(ne, 5)))
            print ' Map %s done...' % (i)
            binFile.close()
            outputFile.write("\n%s                                                      END OF TEC MAP      "
                            %(calc_spaces((i+1), 6)))
        dataFile = ''
        cont = 0
    outputFile.write("\n                                                            END OF FILE         ")
    print '\n All done!'


# Function to join and format coordinates, returning a single list
def join_coordinates(coordList):
    coordList = filter(lambda a: a != '\n', coordList)
    coordList = ''.join(coordList).split(' ')
    return coordList


# Function to read and extract all interesting information into descriptor files
# LON/LAT/ALT/ and format all data --- optimized for different values of LAT/LON/ALT coordinates
def scavenge_file_ionex_optimized():
    global sortDescriptors, altCoord, lonCoord, latCoord, hgtMax, hgtMin, hgtStep, latMax, latMin, latStep, lonMax, \
    lonMin, lonStep, coords, dataFile, timeinterval, dir
    count, xdef, ydef, zdef = 0, 0, 0, 0
    coordVals = []
    inputFile = open(dir + sortDescriptors[0], 'rb')

    timeinterval = calculate_time_interval(sortDescriptors[0:2])
    julian_to_date(sortDescriptors[0], 1, 0)
    julian_to_date(sortDescriptors[-1], 0, 1)

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

    if lonCoord[0] == ' ':
        lonCoord.pop(0)
    if latCoord[0] == ' ':
        latCoord.pop(0)
    if altCoord[0] == ' ':
        lonCoord.pop(0)

    lonCoord = join_coordinates(lonCoord)
    latCoord = join_coordinates(latCoord)
    altCoord = join_coordinates(altCoord)

    hgtMax, hgtMin, hgtStep = altCoord[-1], altCoord[0], (int(altCoord[1]) - int(altCoord[0])) / 1000
    latMax, latMin, latStep = latCoord[-1], latCoord[-0], math.fabs(int(latCoord[1]) - int(latCoord[0]))
    lonMax, lonMin, lonStep = lonCoord[-1], lonCoord[0], math.fabs(int(lonCoord[1]) - int(lonCoord[0]))

    inputFile.close()


# receiving terminal parameters
dir = str(sys.argv[1])
dimension = str(sys.argv[2])

# call function to read all files on desired path, sort Descriptors by date and
# open descriptor files looking for LON/LAT/ALT information
read_files()
sortDescriptors = ord_descriptors(descriptors)
scavenge_file_ionex_optimized()

# Build output file name
fileName = 'I' + str(dimension) + 'D' + str(format_day(firstjulianday)) + '0' + '.' + str(firstyear)[2:] + 'I'
outputFile = open(dir + fileName, 'w+b')

# write the output file according to all IONEX rules
write_header(dimension)
write_tec_map(dimension)

outputFile.close()

