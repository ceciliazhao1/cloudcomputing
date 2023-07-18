Detail Design Presentation：

https://docs.google.com/presentation/d/1CGREG54TSDyRQ-znUhiAjLerNN9gaBI87cO2LgbNarM/edit?pli=1#slide=id.g2504991d7a9_0_220

Design:

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/1.png" width=30% height =30%>

Initialize each page’s rank to 1.0
On each iteration, have page p send a contribution of rank(p) / numNeighbors(p) to its neighbors (the pages it has links to).
Set each page’s rank to 0.15 + 0.85 * contributionsReceived.
Note:
0.85 is the damping factor

Calculation:

First iteration
```
PR(A)=(1-d)+d *PR(C)=1-0.85+0.85*1=1
PR(B)=(1-d)+d *PR(A)/2=1-0.85+0.85*1/2=0.575
PR(C)=(1-d)+d *(PR(A)/2+PR(B))=1-0.85+0.85*(1/2+1)=1.425
```
Second iteration
```
PR(A)=(1-d)+d *PR(C)=1-0.85+0.85*1.425=1.36125
PR(B)=(1-d)+d *PR(A)/2=1-0.85+0.85*1/2=0.575
PR(C)=(1-d)+d *(PR(A)/2+PR(B))=1-0.85+0.85*(1/2+0.575)=1.06375
```

Pyspark - using GCP dataproc and hdfs:
1. Ssh login the dataproc cluster server.
2. Upload a txt file to show the references among the nodes.

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/2.png" width=40% height =40%>

3. copy the file into hdfs:///mydata
```
$ hdfs dfs -mkdir hdfs:///mydata
$ hdfs dfs -put pageranktxt.txt hdfs:///mydata
$ hdfs dfs -ls hdfs:///mydata
```
4. Upload the pagerank.py

5. Run:

For the 1st iteration it is:
```
$ spark-submit --master yarn --deploy-mode cluster --py-files pagerank.py pagerank.py hdfs:///mydata/pageranktxt.txt 1 hdfs:///mydata/output/1
$  hdfs dfs -cat hdfs:///mydata/output/1/*
```

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/3.png" width=50% height =50%>

For the 2nd iteration it is:
```
$ spark-submit --master yarn --deploy-mode cluster --py-files pagerank.py pagerank.py hdfs:///mydata/pageranktxt.txt 2 hdfs:///mydata/output/2
$ hdfs dfs -cat hdfs:///mydata/output/2/*
```

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/4.png" width=50% height =50%>


Scala-Using dataproc and hdfs:

1. Scala-install scala and sbt:
using the Scala REPL (Read-Evaluate-Print-Loop or interactive interpreter)

2. Set the SCALA_HOME environment variable
3. Check sbt version

4. Create directory structure:

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/5.png" width=50% height =50%>

5. Compile:
```
$ sbt package
```
6. Download spark

7. Put pagerank.txt file into hdfs:
```
$ hdfs dfs -put pagerank.txt /user/czhao322
$ hdfs dfs -ls
```
8. Run:
For the 1st iteration it is:
```
$ spark-submit --class org.apache.spark.examples.SparkPageRank --master local[4] /home/czhao322/target/scala-2.12/pagerank-project_2.12-1.0.jar pagerank.txt 1
```

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/6.png" width=50% height =50%>

For the 2nd iteration it is:
```
$ spark-submit --class org.apache.spark.examples.SparkPageRank --master local[4] /home/czhao322/target/scala-2.12/pagerank-project_2.12-1.0.jar pagerank.txt 2
```

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/spark/pagerank/img/7.png" width=50% height =50%>






