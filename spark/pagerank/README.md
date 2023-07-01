Detail Design Presentation：

https://docs.google.com/presentation/d/1CGREG54TSDyRQ-znUhiAjLerNN9gaBI87cO2LgbNarM/edit?pli=1#slide=id.g2504991d7a9_0_220

Design
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/Full%20Inverted%20Index/partial.png" width=50% height =50%>


An iterative algorithm that performs many joins, so it is a good use case for RDD partitioning.
The algorithm maintains two datasets:
(pageID, linkList) elements containing the list of neighbors of each page,
(pageID, rank) elements containing the current rank for each page.

Initialize each page’s rank to 1.0
On each iteration, have page p send a contribution of rank(p) / numNeighbors(p) to its neighbors (the pages it has links to).
Set each page’s rank to 0.15 + 0.85 * contributionsReceived.
Note:
0.85 is the damping factor

First iteration
PR(A)=(1-d)+d *PR(C)=1-0.85+0.85*1=1
PR(B)=(1-d)+d *PR(A)/2=1-0.85+0.85*1/2=0.575
PR(C)=(1-d)+d *(PR(A)/2+PR(B))=1-0.85+0.85*(1/2+1)=1.425
Second iteration
PR(A)=(1-d)+d *PR(C)=1-0.85+0.85*1.425=1.36125
PR(B)=(1-d)+d *PR(A)/2=1-0.85+0.85*1/2=0.575
PR(C)=(1-d)+d *(PR(A)/2+PR(B))=1-0.85+0.85*(1/2+0.575)=1.06375

Pyspark - using GCP dataproc and hdfs:
PySpark-Upload file:
ssh login the dataproc cluster server:
Upload a file to show the references among the nodes.

copy the file into hdfs:///mydata
```
$ hdfs dfs -mkdir hdfs:///mydata
$ hdfs dfs -put pageranktxt.txt hdfs:///mydata
$ hdfs dfs -ls hdfs:///mydata
```
Upload the pagerank.py:

For the 1st iteration it is:
```
$ spark-submit --master yarn --deploy-mode cluster --py-files pagerank.py pagerank.py hdfs:///mydata/pageranktxt.txt 1 hdfs:///mydata/output/1
$  hdfs dfs -cat hdfs:///mydata/output/1/*
```

For the 2nd iteration it is:
```
$ spark-submit --master yarn --deploy-mode cluster --py-files pagerank.py pagerank.py hdfs:///mydata/pageranktxt.txt 2 hdfs:///mydata/output/2
$ hdfs dfs -cat hdfs:///mydata/output/2/*
```


Scala-Using dataproc and hdfs:

Scala-install scala and sbt
using the Scala REPL (Read-Evaluate-Print-Loop or interactive interpreter)

set the SCALA_HOME environment variable
Check sbt version

Create directory structure.

Compile :
```
$ sbt package
```
Download spark:

Put pageranktxt.txt file into hdfs:
```
$ hdfs dfs -put pageranktxt.txt /user/czhao322
$ hdfs dfs -ls
```
```
$ spark-submit --class org.apache.spark.examples.SparkPageRank --master local[4] /home/czhao322/target/scala-2.12/pagerank-project_2.12-1.0.jar pagerank.txt 1
```
```
$ spark-submit --class org.apache.spark.examples.SparkPageRank --master local[4] /home/czhao322/target/scala-2.12/pagerank-project_2.12-1.0.jar pagerank.txt 2
```






