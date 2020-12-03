# Lab 3 - Hadoop Joins
#### Sam Feig

### How it works
This runs 3 hadoop map-reduce jobs back to back. 

#### Job 1
Mapper (```Mapper1```):<br>
Takes the input files of ```apat63_99.txt``` and ```cite75_99.txt```. 
If the data is citation data it sets the key as ```Citing``` and the value as ```Cited```. If it is patent data, it sets the key as ```PatentNo``` and the value as all the rest of the data except the patent number. 
<br><br>
The same mapper (```Mapper1```) is used for this and Job 2.

Reducer (```Reducer1```):<br>
If the mapped value is patent data, store the patentInfo (the entire value string), and try to get the patent state from field 4. If it is citation data, just add it to the citations list. If the patent data is not null (no pattent data), then run through all the citations. Flip the key and value and append the state by setting the key as ```cited``` and the value as ```Citing CitingState```.
<br><br>
The same reducer (```Reducer1```) is used for this and Job 2. <br>


#### Job 2
Mapper (```Mapper1```):<br>
Takes the input files of ```/output-part-1/part-r-00000``` and ```apat63_99.txt```. 
If the data is citation data it sets the key as ```citing``` and the value as ```cited``` (There should be no citation data in this run as it was all handled in the first map-reduce). If it is patent data, it sets the key as ```patentNo``` and the value as all the rest of the data except the patent number. If there is intermediate data from the first job, it splits on whitespace and sets the key to be the ```cited``` and the value to be the ```citing citingState``` combination from Job 1.
<br><br>
The same mapper (```Mapper1```) is used for this and Job 1. <br>

Reducer (```Reducer1```):<br>
If the mapped value is patent data, store the patentInfo (the entire value string), and try to get the patent state from field 4. If it is citation data, just add it to the citations list. If the patent data is not null (no pattent data), then run through all the citations. Flip the key and value and append the second state by setting the key as ```Citing CitingState``` and the value as ```Cited CitedState```.
<br><br>
The same reducer (```Reducer1```) is used for this and Job 1. <br>

**This is a repeat of the first job but with the output of Job 1 as input instead of the citation data. All it does is get the second state and flip the key/value pair**

#### Job 3
Takes the input files of ```/output-part-2/part-r-00000``` and ```apat63_99.txt```.

Mapper (```Mapper2```):<br>
If the data is citation data it sets the key as ```citing``` and the value as ```cited``` (There should be no citation data in this run as it was all handled in the first map-reduce). If it is patent data, it sets the key as ```patentNo``` and the value as all the rest of the data except the patent number (using substring instead to preserve the extra commas). If there is intermediate data from the first job, it splits on whitespace and sets the key to be the ```Citing```. It then check that the two states are the same and are not empty, if so, it sets the value as ```1```.

Reducer (```Reducer2```):<br>
If the mapped value is patent data, store the patentInfo (the entire value string). Otherwise, sum up the 1's from the ```Mapper2``` to get the count of same state patent citations. If the patent data is not null (no pattent data), set the key to be the ```key,patentInfo,count``` where key is the pattent number, and leave the value empty. This will give us a single string that is in the same format as the input patent data, with the count of same state citations appended to the end.

### How to Run
Navigate to the ```/JavaSolution/``` folder and run ```make``` after downloading the zip files into the root directory of the project.

### Results
```tail -n 20 output/part-r-00000```<br>
```
6009535,1999,14606,1997,"US","MA",171995,2,,714,2,22,6,0,1,,0.5,,2.5,0.1667,0.1667,,,0
6009536,1999,14606,1996,"US","ID",722315,2,,714,2,22,16,0,1,,0.6406,,5.875,0,0,,,1
6009537,1999,14606,1997,"JP","",581270,3,,714,2,22,15,0,1,,0.7022,,5,0.0667,0.0667,,,0
6009538,1999,14606,1997,"US","GA",395480,2,,714,2,22,12,0,1,,0.6111,,4.5833,0.0833,0.0833,,,1
6009539,1999,14606,1996,"US","CO",250060,2,,714,2,22,77,0,1,,0.6811,,6.2597,0.0395,0.039,,,3
6009540,1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,,4
6009541,1999,14606,1997,"US","CA",722315,2,,714,2,22,155,0,1,,0.8503,,2.6968,0.0132,0.0129,,,43
6009542,1999,14606,1998,"US","MA",460700,2,,714,2,22,2,0,1,,0,,6.5,0,0,,,0
6009543,1999,14606,1997,"US","MA",357270,2,,712,2,22,12,0,1,,0.5139,,3.6667,0,0,,,1
6009544,1999,14606,1998,"JP","",358975,3,,714,2,22,2,0,1,,0,,6,0,0,,,0
6009545,1999,14606,1998,"JP","",379245,3,,714,2,22,9,0,1,,0.7407,,6.6667,0.1111,0.1111,,,0
6009546,1999,14606,1998,"US","OR",127090,2,,714,2,22,8,0,1,,0.4063,,7,0,0,,,0
6009547,1999,14606,1997,"US","AZ",280070,2,,714,2,22,9,0,1,,0.4938,,4.8889,0,0,,,0
6009548,1999,14606,1998,"US","NY",280070,2,,714,2,22,14,0,1,,0.2551,,6.1429,0.3571,0.3571,,,0
6009549,1999,14606,1997,"US","CO",105280,2,,714,2,22,9,0,1,,0.642,,4.1111,0.5,0.4444,,,4
6009550,1999,14606,1997,"US","CA",757172,2,,714,2,22,8,0,1,,0.5938,,1.75,0.125,0.125,,,4
6009551,1999,14606,1998,"US","CA",587055,2,,714,2,22,2,0,1,,0.5,,3,1,1,,,2
6009552,1999,14606,1997,"IL","",386735,2,,714,2,22,5,0,1,,0.48,,12.6,0.2,0.2,,,0
6009553,1999,14606,1997,"US","MA",695811,2,,714,2,22,12,0,1,,0.7778,,10.9167,0,0,,,0
6009554,1999,14606,1997,"US","NY",219390,2,,714,2,22,9,0,1,,,,12.7778,0.1111,0.1111,,,8
```
 
