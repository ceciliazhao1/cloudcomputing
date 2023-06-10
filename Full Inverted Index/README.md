Detail Design Presentation：
MapReduce Program + Full Inverted Index
https://docs.google.com/presentation/d/1JY1TQf3hqQtnSNt3MSyeYr0qA3i8aDudIIbxRAEK0LQ/edit#slide=id.g13eaf2dbc0f_0_144

Design

Convert a WordCount MapReduce program into a Partial Inverted Index MapReduce program

In map class:
Use getName() to get the filename.
Also we can use algorithms to get the last digits.

In reduce class:
Use hashset to get the unique file name or index.

Convert a Partial Inverted Index MapReduce program into a Full Inverted Index MapReduce program

In map class:
Use getName() to get the filename.
Also we can use count to get the key’s index.
Like file0: it is what it is
It : (file0,0),(file0,3)

In reduce class:
Use list to get the file list.

Implement

Step 1: Create 3 files as input files and copy into hadoop.

Step 2: Create a MapReduce program to get the file index.

Step 3: Execute the MapReduce program created in Step 2.



Prepare input data
```
  $ mkdir InvertedInput
  $ vi file0
  $ vi file1
  $ vi file2
```
Input data will store in InvertedInput

Setup passphraseless ssh

Now check that you can ssh to the localhost without a passphrase:
```
  $ cd hadoop-3.3.4/
  $ ssh localhost
```
If you cannot ssh to localhost without a passphrase, execute the following commands:
```
  $ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
  $ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  $ chmod 0600 ~/.ssh/authorized_keys
```
Make the HDFS directories required to execute MapReduce jobs(Copy input data to HDFS)
```
  $ cd ..
  $ cd hadoop-3.3.4/
  $ bin/hdfs namenode -format
  $ sbin/start-dfs.sh
  $ wget http://localhost:9870/
  $ bin/hdfs dfs -mkdir /user
  $ bin/hdfs dfs -mkdir /user/czhao322
  $ bin/hdfs dfs -mkdir /user/czhao322/invertedindex
  $ bin/hdfs dfs -mkdir /user/czhao322/invertedindex/input1
  $ bin/hdfs dfs -put ../InvertedInput/* /user/czhao322/invertedindex/input1
```  
  
Prepare code

Build partial java file
```
  $ cd /hadoop-3.3.4
  $ vi partial.java 
```
Compile partial.java and create a jar
```
  $ bin/hadoop com.sun.tools.javac.Main partial.java
  $ jar cf wc.jar partial*class  
```
Run

Execute
```
  $ bin/hadoop jar wc.jar partial /user/czhao322/invertedindex/input1 /user/czhao322/invertedindex/output11
```
Output
```
  $ bin/hdfs dfs -ls /user/czhao322/invertedindex/output11
  $ bin/hdfs dfs -cat /user/czhao322/invertedindex/output11/part-00000
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/Full%20Inverted%20Index/partial.png" width=50% height =50%>
Build full java file
```
  $ cd /hadoop-3.3.4
  $ vi full.java 
```
Compile full.java and create a jar
```
  $ bin/hadoop com.sun.tools.javac.Main full.java
  $ jar cf wc.jar full*class  
```
Run

Make the output directory.
```
$ bin/hdfs dfs -mkdir /user/czhao322/fullindex
```
Execute
```
  $ bin/hadoop jar wc.jar full /user/czhao322/invertedindex/input1 /user/czhao322/fullindex/output1
```
Output
```
  $ bin/hdfs dfs -ls /user/czhao322/fullindex/output1
  $ bin/hdfs dfs -cat /user/czhao322/fullindex/output1/part-00000
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/Full%20Inverted%20Index/full.png" width=50% height =50%>
Stop
```
  $ sbin/stop-dfs.sh
```



