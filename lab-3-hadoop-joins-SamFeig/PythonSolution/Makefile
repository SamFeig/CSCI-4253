##
## Makefile

run: input/cite75_99.txt input/apat63_99.txt
	-rm -rf stream-output
	./RUN-MAP-REDUCE \
		-files CheckCitationCountMapper.py,CheckCitationCountReducer.py \
		-mapper CheckCitationCountMapper.py \
		-reducer CheckCitationCountReducer.py \
		-input input -output stream-output

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


