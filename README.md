
# INPE IONEX TEC MAPS

## The Purpose

It is known that the CRS-INPE ionospheric prediction system and many research institutes result in 2 types of files, one of which is a text file ('descriptor.txt') containing the data about the simulation done, such as latitute, longitude and height used in the forecast, and a binary file ('data.dat'), containing all simulation data estimated and organized according to the text file. 

In this way, an algorithm was developed to interpret these files and to be able to search the data according to the desired location, generating TEC maps and IONEX files of the simulations.

## Creating TEC maps

Using a search system that scans all the corresponding NE and TEC values in the file, coordinate by coordinate, and collects all the values of total electronic content in all the simulated geographic points, was able to create an image with the result obtained, according to Figure 1.

![Imgur](http://i.imgur.com/0gluZxS.png)

The algorithm developed can create numerous TEC maps, as long as all the text and data files (results of the ionospheric prediction system) are in the desired folder, entered by the user in the execution of the script. The developed map is geo-referenced and its coordinates correspond faithfully to the actual observable points, increasing the credibility of the image generated.

In addition to the map present in Figure 2, a global visualization for the TEC maps was developed, according to Figure 2.

![Imgur](http://i.imgur.com/mTxrARE.png)

To run the script, simply run it in the terminal, or using some IDE able to understand Python language. </br>
During the file execution call, the corresponding directory containing the 'descriptor' and 'data' files must be informed via input parameter.

Below is an image of the script running via terminal.

![Imgur](http://i.imgur.com/XYrkZhe.png)

## Creating IONEX files

In the same way that the TEC mapping system uses the 'descriptor' and 'data' files, this system also reads these files, calculates the TEC for the required points and organizes everything into an IONEX file.

Based on a first format proposed by [Schaer, 1996], which follows the Receiver Independent Exchange (RINEX) format [Gurtner and Madner, 1990], the format known as Ionosphere map Exchange (IONEX), which supports the exchange of information in two and three dimensions, was developed in order to be a reference for coded TEC maps.

The algorithm developed reads and interprets the 'descriptor' files used during SUPIM simulations, calculates the TEC referring to those coordinates, searches for that value in the 'data' file and fills a new file, script result, with TEC values, following the format specified by the IONEX standard. Before the algorithm is executed it is necessary to inform the number of desired dimensions (2D or 3D) and the directory containing the text and data files used in the ionospheric simulation system.

At the end, there is a map of TEC referring to the date and time of the simulation, in the IONEX format, which can be read in any system capable of interpreting this format. Figure 3 shows the excerpt of a file referring to an IONEX 2D map, while Figure 4 is the result for an IONEX 3D map.

![Imgur](http://i.imgur.com/t85NLg6.png)

![Imgur](http://i.imgur.com/lrax5Ye.png)

During the file execution call, the corresponding directory containing the 'descriptor' and 'data' files, as well as the number of desired dimensions for creating maps (2D or 3D) must be passed via input parameter. </br>
Below is an image of the script running via terminal.

![Imgur](http://i.imgur.com/6HZ1dT1.png)

## Copyrights

**The project can be reproduced without any problems.** </br>
However, I only ask you to keep **credits to the author**.

Enjoy!

**Hollweg**

