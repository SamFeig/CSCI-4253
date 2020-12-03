# Lab 2 - Convert WordCount to UrlCount Solution

### How it works
URLCount works by using the base template of the map reduce framework for wordCount, but modified to find href tags that contain links. This is done using Java patern matching with REGEX of the form ```href=\".*\"```. It then loops through each line of input matching each individual link and stripping the "href=" off of it. The reducer counts up occurences of individual links and limits the output to only links that occure more than 5 times. To get around Java/hadoop combiner issues there is a seperate combiner function/class that does the same job as the reducer but without the more than 5 occurances check.

### How to Run
To run this you will need a system that has Java and Hadoop installed on it. First run ```make prepare``` to download the files needed and set up the directory structure. Then run ```make URLCount``` to compile the java file. Finally, run ```make runURL``` or ```time make runURL``` if you would like to time the hadoop job. If runing this in ```dataproc```, ssh into the master node of the cluster then run all the make commands after making a user directory in hdfs using ```hdfs dfs -mkdir hdfs://CLUSTERNAME-m/user/USERNAME```. 

### Issues with Java Combiner
The default behavior of Hadoop in Java is that the reducer is duplicated as the combiner on the cluster to improve efficiency and reduce the final number of counting and network operations the reducer has to preform. However, when we add the "only output links that occur more than 5 times" logic, the reducer is no longer both commutative and associative and therefore cannot be used as the combiner as well. If one node has 4 occurances and the other node also has 4 occurances of a specific link, each node would hit the > 5 logic and fail it individually and throw out the links. However in the final reducer there would have been 8 occurances and the link should have been kept. This issue can be solved by writing a seperate combiner function/class that is identical to the reducer and just counts up occurences and doesnt do the "greater than 5 occurances" checking logic.

### Results From Timed Runs

##### JupyterLab Local
time Output:
```real 0m4.937s user 0m4.987s sys 0m0.536s```
 
##### 2-node Cluster
time Output:
```real 0m32.025s user 0m6.465s sys 0m0.356s```
 
##### 4-node Cluster
time Output:
```real 0m30.423s user 0m7.529s sys 0m0.343s```
 
The interesting part of this output is that the local run is much faster than both cluster runs and that the two cluster runs are almost the same speed independent of the number of nodes. This is likely because the clusters are optimized for very large quantities of data. So, when running it for small data sets like we are, the additonal overhead of distributing the executables and files to all nodes adds time instead of reducing time like intended. This is as oposed to the local run that does not need to do this distribution and so is much faster at small data sizes but will slow down with increased amounts of data to process as it is limited by the local number of cores in the CPU. The cluster runs would speed up as you increase the amount of data being processed as it can use many more cores than would otherwise be possible locally.