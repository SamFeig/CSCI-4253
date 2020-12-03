CLASSPATH=$(shell hadoop classpath)

##/
## All of my map-reduce files in PatentMR directory.
## This is done using GNU Make function
##

BASE1= PatentJoin

HADOOP_CLASSPATH=$(shell hadoop classpath)

run: $(BASE1).jar input/cite75_99.txt input/apat63_99.txt
	-rm -rf output*
	hadoop jar $(BASE1).jar input output

$(BASE1).jar: $(BASE1).java
	javac -classpath $(HADOOP_CLASSPATH) -d ./ $(BASE1).java
	# Set entry class to be PatentJoin
	jar cfe $(BASE1).jar $(BASE1) *.class 
	-rm -f $(BASE1)*.class

%.class: %.java
	javac -classpath .:$(CLASSPATH) $<

input:
	mkdir ./input

input/cite75_99.txt: input ../acite75_99.zip
	unzip ../acite75_99.zip
	touch cite75_99.txt # update modification time
	mv cite75_99.txt input

input/apat63_99.txt: input ../apat63_99.zip
	unzip ../apat63_99.zip
	touch apat63_99.txt # update modification time
	mv apat63_99.txt input

prepare:
	echo "Some of the following commands may fail because your"
	echo "files are already setup"
	echo "====="
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)
	-hdfs dfs -rm -r -f /user/$(USER)/input
	-hdfs dfs -rm -r -f /user/$(USER)/output	

clean:
	-rm -f *.class */*.class
	-rm -f *.jar
