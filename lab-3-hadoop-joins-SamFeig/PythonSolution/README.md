# Python starter code

The following code is a streaming map-reducer written in Python.
It performs a single map-reduce phase. The goal of the map/reduce is to find
any mis-formatted input files and to serve as an example of how you can
implemented map/reduce in Python.

The mapper processes either the citations or the patent data. This data looks
like
```
"CITING","CITED"
3858241,956203
3858241,1324234
```
or
```
"PATENT","GYEAR","GDATE","APPYEAR","COUNTRY","POSTATE","ASSIGNEE","ASSCODE","CLAIMS","NCLASS","CAT","SUBCAT","CMADE","CRECEIVE","RATIOCIT","GENERAL","ORIGINAL","FWDAPLAG","BCKGTLAG","SELFCTUB","SELFCTLB","SECDUPBD","SECDLWBD"
3070801,1963,1096,,"BE","",,1,,269,6,69,,1,,0,,,,,,,
3070802,1963,1096,,"US","TX",,1,,2,6,63,,0,,,,,,,,,
```

In each case, it outputs the patent number which is used by the
reduce.  For patent records, it also outputs all the patent
information; for citations it just outputs a 'y'. In other words, it will produce
```
3858241	y
3858241	y
```
or
```
3070801	1963,1096,,"BE","",,1,,269,6,69,,1,,0,,,,,,,
3070802	1963,1096,,"US","TX",,1,,2,6,63,,0,,,,,,,,,
```

The reducer examines all the records for the same patent.  It counts
the citations and compares that to the expected number of citations in
the patent data. It distinguishes between the 'y' entries and the longer
patent information by counting the number of commas.

If a patent has patent data and the citation counts match
an "ok" is reported. Ootherwise "bad" and the expected and found citations.

You should find all patents are "ok" when you run sample and examine the output.

## Python details

The `Makefile` provides targets to produce the needed input files.
Because there is no ChainMapper when using streaming, you'll need to
need to write multiple Mapper/Reducer files.

This means you'l need to add additional rules to move around the input
files as needed. You should use additional make targets such as
e.g. `run1`, `run2`, etc to indicate the needed steps.

The shell script `RUN-MAP-REDUCE` takes care of finding the
appropriate JAR file for the streaming API.

You should leave your final output in 'output'


